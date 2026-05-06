import logging
import sys
from typing import Optional, Dict, Any, Generator

try:
    from datasets import load_dataset
    from datasets.exceptions import DatasetNotFoundError
except ImportError:
    DatasetNotFoundError = type("DatasetNotFoundError", (Exception,), {})
    load_dataset = None

logger = logging.getLogger(__name__)
# The application enforce logging to stdout
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

class InsufficientStorageError(Exception):
    """Raised when there is not enough local storage to download the dataset."""
    pass

class DatasetIngestionError(Exception):
    """Raised when dataset ingestion fails for a generic reason."""
    pass

class DatasetManager:
    def __init__(self, cache_dir: Optional[str] = None):
        self.cache_dir = cache_dir

    def load_dataset_split(self, dataset_name: str, split: str = "train") -> Any:
        """
        Loads a dataset split from HuggingFace, caching it locally.
        
        Args:
            dataset_name: The name of the dataset to load (e.g., "rvl_cdip")
            split: The split to load (e.g., "train", "test")
            
        Returns:
            The loaded dataset object.
        """
        try:
            logger.info(f"Attempting to load dataset '{dataset_name}', split '{split}'")
            if load_dataset is None:
                raise ImportError("datasets library is not installed")
                
            # Using datasets library to load. This handles downloading and caching.
            dataset = load_dataset(dataset_name, split=split, cache_dir=self.cache_dir)
            logger.info(f"Successfully loaded dataset '{dataset_name}'")
            return dataset
        except DatasetNotFoundError as e:
            logger.error(f"dataset not found: {dataset_name}")
            raise DatasetIngestionError(f"dataset not found: {dataset_name}") from e
        except OSError as e:
            if "No space left on device" in str(e) or e.errno == 28:
                logger.error("Insufficient storage error while downloading dataset")
                raise InsufficientStorageError("Insufficient storage error") from e
            logger.error(f"OS Error during dataset ingestion: {e}")
            raise DatasetIngestionError(f"OS Error: {e}") from e
        except Exception as e:
            err_str = str(e).lower()
            if "not found" in err_str:
                logger.error(f"dataset not found: {dataset_name}")
                raise DatasetIngestionError(f"dataset not found: {dataset_name}") from e
            if "space left" in err_str or "insufficient storage" in err_str:
                logger.error("Insufficient storage error while downloading dataset")
                raise InsufficientStorageError("Insufficient storage error") from e
            
            logger.error(f"Failed to load dataset: {e}")
            raise DatasetIngestionError(f"Failed to load dataset: {e}") from e

    def stream_documents(self, dataset: Any) -> Generator[Dict[str, Any], None, None]:
        """
        Streams documents from the loaded dataset, transforming them to a standard format.
        """
        for row in dataset:
            # Standarize the output format, extracting common label/text fields.
            yield {
                "id": row.get("id", id(row)),
                "content": row.get("text", row.get("content", row.get("image", None))),
                "label": row.get("label", row.get("target", None)),
                "raw_row": row
            }

import abc
from typing import Generator, Dict, Any, List

class ModelUnavailableError(Exception):
    pass

class AIRunner(abc.ABC):
    """
    Abstract Base Class for Pluggable AI Model Runners.
    Enforces a standard interface for managing daemon lifecycles, installing binaries,
    and executing inference batches.
    """

    @abc.abstractmethod
    def install(self) -> None:
        """
        Downloads and provisions the executable binary or dependencies for the runner.
        Should handle OS/arch detection and output user notifications.
        """
        pass

    @abc.abstractmethod
    def get_version(self) -> str:
        """
        Retrieves the installed runner's version string.
        """
        pass

    @abc.abstractmethod
    def __enter__(self):
        """
        Starts the embedded daemon process.
        """
        pass

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Stops the embedded daemon process and cleans up threads.
        """
        pass

    @abc.abstractmethod
    def iter_logs(self) -> Generator[str, None, None]:
        """
        Generator that yields `stdout/stderr` log lines from the daemon.
        """
        pass

    @abc.abstractmethod
    def check_model(self, model_name: str) -> bool:
        """
        Checks if the requested model exists locally for this runner.
        """
        pass

    @abc.abstractmethod
    def pull_model(self, model_name: str) -> None:
        """
        Pulls or downloads the model weights for this runner.
        """
        pass

    @abc.abstractmethod
    def execute_batch(self, model_name: str, dataset_stream: Generator, prompt_template: str) -> List[Dict[str, Any]]:
        """
        Iterates through the dataset stream, queries the local API, and returns an array of results.
        Should handle its own crash recovery and return partial results if connection drops.
        """
        pass

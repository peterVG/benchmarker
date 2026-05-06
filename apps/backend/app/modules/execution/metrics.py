from typing import Dict, Any

class MetricsCollector:
    """
    Calculates telemetry (latency, tokens/sec) and accuracy scores
    from AI runner responses.
    """
    
    @staticmethod
    def calculate_telemetry(runner_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts and calculates performance telemetry from an AI runner response.
        """
        metrics = runner_response.get("metrics", {})
        eval_duration_ns = metrics.get("eval_duration")
        eval_count = metrics.get("eval_count")
        total_duration_ns = metrics.get("total_duration")
        
        eval_duration_sec = eval_duration_ns / 1e9 if eval_duration_ns else 0
        total_duration_sec = total_duration_ns / 1e9 if total_duration_ns else 0
        tokens_per_sec = eval_count / eval_duration_sec if eval_duration_sec > 0 and eval_count else 0
        
        return {
            "total_latency_sec": round(total_duration_sec, 4),
            "eval_duration_sec": round(eval_duration_sec, 4),
            "tokens_per_sec": round(tokens_per_sec, 2),
            "eval_count": eval_count
        }

    @staticmethod
    def calculate_accuracy(generated_text: str, ground_truth: str) -> Dict[str, Any]:
        """
        Performs basic string-matching accuracy validation for text classification.
        For advanced OCR metrics (CER, WER, IoU), see docs/research/ocr_evaluation_metrics.md.
        """
        gen_clean = generated_text.strip().lower()
        truth_clean = ground_truth.strip().lower()
        
        exact_match = (gen_clean == truth_clean)
        substring_match = (truth_clean in gen_clean)
        
        return {
            "exact_match": exact_match,
            "substring_match": substring_match,
            "score": 1.0 if substring_match else 0.0
        }

    @classmethod
    def process_result(cls, result: Dict[str, Any], ground_truth_key: str = "label") -> Dict[str, Any]:
        """
        Processes a single batch execution result to extract telemetry and accuracy.
        """
        telemetry = cls.calculate_telemetry(result)
        
        generated_text = result.get("response", "")
        ground_truth = str(result.get("item", {}).get(ground_truth_key, ""))
        
        accuracy = cls.calculate_accuracy(generated_text, ground_truth)
        
        return {
            "item": result.get("item"),
            "response": generated_text,
            "telemetry": telemetry,
            "accuracy": accuracy
        }

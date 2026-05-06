# OCR Model Evaluation Metrics (Draft)

When evaluating Optical Character Recognition (OCR) models and tools, accuracy must be measured across multiple dimensions depending on the complexity of the source document and the desired output.

## 1. Text Accuracy Metrics
These metrics compare the raw extracted text against the ground truth text, ignoring spatial positioning.
*   **Character Error Rate (CER):** The percentage of characters that were incorrectly recognized (insertions, deletions, substitutions). This is the most common low-level OCR metric.
*   **Word Error Rate (WER):** The percentage of words that were incorrectly recognized. Useful for evaluating semantic understanding.
*   **String Exact Match:** A binary metric (1 or 0) indicating if the entire extracted string perfectly matches the ground truth.
*   **Substring Match / Keyword Recall:** Indicates if specific target keywords or phrases were successfully extracted from the document.
*   **Levenshtein Distance / Edit Distance:** The raw number of single-character edits required to change the extracted text into the ground truth text.

## 2. Structural & Spatial Metrics (Layout Analysis)
These metrics evaluate how well the model understood the physical layout of the document.
*   **Bounding Box IoU (Intersection over Union):** Compares the spatial bounding box of an extracted word/block against the ground truth bounding box.
*   **Reading Order Accuracy:** Evaluates if the extracted text blocks are sequenced in the correct human-readable order (e.g., handling multi-column layouts).
*   **Table Extraction Accuracy:** Measures the correct identification of rows, columns, and cell associations (e.g., Grid-based evaluation, TEDS - Tree Edit Distance based Similarity).

## 3. Semantic & Key-Value Extraction Metrics
For Information Extraction (IE) tasks where documents (like receipts or invoices) have specific fields.
*   **Field-Level Precision/Recall/F1:** Measures whether specific key-value pairs (e.g., "Total Amount", "Invoice Date") were correctly identified and extracted.
*   **Entity Recognition Accuracy:** Evaluates the correct classification of extracted text into entities (e.g., Person Name, Address).

## 4. Performance & Telemetry Attributes
*   **Latency (Time to First Token / Total Duration):** Time taken to process the document.
*   **Throughput (Pages per Second / Tokens per Second):** Processing speed for batch operations.
*   **Resource Utilization (VRAM / RAM):** Peak memory footprint required during inference.
*   **Model Size / Parameter Count:** The storage footprint of the model weights.

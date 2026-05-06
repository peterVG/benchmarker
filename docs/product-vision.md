# Benchmarker

## Product Vision
**Description:** A lightweight, automated benchmarking harness designed to batch-test local AI models (specifically for OCR and text classification) across diverse hardware profiles. It evaluates system performance and model accuracy, outputting presentation-ready reports.

## Target Users & Customer Profile
**Description:** Solo AI developer/engineer prioritizing automated dataset pipelines, precise metric tracking, and exportable data visualizations over a polished consumer user interface.

## Core Features
**Description:**
1. Automated dataset ingestion (e.g., HuggingFace datasets like RVL-CDIP, FUNSD, SROIE).
2. Batch execution harness to run documents through local vision/language models.
3. Metric collection engine tracking *System Performance* (VRAM, latency, tokens/sec) and *Accuracy* (using ground-truth comparisons).
4. Persistent storage of historical test results for retroactive browsing.
5. Presentation-ready reporting via a simple HTML pager.

## User Requirements
**Description:**
- "I need to rapidly switch local models and run an automated benchmark script without altering my dataset structure."
- "I need exportable, good-looking graphical and text reports for presentations and articles."
- "I need a persistent record of all past test runs that I can browse retroactively."
- "The tool must run consistently on both Apple Silicon (Macbook M5 24GB) and Nvidia architectures (Asus GX10 DGX 128GB)."

## Technical Stack
**Description:**
- **Execution Layer:** Ollama (for cross-platform local model execution).
- **Orchestration:** Python backend scripting using the HuggingFace `datasets` library.
- **Datastore:** SQLite (for persistent storage of benchmarking metrics and historical test runs).
- **Reporting:** Simple HTML pager/dashboard for browsing SQLite records and visualizing performance metrics graphically.

## Standards, Laws, and Regulations
**Description:** N/A for personal developer tool, though data sovereignty is maintained by keeping all processing strictly local.

## Technical & Domain References
**Description:**
- HuggingFace OCR Datasets (e.g., FUNSD, SROIE, RVL-CDIP).
- Ollama API Documentation.

## Value Propositions
**Description:** Replaces manual drag-and-drop LLM testing with rigorous, reproducible, hardware-aware data science pipelines that work identically on Mac and PC.

## Unfair Advantage / The Moat
**Description:** N/A (Internal Developer Tool)

## Key Constraints
**Description:**
- Must run entirely locally with no external APIs.
- Must execute seamlessly on both Apple Silicon (M5) and Nvidia architectures without codebase rewrites.
- Optimization for minimal dependencies and lightweight operation.

## Market Analysis
**Description:** N/A (Internal Developer Tool)

## Key Competitors
**Description:** N/A (Internal Developer Tool)

## Revenue Streams
**Description:** N/A (Internal Developer Tool)

## Sales Channels
**Description:** N/A (Internal Developer Tool)

## Key Resources & Partnerships
**Description:** N/A (Internal Developer Tool)

## Cost Structure
**Description:** Free open-source local tooling (Ollama, Python, SQLite). No recurring cloud compute costs.

## Key Metrics
**Description:**
- System metrics (tokens per second, RAM/VRAM usage, time to first token).
- Accuracy metrics (classification correctness, precise text extraction rate).

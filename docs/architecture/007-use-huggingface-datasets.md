# Architecture Decision Record - Benchmarker
007-use-huggingface-datasets.md

1. **Title:** Use HuggingFace Datasets for Ingestion
2. **Status:** Accepted
3. **Context / Requirement Reference:** F-001 Automated Dataset Ingestion requires standardizing inputs for benchmarking OCR and Text Classification models without manual user effort.
4. **Decision:** We will use the Python `datasets` library from HuggingFace.
5. **Rationale:** `datasets` provides programmatic, one-line access to standard industry benchmarks (RVL-CDIP, FUNSD, SROIE). It automatically handles caching and stream downloading, drastically reducing script complexity.
6. **Assumptions:** The host machine has internet access during the initial dataset ingestion phase (though offline execution works thereafter).
7. **Alternatives Considered:** 
   - Writing custom parsers for raw `.zip` files hosted on various university websites (rejected due to high maintenance burden and fragility).
8. **Consequences / Implications:** The backend script gains a dependency on the HuggingFace ecosystem, but it simplifies data preparation significantly.
9. **Related Decisions / Notes:** Integrates with `dataset_ingestion_SRS-BENCH-001.feature`.

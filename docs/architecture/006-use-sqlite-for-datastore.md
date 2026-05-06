# Architecture Decision Record - Benchmarker
006-use-sqlite-for-datastore.md

1. **Title:** Use SQLite for Results Datastore
2. **Status:** Accepted
3. **Context / Requirement Reference:** F-004 Persistent Storage of Results and TC-002 SQLite Datastore mandate a zero-friction, serverless database to persist benchmarking metrics.
4. **Decision:** We will use SQLite to store all telemetry, configuration, and accuracy metric data.
5. **Rationale:** SQLite requires zero installation or provisioning. The database lives as a single file (`data/benchmarker.sqlite`), making it fully portable and compliant with the "Scale-to-Zero" (NFR-004) and "Local-First Processing" (NFR-002) requirements.
6. **Assumptions:** Benchmark throughput will not exceed the concurrent write limits of SQLite, which is safe since we run batches sequentially.
7. **Alternatives Considered:** 
   - `PostgreSQL` via Docker (rejected because it violates the "Minimize Dependencies" rule and requires an active daemon).
   - Flat JSON or CSV files (rejected because F-005 Presentation Reporting requires structured querying).
8. **Consequences / Implications:** The frontend reporting tool needs to parse a local SQLite file instead of making network calls to a hosted DB server.
9. **Related Decisions / Notes:** Integrates with `persistent_storage_SRS-BENCH-004.feature`.

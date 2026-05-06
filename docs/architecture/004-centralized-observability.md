# Architecture Decision Record - Benchmarker
004-centralized-observability.md

1. **Title:** Use Loki, Redpanda, Promtail, Prometheus, and Grafana for Centralized Observability
2. **Status:** Accepted
3. **Context / Requirement Reference:** The Centralized Logging & Observability Mandate prohibits local file logging and requires applications to output to stdout, captured by a centralized stack.
4. **Decision:** We will use Promtail to scrape Docker stdout, Redpanda to buffer events, Loki to store logs, Prometheus to store metrics, and Grafana to visualize everything.
5. **Rationale:** This stack treats logs as event streams, which is the modern standard. Redpanda provides high-throughput Kafka-compatible buffering without Zookeeper. Loki natively integrates with Grafana.
6. **Assumptions:** Docker Compose is available on the host machine to orchestrate the infrastructure.
7. **Alternatives Considered:** 
   - ELK Stack (Elasticsearch, Logstash, Kibana) - Heavier resource footprint compared to the PLG (Promtail, Loki, Grafana) stack.
8. **Consequences / Implications:** Developers cannot rely on text file logs locally; they must use the Grafana UI.
9. **Related Decisions / Notes:** Orchestration is handled via the root `docker-compose.yml`.

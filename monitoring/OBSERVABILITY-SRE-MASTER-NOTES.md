# 📊 OBSERVABILITY SRE MASTER STUDY GUIDE

This single document covers the principles and tools required to maintain visibility in complex production systems.

---

## 📈 1. The Four Golden Signals
The baseline for any SRE monitoring strategy:
- **Latency**: Request time.
- **Traffic**: Load/Demand.
- **Errors**: Failure rate.
- **Saturation**: Resource utilization.

---

## 🏛️ 2. The Three Pillars
- **Metrics**: Time-series data (Prometheus).
- **Logs**: Event streams (Loki / ELK).
- **Traces**: Request flow (Tempo / Jaeger).

---

## 🔥 3. Prometheus & Grafana
- **Prometheus**: Scrapes metrics using PromQL.
- **Grafana**: Multi-source visualization. Use variable-driven dashboards for scale.

---

## 📜 4. Log Aggregation (Loki & ELK)
- **Loki**: Optimized for costs, uses Prometheus-style labels.
- **ELK (Elasticsearch/Kibana)**: Full-text search and complex analytics.

---

## 🎯 5. SLAs, SLOs, and SLIs
- **SLI**: What you measure (Indicator).
- **SLO**: Your goal (Objective).
- **SLA**: The contract with the customer (Agreement).
- **Error Budget**: The allowed downtime (100% - SLO).

---

## 🏠 6. Localhost Testing (Docker Compose)
```yaml
services:
  prometheus: { image: prom/prometheus }
  grafana: { image: grafana/grafana }
  loki: { image: grafana/loki }
```

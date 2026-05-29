# 📊 Observability Mastery: The Soul of SRE

Monitoring is about knowing "something is wrong." Observability is about knowing "WHY it is wrong." For an SRE, this is the most critical tool for maintaining SLAs.

## 1. The Four Golden Signals
If you monitor nothing else, monitor these four:
- **Latency**: Time it takes to service a request.
- **Traffic**: Demand placed on the system (e.g., HTTP requests/sec).
- **Errors**: Rate of requests that fail (e.g., HTTP 500s).
- **Saturation**: How "full" your service is (e.g., CPU/Memory usage).

## 2. The Three Pillars of Observability
- **Metrics**: Aggregated data over time (e.g., CPU is 80%). **Tool**: Prometheus.
- **Logs**: Event details (e.g., "User X failed to login"). **Tool**: Loki / ELK.
- **Traces**: End-to-end journey of a request across services. **Tool**: Tempo / Jaeger.

## 3. Prometheus & Grafana (The Power Duo)
- **Prometheus**: Pull-based metrics collection. Uses **PromQL** for querying.
- **Grafana**: Visualizes PromQL data. **SRE Tip**: Use "Variable-driven" dashboards to switch between Dev, Stage, and Prod environments easily.

## 4. Alerting & SLIs/SLOs
- **SLI (Indicator)**: What you measure (e.g., Uptime %).
- **SLO (Objective)**: The goal you set (e.g., 99.9% Uptime).
- **Error Budget**: The difference between 100% and your SLO (e.g., 0.1%).
- **Alertmanager**: Routes alerts to Slack/PagerDuty. **SRE Best Practice**: Only page for "Actionable" issues. Don't page for "CPU is 90%" if the app is fine.

## 5. Log Aggregation with Loki
Loki is like Prometheus, but for logs.
- **Pros**: Uses the same labels as Prometheus. Very cost-effective because it doesn't index the full log text like Elasticsearch.

---

## 🏠 How to test Observability on Localhost?
Run the full stack using **Docker Compose**.

1.  **Spin up the stack**:
    ```bash
    docker-compose up -d prometheus grafana loki
    ```
2.  **Verify**: Access Grafana at `localhost:3000` and start building dashboards for your local containers.
3.  **Simulation**: Practice writing Alerting rules in Prometheus and visualizing them in Grafana.

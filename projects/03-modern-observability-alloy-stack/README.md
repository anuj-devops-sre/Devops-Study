# 📈 Project: Modern Observability with Grafana Alloy Stack

This project implements the modern **LGTM stack** (Loki, Grafana, Tempo, Mimir/Prometheus) using **Grafana Alloy** as the unified telemetry collector.

## 🏗️ Architecture
`App/Host` -> `Grafana Alloy` -> `Prometheus (Metrics)` & `Loki (Logs)` -> `Grafana (Visualization)`

### Why Grafana Alloy?
- **Unified Agent**: Replaces Promtail, Prometheus Agent, and OpenTelemetry Collector.
- **HCL Configuration**: Powerful, programmable configuration language.
- **High Performance**: Built for scale and low resource usage.
- **Native Support**: Works perfectly with Grafana Cloud and local OSS stacks.

## 🛠️ Components
1.  **Grafana**: The visualization layer.
2.  **Loki**: The log aggregation engine.
3.  **Prometheus**: The time-series metrics database.
4.  **Alloy**: The modern agent that scrapes metrics and tail logs.

## 📂 Configuration

### 1. Alloy Config (`config/alloy/config.alloy`)
Alloy uses a new syntax. Here is a basic config to scrape logs and metrics:
```hcl
// Collect Metrics
prometheus.scrape "local_scrape" {
  targets = [{"__address__" = "node-exporter:9100"}]
  forward_to = [prometheus.remote_write.local_prom.receiver]
}

prometheus.remote_write "local_prom" {
  endpoint {
    url = "http://prometheus:9090/api/v1/write"
  }
}

// Collect Logs (Replaces Promtail)
loki.source.file "local_logs" {
  targets = [
    { "__path__" = "/var/log/*.log", "job" = "system_logs" },
  ]
  forward_to = [loki.write.local_loki.receiver]
}

loki.write "local_loki" {
  endpoint {
    url = "http://loki:3100/loki/api/v1/push"
  }
}
```

### 2. Local Stack Setup (`docker-compose.yml`)
```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    command: ["--config.file=/etc/prometheus/prometheus.yml", "--enable-feature=remote-write-receiver"]
    ports: ["9090:9090"]

  loki:
    image: grafana/loki:latest
    ports: ["3100:3100"]

  grafana:
    image: grafana/grafana:latest
    ports: ["3000:3000"]
    environment: ["GF_SECURITY_ADMIN_PASSWORD=admin"]

  alloy:
    image: grafana/alloy:latest
    volumes:
      - ./config/alloy/config.alloy:/etc/alloy/config.alloy
      - /var/log:/var/log
    command: ["run", "--storage.path=/var/lib/alloy/data", "/etc/alloy/config.alloy"]
    depends_on: ["prometheus", "loki"]

  node-exporter:
    image: prom/node-exporter:latest
```

## 🚀 Getting Started
1.  `docker-compose up -d`
2.  Open Grafana at `http://localhost:3000`.
3.  Add **Prometheus** and **Loki** as data sources.
4.  Import **Node Exporter Full** dashboard (ID: 1860).

## 📉 SRE Impact
- **Consolidation**: One agent to manage instead of three.
- **Visibility**: Real-time correlation between logs and metrics in Grafana.
- **Future Proof**: Alloy is the successor to Promtail; mastering it puts you ahead of the curve.

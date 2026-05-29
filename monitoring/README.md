# 📊 Monitoring & Observability Stack

This module provides a production-grade observability stack using **Prometheus**, **Grafana**, and **Loki**.

## 🚀 Components

- **Prometheus**: Time-series database for metrics collection.
- **Grafana**: Multi-platform analytics and interactive visualization.
- **Loki**: Horizontally scalable log aggregation system.
- **ELK Stack (Elasticsearch, Logstash, Kibana)**: Search, analyze, and visualize data in real-time.
- **CloudWatch**: AWS-native monitoring and observability service.
- **Promtail**: Agent which ships the contents of local logs to Loki.
- **Node Exporter**: Prometheus exporter for hardware and OS metrics.

## 🛠️ Getting Started

1. **Start the stack:**
   ```bash
   cd monitoring
   docker-compose up -d
   ```

2. **Access the dashboards:**
   - **Grafana**: [http://localhost:3000](http://localhost:3000) (User: `admin`, Pass: `admin`)
   - **Prometheus**: [http://localhost:9090](http://localhost:9090)

3. **Verify Datasources:**
   Grafana is pre-provisioned with Prometheus and Loki datasources. Go to **Configuration -> Data Sources** to verify.

## 📈 Key Metrics & Logs

- **Metrics**: Scrapes LocalStack, Prometheus itself, and the host machine (via Node Exporter).
- **Logs**: Promtail is configured to scrape `/var/log/*log` from the host.

## 🛡️ Best Practices
- **Security**: Default admin password is set via environment variables. In production, use a Secret Manager.
- **Persistence**: Currently uses ephemeral storage for testing. For production, attach external volumes (EBS/S3).

# 🚀 Project: CloudWatch Logs to ELK via Fluentd

This project implements a centralized logging pipeline to ship AWS CloudWatch logs to an Elasticsearch + Kibana stack using **Fluentd** as the log aggregator.

## 🏗️ Architecture
`AWS CloudWatch Logs` -> `Fluentd (with cloudwatch plugin)` -> `Elasticsearch` -> `Kibana`

### Why Fluentd?
- **Lightweight**: Low memory footprint (written in Ruby/C).
- **Flexible**: 500+ plugins for various inputs and outputs.
- **Unified Logging Layer**: Decouples data sources from backend storage.

## 🛠️ Prerequisites
1.  **IAM Role**: Fluentd needs `logs:DescribeLogGroups`, `logs:DescribeLogStreams`, and `logs:GetLogEvents` permissions.
2.  **AWS Credentials**: Configured in the Fluentd container/host.

## 📂 Configuration

### 1. Fluentd Config (`config/fluent.conf`)
```apache
<source>
  @type cloudwatch_logs
  log_group_name "/aws/eks/prod-cluster"
  log_stream_name "kube-apiserver"
  region "us-east-1"
  tag cloudwatch.eks
</source>

<match cloudwatch.**>
  @type elasticsearch
  host elasticsearch
  port 9200
  logstash_format true
  logstash_prefix aws-logs
  flush_interval 5s
</match>
```

### 2. Local Lab Setup (`docker-compose.yml`)
You can simulate the ELK stack and Fluentd locally:
```yaml
services:
  elasticsearch:
    image: elasticsearch:8.8.0
    environment: ["discovery.type=single-node", "xpack.security.enabled=false"]
    ports: ["9200:9200"]

  kibana:
    image: kibana:8.8.0
    ports: ["5601:5601"]
    depends_on: ["elasticsearch"]

  fluentd:
    build: .
    volumes: ["./config:/fluentd/etc"]
    depends_on: ["elasticsearch"]
```

## 🚀 Deployment Steps
1.  **IAM Setup**: Create an IAM user/role with CloudWatch read permissions.
2.  **Fluentd Plugin**: Install `fluent-plugin-cloudwatch-logs` inside your Fluentd image.
3.  **Run Stack**: `docker-compose up -d`.
4.  **Visualize**: Open Kibana at `http://localhost:5601`, create an Index Pattern `aws-logs-*`, and start searching.

## 📉 SRE Impact
- **Troubleshooting**: Search logs from multiple AWS accounts and services in one place.
- **Retention Management**: Save costs by setting low retention in CloudWatch and long-term storage in Elasticsearch/S3.
- **Alerting**: Configure Kibana alerts for specific error patterns (e.g., "Out of Memory" or "401 Unauthorized").

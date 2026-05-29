# 🏗️ Terraform: Modern Observability Infrastructure (LGTM Stack)

This directory contains the IaC for the **Grafana Alloy + LGTM** observability stack.

## 📂 Resources Provisioned
1.  **EC2 Instance**: To host the Dockerized LGTM stack (Loki, Grafana, Prometheus).
2.  **VPC / Subnets**: Network isolation for the monitoring stack.
3.  **CloudWatch Logs**: Integration for Alloy to scrape logs.
4.  **Security Groups**: Ports 3000 (Grafana), 9090 (Prom), 3100 (Loki), 12345 (Alloy UI).

## 🚀 Usage
1.  Navigate to this directory.
2.  `terraform init`
3.  `terraform plan`
4.  `terraform apply`

## 📜 Key Files
- `main.tf`: EC2 and network setup.
- `alloy_iam.tf`: Permissions for Alloy to scrape CloudWatch and EC2 metrics.
- `variables.tf`: Configuration inputs.

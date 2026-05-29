# 🏗️ Terraform: Centralized Logging Infrastructure (Fluentd to ELK)

This directory contains the Infrastructure as Code (IaC) required to support the **CloudWatch to ELK** project.

## 📂 Resources Provisioned
1.  **IAM Role & Policy**: Permissions for Fluentd to read from CloudWatch and write to Elasticsearch.
2.  **CloudWatch Log Groups**: Sources for the logs.
3.  **Security Groups**: Network access rules for the logging stack.

## 🚀 Usage
1.  Navigate to this directory.
2.  `terraform init`
3.  `terraform plan`
4.  `terraform apply`

## 📜 Key Files
- `main.tf`: Main infrastructure definition.
- `iam.tf`: IAM roles and policies (Critical for Fluentd).
- `variables.tf`: Configuration inputs.
- `outputs.tf`: Important data like the IAM Role ARN.

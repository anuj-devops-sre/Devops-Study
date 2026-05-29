# 💻 Local SRE Environment: Cloud on Localhost

A key SRE skill is developing and testing infrastructure locally to save time and cloud costs.

## 1. LocalStack (AWS Emulator)
LocalStack allows you to run a full AWS environment on your laptop.
- **Services Supported**: S3, EC2, Lambda, DynamoDB, SQS, SNS, and more.
- **Why use it?**: No bills, no internet needed, instant cleanup.

### 🛠️ Installation & Start
```bash
# Via Docker Compose
docker-compose up -d localstack

# Verify
awslocal s3 ls
```

## 2. Kind/Minikube (Kubernetes Locally)
Instead of paying for EKS for testing, run K8s inside Docker.
- **Kind (Kubernetes in Docker)**: Fast, lightweight, great for CI/CD.
- **Use Case**: Testing Helm charts, Network Policies, and RBAC locally.

## 3. Docker Compose (Microservices Setup)
Simulate a multi-tier app architecture locally.
```yaml
version: '3'
services:
  app:
    build: .
    ports: ["8080:8080"]
  db:
    image: postgres:latest
```

## 🚀 SRE Localhost Workflow
1.  Write Terraform code.
2.  Point Terraform to **LocalStack** (via provider overrides).
3.  `terraform apply` locally.
4.  Verify infra with `awslocal` CLI.
5.  Destroy and push to Cloud only when verified.

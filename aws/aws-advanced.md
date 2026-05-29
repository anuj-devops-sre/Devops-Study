# ☁️ AWS EKS, ECS, EC2, RDS, S3 & CloudWatch

This guide covers the core AWS services used in our production environments.

## 🚀 ECS (Elastic Container Service)
- **Clusters**: Logical grouping of tasks or services.
- **Task Definitions**: Blueprint for your application (containers, CPU/Memory).
- **Services**: Maintains the desired count of tasks.

## 📊 CloudWatch
- **Metrics**: Standard and Custom metrics for monitoring.
- **Logs**: Centralized logging for EC2, Lambda, and ECS.
- **Alarms**: Triggers actions based on metric thresholds.

## 🗄️ RDS (Relational Database Service)
- Managed databases (PostgreSQL, MySQL).
- Multi-AZ for high availability.
- Read Replicas for scaling.

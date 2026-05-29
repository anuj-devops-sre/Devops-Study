# 💻 EC2 (Elastic Compute Cloud) SRE MASTER NOTES

Elastic Compute is the core of AWS. Focus on **Performance, Scale, and Cost**.

## 1. Instance Families
- **T-Series**: Burstable (Dev/Test).
- **M-Series**: Balanced (General Purpose).
- **C-Series**: High CPU (Batch jobs/Encoding).
- **R-Series**: High RAM (Databases/Redis).
- **Graviton (ARM)**: **SRE Choice**: 40% better price-performance.

## 2. Cost Strategies
- **Spot Instances**: Up to 90% savings. Use for fault-tolerant apps (K8s nodes).
- **Reserved Instances (RI) / Savings Plans**: ~72% savings for stable, 24/7 workloads.
- **On-Demand**: Default price. Use for testing/spiky loads.

## 3. SRE Best Practices
- **Never launch single EC2**: Use **ASGs** (Auto Scaling Groups) across multiple AZs.
- **AMI Management**: Use **Packer** to build pre-configured "Golden AMIs".
- **Right-Sizing**: Use CloudWatch metrics to see if instances are over-provisioned.

## 4. Local Testing
```bash
awslocal ec2 run-instances --image-id ami-ff00ff00 --instance-type t2.micro
```

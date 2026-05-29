# ☁️ AWS SRE MASTER STUDY GUIDE

This single document covers all core AWS services required for a Mid-level SRE/Platform Engineer role, focusing on **Architecture, Scalability, and Cost Optimization**.

---

## 🔐 1. IAM (Identity & Access Management)
Identity and Access Management is the first line of defense. Focus on the **Principle of Least Privilege**.

### Core Concepts
- **Users/Groups/Roles**: Long-term vs. Temporary credentials.
- **Policies**: JSON definitions (Identity-based vs. Resource-based).
- **Evaluation Logic**: Explicit Deny > Explicit Allow > Default Deny.

### SRE Best Practices
- **Use Roles, Not Keys**: Use Instance Profiles for EC2 or **IRSA** for EKS.
- **Condition Keys**: Restrict access by IP, Region, or Tag.
- **Service Control Policies (SCP)**: Restrict permissions at the Organization level.

---

## 💻 2. EC2 (Elastic Compute Cloud)
Virtual servers in the cloud. Focus on **Instance Families and Purchasing Options**.

### Instance Types
- **T-Series**: Burstable (Dev/Test).
- **M-Series**: General Purpose (Balanced).
- **C-Series**: Compute Optimized (Batch processing).
- **R-Series**: Memory Optimized (DBs/Caching).
- **Graviton (ARM)**: **SRE Tip**: 40% better price-performance.

### Cost Strategy
- **On-Demand**: 0% saving.
- **Reserved/Savings Plans**: ~72% saving (Long-term).
- **Spot Instances**: ~90% saving (Fault-tolerant workloads/K8s nodes).

---

## 🌐 3. VPC & Networking
The logical data center. Focus on **Traffic Flow and Security**.

### Core Components
- **Public Subnet**: Route to Internet Gateway (IGW).
- **Private Subnet**: No direct internet route (DBs/App Servers).
- **NAT Gateway**: Allows private resources to talk to the internet.
- **Security Groups vs. NACLs**: Stateful (Instance) vs. Stateless (Subnet).

### SRE Cost Optimization
- **VPC Endpoints (PrivateLink)**: Avoid NAT Gateway fees for S3/ECR/DynamoDB.
- **NAT Instances**: Cheaper alternative for Non-prod environments.

---

## 📦 4. S3 (Simple Storage Service)
Focus on **Durability and Lifecycle Management**.

### Storage Classes
- **Standard**: Frequent access.
- **Standard-IA**: Infrequent access (Lower storage price, high retrieval fee).
- **Glacier Deep Archive**: Cheapest (Compliance logs).
- **Intelligent-Tiering**: **SRE Best Practice**. Automatically optimizes costs.

### Security & Compliance
- **Public Access Block**: Enable at account level.
- **Versioning & Object Lock**: Prevent accidental deletes/WORM compliance.

---

## 🗄️ 5. RDS & Databases
Managed relational databases. Focus on **Availability and Performance**.

### Multi-AZ vs. Read Replicas
- **Multi-AZ**: High Availability (Failover).
- **Read Replicas**: Performance Scaling (Read-heavy loads).

### Aurora
- Cloud-native, 6 copies of data, faster failover.
- **Serverless v2**: Great for scaling Dev/Stage environments.

---

## 🏠 6. Localhost Testing (LocalStack)
Simulate AWS on your laptop to save costs.
```bash
# S3 Test
awslocal s3 mb s3://test-bucket
# EC2 Test
awslocal ec2 run-instances --image-id ami-ff00ff00 --instance-type t2.micro
```

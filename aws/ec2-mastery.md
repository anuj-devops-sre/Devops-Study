# 💻 EC2 Mastery: From Zero to SRE

Elastic Compute Cloud (EC2) is the backbone of AWS infrastructure. For an SRE, it's not just about "launching a server," but about **Scale, Cost, and Reliability**.

## 1. What is EC2?
Virtual servers in the cloud. It provides resizable compute capacity.

## 2. Instance Types (The "Alphabet Soup")
Recruiters look for knowledge of when to use which type:
- **T-Series (t2, t3)**: Burstable performance. Best for low-traffic apps or dev environments.
- **M-Series (m5, m6g)**: General purpose. Balanced CPU/Memory.
- **C-Series (c5, c6g)**: Compute Optimized. High-performance CPUs (Batch processing, media encoding).
- **R-Series (r5, r6g)**: Memory Optimized. Large RAM (Databases, Caching like Redis).
- **Graviton (m6g, c6g, r6g)**: AWS-designed ARM chips. **SRE Tip**: Always suggest these for **40% better price-performance**.

## 3. Purchasing Options (The SRE Cost Strategy)
| Option | Use Case | Cost Saving |
| :--- | :--- | :--- |
| **On-Demand** | Spiky workloads, testing. | 0% |
| **Reserved (RI)** | Long-term stable apps (1-3 years). | Up to 72% |
| **Savings Plans** | Flexible commitment across instance types. | Up to 72% |
| **Spot Instances** | Stateless, fault-tolerant apps (K8s worker nodes). | **Up to 90%** |

## 4. How to Create (The SRE Way)
Don't use the Console. Use **Infrastructure as Code (Terraform)**:
```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  
  tags = {
    Name = "HelloWorld"
    Environment = "Prod"
  }
}
```

## 5. SRE Best Practices & Cost Saving
1.  **Right-Sizing**: Use AWS Compute Optimizer to see if you are over-provisioning (e.g., using a Large when a Small is enough).
2.  **Spot Instances for K8s**: Use Spot for 80% of your EKS nodes using **Karpenter**.
3.  **Graviton Migration**: Move your Linux workloads to Graviton (ARM) instances.
4.  **Auto Scaling**: Never launch a single EC2 for production. Use **Auto Scaling Groups (ASG)** across multiple AZs.

---

## 🏠 How to test EC2 on Localhost?
Since you can't run a real EC2 on your laptop easily, SREs use **LocalStack** or **Docker** to simulate environments.

1.  **Simulate with LocalStack**:
    ```bash
    localstack start
    awslocal ec2 run-instances --image-id ami-ff00ff00 --instance-type t2.micro
    ```
2.  **Mock Infrastructure**: Use Docker Compose to act as "instances" for networking labs.

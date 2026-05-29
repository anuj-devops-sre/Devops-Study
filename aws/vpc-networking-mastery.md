# 🌐 VPC & Networking: The SRE's Logical Data Center

Networking is where 90% of production issues and 40% of cloud bills live. For a Mid-level SRE, you must master **Traffic Flow, Security, and Cost**.

## 1. What is a VPC?
A private, isolated section of AWS where you launch resources. Think of it as your own virtual data center.

## 2. Core Components (The Build)
- **Subnets**: 
  - **Public**: Has a route to the Internet Gateway (IGW). Used for Load Balancers/Bastion hosts.
  - **Private**: No direct internet route. Used for App Servers and Databases. **SRE Rule**: Always keep DBs in Private Subnets.
- **NAT Gateway**: Allows private resources to talk to the internet (e.g., for OS updates) without being reachable from the outside.
- **Security Groups (SG)**: Stateful firewalls at the Instance level (Allow rules only).
- **NACLs**: Stateless firewalls at the Subnet level (Allow and Deny rules).

## 3. SRE Cost Optimization (The "Bill Killer")
Recruiters love asking about NAT Gateway costs.
| Problem | SRE Solution | Impact |
| :--- | :--- | :--- |
| **High NAT Gateway Bill** | Use **VPC Endpoints (PrivateLink)** for S3, ECR, and DynamoDB. | Saves ~$0.045/GB data processing fee. |
| **Cross-AZ Data Transfer** | Keep traffic within the same Availability Zone where possible. | Reduces "Inter-AZ" transfer costs. |
| **NAT Gateway for Dev** | Use a **NAT Instance** (t3.micro) instead of a NAT Gateway. | Saves ~$32/month per VPC. |

## 4. How to Create (Terraform Standard)
```hcl
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  name   = "my-vpc"
  cidr   = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true # Cost saving for non-prod
}
```

## 5. Troubleshooting (Day-2 Operations)
- **Problem**: EC2 can't reach the internet.
- **SRE Checklist**:
  1. Check if the Subnet has a Route Table entry to a NAT Gateway.
  2. Check if the NAT Gateway is in a Public Subnet with an IGW.
  3. Check if Security Group egress rules allow traffic.

---

## 🏠 How to test Networking on Localhost?
You can't create a real "VPC" on a laptop, but you can simulate the **Network Topology** using **Docker Networks**.

1.  **Isolate Containers**:
    ```bash
    # Create a private network
    docker network create --internal private_net
    
    # Create a public network
    docker network create public_net
    ```
2.  **Simulation**: Run your DB container on `private_net` and your Nginx container on both `public_net` and `private_net` to act as a bridge (Reverse Proxy).

# 🔐 AWS IAM Deep Dive: The SRE Security Perimeter

Identity and Access Management (IAM) is the first line of defense. A Mid-level SRE must move beyond "FullAccess" to the **Principle of Least Privilege**.

## 1. Core Concepts
- **Users**: Long-term credentials for humans or apps.
- **Groups**: Collections of users.
- **Roles**: Temporary credentials. Used by EC2, Lambda, or EKS Pods (IRSA).
- **Policies**: JSON definitions of what is allowed.
  - **Identity-based**: Attached to Users/Roles.
  - **Resource-based**: Attached to S3 Buckets, KMS Keys, or SQS queues.

## 2. Policy Evaluation Logic
1.  **Explicit Deny**: If any policy says "Deny", the request is blocked immediately.
2.  **Explicit Allow**: If no Deny exists, an Allow is required.
3.  **Default Deny**: If neither Deny nor Allow exists, the request is blocked.

## 3. SRE Best Practices
- **Never use Root User**: Use IAM Admin instead.
- **Enforce MFA**: Mandatory for all console users.
- **Use Roles, Not Keys**: Never hardcode Access Keys. Use Instance Profiles for EC2 or **IRSA** for EKS.
- **Condition Keys**: Restrict access by IP, Region, or Tag.
  ```json
  "Condition": {"StringEquals": {"aws:RequestedRegion": "us-east-1"}}
  ```

## 4. Advanced Topics
- **Service Control Policies (SCP)**: Restrict permissions at the AWS Organization level.
- **Permission Boundaries**: Set the maximum permissions an IAM entity can have.

---

## 🛠️ Local Practice (LocalStack)
```bash
# Create an IAM Role locally
awslocal iam create-role --role-name MyLocalRole --assume-role-policy-document file://trust-policy.json
```

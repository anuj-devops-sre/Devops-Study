# 🔐 IAM (Identity & Access Management) SRE MASTER NOTES

Identity is the first line of defense. Focus on the **Principle of Least Privilege**.

## 1. Core Components
- **Users**: Long-term credentials (IAM User).
- **Groups**: Collections of users with shared policies.
- **Roles**: Temporary credentials. Used by services (EC2, Lambda) or federated users.
- **Policies**: JSON documents.
  - **Identity-based**: Attached to IAM entities.
  - **Resource-based**: Attached to S3, KMS, etc.

## 2. Policy Evaluation Logic (Interview Favorite)
1. **Explicit Deny**: Request is blocked immediately.
2. **Explicit Allow**: Request is allowed if no deny exists.
3. **Default Deny**: Blocked if neither allow nor deny exists.

## 3. SRE Best Practices
- **MFA Enforcement**: Mandatory for all console users.
- **Roles over Keys**: Use **IRSA** (IAM Roles for Service Accounts) in EKS to avoid hardcoded keys.
- **SCPs (Service Control Policies)**: Organization-wide permission guardrails.
- **IAM Access Analyzer**: Find resources that are shared publicly.

## 4. Local Testing
```bash
awslocal iam create-user --user-name test-user
```

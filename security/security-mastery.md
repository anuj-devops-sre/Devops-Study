# 🛡️ DevSecOps Mastery: Security at Scale

Security is no longer a separate team; it's a core SRE responsibility. For a Mid-level role, you must "Shift Left" by integrating security early.

## 1. Secret Management (The Gold Standard)
Never store secrets in Git or Environment Variables.
- **AWS Secrets Manager / Parameter Store**: Native AWS solution.
- **HashiCorp Vault**: Industry standard for multi-cloud. **SRE Tip**: Use "Dynamic Secrets" that expire after 1 hour.

## 2. Infrastructure as Code (IaC) Scanning
Scan your Terraform/CloudFormation before you deploy.
- **Checkov / tfsec**: Scans for misconfigurations (e.g., "S3 bucket is public").
- **Terrascan**: Static code analysis for IaC.

## 3. Container Security
- **Image Scanning**: Use **Trivy** or **Snyk** in your pipeline.
- **Runtime Security**: Use **Falco** to detect suspicious activity inside a running container (e.g., someone trying to spawn a shell).
- **Distroless Images**: Reduce attack surface by removing the OS shell.

## 4. Kubernetes Security (The 4C's)
- **Code**: Static analysis of application code.
- **Container**: Image scanning and signing (Notary).
- **Cluster**: RBAC, Network Policies, and Pod Security Standards.
- **Cloud**: IAM Roles for Service Accounts (IRSA).

## 5. Compliance as Code
Use tools like **Open Policy Agent (OPA)** to enforce rules (e.g., "Every EC2 must have a 'CostCenter' tag").

---

## 🏠 How to test Security on Localhost?
1.  **Scan your code**:
    ```bash
    trivy conf ./terraform-folder
    ```
2.  **Run Vault locally**:
    ```bash
    docker run -p 8200:8200 hashicorp/vault
    ```
3.  **Simulation**: Try to store a secret in Vault and retrieve it via a Python script.

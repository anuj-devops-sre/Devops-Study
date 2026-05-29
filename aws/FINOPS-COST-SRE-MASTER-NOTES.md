# 💰 FINOPS & CLOUD COST MANAGEMENT SRE GUIDE

As an SRE, you don't just keep the site up; you keep the company profitable. FinOps is the practice of **Cloud Financial Management**.

---

## 1. The FinOps Lifecycle
- **Inform**: Visibility into spend (Who is spending what?).
- **Optimize**: Reducing waste (Right-sizing, Spot instances).
- **Operate**: Aligning teams to unit economics (Cost per transaction).

## 2. AWS Tools for SREs
- **AWS Cost Explorer**: Analyzing trends and forecasting.
- **AWS Budgets**: Alerting when spend exceeds a threshold.
- **Cost & Usage Report (CUR)**: Granular raw data for deep analysis.
- **Compute Optimizer**: Uses AI to recommend better instance types.

## 3. SRE Cost Savings Checklist
- **Unused Resources**: Delete unattached EBS volumes, Elastic IPs, and idle Load Balancers.
- **Lifecycle Policies**: Move old S3 data to Glacier.
- **Spot for K8s**: Move 80% of stateless Pods to Spot nodes.
- **ARM Migration**: Switch from x86 to Graviton (m7g) for 20% savings.

## 4. Tagging Strategy (The Bedrock)
You can't optimize what you can't measure. 
- **Mandatory Tags**: `Environment`, `Owner`, `Project`, `CostCenter`.
- **Enforcement**: Use Terraform or OPA to block any resource created without these tags.

## 5. Right-Sizing Workflow
1. Identify instances with <10% CPU usage for 30 days.
2. Downsize to a smaller instance or change family (e.g., m5.large -> t3.medium).
3. Switch to **Savings Plans** for the "baseline" usage that never changes.

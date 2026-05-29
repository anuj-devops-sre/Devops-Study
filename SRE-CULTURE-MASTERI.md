# 🏗️ SRE Culture: Incident Management & Reliability

Being an SRE is 50% technical and 50% culture. Mid-level roles require understanding how to handle production failures.

## 1. Error Budgets & SLOs
- **Availability**: 99.9% (3 nines) means ~43 minutes of downtime per month.
- **Error Budget**: If your SLO is 99.9%, you have 0.1% budget to "spend" on new features. If the budget is gone, stop new features and fix stability.

## 2. Incident Response (The On-Call Life)
- **MTTD (Mean Time to Detect)**: How fast you found out.
- **MTTR (Mean Time to Repair)**: How fast you fixed it.
- **Goal**: Minimize MTTR through runbooks and automation.

## 3. Post-Mortems (Blame-Free)
Always write a post-mortem after a high-severity incident.
- **What happened?**
- **Why did it happen?** (Root Cause)
- **How to prevent it from happening again?** (Action Items)
- **SRE Tip**: Focus on systems, not people. Don't blame an engineer for a typo; blame the system for not catching the typo.

## 4. Automation of Toil
**Toil** is manual, repetitive work with no long-term value.
- If you do it 3 times, automate it.
- SRE goal: Spend <50% of your time on operations (toil) and >50% on project/development work.

## 5. Deployment Strategies (Recap)
- **Canary**: Minimize blast radius.
- **Blue/Green**: Instant rollback.
- **Rolling Update**: Default, but slower to rollback.

---

## 🚀 SRE Career Path
- **Level 1**: Can fix a failing Pod.
- **Level 2 (You)**: Can build an EKS cluster with HPA and Karpenter.
- **Level 3 (Senior)**: Can design a multi-region disaster recovery strategy and manage error budgets for the whole company.

# ☸️ Kubernetes SRE Mastery: The Production Standard

Kubernetes is the ultimate platform for an SRE. For a Mid-level role, you must move beyond Pods and Services to **Scalability, Reliability, and Security (RBAC/IRSA)**.

## 1. Auto-Scaling (The SRE Heartbeat)
Recruiters will grill you on how you handle traffic spikes.
- **HPA (Horizontal Pod Autoscaler)**: Scales the number of Pods based on CPU/Memory usage.
- **VPA (Vertical Pod Autoscaler)**: Recommends/sets the right CPU/Memory limits for your Pods.
- **Karpenter / Cluster Autoscaler**: Provision new nodes when Pods can't be scheduled. **SRE Tip**: Karpenter is faster and more efficient for EKS.

## 2. Reliability (Liveness vs. Readiness)
Never launch a Pod without these:
- **Readiness Probe**: "Is the app ready to take traffic?" (If fail, Pod is removed from Service endpoints).
- **Liveness Probe**: "Is the app still alive?" (If fail, K8s restarts the Pod).
- **Startup Probe**: For slow-starting apps to avoid premature restarts.

## 3. Security & Governance
- **RBAC**: Role-Based Access Control. Limit who can do what in which Namespace.
- **IRSA (IAM Roles for Service Accounts)**: **SRE Best Practice**. Give Pods specific AWS IAM permissions instead of using Node IAM roles.
- **Network Policies**: Restrict traffic between Pods (e.g., only Frontend can talk to Backend).

## 4. Disaster Recovery & Zero Downtime
- **Pod Disruption Budgets (PDB)**: Ensures a minimum number of Pods stay up during maintenance (e.g., node upgrades).
- **Rolling Updates**: The default strategy for zero-downtime deployments.

## 5. How to Deploy (SRE Tooling)
- **Helm**: Manage packages and environments (Values files for Dev/Stage/Prod).
- **ArgoCD / Flux**: GitOps approach. The cluster state always matches the Git repo.

---

## 🏠 How to test Kubernetes on Localhost?
Don't wait for EKS. Use **Kind** or **Minikube**.

1.  **Start a Kind Cluster**:
    ```bash
    kind create cluster --name sre-lab
    ```
2.  **Deploy a Sample App**:
    ```bash
    kubectl create deployment nginx --image=nginx
    kubectl expose deployment nginx --port=80 --type=NodePort
    ```
3.  **Simulation**: Use this to practice writing Helm charts and Network Policies before pushing to Cloud.

# 🧊 GITOPS & ARGOCD SRE MASTER STUDY GUIDE

GitOps is the modern standard for Continuous Deployment (CD) in Kubernetes. It uses Git as the "Single Source of Truth" for infrastructure and applications.

---

## 1. What is GitOps?
GitOps is a practice where the entire state of your cluster is defined in a Git repository.
- **Pull-based**: An agent (ArgoCD) inside the cluster pulls changes from Git.
- **Drift Detection**: If someone changes a resource manually (via kubectl), ArgoCD detects it and reverts it to match Git.

## 2. ArgoCD Architecture
- **Application Controller**: Monitors running applications and compares them with the desired state in Git.
- **Repo Server**: Maintains a local cache of the Git repository.
- **Server**: Provides the API and Web UI.

## 3. Core Concepts
- **Sync Policy**: Manual or Automatic.
- **Prune**: Automatically delete resources that are removed from Git.
- **Self-Heal**: Automatically fix manual changes (Drift).
- **App-of-Apps Pattern**: A master ArgoCD app that manages other ArgoCD apps.

## 4. Deployment Strategies with Argo Rollouts
ArgoCD alone does Rolling Updates. For advanced strategies, use **Argo Rollouts**:
- **Blue/Green**: Switch traffic between two identical versions.
- **Canary**: Gradually shift traffic (e.g., 10%, 20%, 50%, 100%) based on metrics (Prometheus).

## 5. SRE Best Practices
1.  **Repo Structure**: Keep Infrastructure (Terraform), K8s Manifests, and Application Code in separate repos or folders.
2.  **Health Checks**: Define custom health checks in ArgoCD for complex CRDs.
3.  **Notifications**: Integrate with Slack to get alerts on Sync Failures.

---

## 🏠 Local Practice
```bash
# Install ArgoCD in your local cluster (Kind/Minikube)
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Access the UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

# ☸️ K8S SRE MASTER STUDY GUIDE

This single document covers core and advanced Kubernetes concepts required for an SRE role, focusing on **Workloads, Scaling, and Cluster Reliability**.

---

## 🏗️ 1. Core Workload Objects
Understand how to run and manage applications.

- **Pods**: Smallest unit. **SRE Rule**: Never deploy naked Pods.
- **Deployments**: Handle rolling updates and rollbacks.
- **StatefulSets**: For databases (Stable IDs + Persistent Storage).
- **DaemonSets**: Runs on every node (Logging/Monitoring agents).

---

## 🌐 2. Networking & Traffic Flow
How apps talk to each other and the outside world.

- **Services**: 
  - `ClusterIP`: Internal.
  - `NodePort`: External via port.
  - `LoadBalancer`: Cloud LB (NLB/ALB).
- **Ingress**: Layer 7 routing (Domain names, SSL termination).

---

## 📈 3. Auto-Scaling (The SRE Heartbeat)
- **HPA**: Horizontal scaling of Pods based on CPU/Memory.
- **VPA**: Vertical scaling (Right-sizing resource requests).
- **Karpenter / Cluster Autoscaler**: Efficient node provisioning.

---

## 🛡️ 4. Reliability & Security
- **Probes**: 
  - `Readiness`: Is it ready for traffic?
  - `Liveness`: Is it healthy/alive?
- **PDB (Pod Disruption Budget)**: Minimum availability during maintenance.
- **RBAC**: Fine-grained access control.
- **IRSA (IAM Roles for Service Accounts)**: Attach AWS IAM roles to specific Pods.

---

## 📦 5. Configuration & Storage
- **ConfigMaps & Secrets**: Externalizing config and sensitive data.
- **PV / PVC / StorageClass**: Dynamic storage provisioning (e.g., EBS gp3).
- **Helm**: Package manager for templating and versioning deployments.

---

## 🤠 6. Rancher & Multi-Cluster
- **Rancher**: Centralized management for multiple clusters (EKS, RKE2).
- **Fleet**: GitOps for large-scale cluster management.

---

## 🏠 7. Localhost Testing (Kind/Minikube)
```bash
# Create local cluster
kind create cluster --name sre-lab
# Apply manifest
kubectl apply -f deployment.yaml
```

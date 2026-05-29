# ☸️ Kubernetes Core Objects: The SRE Foundations

For a Mid-level SRE, you must understand not just what these objects are, but how they interact to provide **Resilience and Scalability**.

## 1. Workload Objects
- **Pods**: Smallest unit. SRE Tip: Never deploy a naked Pod; always use a Deployment.
- **ReplicaSets**: Ensures the desired number of Pods are running.
- **Deployments**: **The Standard**. Handles rolling updates and rollbacks.
- **StatefulSets**: For databases (PostgreSQL/Redis) that need stable network IDs and persistent storage.
- **DaemonSets**: Runs a Pod on **every** node (e.g., Fluentd, Alloy, Node Exporter).

## 2. Networking Objects
- **Services**: Stable IP/DNS for Pods.
  - `ClusterIP`: Internal only.
  - `NodePort`: External via port on each node.
  - `LoadBalancer`: Provisions a Cloud LB (AWS NLB/ALB).
- **Ingress**: Layer 7 routing (e.g., `api.example.com` -> `backend-service`).

## 3. Configuration & Secrets
- **ConfigMaps**: Store non-sensitive config (e.g., `nginx.conf`).
- **Secrets**: Store sensitive data (API keys). **SRE Tip**: Base64 is NOT encryption. Use Vault or Sealed Secrets for real security.

## 4. Resource Management (The SRE Guardrails)
- **HPA (Horizontal Pod Autoscaler)**: CPU/Memory based scaling.
- **PDB (Pod Disruption Budget)**: "Ensure at least 2 replicas are always alive during maintenance."
- **Requests & Limits**: 
  - `Requests`: What the Pod is guaranteed.
  - `Limits`: Max it can consume. **Warning**: OOMKilled happens if you cross memory limits.

## 5. Scheduling & Storage
- **Taints & Tolerations**: Keep specific nodes for specific workloads (e.g., GPU nodes).
- **Affinity / Anti-Affinity**: "Keep these 2 Pods on different nodes for High Availability."
- **PV / PVC / StorageClass**: Dynamic volume provisioning.
  - `PV`: Actual storage.
  - `PVC`: User's request for storage.
  - `StorageClass`: The provider (e.g., AWS EBS `gp3`).

---

## 🛠️ Local Practice
```bash
# Apply a basic Deployment
kubectl apply -f https://k8s.io/examples/controllers/nginx-deployment.yaml

# Check rollout status
kubectl rollout status deployment/nginx-deployment
```

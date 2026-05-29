# 🏗️ K8S WORKLOADS SRE MASTER NOTES

Mastering how to run applications reliably in a cluster.

## 1. Core Objects
- **Pods**: The smallest unit. **SRE Rule**: Never deploy a naked Pod; always use a controller.
- **Deployments**: The standard for stateless apps. Handles Rolling Updates & Rollbacks.
- **StatefulSets**: For stateful apps (Databases). Stable network IDs & Persistent Storage.
- **DaemonSets**: Runs one Pod per node. Used for Alloy, Fluentd, and Node Exporter.
- **Jobs & CronJobs**: For batch processing and scheduled tasks.

## 2. Best Practices
- **Graceful Shutdown**: Implement `preStop` hooks and `terminationGracePeriodSeconds`.
- **Init Containers**: Setting up prerequisites (e.g., waiting for a DB) before the app starts.
- **Sidecar Pattern**: Adding helper containers for logging or proxying (e.g., Envoy).

## 3. Local Practice
```bash
kubectl create deployment nginx --image=nginx
kubectl get pods
```

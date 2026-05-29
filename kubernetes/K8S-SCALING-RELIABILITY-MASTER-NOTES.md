# 📈 K8S SCALING & RELIABILITY MASTER NOTES

High availability and automated operations.

## 1. Autoscaling
- **HPA (Horizontal Pod Autoscaler)**: Adds/removes Pods based on metrics.
- **VPA (Vertical Pod Autoscaler)**: Adjusts CPU/RAM of existing Pods.
- **Karpenter**: Intelligent node provisioning for EKS (Faster than Cluster Autoscaler).

## 2. Health Checks (Probes)
- **Readiness Probe**: Is the app ready to serve traffic?
- **Liveness Probe**: Is the app healthy or does it need a restart?
- **Startup Probe**: For heavy legacy apps that take time to boot.

## 3. Resource Management
- **Requests**: What a container is guaranteed.
- **Limits**: Max it can consume. **Warning**: CPU throttle vs. Memory Kill (OOMKilled).

## 4. Availability
- **PDB (Pod Disruption Budget)**: Minimum available replicas during maintenance.
- **Affinity**: Keep replicas on different nodes/AZs.

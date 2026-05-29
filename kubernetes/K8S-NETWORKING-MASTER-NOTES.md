# 🌐 K8S NETWORKING SRE MASTER NOTES

Traffic flow and Service discovery.

## 1. Service Types
- **ClusterIP**: Internal-only communication (Default).
- **NodePort**: Exposed on a specific port on every node.
- **LoadBalancer**: Provisions a Cloud LB (e.g., AWS NLB).
- **ExternalName**: Maps a service to a DNS name.

## 2. Ingress & Controllers
- **Ingress**: High-level rules for HTTP/HTTPS routing.
- **Ingress Controller**: The engine (e.g., Nginx, Traefik, ALB Controller).
- **SSL Termination**: Handling HTTPS at the Ingress level.

## 3. Network Policies (Security)
- **Zero Trust**: By default, all Pods can talk to all Pods.
- **Rules**: Use NetworkPolicies to restrict traffic (e.g., "Allow Backend to talk to DB only").

## 4. Troubleshooting
- `kubectl exec -it <pod> -- nslookup <service-name>`
- `kubectl describe ingress <name>`

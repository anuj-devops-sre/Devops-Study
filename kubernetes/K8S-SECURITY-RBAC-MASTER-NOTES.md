# 🔐 K8S SECURITY & RBAC MASTER NOTES

Securing the cluster perimeter and internal communications.

## 1. RBAC (Role-Based Access Control)
- **Roles & ClusterRoles**: Defining permissions (verbs like get, list, watch).
- **RoleBindings**: Linking permissions to Users, Groups, or ServiceAccounts.

## 2. Service Accounts & IRSA
- **ServiceAccount**: Identity for Pods.
- **IRSA (IAM Roles for Service Accounts)**: Attach AWS IAM roles directly to Pods. **SRE Best Practice**.

## 3. Secret Management
- **Secrets**: Base64 encoded (not encrypted).
- **Sealed Secrets / External Secrets**: Mapping HashiCorp Vault or AWS Secrets Manager into K8s.

## 4. Workload Security
- **Runtime Protection**: Using **Falco** to detect abnormal behavior.
- **Non-Root**: Configuring `securityContext` to run as a non-privileged user.

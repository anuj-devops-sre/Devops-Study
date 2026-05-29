# ⚙️ Ansible: Configuration Management

## 🌟 Introduction
Ansible is an agentless automation tool. It uses SSH to communicate with servers.

## 🟢 Level 0: Basics
- **Inventory:** List of servers to manage (`/etc/ansible/hosts`).
- **Ad-hoc Commands:** `ansible all -m ping`.
- **YAML:** Ansible uses YAML for configuration.

## 🟡 Level 1: Playbooks (Junior DevOps)
- **Tasks:** Single unit of work.
- **Handlers:** Tasks that run only when notified (e.g., restart Nginx after config change).
- **Variables:** Parameterizing your automation.

## 🟠 Level 2: Enterprise Scaling (Mid-Level)
- **Roles:** Reusable, structured folders for complex automation.
- **Ansible Vault:** Encrypting secrets (passwords, keys).
- **Dynamic Inventory:** Automatically fetching server lists from AWS/GCP.
- **CI/CD Integration:** Running Ansible from Jenkins or GitHub Actions.

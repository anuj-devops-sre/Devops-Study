# 📜 ANSIBLE FLEET MANAGEMENT SRE MASTER GUIDE

Infrastructure as Code manages the Cloud; **Configuration Management** manages the OS. For an SRE, Ansible is the tool of choice for managing thousands of servers.

---

## 1. Core Architecture
- **Agentless**: Works over SSH. No need to install software on target nodes.
- **Idempotency**: Running a playbook twice results in the same state without errors.
- **Control Node**: Where you run Ansible.
- **Managed Nodes**: The servers you manage.

## 2. Key Components
- **Inventory**: List of servers (INI or YAML).
- **Playbooks**: YAML files defining the desired state.
- **Roles**: Reusable, organized structure for complex playbooks.
- **Ansible Galaxy**: Community hub for pre-built roles.

## 3. SRE Use Cases
- **OS Hardening**: Disabling root login and setting up firewalls across 100 servers.
- **Patch Management**: Running `apt upgrade` safely across a fleet.
- **Application Deployment**: Deploying apps on non-containerized legacy systems.
- **Log Collection**: Installing and configuring Alloy/Fluentd agents everywhere.

## 4. Advanced SRE Patterns
- **Ansible Vault**: Encrypting sensitive data (SSH keys, API tokens) in your playbooks.
- **Dynamic Inventory**: Automatically fetching server lists from AWS (using EC2 tags).
- **Check Mode**: `ansible-playbook --check` to see what would change without actually changing it.

---

## 🏠 Local Practice
```bash
# Install Ansible
pip install ansible

# Run a simple ping
ansible all -i "localhost," -c local -m ping
```

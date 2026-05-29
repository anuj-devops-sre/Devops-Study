# 🛠️ DevOps to SRE: Zero to Mid-Level Roadmap

This roadmap is designed to transform you into a **Site Reliability Engineer (SRE)**. It moves from core systems knowledge to automated infrastructure and high-availability systems.

---

## 🏗️ Phase 1: The Foundation (The "Dev" & "Ops" Basics)
*Target: Understand how systems talk and how code is managed.*

1.  **Linux Mastery** (`./linux/day1-linux-basics.md`)
    *   [x] File Systems, Permissions, and Users.
    *   [x] Shell Scripting (Automating boring tasks).
    *   [x] Process management and Systemd.
2.  **Networking Fundamentals** (`./networking/day1-osi-model.md`)
    *   [x] OSI Model & TCP/IP.
    *   [x] DNS, HTTP/HTTPS, SSL/TLS.
    *   [x] Load Balancing (Nginx/HAProxy/NLB).
3.  **Git & Version Control** (`./git/git.md`)
    *   [x] Branching strategies (Gitflow).
    *   [x] Resolving conflicts & Rebasing.

---

## 📦 Phase 2: Containerization & Cloud (The Modern Stack)
*Target: Move away from "it works on my machine" to "it works everywhere".*

1.  **Docker** (`./docker/docker.md`)
    *   [x] Writing efficient Dockerfiles (Multi-stage builds).
    *   [x] Docker Compose for multi-container apps.
    *   [x] Networking & Volumes.
2.  **Cloud Infrastructure (AWS)** (`./aws/README.md`)
    *   [x] Identity & Access Management (IAM).
    *   [x] VPC Design (Public/Private Subnets, NAT).
    *   [x] Compute (EC2) & Storage (S3, EBS).
3.  **Infrastructure as Code (Terraform)** (`./terraform/00-basics/main.tf`)
    *   [x] Providers & Resources.
    *   [x] Modules (Reusable code).
    *   [x] Remote State (S3 + DynamoDB).

---

## ☸️ Phase 3: Orchestration & Reliability (The SRE Core)
*Target: Managing scale, reliability, and automated recovery.*

- [x] **Kubernetes** (`./kubernetes/kubernats.md`)
    *   [x] Pods, Deployments, Services.
    *   [x] ConfigMaps & Secrets.
    *   [x] Ingress Controllers.
    *   [x] Helm Charts (Package management).
    *   [x] RKE2 Production-grade Cluster Setup.

2.  **Observability (The SRE Soul)** (`./monitoring/README.md`)
    *   [x] Prometheus & Grafana (Metrics).
    *   [x] ELK/Loki (Logging).
    *   [ ] Golden Signals (Latency, Traffic, Errors, Saturation).
3.  **Databases & Storage** (`./databases/README.md`)
    *   [ ] Relational: PostgreSQL & MySQL (High Availability).
    *   [ ] NoSQL: MongoDB & Redis (Caching).
    *   [ ] OLAP: ClickHouse (Big Data/Analytics).
4.  **CI/CD Pipelines & Advanced IaC** (`./projects/01-docker-3tier-app/README.md`)
    *   [x] GitHub Actions (Automation).
    *   [ ] Jenkins (Enterprise CI/CD).
    *   [ ] Ansible (Configuration Management).
    *   [ ] ArgoCD (GitOps).
5.  **Cost Optimization & AI in Ops**
    *   [ ] AWS Cost Explorer & Right-sizing.
    *   [ ] AI-driven automation (Claude AI, Cursor, ChatGPT).

---

## 🚀 Tiered Projects (Interview Ready)

| Tier | Project Name | Skills Used |
| :--- | :--- | :--- |
| **Basic** | Static Website on S3/CloudFront | AWS, DNS, CDN |
| **Mid** | [Three-Tier App on Docker Compose](./projects/01-docker-3tier-app/README.md) | Docker, Networking, Nginx |
| **SRE** | Production K8s Cluster with Monitoring | Terraform, EKS/RKE2, Prometheus, Helm |

---

## 📚 Interview Prep
- [ ] 100+ Linux Interview Questions.
- [ ] Scenario-based Troubleshooting (e.g., "The site is slow, where do you start?").
- [ ] Post-Mortem writing.

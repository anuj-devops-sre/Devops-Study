# 🚀 Devops-Study: The Ultimate Learning Path

[![DevOps](https://img.shields.io/badge/DevOps-Learning-blueviolet?style=for-the-badge&logo=devops)](https://github.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](http://makeapullrequest.com)

Welcome to the **Devops-Study** repository! This is a curated, hands-on roadmap designed to take you from a DevOps beginner to a production-ready engineer. Whether you're mastering the Linux terminal or orchestrating complex Kubernetes clusters, this repo has you covered.

---

## 👨‍💻 Meet the Engineer

**Anuj Kumar Dwivedi**  
*Senior DevOps & SRE Engineer @ Cashify*  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/anuj-kumar-dwivedi/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/anuj-devops-sre)

### 🛠️ Professional Tech Stack

| Category | Tools |
| :--- | :--- |
| **☁️ Cloud & Infra** | [![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)](./aws/) [![EKS](https://img.shields.io/badge/EKS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)](./kubernetes/) [![LocalStack](https://img.shields.io/badge/LocalStack-%23000000.svg?style=for-the-badge&logo=localstack&logoColor=white)](./localstack/) |
| **🐳 Containers** | [![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)](./kubernetes/) [![Docker](https://img.shields.io/badge/docker-%232496ed.svg?style=for-the-badge&logo=docker&logoColor=white)](./docker/) [![Helm](https://img.shields.io/badge/Helm-%230F1628.svg?style=for-the-badge&logo=helm&logoColor=white)](./kubernetes/) [![Rancher](https://img.shields.io/badge/Rancher-%2300758F.svg?style=for-the-badge&logo=rancher&logoColor=white)](./rancher/rancher-guide.md) |
| **⚙️ CI/CD & IaC** | [![Jenkins](https://img.shields.io/badge/jenkins-%232C5263.svg?style=for-the-badge&logo=jenkins&logoColor=white)](./ci-cd/jenkins.md) [![GitHub Actions](https://img.shields.io/badge/Github%20Actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)](./git/) [![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)](./terraform/) [![Ansible](https://img.shields.io/badge/ansible-%23EE0000.svg?style=for-the-badge&logo=ansible&logoColor=white)](./ci-cd/ansible.md) |
| **📊 Observability** | [![Grafana](https://img.shields.io/badge/grafana-%23F46800.svg?style=for-the-badge&logo=grafana&logoColor=white)](./monitoring/) [![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white)](./monitoring/) [![Loki](https://img.shields.io/badge/Loki-005AD4?style=for-the-badge&logo=grafana&logoColor=white)](./monitoring/) [![Elasticsearch](https://img.shields.io/badge/Elasticsearch-005571?style=for-the-badge&logo=elasticsearch&logoColor=white)](./monitoring/) |
| **🗄️ Databases** | [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](./databases/postgresql.md) [![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)](./databases/postgresql.md) [![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)](./databases/redis.md) [![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)](./databases/redis.md) [![ClickHouse](https://img.shields.io/badge/ClickHouse-FFCC00?style=for-the-badge&logo=clickhouse&logoColor=black)](./databases/clickhouse.md) |
| **💻 Scripting** | [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./scripting/python-for-devops.md) [![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)](./linux/) [![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](./linux/) |
| **🤖 AI for Ops** | [![Claude AI](https://img.shields.io/badge/Claude%20AI-D97757?style=for-the-badge&logo=anthropic&logoColor=white)](./ai-ops/ai-tools.md) [![ChatGPT](https://img.shields.io/badge/ChatGPT-74aa1c?style=for-the-badge&logo=openai&logoColor=white)](./ai-ops/ai-tools.md) |

---

## 🏗️ Production-Ready Reference Architectures

This repository serves as a learning foundation. For production-grade implementations used in the field, refer to my specialized repositories:

*   🚀 **[EKS Cluster IaC](https://github.com/anuj-devops-sre/eks-cluster-terraform)**: Production-ready EKS with Node Groups, IRSA, and Autoscaling.
*   🔄 **[Jenkins CI/CD Pipelines](https://github.com/anuj-devops-sre/jenkins-cicd-pipeline)**: End-to-end automation from code to ECR/EKS.
*   📈 **[Advanced Observability](https://github.com/anuj-devops-sre/grafana-prometheus-loki)**: Full-stack monitoring with Grafana, Prometheus, and Loki.
*   💰 **[AWS Cost Optimization](https://github.com/anuj-devops-sre/aws-cost-optimization)**: Practical scripts for reducing cloud spend.

---

## 🗺️ Learning Roadmap

### 📂 Phase 1: Fundamentals
- [x] **[Linux](./linux/)**: Bash scripting, process management, and file systems.
- [x] **[Networking](./networking/)**: OSI Model, TCP/IP, DNS, and Load Balancers.
- [x] **[Git](./git/)**: Version control, branching strategies, and collaboration.

### 📂 Phase 2: Cloud & Infrastructure
- [x] **[AWS](./aws/)**: EC2, S3, IAM, VPC, and more.
- [x] **[Terraform](./terraform/)**: Automating infrastructure with IaC.
- [x] **[LocalStack](./localstack/)**: Developing and testing cloud apps locally.

### 📂 Phase 3: Containers & Orchestration
- [x] **[Docker](./docker/)**: Building images, multi-stage builds, and Compose.
- [x] **[Kubernetes](./kubernetes/)**: Pods, Deployments, Services, and Helm.
- [x] **[RKE2 Cluster](./terraform/rke2-cluster/)**: Production-grade cluster setup.

### 📂 Phase 4: Observability & Security
- [x] **[Monitoring](./monitoring/)**: Prometheus, Grafana, and Loki.
- [ ] **[Security](./security/)**: DevSecOps, Vault, and scanning tools.

---

## 📁 Repository Structure

```text
Devops-Study/
├── 🐧 linux/          # System administration & scripting
├── 🌐 networking/     # Core networking protocols
├── 🏗 terraform/      # IaC modules & cloud deployments
├── 🐳 docker/         # Containerization labs
├── ☸️ kubernetes/     # Orchestration & k8s manifests
├── ☁️ aws/            # Cloud infrastructure notes
└── 🚀 projects/       # End-to-end DevOps projects
```

---

## 🎯 Goal
The primary objective of this repository is to provide a structured approach to learning DevOps by focusing on **practical implementation** and **real-world scenarios**. 

---

## 🤝 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

---
<p align="center">
  Made with ❤️ for the DevOps Community
</p>

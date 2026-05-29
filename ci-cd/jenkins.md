# 🔄 Jenkins: The Grandfather of CI/CD

## 🌟 Introduction
Jenkins is an open-source automation server that helps automate the parts of software development related to building, testing, and deploying.

## 🟢 Level 0: Installation
- Running as a container: `docker run -p 8080:8080 jenkins/jenkins:lts`.
- Plugins: The power of Jenkins (Git, Docker, Pipeline, Slack).

## 🟡 Level 1: Pipelines (Declarative)
Moving from "Freestyle" jobs to **Jenkinsfile**.
```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps { echo 'Building...' }
        }
        stage('Test') {
            steps { echo 'Testing...' }
        }
        stage('Deploy') {
            steps { echo 'Deploying...' }
        }
    }
}
```

## 🟠 Level 2: SRE Best Practices
- **Shared Libraries:** Reusable Groovy code across multiple teams.
- **Jenkins Agents:** Scaling Jenkins with dynamic agents (Docker/K8s).
- **Security:** RBAC (Role Based Access Control) and Secret Management.
- **Blue/Green & Canary:** Implementing advanced deployment patterns.

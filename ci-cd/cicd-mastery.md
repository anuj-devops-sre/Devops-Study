# 🔄 CI/CD Mastery: The Automation Engine

CI/CD is the bridge between development and operations. For an SRE, it's about **Speed, Safety, and Reproducibility**.

## 1. CI vs. CD (The Difference)
- **CI (Continuous Integration)**: Automating builds and tests. Developers push code frequently.
- **CD (Continuous Delivery)**: Code is always in a "ready-to-deploy" state. Deployment to Prod requires a manual approval.
- **CD (Continuous Deployment)**: Code is automatically deployed to Prod if it passes all tests. **SRE Goal**.

## 2. GitHub Actions (Modern CI)
- **Philosophy**: Event-driven automation built into GitHub.
- **Components**: Workflows (YAML), Jobs, Steps, Actions.
```yaml
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Tests
        run: npm test
```

## 3. Jenkins (The Enterprise Workhorse)
- **Philosophy**: Highly customizable, plugin-heavy.
- **Pipelines as Code**: Always use **Jenkinsfile** (Declarative syntax).
```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps { sh 'mvn clean package' }
        }
    }
}
```

## 4. Secrets Management (The SRE Guardrail)
Never hardcode API keys or passwords.
- **GitHub Secrets**: For Actions.
- **Jenkins Credentials**: For Jenkins.
- **HashiCorp Vault**: **SRE Best Practice** for external secret management.

## 5. Deployment Strategies
- **Rolling Update**: Default K8s strategy. Pods are replaced one by one.
- **Blue/Green**: Two identical environments. Switch traffic from Blue to Green.
- **Canary**: Deploy to a small % of users first, then scale up if no errors.

---

## 🏠 How to test CI/CD on Localhost?
1.  **Jenkins**: Run it as a container.
    ```bash
    docker run -p 8080:8080 jenkins/jenkins:lts
    ```
2.  **GitHub Actions**: Use **act** to run actions locally.
    ```bash
    act push
    ```
3.  **Simulation**: Build a pipeline that builds a Docker image and pushes it to a local registry.

# DevOps (Development & Operations) & SRE (Site Reliability Engineering) — Complete Interview Notes
### Zero to Mid Level | ~200 Topics Covered

> **How to use these notes:**
> - Each topic has a **1-line definition** + **explanation** + **interview answer tip**
> - Read once, revise the bold lines
> - Real examples from AWS/K8s wherever possible

---

# 📖 Full Forms Glossary (A–Z)

> Every abbreviation used in this document — memorise these before your interview.

| Abbreviation | Full Form |
|-------------|-----------|
| ALB | Application Load Balancer |
| AMI | Amazon Machine Image |
| API | Application Programming Interface |
| ArgoCD | Argo Continuous Delivery |
| AWS | Amazon Web Services |
| CI | Continuous Integration |
| CIDR | Classless Inter-Domain Routing |
| CLI | Command Line Interface |
| CNI | Container Network Interface |
| CPU | Central Processing Unit |
| CD | Continuous Delivery / Continuous Deployment |
| CRD | Custom Resource Definition |
| DevOps | Development and Operations |
| DNS | Domain Name System |
| DSL | Domain Specific Language |
| EC2 | Elastic Compute Cloud |
| ECR | Elastic Container Registry |
| ECS | Elastic Container Service |
| EKS | Elastic Kubernetes Service |
| ESO | External Secrets Operator |
| etcd | Extended Typed Correlated Distributed store (distributed key-value store) |
| FTP | File Transfer Protocol |
| GitOps | Git-based Operations |
| HPA | Horizontal Pod Autoscaler |
| HTTP | HyperText Transfer Protocol |
| HTTPS | HyperText Transfer Protocol Secure |
| IaC | Infrastructure as Code |
| IAM | Identity and Access Management |
| IGW | Internet Gateway |
| IP | Internet Protocol |
| IRSA | IAM Roles for Service Accounts |
| K8s | Kubernetes (8 letters between K and s) |
| KMS | Key Management Service |
| LogQL | Log Query Language |
| LRU | Least Recently Used |
| MAC | Media Access Control |
| MSK | Managed Streaming for Apache Kafka |
| mTLS | Mutual Transport Layer Security |
| MX | Mail Exchange |
| NAT | Network Address Translation |
| NLB | Network Load Balancer |
| OIDC | OpenID Connect |
| OSI | Open Systems Interconnection |
| OWASP | Open Web Application Security Project |
| PID | Process ID |
| PromQL | Prometheus Query Language |
| PV | PersistentVolume |
| PVC | PersistentVolumeClaim |
| RAM | Random Access Memory |
| RBAC | Role-Based Access Control |
| RDS | Relational Database Service |
| RKE2 | Rancher Kubernetes Engine 2 |
| S3 | Simple Storage Service |
| SCP | Secure Copy Protocol |
| SDK | Software Development Kit |
| SES | Simple Email Service |
| SLI | Service Level Indicator |
| SLA | Service Level Agreement |
| SLO | Service Level Objective |
| SNS | Simple Notification Service |
| SQS | Simple Queue Service |
| SRE | Site Reliability Engineering |
| SSH | Secure Shell |
| SSL | Secure Sockets Layer |
| TCP | Transmission Control Protocol |
| TLD | Top Level Domain |
| TLS | Transport Layer Security |
| TTL | Time To Live |
| UDP | User Datagram Protocol |
| UI | User Interface |
| URL | Uniform Resource Locator |
| VAPT | Vulnerability Assessment and Penetration Testing |
| VPA | Vertical Pod Autoscaler |
| VPC | Virtual Private Cloud |
| VPN | Virtual Private Network |
| WASM | WebAssembly |
| YAML | YAML Ain't Markup Language |

---


---

# 🔵 1. Linux & Shell Scripting

---

### Linux Basics

**File System Structure**
```
/           → root (top of everything)
/etc        → config files (nginx.conf, hosts, fstab)
/var/log    → all log files live here
/home       → user home directories
/opt        → manually installed software
/tmp        → temporary files (cleared on reboot)
/proc       → running process info (virtual filesystem)
```

**Must-Know Commands**
```bash
ls -la              # list with permissions + hidden files
chmod 755 file      # rwxr-xr-x → owner full, others read+execute
chown user:group f  # change ownership
find / -name "*.log" 2>/dev/null   # find files
grep -r "error" /var/log/          # search inside files
awk '{print $1}' file              # print first column
sed 's/old/new/g' file             # find and replace
tail -f /var/log/syslog            # live log watching
ps aux | grep nginx                # find a running process
netstat -tlnp                      # open ports
df -h                              # disk usage
free -m                            # memory usage
top / htop                         # system performance
```

**Permissions (chmod)**
```
r = 4, w = 2, x = 1
chmod 755 = rwxr-xr-x (owner all, others read+exec)
chmod 644 = rw-r--r-- (owner read+write, others read only)
chmod 600 = rw------- (only owner, used for SSH keys)
```

**Interview tip:** "Tell me a Linux command you use daily" → say `grep`, `awk`, `tail -f` with a real use case like log debugging.

---

### Process Management
```bash
ps aux                    # all running processes
kill -9 <PID>             # force kill
kill -15 <PID>            # graceful kill (SIGTERM)
nohup ./script.sh &       # run in background, survive logout
jobs                      # list background jobs
systemctl start nginx     # start a service
systemctl status nginx    # check service status
systemctl enable nginx    # start on boot
journalctl -u nginx -f    # live logs for a systemd service
```

**What is a zombie process?**
A process that has finished but its parent hasn't read its exit status. Shows as `Z` in `ps`. Not using resources — just a stale entry. Fix by restarting the parent.

---

### Shell Scripting (Bash)

**Template every script should follow:**
```bash
#!/bin/bash
set -e          # exit on any error
set -o pipefail # catch errors in pipes

LOGFILE="/var/log/myscript.log"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOGFILE
}

log "Script started"

# your logic here

log "Script done"
```

**Common patterns:**
```bash
# If/else
if [ -f "/etc/nginx/nginx.conf" ]; then
  echo "nginx config exists"
else
  echo "missing"
fi

# Loop
for pod in $(kubectl get pods -o name); do
  echo "Pod: $pod"
done

# Function
backup_db() {
  local DB_NAME=$1
  mysqldump $DB_NAME > /backup/${DB_NAME}_$(date +%F).sql
}
backup_db myapp

# Read a file line by line
while IFS= read -r line; do
  echo "Processing: $line"
done < servers.txt
```

---

### Cron Jobs
```bash
# Edit crontab
crontab -e

# Format: minute hour day month weekday command
0 2 * * *   /opt/scripts/backup.sh       # every day at 2 AM
*/5 * * * * /opt/scripts/health_check.sh # every 5 minutes
0 0 * * 0   /opt/scripts/cleanup.sh      # every Sunday midnight

# View cron logs
grep CRON /var/log/syslog
```

**Interview tip:** "Always redirect cron output to a log file: `>> /var/log/myjob.log 2>&1` — otherwise errors are silently lost."

---

### SSH (Secure Shell) & SCP (Secure Copy Protocol)
```bash
ssh -i key.pem ubuntu@1.2.3.4         # connect with key
ssh -L 8080:localhost:80 user@server   # local port forward
scp -i key.pem file.txt user@1.2.3.4:/home/user/   # copy file to server
scp -r folder/ user@1.2.3.4:/opt/     # copy folder
ssh-keygen -t rsa -b 4096             # generate key pair
```

---

# 🔵 2. Networking Basics

---

### OSI — Open Systems Interconnection Model
```
Layer 7 - Application  → HTTP, DNS, FTP (what apps use)
Layer 6 - Presentation → SSL/TLS, encoding
Layer 5 - Session      → session management
Layer 4 - Transport    → TCP, UDP (ports live here)
Layer 3 - Network      → IP addresses, routing
Layer 2 - Data Link    → MAC addresses, switches
Layer 1 - Physical     → cables, WiFi signals
```

**Interview tip:** "When a request fails, think OSI layers from bottom up — is the cable/network fine? IP reachable? Port open? App responding?"

---

### TCP/IP — Transmission Control Protocol / Internet Protocol
#### DNS — Domain Name System | HTTP — HyperText Transfer Protocol | HTTPS — HTTP Secure

**TCP (Transmission Control Protocol) vs UDP (User Datagram Protocol)**
- TCP = reliable, ordered, slower (HTTP, SSH, databases)
- UDP = fast, no guarantee (video streaming, DNS queries)

**DNS Resolution flow:**
```
Browser → /etc/hosts → Local DNS cache → Recursive Resolver
→ Root DNS → TLD DNS (.com) → Authoritative DNS → IP returned
```

**HTTP vs HTTPS:**
- HTTP = plain text, port 80
- HTTPS = HTTP + TLS encryption, port 443
- TLS handshake: server sends certificate → client verifies → symmetric key exchanged → encrypted traffic

**Common HTTP status codes:**
```
200 OK          → success
201 Created     → resource created
301/302         → redirect
400 Bad Request → client sent wrong data
401 Unauthorized→ not authenticated
403 Forbidden   → authenticated but no permission
404 Not Found   → resource doesn't exist
500 Server Error→ app crashed
502 Bad Gateway → upstream server returned invalid response
503 Unavailable → server overloaded or down
504 Gateway Timeout → upstream didn't respond in time
```

---

### Load Balancer

**What it does:** Distributes incoming traffic across multiple servers so no single server is overwhelmed.

**Types:**
- **Layer 4 — NLB (Network Load Balancer)** — routes by IP + port. Fast, no content inspection. Good for TCP/UDP.
- **Layer 7 — ALB (Application Load Balancer)** — routes by URL path, headers, host. Can do `/api → service-a`, `/web → service-b`.

**Algorithms:**
- Round Robin — rotate through servers equally
- Least Connections — send to server with fewest active connections
- IP Hash — same client always goes to same server (sticky sessions)

---

### Subnets, CIDR (Classless Inter-Domain Routing), NAT (Network Address Translation)

**CIDR:**
```
192.168.1.0/24  → 256 IPs (192.168.1.0 to 192.168.1.255)
10.0.0.0/16     → 65,536 IPs
10.0.1.0/28     → 16 IPs (small subnet)
```

**Public vs Private subnet:**
- Public subnet → has route to Internet Gateway → EC2 instances get public IPs
- Private subnet → no direct internet → uses NAT Gateway to reach internet outbound

**NAT Gateway:** Allows private subnet resources to initiate outbound internet connections but blocks inbound. Used so EC2/pods can download packages without being publicly exposed.

---

### Reverse Proxy (Nginx)

**What it does:** Sits in front of your app servers. Client talks to Nginx, Nginx talks to your app.

**Benefits:** SSL termination, load balancing, caching, hide internal servers.

```nginx
server {
    listen 80;
    server_name api.mycompany.com;

    location / {
        proxy_pass http://localhost:3000;   # forward to app
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

# 🔵 3. Git & Version Control

---

### Git Basics
```bash
git clone <url>              # download repo
git status                   # what changed
git add .                    # stage all changes
git commit -m "message"      # save snapshot
git push origin main         # upload to remote
git pull                     # download latest
git log --oneline            # see commit history
git diff                     # see what changed
```

### Branching Strategy (GitFlow)
```
main        → production code only (protected)
develop     → integration branch
feature/*   → new features (branch from develop)
hotfix/*    → urgent production fix (branch from main)
release/*   → pre-release testing
```

### Merge vs Rebase
- **Merge** — creates a merge commit, preserves history, safe for shared branches
- **Rebase** — rewrites history, linear log, use only on your own local branches

```bash
git merge feature-branch      # merge with history
git rebase main               # replay commits on top of main (cleaner)
git cherry-pick <commit-hash> # pick one specific commit from another branch
```

### Conflict Resolution
```bash
git pull                     # conflict occurs
# Edit the file — remove <<<<<<, =======, >>>>>>> markers
git add <resolved-file>
git commit
```

### Git Tags & Releases
```bash
git tag v1.0.0                         # lightweight tag
git tag -a v1.0.0 -m "Release 1.0"    # annotated tag
git push origin v1.0.0                 # push tag to remote
```

**Interview tip:** "Always use feature branches. Never commit directly to main. Use PRs for code review."

---

# 🔵 4. Docker & Containers

---

### What is Containerization?
A container packages your app + its dependencies + runtime into one isolated unit. Unlike VMs, containers share the host OS kernel — they're lightweight and start in seconds.

```
VM:         App | Libs | Guest OS | Hypervisor | Hardware
Container:  App | Libs | Container Runtime | Host OS | Hardware
```

### Docker Architecture
```
Docker Client (CLI)
      ↓
Docker Daemon (dockerd) — manages images, containers, networks
      ↓
Container Runtime (containerd → runc)
```

### Dockerfile
```dockerfile
# Multi-stage build example (production best practice)
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production    # install deps
COPY . .
RUN npm run build

FROM node:20-alpine             # fresh small image
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
USER node                       # don't run as root
CMD ["node", "dist/server.js"]
```

**Best practices:**
- Use Alpine images (smaller)
- Multi-stage builds (no build tools in final image)
- Don't run as root (`USER node`)
- `.dockerignore` to exclude `node_modules`, `.git`
- One process per container

### Docker Commands
```bash
docker build -t myapp:v1 .
docker run -d -p 3000:3000 --name myapp myapp:v1
docker ps                       # running containers
docker ps -a                    # all containers including stopped
docker logs -f myapp            # live logs
docker exec -it myapp sh        # get inside container
docker stop myapp
docker rm myapp
docker images
docker rmi myapp:v1
docker system prune -a          # clean up everything
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DB_HOST=postgres
    depends_on:
      - postgres

  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

```bash
docker-compose up -d      # start all services
docker-compose down       # stop and remove
docker-compose logs -f    # follow all logs
```

### Docker Networking
```bash
docker network create mynet
docker run --network mynet --name db postgres
docker run --network mynet --name app myapp   # app can reach db by name "db"
```

Network types:
- **bridge** — default, containers on same host can communicate
- **host** — container uses host's network directly (no isolation)
- **none** — no networking

---

# 🔵 5. Kubernetes (K8s)

---

### Architecture

```
Control Plane (Master):
  API Server    → single entry point, all kubectl commands hit this
  etcd          → distributed key-value store, entire cluster state saved here
  Scheduler     → decides which node a pod goes on
  Controller Manager → ensures desired state matches actual state

Worker Nodes:
  kubelet       → agent on each node, talks to API server
  kube-proxy    → handles network rules for Services
  container runtime (containerd) → actually runs containers
```

**Interview tip:** "If etcd dies, the cluster still runs existing workloads but you can't make any changes."

### Pods, Deployments, Services

**Pod** = smallest unit. One or more containers sharing network + storage.

**Deployment** = manages pods. Handles rolling updates, rollbacks, scaling.
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api
        image: myapp:v2
        ports:
        - containerPort: 3000
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 5
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
```

**Liveness Probe** — is the app alive? If fails → container restarts.
**Readiness Probe** — is the app ready for traffic? If fails → removed from Service endpoints, no traffic sent.

**Service types:**
```
ClusterIP    → internal only (default)
NodePort     → exposes on each node's IP:port
LoadBalancer → creates cloud load balancer (AWS ALB/NLB)
ExternalName → maps to external DNS name
```

### ConfigMaps & Secrets (Sensitive Credentials)

**ConfigMap** — non-sensitive config (env vars, config files)
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"
  DB_HOST: "postgres.default.svc.cluster.local"
```

**Secret** — sensitive data, base64 encoded (NOT encrypted by default — use IRSA + Secrets Manager for real security)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  DB_PASSWORD: cGFzc3dvcmQ=    # base64 encoded "password"
```

Use in a pod:
```yaml
envFrom:
- configMapRef:
    name: app-config
- secretRef:
    name: db-secret
```

### Namespaces
Logical isolation inside a cluster. Same as folders.

```bash
kubectl create namespace staging
kubectl get pods -n staging
kubectl get all -n kube-system    # system components namespace
```

Common namespace structure:
- `default` → dev testing
- `staging` → staging environment
- `production` → prod workloads
- `kube-system` → k8s internal (don't touch)
- `monitoring` → prometheus, grafana

### RBAC — Role-Based Access Control

**Who can do what in the cluster.**

```yaml
# Role — what actions are allowed on what resources
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: dev-role
  namespace: staging
rules:
- apiGroups: ["apps"]
  resources: ["deployments", "pods"]
  verbs: ["get", "list", "watch"]   # read-only

---
# RoleBinding — attach role to a user/serviceaccount
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-binding
  namespace: staging
subjects:
- kind: User
  name: developer@mycompany.com
roleRef:
  kind: Role
  name: dev-role
  apiGroup: rbac.authorization.k8s.io
```

- **Role/RoleBinding** → scoped to one namespace
- **ClusterRole/ClusterRoleBinding** → applies to entire cluster

### Taints & Tolerations

**Taints** = mark a node to repel pods
**Tolerations** = allow a pod to be scheduled on a tainted node

```bash
# Taint a node — only pods with matching toleration can run here
kubectl taint nodes node1 dedicated=ml-workload:NoSchedule
```

```yaml
# In pod spec — allow this pod on that tainted node
tolerations:
- key: "dedicated"
  operator: "Equal"
  value: "ml-workload"
  effect: "NoSchedule"
```

Use case: Reserve specific nodes for ML jobs, GPU workloads, or critical services.

### HPA (Horizontal Pod Autoscaler) & VPA (Vertical Pod Autoscaler)

**HPA (Horizontal Pod Autoscaler)** — adds more pods when CPU/memory goes up
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70   # scale up when CPU > 70%
```

**VPA (Vertical Pod Autoscaler)** — adjusts CPU/memory requests of pods automatically. Don't use HPA + VPA on same deployment (conflict).

### DaemonSet & StatefulSet

**DaemonSet** — runs exactly ONE pod on EVERY node. Use for: log collectors (Fluentd), monitoring agents (node-exporter), network plugins.

**StatefulSet** — for apps that need stable identity + persistent storage. Use for: databases (MySQL, MongoDB, Elasticsearch, Kafka). Each pod gets a stable name (`mysql-0`, `mysql-1`) and its own PVC.

### PV (PersistentVolume) & PVC (PersistentVolumeClaim)

```
PersistentVolume (PV)     → actual storage (EBS volume, NFS mount)
PersistentVolumeClaim (PVC) → pod's request for storage
StorageClass              → defines how to auto-provision storage
```

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
spec:
  accessModes:
    - ReadWriteOnce      # only one node at a time
  storageClassName: gp3  # AWS EBS gp3
  resources:
    requests:
      storage: 20Gi
```

### Network Policies

By default all pods can talk to all pods. Network Policy restricts this.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-policy
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend    # only frontend can send traffic to api
    ports:
    - port: 3000
```

### etcd
Distributed key-value store — the cluster's brain/memory. Every object (pod, service, deployment) is stored here. If etcd is unhealthy, cluster becomes read-only. Always backup etcd in production.

---

# 🔵 6. CI/CD — Continuous Integration / Continuous Delivery

---

### What is CI/CD (Continuous Integration / Continuous Delivery)?

**CI (Continuous Integration)** — every code push triggers: build → test → lint. Catch bugs early.

**CD (Continuous Delivery)** — automatically deploy to staging after CI passes.

**CD (Continuous Deployment)** — automatically deploy to production (rare, high maturity needed).

### Jenkins

```groovy
// Jenkinsfile
pipeline {
    agent any

    environment {
        ECR_REPO = "123456789.dkr.ecr.ap-south-1.amazonaws.com/myapp"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/myorg/myapp.git'
            }
        }

        stage('Test') {
            steps {
                sh 'npm test'
            }
        }

        stage('Build & Push') {
            steps {
                sh """
                    docker build -t ${ECR_REPO}:${IMAGE_TAG} .
                    aws ecr get-login-password | docker login --username AWS --password-stdin ${ECR_REPO}
                    docker push ${ECR_REPO}:${IMAGE_TAG}
                """
            }
        }

        stage('Deploy to Staging') {
            steps {
                sh "helm upgrade --install myapp ./chart --set image.tag=${IMAGE_TAG} -n staging"
            }
        }
    }

    post {
        failure {
            slackSend(message: "Build failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}")
        }
    }
}
```

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Build and Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Configure AWS
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ap-south-1

    - name: Build and Push
      run: |
        docker build -t $ECR_REPO:${{ github.sha }} .
        docker push $ECR_REPO:${{ github.sha }}

    - name: Deploy
      run: |
        helm upgrade --install myapp ./chart \
          --set image.tag=${{ github.sha }}
```

### Deployment Strategies

**Rolling Update (default in K8s)** — replace pods one by one. Zero downtime but old and new run simultaneously briefly.

**Blue-Green** — run 2 identical environments. Switch traffic from Blue to Green instantly. Easy rollback = switch back.
```
Blue (current) ← traffic
Green (new)    ← idle

After deploy:
Blue (old)    ← idle (keep for rollback)
Green (new)   ← traffic
```

**Canary** — send 5% of traffic to new version, watch for errors, slowly increase to 100%.
```
v1 pods → 95% traffic
v2 pods → 5% traffic (canary)
```

---

# 🔵 7. AWS Cloud

---

### IAM
- **User** — a person (has console/API access)
- **Role** — assumed by services (EC2, Lambda, pods via IRSA)
- **Policy** — JSON document defining what actions are allowed/denied
- **Principle of Least Privilege** — give only the minimum permissions needed

### EC2
- **AMI** — Amazon Machine Image (template for an EC2 instance)
- **Instance types** — t3 (burstable), m7 (general), c7 (compute), r7 (memory), g4 (GPU)
- **Security Group** — stateful firewall at instance level (inbound + outbound rules)
- **Key pair** — SSH access

### VPC (Virtual Private Cloud)
```
VPC (10.0.0.0/16)
├── Public Subnet (10.0.1.0/24)  → has IGW route → EC2 with public IP
├── Private Subnet (10.0.2.0/24) → no IGW → uses NAT Gateway
│
├── Internet Gateway (IGW)       → public internet access
├── NAT Gateway                  → private subnets outbound only
└── Route Tables                 → controls where traffic goes
```

### S3
- Object storage — files, images, backups, Terraform state
- **Bucket Policy** — resource-based policy to control access
- **Versioning** — keep multiple versions of same file
- **Lifecycle rules** — auto move to Glacier after 30 days, delete after 1 year

### EKS (already covered in detail above)

### CloudWatch
```bash
# Key concepts:
Metrics    → CPU, memory, request count numbers over time
Logs       → application/system log storage
Alarms     → trigger SNS/action when metric crosses threshold
Log Groups → container for related log streams
Insights   → query logs with SQL-like syntax
```

### Route53
- DNS service — maps domain names to IPs
- **Record types:** A (IP), CNAME (alias), MX (email), TXT (verification)
- **Routing policies:** Simple, Weighted (canary), Failover, Latency-based

### KMS & Secrets Manager
- **KMS** — encryption key management. Encrypt EBS, S3, RDS at rest.
- **Secrets Manager** — store DB passwords, API keys. Auto-rotation supported. Pods access via IRSA (no hardcoded secrets).

---

# 🔵 8. Terraform & IaC (Infrastructure as Code)

---

### What is IaC (Infrastructure as Code)?
Infrastructure as Code — define your cloud resources in code files. Version controlled, repeatable, no manual clicking.

### Core Terraform Flow
```bash
terraform init      # download providers, initialize backend
terraform plan      # show what will change (dry run)
terraform apply     # create/update resources
terraform destroy   # delete all resources
terraform fmt       # format code
terraform validate  # check syntax
```

### Basic Structure
```hcl
# main.tf
provider "aws" {
  region = "ap-south-1"
}

resource "aws_instance" "web" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t3.micro"

  tags = {
    Name = "my-web-app"
    Env  = var.environment
  }
}

output "instance_ip" {
  value = aws_instance.web.public_ip
}
```

```hcl
# variables.tf
variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "staging"
}
```

### State Management
```hcl
# backend.tf — always use remote state in teams
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "eks/demo-test/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "terraform-lock"   # prevents concurrent applies
    encrypt        = true
  }
}
```

**Why remote state?** If state is local, teammates can't collaborate. S3 backend + DynamoDB locking = safe team usage.

### Modules
Reusable blocks of Terraform code.
```hcl
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name = "demo-test"
  vpc_id       = module.vpc.vpc_id
}
```

### Terraform Import
Bring existing AWS resources under Terraform management:
```bash
terraform import aws_instance.web i-1234567890abcdef0
```

**Interview tip:** "Terraform plan before every apply. Use remote state. Never run terraform apply in production without a plan review."

---

# 🔵 9. Ansible

---

### What is Configuration Management?
Ensures servers are in a desired, consistent state. Install Nginx on 50 servers? One playbook. Update a config file across 100 EC2s? One command.

### Inventory
```ini
# hosts.ini
[webservers]
10.0.1.10
10.0.1.11

[dbservers]
10.0.2.20

[all:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/key.pem
```

### Playbook
```yaml
# deploy.yml
- name: Install and start Nginx
  hosts: webservers
  become: yes            # run as sudo

  tasks:
  - name: Install Nginx
    apt:
      name: nginx
      state: present
      update_cache: yes

  - name: Copy config
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    notify: Restart Nginx

  - name: Ensure Nginx is running
    service:
      name: nginx
      state: started
      enabled: yes

  handlers:
  - name: Restart Nginx
    service:
      name: nginx
      state: restarted
```

```bash
ansible-playbook -i hosts.ini deploy.yml          # run playbook
ansible webservers -i hosts.ini -m ping           # ad-hoc ping
ansible webservers -i hosts.ini -m shell -a "df -h"  # check disk
```

### Ansible Vault
```bash
ansible-vault encrypt secrets.yml     # encrypt file
ansible-vault decrypt secrets.yml     # decrypt
ansible-vault edit secrets.yml        # edit encrypted file
ansible-playbook deploy.yml --ask-vault-pass   # run with vault
```

---

# 🔵 10. Monitoring & Observability

---

### Monitoring vs Observability
- **Monitoring** — watch predefined metrics. "Is CPU above 80%?" You know what to look for.
- **Observability** — understand WHY something is broken using metrics + logs + traces. You can explore unknown failures.

### Prometheus
Scrapes metrics from endpoints. Stores time-series data.

```yaml
# prometheus.yml scrape config
scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
    - role: pod
    relabel_configs:
    - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
      action: keep
      regex: true
```

**PromQL examples:**
```promql
# CPU usage per pod
rate(container_cpu_usage_seconds_total[5m])

# Memory usage
container_memory_usage_bytes{namespace="production"}

# HTTP error rate
rate(http_requests_total{status=~"5.."}[5m])
  /
rate(http_requests_total[5m])
```

### Grafana
Visualizes Prometheus metrics. Create dashboards with graphs, alerts.

**Key dashboards to set up:**
- Node CPU/Memory/Disk
- Pod restart count
- HTTP request rate + error rate
- Database connection pool

### Loki + Promtail
- **Promtail** — agent on each node, collects logs, sends to Loki
- **Loki** — log storage and query engine (like Prometheus but for logs)

```logql
# LogQL query examples
{namespace="production", app="api"} |= "error"
{job="fluentd"} | json | level="ERROR" | line_format "{{.message}}"
```

### SLI (Service Level Indicator) / SLO (Service Level Objective) / SLA (Service Level Agreement) / Error Budget
```
SLI (Service Level Indicator)  → actual measurement (e.g., 99.5% success rate)
SLO (Service Level Objective)  → target you set (e.g., 99.9% uptime)
SLA (Service Level Agreement)  → contractual promise to customer (99.9%)
Error Budget = 100% - SLO      → 0.1% = ~44 min/month downtime allowed
```

**Interview tip:** "If error budget is exhausted, freeze new feature releases and focus on reliability. If budget is healthy, you can move fast."

---

# 🔵 11. ArgoCD (Argo Continuous Delivery) & GitOps (Git-based Operations)

---

### What is GitOps (Git-based Operations)?
Git is the single source of truth. Every change to infrastructure/apps goes through Git. ArgoCD watches the Git repo and automatically syncs the cluster to match.

```
Developer → git push → Git Repo (desired state)
                           ↓ ArgoCD watches
                       EKS Cluster (actual state)
                       ArgoCD syncs any diff
```

### ArgoCD Architecture
```
ArgoCD API Server  → UI and CLI access
Repo Server        → clones Git repos, generates manifests
Application Controller → compares Git vs cluster, syncs
```

### ArgoCD Application
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-microservice
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/k8s-manifests.git
    targetRevision: main
    path: apps/my-microservice
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true       # delete resources removed from Git
      selfHeal: true    # revert manual kubectl changes
```

### ArgoCD vs Jenkins
| | Jenkins | ArgoCD |
|--|---------|--------|
| Type | Push-based CI/CD | Pull-based GitOps |
| Trigger | Webhook/schedule | Watches Git |
| Rollback | Re-run pipeline | `git revert` |
| Best for | Build, test, complex pipelines | K8s deployment sync |

**Use both:** Jenkins for build + test + push image. ArgoCD for deploy.

---

# 🔵 12. Security & DevSecOps (Development Security Operations)

---

### RBAC — Role-Based Access Control (covered in K8s section)

### Secrets Management

Never store secrets in Git. Options:
1. **AWS Secrets Manager + External Secrets Operator (ESO)** — secrets stored in AWS, synced to K8s Secrets automatically
2. **Vault (HashiCorp)** — self-hosted secrets store with dynamic secrets

```yaml
# External Secrets Operator example
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
spec:
  secretStoreRef:
    name: aws-secrets-manager
  target:
    name: db-secret         # creates this K8s Secret
  data:
  - secretKey: DB_PASSWORD
    remoteRef:
      key: production/myapp/db
      property: password
```

### Image Scanning (Trivy)
```bash
# Scan a Docker image for vulnerabilities
trivy image myapp:latest

# Scan in CI pipeline
trivy image --severity HIGH,CRITICAL --exit-code 1 myapp:latest
# exit-code 1 = fail the pipeline if HIGH/CRITICAL found
```

### SSL/TLS Certificates
```bash
# cert-manager in K8s — auto-issue and renew Let's Encrypt certs
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
```

### Least Privilege Principle
Every user, service account, and IAM role should have only the minimum permissions needed for its job. Nothing more.

---

# 🔵 13. Databases (DevOps Perspective)

---

### PostgreSQL
```bash
# Replication: Primary → Standby (streaming replication)
# Primary writes, Standby reads (read replicas)

# Backup
pg_dump mydb > backup.sql
pg_dumpall > all_databases.sql

# Restore
psql mydb < backup.sql

# Key monitoring queries
SELECT pid, query, state, wait_event FROM pg_stat_activity;  # active connections
SELECT pg_size_pretty(pg_database_size('mydb'));             # db size
```

### Redis
- In-memory cache. Key-value store.
- **Eviction policies:**
  - `allkeys-lru` — evict least recently used (most common for cache)
  - `volatile-lru` — evict LRU only from keys with TTL set
  - `noeviction` — return error when memory full (use for session store)

```bash
redis-cli ping
redis-cli info memory
redis-cli monitor    # watch live commands (debug only)
```

### etcd — Extended Typed Correlated Distributed store (K8s state store)
```bash
# Backup etcd
ETCDCTL_API=3 etcdctl snapshot save backup.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/etcd/ca.crt \
  --cert=/etc/etcd/server.crt \
  --key=/etc/etcd/server.key

# Restore
etcdctl snapshot restore backup.db
```

**Interview tip:** "In production, etcd backup should be automated and stored in S3. Losing etcd without a backup = losing entire cluster state."

---

# 🔵 14. Python & Go (DevOps Focus)

---

### Python Automation

```python
#!/usr/bin/env python3
import boto3
import subprocess
from datetime import datetime

# List all EC2 instances and their states
ec2 = boto3.client('ec2', region_name='ap-south-1')
response = ec2.describe_instances()

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        name = next((t['Value'] for t in instance.get('Tags', [])
                     if t['Key'] == 'Name'), 'unnamed')
        print(f"{name}: {instance['InstanceId']} — {instance['State']['Name']}")
```

```python
# Make a REST API call
import requests

def get_pod_metrics(namespace):
    url = f"http://prometheus:9090/api/v1/query"
    params = {
        'query': f'container_memory_usage_bytes{{namespace="{namespace}"}}'
    }
    resp = requests.get(url, params=params)
    return resp.json()['data']['result']
```

---

# 🔵 15. Service Mesh

---

### What is a Service Mesh?
Handles service-to-service communication inside the cluster. Adds: encryption (mTLS), traffic control, observability — without changing app code.

```
Without mesh:  Service A → HTTP → Service B (plain, no visibility)
With mesh:     Service A → Sidecar → encrypted mTLS → Sidecar → Service B
               (Envoy proxy)                          (Envoy proxy)
```

### Istio vs Linkerd
| | Istio | Linkerd |
|--|-------|---------|
| Complexity | High | Low |
| Features | Rich (traffic mgmt, WASM) | Simpler, faster |
| Resource usage | Heavy | Lightweight |
| Best for | Large orgs needing full control | Teams wanting easy mTLS |

### mTLS — Mutual Transport Layer Security
Mutual TLS — both client AND server verify each other's certificates. Prevents any unauthorized service from talking to another.

### Traffic Management with Istio
```yaml
# VirtualService — canary: 90% to v1, 10% to v2
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: api
spec:
  http:
  - route:
    - destination:
        host: api
        subset: v1
      weight: 90
    - destination:
        host: api
        subset: v2
      weight: 10
```

---

# 🔵 16. Soft Skills / HR Questions

---

**"Tell me about yourself"**
> "I'm a DevOps/Infrastructure Engineer with experience in cloud infrastructure including EKS on AWS, Karpenter for node scaling, Elasticsearch clusters on EC2, and Jenkins pipelines. I've been working on migrating services from Lambda to Kubernetes and my goal is to become a strong AWS infrastructure expert."

**"Why DevOps?"**
> "I like the combination of development thinking and operational responsibility. DevOps removes the wall between writing code and running it — I find it satisfying to own a system end to end, from deployment pipeline to production monitoring."

**"Describe a difficult challenge"**
> Structure: Situation → Problem → What you did → Result
> Example: "Our Elasticsearch ILM policies weren't auto-deleting indices because empty indices never triggered rollover. Pods were going Pending because disk was filling up. I diagnosed it via `GET _ilm/explain`, found the root cause, added `max_age: 1d` rollover to the hot phase, and wrote bulk force-move scripts for ~51 stuck indices. Resolved without any data loss."

**"How do you handle production incidents?"**
> "First, stop the bleeding — rollback or redirect traffic. Then understand the scope. Communicate to stakeholders. Find root cause using logs, metrics, traces. Fix. Write a postmortem with timeline and action items so it doesn't happen again."

**"What is your on-call experience?"**
> Mention: alert response time, runbooks you follow, tools you use (PagerDuty, Slack alerts, CloudWatch), and one real incident you resolved.

**"Career goals?"**
> "In the short term, I want to deepen my AWS expertise — specifically around cost optimization with Karpenter, GitOps with ArgoCD, and security with IRSA and Secrets Manager. Long term, I want to architect resilient, scalable infrastructure that lets product teams ship fast without worrying about the platform."

---

# Quick Revision — One-Liners

| Topic | One Line |
|-------|---------|
| Container vs VM | Container shares OS kernel, VM has its own OS |
| Pod | Smallest K8s unit, runs one or more containers |
| Deployment | Manages pods, handles scaling + rolling updates |
| Service | Stable network address for a set of pods |
| Ingress | Single entry point routing traffic to many services |
| ConfigMap | Non-sensitive app config in K8s |
| Secret | Sensitive data in K8s (base64 encoded, not encrypted) |
| RBAC (Role-Based Access Control) | Who can do what in the cluster |
| HPA (Horizontal Pod Autoscaler) | Scale pods based on CPU/memory |
| Karpenter | Scale nodes based on pod demand |
| IRSA (IAM Roles for Service Accounts) | Pods get AWS IAM identity without hardcoded keys |
| Helm | Package manager for K8s (like apt for ubuntu) |
| ArgoCD | Watches Git, syncs cluster to match desired state |
| Terraform | IaC tool — define AWS resources in code |
| Ansible | Configuration management — keep servers consistent |
| SLO (Service Level Objective) | Target uptime/reliability you commit to |
| Error Budget | Allowed failure = 100% - SLO |
| mTLS (Mutual TLS) | Both sides verify identity (service mesh) |
| etcd (Distributed key-value store) | K8s brain — stores all cluster state |
| NAT Gateway (Network Address Translation) | Private subnet outbound internet (no inbound) |

---

*Total: 16 Categories | ~200 Topics | DevOps + SRE Interview Ready*
*Stack: AWS ap-south-1, EKS, RKE2, Karpenter, Elasticsearch*

---

---

# 🔴 17. Troubleshooting Scenarios (Mid-Level Interview)

> Ye section specifically "scenario-based" questions ke liye hai.
> Format: **Problem → Tumhara thought process → Commands → Fix**
> Interview mein hamesha thought process boldo pehle — command baad mein.

---

## Kubernetes Troubleshooting

---

### Scenario 1: Pod CrashLoopBackOff

**Interviewer:** "Tumhara pod CrashLoopBackOff mein hai, kya karoge?"

**Thought process:**
```
CrashLoopBackOff = pod start hota hai, crash hota hai, K8s restart karta hai, phir crash — loop
Reasons: app crash, wrong config, missing env var, OOMKilled, wrong image
```

**Step by step debug:**
```bash
# Step 1: pod ka status dekho
kubectl get pods
# Output: my-app-xxx   0/1   CrashLoopBackOff   5   3m

# Step 2: logs dekho (crash hone se pehle ka output)
kubectl logs my-app-xxx
kubectl logs my-app-xxx --previous   # pichle crash ka log

# Step 3: pod ka description dekho
kubectl describe pod my-app-xxx
# Events section mein dekho — OOMKilled? ImagePullBackOff? Config error?

# Step 4: agar OOMKilled dikh raha hai
# → memory limit badhaao deployment mein
kubectl edit deployment my-app
# resources.limits.memory: "256Mi" → "512Mi"

# Step 5: agar env var missing hai
kubectl exec -it my-app-xxx -- env | grep DB_HOST
# agar empty → ConfigMap ya Secret check karo

# Step 6: image issue hai toh
kubectl describe pod my-app-xxx | grep Image
# verify karo ECR mein image exist karta hai
aws ecr list-images --repository-name my-app --region ap-south-1
```

**Common root causes:**
| Exit Code | Meaning |
|-----------|---------|
| Exit 0 | App ne khud quit kiya (intentional) |
| Exit 1 | App crash — code mein error |
| Exit 137 | OOMKilled — memory limit exceed |
| Exit 143 | SIGTERM — graceful kill timeout |

---

### Scenario 2: Pod Stuck in Pending

**Interviewer:** "Pod Pending state mein hai aur deploy nahi ho raha, debug karo."

**Thought process:**
```
Pending = pod schedule nahi hua kisi node par
Reasons: resources nahi hain, taint/toleration mismatch, PVC bind nahi hua, node selector match nahi
```

```bash
# Step 1: describe karo — Events section sab bata dega
kubectl describe pod my-app-xxx

# Common event messages aur unka matlab:
# "0/2 nodes are available: insufficient cpu"
#   → nodes par CPU nahi — replicas kam karo ya node add karo

# "0/2 nodes are available: node had taint"
#   → pod mein toleration missing hai
#   → deployment mein tolerations add karo

# "persistentvolumeclaim not found"
#   → PVC exist nahi karta
#   kubectl get pvc   # check karo

# "no nodes match node selector"
#   → nodeSelector label galat hai
#   kubectl get nodes --show-labels

# Step 2: node resources dekho
kubectl describe nodes | grep -A5 "Allocated resources"

# Step 3: agar Karpenter hai aur node nahi aa raha
kubectl logs -n kube-system -l app.kubernetes.io/name=karpenter
# Karpenter ko EC2 launch karne mein koi issue?
```

---

### Scenario 3: Pod Running But App Not Reachable

**Interviewer:** "Pod Running hai, curl karo toh connection refused aa raha hai."

```bash
# Step 1: pod ke andar jaake check karo — app actually chal raha hai?
kubectl exec -it my-app-xxx -- sh
curl localhost:3000   # andar se hit karo
# agar andar bhi fail → app start nahi hua → logs dekho

# Step 2: service correct port map kar raha hai?
kubectl get service my-app
kubectl describe service my-app
# targetPort aur containerPort match karte hain?

# Step 3: service ke endpoints populated hain?
kubectl get endpoints my-app
# agar empty → service ka selector deployment ke labels se match nahi karta
# service mein: selector: app: my-app
# deployment mein: labels: app: my-app  ← same hona chahiye

# Step 4: agar Ingress hai
kubectl describe ingress my-ingress
# ALB provisioned hua? Address column mein value hai?
kubectl logs -n kube-system deployment/aws-load-balancer-controller
```

---

### Scenario 4: Node NotReady

**Interviewer:** "Ek node NotReady ho gaya, kya karoge?"

```bash
# Step 1: node status dekho
kubectl get nodes
# NAME        STATUS     ROLES    AGE
# node-1      NotReady   <none>   2d   ← problem

# Step 2: node describe karo
kubectl describe node node-1
# Conditions section dekho:
# MemoryPressure, DiskPressure, PIDPressure, Ready — sab False hona chahiye
# Ready = False matlab kubelet ne heartbeat bheja nahi

# Step 3: node par kya chal raha hai
kubectl get pods --all-namespaces --field-selector spec.nodeName=node-1
# kaunse pods us node par the?

# Step 4: pods ko doosre nodes par move karo
kubectl cordon node-1      # naye pods mat schedule karo is node par
kubectl drain node-1 --ignore-daemonsets --delete-emptydir-data
# sab pods dusre nodes par shift ho jayenge

# Step 5: AWS console mein EC2 instance check karo
# ya SSH karke kubelet status dekho
# systemctl status kubelet
# journalctl -u kubelet -f

# Step 6: fix ke baad wapas enable karo
kubectl uncordon node-1
```

---

### Scenario 5: ImagePullBackOff

```bash
# Describe karo
kubectl describe pod my-app-xxx | grep -A10 Events

# Common reasons:
# 1. Image name galat hai → ECR URL check karo
# 2. ECR login expire ho gayi → re-authenticate
aws ecr get-login-password --region ap-south-1 | \
  docker login --username AWS --password-stdin $REGISTRY

# 3. Node ka IAM role ECR pull ka permission nahi deta
# Node role mein ye policy honi chahiye:
# AmazonEC2ContainerRegistryReadOnly

# 4. Private repo hai, imagePullSecret missing hai
kubectl create secret docker-registry ecr-secret \
  --docker-server=$REGISTRY \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password)
```

---

### Scenario 6: OOMKilled — Out of Memory

```bash
# Pod describe karo
kubectl describe pod my-app-xxx | grep -i oom
# "OOMKilled" dikhega Last State mein

# Solution 1: memory limit badhaao
kubectl edit deployment my-app
# limits.memory: "256Mi" → "512Mi"

# Solution 2: actual memory usage dekho pehle
kubectl top pod my-app-xxx   # metrics-server chahiye

# Solution 3: app mein memory leak hai toh
# profiling karo — Node.js: --inspect, Java: heap dump
```

---

### Scenario 7: Deployment Rollout Stuck

```bash
# Check rollout status
kubectl rollout status deployment my-app
# "Waiting for deployment to complete..."

# Describe karo
kubectl describe deployment my-app
# Events mein dekho

# Common reason: new pods start nahi ho rahe (crash/image issue)
kubectl get pods | grep my-app
# Agar new pods CrashLoopBackOff mein hain → rollback karo

# Rollback previous version par
kubectl rollout undo deployment my-app

# Rollout history
kubectl rollout history deployment my-app
kubectl rollout undo deployment my-app --to-revision=2
```

---

## Linux Troubleshooting

---

### Scenario 8: Server Slow / High CPU

**Interviewer:** "Production server slow hai, users complaints kar rahe hain. Kya karoge?"

```bash
# Step 1: top level check — kya slow hai?
top
# ya htop (better UI)
# CPU high? Memory high? Load average?

# Step 2: CPU kaunsi process kha rahi hai?
ps aux --sort=-%cpu | head -10
# PID aur process name note karo

# Step 3: load average samjho
uptime
# 3 numbers: 1min, 5min, 15min load average
# CPU cores se compare karo (4 core server par load 4.0 = 100% busy)
# load > cores = system overwhelmed

# Step 4: koi runaway process hai?
kill -9 <PID>   # agar specific process culprit hai

# Step 5: K8s pod CPU check
kubectl top pods --all-namespaces | sort -k3 -rn | head -10
kubectl top nodes
```

---

### Scenario 9: Disk Full

**Interviewer:** "Disk full ho gaya, deploy nahi ho raha."

```bash
# Step 1: kahan full hai?
df -h
# Filesystem      Size  Used Avail Use%
# /dev/xvda1       50G   50G     0  100%  ← problem

# Step 2: kaunsi directory le rahi hai space?
du -sh /* 2>/dev/null | sort -rh | head -10
du -sh /var/log/* | sort -rh | head -10

# Step 3: common culprits
# Docker images/containers
docker system df          # docker space usage
docker system prune -a    # unused images/containers delete

# K8s logs
ls -lh /var/log/containers/
journalctl --disk-usage

# Application logs
ls -lh /var/log/myapp/
# purane logs compress ya delete karo

# Step 4: large files dhundho
find / -size +500M -type f 2>/dev/null

# Step 5: future ke liye
# logrotate configure karo
# /etc/logrotate.d/myapp
```

---

### Scenario 10: Memory Full / OOM on Server

```bash
# Step 1: memory status
free -m
# total=16384, used=16000, free=384 → almost full

# Step 2: kaunsi process kha rahi hai?
ps aux --sort=-%mem | head -10

# Step 3: swap dekho
swapon --show
# agar swap nahi hai → add karo temporarily
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

# Step 4: K8s mein pods evict ho rahe hain?
kubectl get events | grep Evicted
kubectl describe node | grep -A5 "MemoryPressure"
```

---

### Scenario 11: Port Already in Use

```bash
# Error: "bind: address already in use :3000"

# Kaun use kar raha hai port 3000?
lsof -i :3000
netstat -tlnp | grep 3000
ss -tlnp | grep 3000

# PID kill karo
kill -9 <PID>

# Ya process name se
pkill -f "node server.js"
```

---

### Scenario 12: SSH Connection Refused

```bash
# Step 1: server reachable hai?
ping server-ip
traceroute server-ip

# Step 2: port 22 open hai?
telnet server-ip 22
nmap -p 22 server-ip

# Step 3: AWS Security Group mein port 22 allow hai?
# Console → EC2 → Security Groups → Inbound rules

# Step 4: SSH service chal rahi hai? (agar server access kisi aur tarike se ho)
systemctl status sshd

# Step 5: key permission galat hai?
chmod 600 ~/.ssh/key.pem
chmod 700 ~/.ssh/
```

---

## AWS Troubleshooting

---

### Scenario 13: EC2 Instance Not Reachable

```bash
# Checklist (is order mein check karo):
# 1. Instance running state mein hai? (AWS Console)
# 2. Security Group mein inbound rule hai?
# 3. NACL (Network ACL) block toh nahi kar raha?
# 4. Public IP assigned hai? (agar public subnet mein hai)
# 5. Route table mein IGW route hai?
# 6. Instance status checks pass hain? (Console → Status checks)
```

---

### Scenario 14: ECR Push Failing

```bash
# Error: "no basic auth credentials"
# Fix: re-login
aws ecr get-login-password --region ap-south-1 | \
  docker login --username AWS --password-stdin \
  $(aws sts get-caller-identity --query Account --output text).dkr.ecr.ap-south-1.amazonaws.com

# Error: "repository does not exist"
aws ecr create-repository --repository-name my-app --region ap-south-1

# Error: "denied: User not authorized"
# IAM policy mein ecr:GetAuthorizationToken aur ecr:BatchCheckLayerAvailability nahi hai
# Attach: AmazonEC2ContainerRegistryFullAccess
```

---

### Scenario 15: Terraform Apply Failing

```bash
# Error: "Error acquiring the state lock"
# Matlab koi aur terraform apply chal raha hai, ya pichla crash ho gaya

# Check karo DynamoDB lock table mein
aws dynamodb scan --table-name terraform-lock

# Force unlock (sach mein koi apply nahi chal raha toh hi karo)
terraform force-unlock <LOCK_ID>

# Error: "resource already exists"
# Resource manually bana tha, terraform ko pata nahi
terraform import aws_instance.web i-1234567890

# Error: "AccessDenied"
# IAM permissions nahi hain — aws sts get-caller-identity check karo
aws sts get-caller-identity
```

---

## CI/CD Troubleshooting

---

### Scenario 16: Jenkins Pipeline Failing

```bash
# Step 1: Console output padho carefully
# Error line dhundho — "ERROR", "FAILED", "Exception"

# Step 2: common failures:
# "Permission denied" → Jenkins user ko permission chahiye
# "docker: command not found" → Jenkins agent par docker nahi
# "git: authentication failed" → credentials update karo

# Step 3: agar docker push fail ho raha hai
# ECR login expire ho gayi — pipeline mein login step add karo
sh """
  aws ecr get-login-password --region ap-south-1 | \
  docker login --username AWS --password-stdin ${ECR_REGISTRY}
"""

# Step 4: workspace clean karo
sh "docker system prune -f"
sh "rm -rf *"
```

---

---

# 🟢 18. Real Experience Stories — STAR Format

> STAR = **S**ituation → **T**ask → **A**ction → **R**esult
> Ye tumhare actual production experience pe based hain.
> Interview mein confidently boldo — ye real hai tumhara.

---

## Story 1: Elasticsearch ILM Policy Fix

**Question trigger:** "Describe a difficult production problem you solved."

**Situation:**
> "Hamare production log-cluster par Elasticsearch mein data stream backing indices automatically delete nahi ho rahe the. Ye ek 3-node Elasticsearch 8.18.2 cluster tha EC2 r8g Graviton4 instances par."

**Task:**
> "Mujhe diagnose karna tha ki ILM (Index Lifecycle Management) policy apply hone ke bawajood indices stuck kyun hain, aur bina data loss ke fix karna tha."

**Action:**
> "Maine Kibana Dev Tools se `GET _ilm/explain` run kiya. Dekha ki indices `hot/rollover/check-rollover-ready` phase mein stuck hain. Root cause ye nikla ki empty indices — 0 documents wale — rollover trigger nahi karte the kyunki humari policy mein sirf `min_docs` condition thi, `max_age` nahi thi.
>
> Maine fix kiya:
> - `datastream-cleanup` aur `node-appserver-ttl-cleanup-policy` dono mein `max_age: 1d` rollover condition add ki
> - ~51 stuck indices ke liye bulk force-move script likhi `POST _ilm/move/{index-name}` se
> - Beta environment mein pehle test kiya, phir Stage aur Production par apply kiya"

**Result:**
> "Indices automatically delete hone lage. Disk space free hua. Zero data loss. Aur ab naye indices bhi same issue mein nahi aate kyunki age-based rollover add ho gaya."

**Interview tip:** Agar pooche "what would you do differently?" → "Pehle se `max_age` condition add karta policy mein, aur ILM monitoring alert lagata jo stuck indices pe alert kare."

---

## Story 2: Karpenter Node Scaling Setup

**Question trigger:** "Have you worked on auto-scaling? Tell me about it."

**Situation:**
> "Hamare RKE2 cluster par fixed node count tha. Traffic spikes pe pods `Pending` state mein reh jaate the kyunki nodes nahi the. Aur off-peak hours mein bhi nodes full run karte the — unnecessary cost."

**Task:**
> "Karpenter implement karna tha spot aur on-demand nodes ke saath, taaki pods ke hisaab se nodes automatically aayein aur jayein."

**Action:**
> "Maine `EC2NodeClass` aur `NodePool` configure kiye. Spot instances ke liye `myorg.io/lifecycle: spot` label add kiya taaki workloads ko spot vs on-demand par schedule kiya ja sake. `consolidateAfter: 30s` set kiya taaki idle nodes quickly terminate ho jayein. Instance families `m`, `c`, `r` set kiye flexibility ke liye taaki Karpenter best available instance choose kar sake."

**Result:**
> "Pods ab ~60 seconds mein schedule ho jaate hain traffic spike par. Off-peak par nodes consolidate ho jaate hain. Infrastructure cost mein noticeable reduction aaya spot instances ki wajah se."

---

## Story 3: Lambda to RKE2 Migration

**Question trigger:** "Have you done any service migrations? Tell me about a complex one."

**Situation:**
> "Hamare production mein teen Lambda-based services the — `ttl-evaluation`, `ttl-pdd-db`, `ttl-pdd` — jo AWS Lambda par run kar rahe the. Decision liya gaya ki inhe RKE2 Kubernetes cluster par migrate karna hai for better control, observability, aur cost."

**Task:**
> "Migration plan banana tha, risks assess karne the, aur zero-downtime migration execute karni thi."

**Action:**
> "Maine pehle ek migration report banai jisme:
> - Har service ka current Lambda config document kiya (memory, timeout, triggers)
> - Kubernetes Deployment aur Service YAML banaye equivalent config ke saath
> - Resource requests/limits set kiye Lambda memory ke basis par
> - Rollback strategy define ki — Lambda parallel mein rakhna jab tak K8s stable na ho
>
> Migration ke time:
> - Pehle staging par deploy kiya aur test kiya
> - Production par blue-green style migrate kiya
> - Lambda ko 1 week baad disable kiya jab sab stable tha"

**Result:**
> "Teeno services successfully RKE2 par chal rahe hain. Better log visibility mili Kibana se. Resource usage predictable ho gaya compared to Lambda cold starts."

---

## Story 4: Production Incident Handling (Generic Template)

**Question trigger:** "Tell me about a time you handled a production incident."

**Use this structure for any incident:**

```
Situation: "Hum [time] par the jab [alert/symptom] aaya."

Task: "Meri responsibility thi [kya fix karna tha, kitna impact tha]."

Action:
  1. "Pehle maine impact assess kiya — [kitne users affected, kaunsi service down]"
  2. "Immediate mitigation kiya — [rollback/redirect/restart]"
  3. "Root cause dhundha — [commands, logs, metrics jo dekhe]"
  4. "Permanent fix apply kiya"
  5. "Team ko communicate kiya throughout"

Result: "Service [X minutes] mein restore hui. Postmortem mein [action item] add kiya
         taaki ye dobara na ho."
```

---

## Story 5: AWS Infrastructure Work

**Question trigger:** "What AWS services have you worked with hands-on?"

> "Maine primarily AWS par kaam kiya hai:
>
> **EKS** — Managed Kubernetes cluster setup, node groups configure kiye, Karpenter ke saath node autoscaling.
>
> **EC2** — Elasticsearch cluster r8g Graviton4 ARM64 instances par — 3-node setup manage kiya including ILM troubleshooting.
>
> **ECR** — Docker images push/pull pipeline Jenkins se. Image tagging strategy — git commit hash as tag.
>
> **IAM** — IRSA setup for pods, least privilege policies, service accounts for Jenkins.
>
> **VPC** — Subnet configuration, security groups for EKS node groups aur Elasticsearch.
>
> **CloudWatch** — Log groups for Lambda functions, alarms for EC2 metrics.
>
> Mera goal hai ek strong AWS infrastructure expert banna — isliye actively EKS, cost optimization, aur security (Secrets Manager, KMS) seekh raha hoon."

---

## Quick STAR Formula Reminder

```
S — Scene set karo (1-2 sentences, context)
T — Tumhara role kya tha specifically
A — Exactly kya kiya, step by step (longest part)
R — Number se boldo result — time saved, cost reduced, downtime avoided

❌ Avoid: "We did this, we solved it"
✅ Better: "Maine specifically X kiya, jo Y result diya"

Interview mein "I" use karo, "we" nahi — tumhara contribution clear hona chahiye.

## Ec2 Type and its requirments:

Konsa choose kare — decision tree
RAM zyada chahiye CPU se?         → R family
CPU zyada chahiye RAM se?         → C family
Balanced?                          → M family
Bursty workload?                   → T family
Fast local disk?                   → I family (NVMe) ya `d` suffix
GPU chahiye?                       → G / P family
Sasta chahiye + ARM compatible?    → Graviton variants (g suffix)
Pata nahi?                         → m6i.large se shuru kar, monitor kar, adjust kar
```

---

*Document updated with: Troubleshooting Scenarios (16 scenarios) + Real Experience Stories (5 STAR stories)*
*Total: 18 Sections | Mid-Level DevOps Interview Ready 🎯*

# Kubernetes: Zero to Mid-Level Guide (DevOps/SRE Lens)

A practical, operator-focused guide for engineers running Kubernetes in production — not a developer tutorial. Heavy on daily commands, triage flows, and the realities of running on AWS with RKE2 + Karpenter.

> **Companion doc:** `docker-guide-zero-to-mid.md` — read that first if Docker basics aren't second nature yet. This guide assumes you can build/run/debug containers.

---

## Verification Status (What's Confirmed vs. Stack-Specific)

This doc was researched against current public sources (Karpenter v1 docs, AWS LB Controller docs, RKE2 docs, Pod Identity vs IRSA blogs). Below is what I've verified and what genuinely depends on your specific cluster setup.

### ✅ Verified against current docs (May 2026)

| Topic | Verified | Source |
|---|---|---|
| Karpenter API is `karpenter.sh/v1` (NodePool, EC2NodeClass) — GA Aug 2024 | Yes | karpenter.sh/v1.0 docs, AWS announcement |
| `amiSelectorTerms` and `consolidateAfter` are required in v1 | Yes | Karpenter v1 migration guide |
| EKS Pod Identity does NOT work on RKE2 (EKS-only) | Yes | AWS Pod Identity docs |
| Self-hosted IRSA on RKE2 via pod-identity-webhook is the standard | Yes | `github.com/chaospuppy/irsa-demo` |
| RKE2 + Calico Pod IPs are NOT directly routable from ALB — `target-type: ip` fails | Yes | AWS LB Controller issue #4223 |
| AWS LB Controller v2.13+ supports non-EKS (RKE2) deployments | Yes | LB Controller docs |
| RKE2 CoreDNS labels include both `k8s-app=kube-dns` and `app.kubernetes.io/name=rke2-coredns` | Yes | RKE2 GitHub discussions |
| RKE2 manifest auto-deploy dir is `/var/lib/rancher/rke2/server/manifests/` | Yes | RKE2 docs |

### ⚠ Depends on your specific cluster — verify before copy-pasting

| Topic | What to verify |
|---|---|
| Do spot Nodes have a `cashify.in/lifecycle=spot:NoSchedule` taint, or just a label? | `kubectl get nodes -l cashify.in/lifecycle=spot -o custom-columns=NAME:.metadata.name,TAINTS:.spec.taints` |
| Karpenter version actually deployed | `kubectl api-resources \| grep karpenter` — should show `karpenter.sh/v1` |
| Is IRSA already set up? If yes, via which path? | `kubectl get mutatingwebhookconfigurations \| grep -i identity` + check SA annotations |
| Does the Node IAM role have `AmazonEC2ContainerRegistryReadOnly` (for kubelet ECR pulls)? | Check IAM role policies on the Node instance profile |
| Is kubelet credential provider configured for ECR? (RKE2 may not auto-do this) | Check `/etc/rancher/rke2/credential-providers/` on Nodes |
| AWS LB Controller actually installed and version | `kubectl get deploy -n kube-system aws-load-balancer-controller -o jsonpath='{.spec.template.spec.containers[0].image}'` |
| CSI drivers available (EBS, EFS) | `kubectl get csidrivers` |

### ❌ I cannot verify without cluster access

These are environment-specific:
- Your exact NodePool YAML, instance families, AZ list
- Whether you taint or just label
- Your IRSA OIDC issuer URL
- Your Subnet tag conventions
- Whether you use Network Policy enforcement (depends on CNI mode)

**Treat any concrete YAML in this doc as a template to adapt, not to copy-paste into prod.**

---

## Acronyms & Shortcuts (Glossary)

Every acronym used in this doc, in one place. They're also expanded inline on first use.

| Short | Full form | Quick meaning |
|---|---|---|
| **HA** | High Availability | Redundancy so a single failure doesn't take a service down |
| **DR** | Disaster Recovery | Restoring service after a major failure (region loss, data corruption) |
| **API** | Application Programming Interface | Programmatic interface (in k8s context, usually the API server) |
| **CLI** | Command-Line Interface | Terminal-based tool (kubectl, helm, etc.) |
| **YAML** | YAML Ain't Markup Language | The config format Kubernetes uses |
| **CRD** | Custom Resource Definition | A way to add your own resource types to Kubernetes |
| **CR** | Custom Resource | An instance of a CRD |
| **CNI** | Container Network Interface | Plugin spec for pod networking (Calico, Cilium, Flannel) |
| **CSI** | Container Storage Interface | Plugin spec for storage (EBS CSI, EFS CSI) |
| **CRI** | Container Runtime Interface | Plugin spec for the container runtime (containerd, CRI-O) |
| **RBAC** | Role-Based Access Control | Permissions system (who can do what) |
| **SA** | ServiceAccount | The identity a Pod uses to call the API |
| **IRSA** | IAM Roles for Service Accounts | AWS feature: tie a k8s ServiceAccount to an IAM Role |
| **IAM** | Identity and Access Management | AWS's permission system |
| **HPA** | Horizontal Pod Autoscaler | Scales pod count based on metrics |
| **VPA** | Vertical Pod Autoscaler | Adjusts a pod's CPU/memory requests |
| **CA** | Cluster Autoscaler | Adds/removes nodes (older AWS approach; Karpenter is the modern one) |
| **PV** | PersistentVolume | A piece of storage in the cluster |
| **PVC** | PersistentVolumeClaim | A request for storage by a Pod |
| **SC** | StorageClass | Defines how storage is dynamically provisioned |
| **PDB** | PodDisruptionBudget | Limits how many pods can be voluntarily disrupted at once |
| **PSP** | Pod Security Policy | (Deprecated) old admission control for pod security |
| **PSS** | Pod Security Standards | Replaces PSP — Privileged / Baseline / Restricted profiles |
| **QoS** | Quality of Service | Pod scheduling class: Guaranteed / Burstable / BestEffort |
| **DNS** | Domain Name System | Name resolution; in k8s, CoreDNS handles it |
| **TLS** | Transport Layer Security | Encrypted transport (HTTPS) |
| **ALB** | Application Load Balancer | AWS L7 load balancer |
| **NLB** | Network Load Balancer | AWS L4 load balancer |
| **ECR** | Elastic Container Registry | AWS's container image registry |
| **EBS** | Elastic Block Store | AWS block storage (attached to one node) |
| **EFS** | Elastic File System | AWS NFS-style shared filesystem |
| **AZ** | Availability Zone | A data center within an AWS region |
| **OOM** | Out Of Memory | Kernel killed the process for using too much memory |
| **SIGTERM/SIGKILL** | Termination signals | TERM = graceful, KILL = immediate |
| **DS** | DaemonSet | A Pod that runs on every node (or a subset) |
| **STS** | StatefulSet | A Deployment with stable identities for stateful apps |
| **RS** | ReplicaSet | Maintains a count of Pod replicas; managed by a Deployment |
| **GC** | Garbage Collection | Cleaning up orphaned resources |

---

## Table of Contents

1. [Mental Model: Control Plane vs Data Plane](#1-mental-model-control-plane-vs-data-plane)
2. [Cluster, Node, Namespace](#2-cluster-node-namespace)
3. [kubectl Essentials (Daily Commands)](#3-kubectl-essentials-daily-commands)
4. [Manifests, YAML, Labels & Selectors](#4-manifests-yaml-labels--selectors)
5. [Workloads](#5-workloads)
6. [Networking](#6-networking)
7. [Storage](#7-storage)
8. [Configuration & Secrets](#8-configuration--secrets)
9. [Scheduling & Placement](#9-scheduling--placement)
10. [Scaling (HPA, VPA, Karpenter)](#10-scaling)
11. [Security: RBAC, ServiceAccounts, IRSA, Pod Security](#11-security-rbac-serviceaccounts-irsa-pod-security)
12. [Packaging & Deployment](#12-packaging--deployment--helm-kustomize-operators)
13. [Observability — Logs, Metrics, Events, Debugging](#13-observability--logs-metrics-events-debugging)
14. [Production Troubleshooting](#14-production-troubleshooting)
15. [RKE2-Specific Operations](#15-rke2-specific-operations)
16. [Backup, DR & Cluster Upgrades](#16-backup-dr--cluster-upgrades)
17. [kubectl Operator's Cheat Sheet](#17-kubectl-operators-cheat-sheet)
18. [Docker → Kubernetes Mental Map (Full)](#18-docker--kubernetes-mental-map-full)
19. [Daily Revision (14-Day Rotation)](#daily-revision-7-day-rotation)
20. [Commands Daily Drill (14-Day Rotation)](#commands-daily-drill-pure-muscle-memory)

**Status:** All 18 sections complete. Daily Revision and Commands Drill extended to 14 days. Continue cycling through the rotations to build retention.

---

## 1. Mental Model: Control Plane vs Data Plane

A Kubernetes cluster is two things glued together:

**Control Plane** — the brain. Makes decisions. Stores state.
- **API server** (`kube-apiserver`) — the front door. Every command goes through it.
- **etcd** — the database. Holds all cluster state (versioned key-value store).
- **scheduler** (`kube-scheduler`) — decides which node a Pod runs on.
- **controller manager** (`kube-controller-manager`) — runs the reconciliation loops (e.g., "Deployment says 3 replicas, only 2 exist → create 1 more").
- **cloud controller manager** — talks to AWS (provisions load balancers, attaches EBS volumes).

**Data Plane** — the muscles. Runs your workloads.
- **kubelet** — the agent on every node. Talks to the API server, manages containers via the CRI (Container Runtime Interface).
- **kube-proxy** — programs iptables/IPVS rules on each node so Service traffic reaches the right Pods.
- **container runtime** — containerd (default in RKE2) or CRI-O. Actually runs containers.
- **CNI plugin** — provides Pod networking (Calico in RKE2 by default).

### The reconciliation loop (the One Big Idea)

You don't "run" things on Kubernetes. You **declare desired state** in YAML, the API server stores it in etcd, and **controllers** continuously diff actual vs desired and act to close the gap.

```
You apply:  "Deployment app=api, replicas=3"
   ↓
API server stores it in etcd
   ↓
Deployment controller sees: "I should have 3 Pods, I have 0"
   ↓
Creates ReplicaSet → ReplicaSet controller creates 3 Pods
   ↓
Scheduler picks a node for each Pod
   ↓
kubelet on each node tells containerd to run the container
```

If you `kubectl delete pod` one of them, the loop notices and recreates it. **That's why "fixing" a misbehaving Pod by deleting it works** — the controller brings it back fresh.

### High Availability (HA) of the control plane

A **single control-plane node** = single point of failure. Lose it, you lose the API (existing Pods keep running but nothing new can be scheduled, scaled, or healed).

**HA control plane** = run 3 (or 5) control-plane nodes. etcd uses Raft consensus, which needs a majority (quorum) to commit writes:

| etcd nodes | Tolerates loss of |
|---|---|
| 1 | 0 (any loss = downtime) |
| 3 | 1 |
| 5 | 2 |
| 7 | 3 |

Always use odd numbers (even counts give no extra fault tolerance and risk split-brain). **3 is the standard.** 5 only if you're at very large scale or in 3+ AZs.

**Data-plane HA** is separate: multiple worker nodes across AZs, multiple replicas per Deployment, PodDisruptionBudgets, and topology spread (covered in Section 9).

For your stack: your Elasticsearch log-cluster is 3 nodes for the same reason — quorum survives 1 node loss.

---

## 2. Cluster, Node, Namespace

### Cluster

The unit of "one Kubernetes." One control plane, many nodes, one shared etcd. You typically have multiple clusters: Dev, Stage, Beta, Prod. Each is fully independent.

```bash
kubectl cluster-info
kubectl get nodes
kubectl version --short
```

### Node

A machine (VM or bare metal) running the kubelet. Types:
- **Control-plane node** — runs API server, etcd, scheduler, controller-manager. In RKE2 called a "server" node.
- **Worker node** — runs your workloads. In RKE2 called an "agent" node.

```bash
kubectl get nodes -o wide
kubectl describe node <node-name>
kubectl top nodes                       # CPU/mem usage (needs metrics-server)
kubectl get nodes --show-labels
```

Useful node fields in `describe`:
- **Conditions** — Ready, MemoryPressure, DiskPressure, PIDPressure, NetworkUnavailable
- **Taints** — what the node refuses (e.g., spot nodes often taint `karpenter.sh/disruption=disrupting`)
- **Allocatable** — actual CPU/mem schedulable (system reserved is subtracted)
- **Non-terminated Pods** — what's currently running, with requests

### Namespace

A logical partition inside a cluster. Used to group related resources and apply RBAC/quotas. **Namespaces do NOT isolate networking by default** (use NetworkPolicy for that).

```bash
kubectl get namespaces                  # short: kubectl get ns
kubectl create namespace ml-services
kubectl get pods -n ml-services
kubectl get pods --all-namespaces       # short: -A
kubectl config set-context --current --namespace=ml-services   # default ns for current context
```

**Common namespace patterns:**
- `kube-system` — control-plane components (don't touch unless you know what you're doing)
- `kube-public` — readable by everyone (rarely used)
- One namespace per team / per app / per environment-within-cluster
- `default` — exists by default; avoid putting real workloads there

Built-in resources that are **NOT** namespaced (cluster-scoped):
- Nodes, PersistentVolumes, StorageClasses, ClusterRoles, ClusterRoleBindings, CRDs, Namespaces themselves

```bash
kubectl api-resources --namespaced=true   # all namespaced kinds
kubectl api-resources --namespaced=false  # all cluster-scoped kinds
```

---

## 3. kubectl Essentials (Daily Commands)

This is your `docker logs / docker exec / docker inspect` for Kubernetes — except with about 30 verbs.

### Setup once

```bash
# Enable kubectl autocomplete (bash)
source <(kubectl completion bash)
echo 'source <(kubectl completion bash)' >> ~/.bashrc

# Most important alias
alias k=kubectl
complete -F __start_kubectl k
```

### Contexts (switching between clusters)

You have Stage / Beta / Prod — context switching is daily.

```bash
kubectl config get-contexts             # list configured clusters
kubectl config current-context          # which am I on?
kubectl config use-context prod-rke2    # switch
kubectl config set-context --current --namespace=ml-services   # set default ns

# kubectx + kubens (highly recommended install)
kubectx prod-rke2                       # switch context
kubens ml-services                      # switch namespace
```

**Pro tip:** put your current context+namespace in your shell prompt. Prevents "I ran that in prod by mistake" disasters. Tools: `kube-ps1`, `starship`.

### The five verbs you'll use thousands of times

```bash
kubectl get <kind> [name]               # list / show
kubectl describe <kind> <name>          # detailed status + events
kubectl logs <pod> [-c container]       # container logs
kubectl exec -it <pod> -- sh            # shell into a Pod
kubectl apply -f <file-or-dir>          # create/update from manifest
```

### `get` — the daily workhorse

```bash
kubectl get pods                                      # short: po
kubectl get pods -A                                   # all namespaces
kubectl get pods -o wide                              # + node, IP, etc.
kubectl get pods -l app=api                           # by label selector
kubectl get pods --field-selector=status.phase=Pending
kubectl get pods --sort-by=.status.startTime
kubectl get pods --sort-by=.metadata.creationTimestamp

# Custom columns (very useful for triage)
kubectl get pods -o custom-columns=\
NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName,RESTARTS:.status.containerStatuses[0].restartCount

# Watch mode
kubectl get pods -w                                   # live updates
kubectl get events -w --sort-by=.lastTimestamp

# Full YAML (for inspection / templating)
kubectl get pod <name> -o yaml
kubectl get pod <name> -o json | jq '.status'
```

Short names (saves typing):
```
po=pods   svc=services   deploy=deployments   rs=replicasets   sts=statefulsets
ds=daemonsets   ns=namespaces   no=nodes   cm=configmaps   pvc=persistentvolumeclaims
pv=persistentvolumes   sa=serviceaccounts   ing=ingresses   ep=endpoints
hpa=horizontalpodautoscalers   netpol=networkpolicies
```

### `describe` — for "what's wrong"

```bash
kubectl describe pod <name>
kubectl describe node <name>
kubectl describe deployment <name>
```

The **Events** section at the bottom is gold — scheduling failures, image pull errors, probe failures all show up there.

### `logs` — beyond the basics

```bash
kubectl logs <pod>                              # current container
kubectl logs <pod> -c <container>               # specific container in multi-container Pod
kubectl logs <pod> --previous                   # logs from the LAST crashed container
kubectl logs <pod> -f                           # follow (like tail -f)
kubectl logs <pod> --tail=200
kubectl logs <pod> --since=15m
kubectl logs <pod> --since-time=2026-05-22T10:00:00Z
kubectl logs -l app=api --max-log-requests=10   # logs from all pods matching label
kubectl logs --previous <pod>                   # crashed container's last logs — CRITICAL for CrashLoopBackOff
```

`--previous` is the one most beginners miss. When a Pod is in `CrashLoopBackOff`, the current container is starting — its logs are empty. The previous one (that crashed) has what you need.

### `exec` — get inside

```bash
kubectl exec -it <pod> -- sh
kubectl exec -it <pod> -c <container> -- bash
kubectl exec <pod> -- env                       # one-shot
kubectl exec <pod> -- cat /etc/resolv.conf
```

### `apply` vs `create` vs `edit` vs `patch`

```bash
# Apply (declarative — preferred): create if missing, update if exists
kubectl apply -f deploy.yaml
kubectl apply -f ./manifests/                   # whole directory
kubectl apply -k ./overlays/prod                # kustomize

# Create (imperative): errors if exists
kubectl create deployment api --image=myapp:0.1

# Edit (opens $EDITOR with live resource — quick fixes)
kubectl edit deployment api

# Patch (programmatic small change)
kubectl patch deployment api -p '{"spec":{"replicas":5}}'
kubectl scale deployment api --replicas=5       # shortcut for replica count

# Replace (full overwrite — rarely correct)
kubectl replace -f deploy.yaml
```

**Rule:** in production, use `apply` with version-controlled YAML. `edit` is for emergency fixes you backport to the repo afterward.

### Rollouts

```bash
kubectl rollout status   deployment/api         # waits until done; great for CI
kubectl rollout history  deployment/api
kubectl rollout undo     deployment/api         # roll back to previous
kubectl rollout undo     deployment/api --to-revision=3
kubectl rollout restart  deployment/api         # force restart all pods (e.g., after Secret change)
kubectl rollout pause    deployment/api
kubectl rollout resume   deployment/api
```

`kubectl rollout restart` is the modern way to bounce a Deployment. Before this existed, people deleted pods one by one.

### Port-forward & proxy (debugging)

```bash
kubectl port-forward pod/api-abc123 8080:8000           # local:pod
kubectl port-forward svc/api 8080:80                    # forward via Service
kubectl port-forward deploy/api 8080:8000               # forward to any pod in deploy
```

Lets you hit a Pod from your laptop without exposing it publicly. Daily-use for debugging.

### `top` — resource usage

```bash
kubectl top nodes
kubectl top pods
kubectl top pods -A --sort-by=memory
kubectl top pods -n ml-services --sort-by=cpu
kubectl top pods --containers                   # per-container breakdown
```

Requires `metrics-server` installed in the cluster (RKE2 ships with it).

### `explain` — built-in docs

Don't memorize fields. Ask the API:

```bash
kubectl explain pod
kubectl explain pod.spec
kubectl explain pod.spec.containers
kubectl explain pod.spec.containers.resources
kubectl explain deployment.spec.strategy --recursive
```

### `debug` — modern Pod debugging

For when you can't `exec` (distroless / scratch image with no shell):

```bash
# Add an ephemeral debug container into a running Pod
kubectl debug -it <pod> --image=busybox --target=<container>

# Create a debug copy of a Pod
kubectl debug <pod> -it --image=busybox --copy-to=debug-<pod> --share-processes

# Debug a node
kubectl debug node/<node-name> -it --image=busybox
```

### Dry-run (safe testing)

```bash
kubectl apply -f deploy.yaml --dry-run=server          # validate against API
kubectl apply -f deploy.yaml --dry-run=client -o yaml  # see the YAML

# Generate YAML without applying (great for getting started)
kubectl create deployment api --image=myapp:0.1 --replicas=3 \
  --dry-run=client -o yaml > deployment.yaml
```

### Daily triage one-liners

```bash
# Pods not Running
kubectl get pods -A --field-selector=status.phase!=Running

# Pods that have ever restarted
kubectl get pods -A -o json | jq -r \
  '.items[] | select(.status.containerStatuses[]?.restartCount > 0) |
   "\(.metadata.namespace)/\(.metadata.name) restarts=\(.status.containerStatuses[0].restartCount)"'

# Recent events (cluster-wide)
kubectl get events -A --sort-by=.lastTimestamp | tail -30

# Pods by node
kubectl get pods -A -o wide --field-selector spec.nodeName=<node-name>

# Where is my service routing? (the Endpoints object answers)
kubectl get endpoints <svc-name>
```

---

## 4. Manifests, YAML, Labels & Selectors

### The YAML skeleton every resource shares

```yaml
apiVersion: <group>/<version>     # e.g., apps/v1, v1, networking.k8s.io/v1
kind: <ResourceKind>              # Pod, Deployment, Service, ...
metadata:
  name: <name>                    # required, DNS-1123 compliant
  namespace: <ns>                 # optional; defaults to current
  labels:                         # key-value, for selection/grouping
    app: api
    env: prod
  annotations:                    # key-value, for arbitrary metadata (not selectable)
    deploy.cashify.in/team: platform
spec:
  # resource-specific desired state
status:
  # filled in by controllers; never write this yourself
```

Find the right `apiVersion` for any kind:
```bash
kubectl api-resources | grep -i ingress
# NAME        SHORTNAMES   APIVERSION                  NAMESPACED   KIND
# ingresses   ing          networking.k8s.io/v1        true         Ingress
```

### Labels vs Annotations

| | Labels | Annotations |
|---|---|---|
| Purpose | Identify and select | Attach metadata |
| Selectable? | Yes (`-l app=api`) | No |
| Used by k8s? | Yes (Services find Pods via labels) | Mostly tools/operators |
| Length | Short (≤63 chars value) | Can be long |
| Examples | `app=api`, `env=prod`, `tier=backend` | `kubectl.kubernetes.io/last-applied-configuration` |

**Labels are the glue.** A Service knows which Pods to send traffic to *only* via label selectors. A Deployment manages Pods *only* via label selectors. Get labels wrong → nothing connects.

### Selectors

Equality-based:
```yaml
selector:
  matchLabels:
    app: api
    env: prod
```

Set-based (more expressive):
```yaml
selector:
  matchExpressions:
    - { key: app, operator: In, values: [api, web] }
    - { key: env, operator: NotIn, values: [dev] }
    - { key: tier, operator: Exists }
```

Selectors on the CLI:
```bash
kubectl get pods -l app=api
kubectl get pods -l 'app in (api,web),env=prod'
kubectl get pods -l app=api --show-labels
```

### Recommended labels (Kubernetes convention)

```yaml
labels:
  app.kubernetes.io/name: api
  app.kubernetes.io/instance: api-prod
  app.kubernetes.io/version: "1.2.3"
  app.kubernetes.io/component: backend
  app.kubernetes.io/part-of: cashify-platform
  app.kubernetes.io/managed-by: helm
```

Following the convention pays off — many tools (Helm, ArgoCD, Datadog) auto-discover via these.

### Field selectors (different from labels)

Filter by built-in fields, not labels:
```bash
kubectl get pods --field-selector=status.phase=Pending
kubectl get pods --field-selector=spec.nodeName=node-1
kubectl get events --field-selector=type=Warning
```

Limited to certain fields per resource — check `kubectl explain` if unsure.

---

## 5. Workloads

The "things that run" in Kubernetes.

### 5.1 Pod — the atomic unit

A Pod is **one or more containers** that share network and storage. Same Pod = same IP, same localhost, same volumes.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: api
  labels: { app: api }
spec:
  containers:
    - name: api
      image: <acct>.dkr.ecr.ap-south-1.amazonaws.com/api:0.1
      ports:
        - containerPort: 8000
      env:
        - name: LOG_LEVEL
          value: info
      resources:
        requests: { cpu: 100m, memory: 128Mi }
        limits:   { cpu: 500m, memory: 512Mi }
```

**You almost never create a raw Pod in production.** Pods are not self-healing — if the node dies, the Pod is gone. Use a **Deployment** (or StatefulSet/DaemonSet/Job) which creates Pods *for* you and replaces them when they die.

#### Pod lifecycle phases

| Phase | Meaning |
|---|---|
| `Pending` | Accepted by API, not yet scheduled OR images pulling |
| `Running` | At least one container is running |
| `Succeeded` | All containers exited 0 |
| `Failed` | All containers terminated, at least one with non-zero exit |
| `Unknown` | Node unreachable |

Container statuses inside a Pod also have reasons: `Running`, `Waiting` (with reason like `ImagePullBackOff`, `CrashLoopBackOff`, `CreateContainerConfigError`), `Terminated`.

#### Init containers

Run **before** main containers, in order. Each must succeed before the next starts. Used for setup: schema migrations, fetching config, waiting for a dependency.

```yaml
spec:
  initContainers:
    - name: wait-for-db
      image: busybox:1.36
      command: ['sh', '-c', 'until nc -z db 5432; do sleep 2; done']
  containers:
    - name: api
      image: api:0.1
```

#### Sidecar containers

A second container in the same Pod that supports the main one — log shipper, proxy, metrics exporter. Same lifecycle as the main container (unlike init containers).

```yaml
spec:
  containers:
    - name: api
      image: api:0.1
    - name: log-shipper
      image: fluent-bit:3.0
      volumeMounts:
        - { name: applogs, mountPath: /var/log }
```

Common in your stack: fluentd/fluent-bit sidecars shipping logs to Elasticsearch.

### 5.2 Probes — liveness, readiness, startup

These drive most "service is flapping" incidents. Get them right.

| Probe | What it answers | Effect on failure |
|---|---|---|
| **livenessProbe** | "Should I restart this container?" | Container is killed and restarted |
| **readinessProbe** | "Should I send traffic here?" | Pod is removed from Service Endpoints (no restart) |
| **startupProbe** | "Has this slow-starting container come up?" | Disables the other probes until it passes once |

```yaml
containers:
  - name: api
    image: api:0.1
    startupProbe:                       # for slow-start apps (JVM, ML model loading)
      httpGet: { path: /healthz, port: 8000 }
      failureThreshold: 30
      periodSeconds: 10                  # → allows 300s for startup
    livenessProbe:
      httpGet: { path: /healthz, port: 8000 }
      initialDelaySeconds: 0             # ok because startupProbe handles startup
      periodSeconds: 10
      failureThreshold: 3
    readinessProbe:
      httpGet: { path: /ready, port: 8000 }
      periodSeconds: 5
      failureThreshold: 2
```

**Common mistakes:**
- Same endpoint for liveness and readiness — they should report different things. Liveness = "process is healthy"; readiness = "I can handle traffic right now (DB connected, caches warm)."
- Too-aggressive liveness on slow-start apps → CrashLoopBackOff during startup. **Use startupProbe.**
- Liveness that depends on downstream services → cascading restarts when DB blips.

### 5.3 Resource requests, limits & QoS

```yaml
resources:
  requests:                 # what the scheduler reserves
    cpu: 200m               # 200 millicores = 0.2 CPU
    memory: 256Mi
  limits:                   # the cap the kernel enforces
    cpu: 1000m              # CPU is throttled when exceeded
    memory: 512Mi           # Memory is OOMKilled when exceeded
```

**Critical distinction:**
- **CPU over limit** → throttled (slowed down, not killed)
- **Memory over limit** → **OOMKilled** (exit 137)

#### QoS (Quality of Service) classes

Kubernetes assigns each Pod a class based on requests/limits. Drives eviction order under node pressure.

| Class | Requirement | Eviction order |
|---|---|---|
| **Guaranteed** | All containers have `requests == limits` for both CPU and memory | Last to evict |
| **Burstable** | At least one request set, but doesn't qualify as Guaranteed | Middle |
| **BestEffort** | No requests or limits anywhere | First to evict |

For critical production workloads → set `requests == limits` → Guaranteed QoS.
For batch/non-critical → Burstable is fine.
Never run real workloads as BestEffort.

```bash
# Check QoS class
kubectl get pod <name> -o jsonpath='{.status.qosClass}'
```

### 5.4 Deployment — what you'll actually use 90% of the time

A Deployment manages a ReplicaSet which manages Pods. You change the Deployment, it creates a new ReplicaSet, performs a rolling update, and keeps history for rollback.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: ml-services
spec:
  replicas: 3
  revisionHistoryLimit: 10               # how many old RSs to keep for rollback
  selector:
    matchLabels: { app: api }
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1                        # extra Pods allowed during rollout
      maxUnavailable: 0                  # zero-downtime rolling
  template:
    metadata:
      labels: { app: api }
    spec:
      containers:
        - name: api
          image: <acct>.dkr.ecr.ap-south-1.amazonaws.com/api:0.1
          ports: [ { containerPort: 8000 } ]
          resources:
            requests: { cpu: 200m, memory: 256Mi }
            limits:   { cpu: 1000m, memory: 512Mi }
          readinessProbe:
            httpGet: { path: /ready, port: 8000 }
          livenessProbe:
            httpGet: { path: /healthz, port: 8000 }
```

**`selector.matchLabels` is immutable** after creation. Plan labels carefully.

#### Rolling update strategies

| Strategy | Behavior |
|---|---|
| `RollingUpdate` (default) | Gradually replace old Pods with new |
| `Recreate` | Kill all old Pods first, then create new (downtime; for apps that can't run two versions at once) |

`maxSurge` / `maxUnavailable` controls (defaults: `25%` each):
- `maxSurge: 1, maxUnavailable: 0` → safe (always at full capacity)
- `maxSurge: 0, maxUnavailable: 1` → no extra resources but reduced capacity
- `maxSurge: 50%, maxUnavailable: 0` → fast rollout with double capacity briefly

#### Rollouts in practice

```bash
# Update the image (triggers rolling update)
kubectl set image deployment/api api=<acct>.dkr.ecr.ap-south-1.amazonaws.com/api:0.2

# Wait for completion (great for CI gating)
kubectl rollout status deployment/api --timeout=5m

# Something broke — roll back
kubectl rollout undo deployment/api

# See history
kubectl rollout history deployment/api
kubectl rollout history deployment/api --revision=5
```

### 5.5 StatefulSet — for stateful apps (Elasticsearch, Postgres, Kafka)

Like a Deployment, but Pods get **stable network identities** and **stable storage**:
- Pod names: `<sts-name>-0`, `<sts-name>-1`, `<sts-name>-2` (ordinal, predictable)
- Each Pod gets its own PVC (volume) that survives Pod deletion and is reattached on recreation
- Ordered, sequential rollout (Pod 0 must be Ready before Pod 1 starts)
- Requires a Headless Service for stable DNS (covered in Section 6)

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: elasticsearch
spec:
  serviceName: elasticsearch              # MUST be a Headless Service
  replicas: 3
  selector: { matchLabels: { app: elasticsearch } }
  template:
    metadata: { labels: { app: elasticsearch } }
    spec:
      containers:
        - name: elasticsearch
          image: docker.elastic.co/elasticsearch/elasticsearch:8.18.2
          volumeMounts:
            - { name: data, mountPath: /usr/share/elasticsearch/data }
  volumeClaimTemplates:                   # creates a PVC per Pod
    - metadata: { name: data }
      spec:
        accessModes: [ ReadWriteOnce ]
        storageClassName: gp3
        resources: { requests: { storage: 200Gi } }
```

Pods reach each other at `elasticsearch-0.elasticsearch.<ns>.svc.cluster.local`, `-1.`, `-2.` — that's why StatefulSets need a headless Service.

### 5.6 DaemonSet — one Pod per node

Runs a Pod on every node (or every node matching a selector). Used for node-level agents.

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata: { name: fluent-bit, namespace: kube-system }
spec:
  selector: { matchLabels: { app: fluent-bit } }
  template:
    metadata: { labels: { app: fluent-bit } }
    spec:
      tolerations:                       # so it runs on tainted nodes too
        - operator: Exists
      containers:
        - name: fluent-bit
          image: fluent/fluent-bit:3.0
```

Common DaemonSets in your stack:
- Log shippers (fluent-bit, fluentd, vector)
- Node exporters (Prometheus node_exporter)
- CNI components (Calico, Cilium)
- CSI node plugins (EBS CSI node driver)
- Security agents

### 5.7 Job — run-to-completion

For batch tasks. The Pod runs once (or N times), exits 0, and is done.

```yaml
apiVersion: batch/v1
kind: Job
metadata: { name: db-migrate }
spec:
  backoffLimit: 3                  # retry on failure up to 3 times
  ttlSecondsAfterFinished: 3600    # auto-delete 1h after completion
  template:
    spec:
      restartPolicy: OnFailure
      containers:
        - name: migrate
          image: api:0.1
          command: ["python", "manage.py", "migrate"]
```

For parallelism: `spec.parallelism` (N pods at a time) + `spec.completions` (target successful pods).

### 5.8 CronJob — scheduled Jobs

```yaml
apiVersion: batch/v1
kind: CronJob
metadata: { name: cleanup-old-data }
spec:
  schedule: "0 2 * * *"                  # daily at 02:00 (cluster's timezone)
  concurrencyPolicy: Forbid              # don't start if previous is still running
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 3
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
            - name: cleanup
              image: api:0.1
              command: ["python", "cleanup.py"]
```

**Gotchas:**
- Timezone is the kube-controller-manager's TZ (usually UTC). Specify with `spec.timeZone` (k8s 1.27+).
- `concurrencyPolicy`: `Allow` (default), `Forbid` (skip if running), `Replace` (kill running, start new).
- Misfires happen — set `startingDeadlineSeconds` to bound how late a missed run can fire.

---

## 6. Networking

The hardest part of Kubernetes for most people. Three concepts solve 95% of cases: **Pod IP**, **Service**, **Ingress**.

### 6.1 The Pod network model

Every Pod gets its own IP. Containers in the same Pod share that IP via localhost.

Rules (enforced by the CNI):
1. Every Pod can reach every other Pod **without NAT**
2. Every Node can reach every Pod **without NAT**
3. The IP a Pod sees itself as = the IP others see it as

Pod IPs are **ephemeral** — they change when Pods restart. Never hardcode them. That's why Services exist.

### 6.2 Service — stable virtual IP for a set of Pods

A Service gives a stable DNS name and ClusterIP that load-balances across all Pods matching its selector.

```yaml
apiVersion: v1
kind: Service
metadata: { name: api }
spec:
  type: ClusterIP                  # default
  selector: { app: api }           # matches Pods with label app=api
  ports:
    - name: http
      port: 80                     # the port the Service exposes
      targetPort: 8000             # the port on the Pod
      protocol: TCP
```

Other Pods reach this Service at:
```
http://api                                  # same namespace
http://api.ml-services                      # cross-namespace (short)
http://api.ml-services.svc.cluster.local    # fully qualified
```

#### The four Service types

| Type | Use case |
|---|---|
| **ClusterIP** (default) | In-cluster only. The most common type. |
| **NodePort** | Exposes the Service on every node's IP at a static port (30000–32767). Rarely used in production directly — Ingress is better. |
| **LoadBalancer** | Provisions an external load balancer (in AWS: an ALB or NLB via the AWS Load Balancer Controller). |
| **ExternalName** | DNS CNAME to an external hostname. No proxying. Used to alias external services. |

#### Headless Service (the fifth option)

`clusterIP: None`. No virtual IP, no load balancing. DNS returns Pod IPs directly. Used by StatefulSets so each Pod is individually addressable.

```yaml
apiVersion: v1
kind: Service
metadata: { name: elasticsearch }
spec:
  clusterIP: None                # makes it headless
  selector: { app: elasticsearch }
  ports: [ { port: 9200 } ]
```

DNS for headless service:
- `elasticsearch.ml-services.svc.cluster.local` → A records for ALL pod IPs
- `elasticsearch-0.elasticsearch.ml-services.svc.cluster.local` → just Pod 0

#### Endpoints — the Service's actual targets

A Service has a corresponding `Endpoints` object listing the Pod IPs it's currently routing to. **If `Endpoints` is empty, the Service has no Pods — that's usually a selector mismatch.**

```bash
kubectl get svc api
kubectl get endpoints api          # short: ep
kubectl describe endpoints api
```

The single most useful debugging step when a Service "isn't working": check Endpoints. Empty = selector wrong, or no Pods are Ready (readinessProbe failing).

### 6.3 Ingress — HTTP routing into the cluster

A Service of type LoadBalancer creates one LB per service — expensive at scale. **Ingress** lets one LB front many services, routing by host/path.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: instance       # RKE2 + Calico: use 'instance', NOT 'ip'
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS":443}]'
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:ap-south-1:...
    alb.ingress.kubernetes.io/healthcheck-path: /healthz
spec:
  rules:
    - host: api.cashify.in
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api
                port: { number: 80 }
```

> **CNI compatibility note:** `target-type: ip` requires Pods to have routable VPC IPs (AWS VPC CNI on EKS). On RKE2 with Calico/Canal (your default), Pod IPs are inside the cluster's overlay and not directly reachable from an ALB — you must use `target-type: instance`, which requires the backing Service to be of type `NodePort`. If you genuinely need `ip` mode (lower latency, no extra NodePort hop), the alternatives are Cilium with VPC native routing or the TargetGroupBinding custom resource with explicit IPs.

#### Ingress Controller — the engine

An Ingress object is just config. **A controller has to read it and program a real load balancer.** Common choices:
- **AWS Load Balancer Controller** — provisions/configures ALBs (your stack)
- **ingress-nginx** — runs nginx as a Deployment behind a Service
- **Traefik**, **HAProxy Ingress**, **Contour** — alternatives

The annotations are controller-specific. `alb.ingress.kubernetes.io/*` only works if you have the AWS LB Controller installed.

#### IngressGroup (AWS-specific)

Multiple Ingress resources can share a single ALB:
```yaml
annotations:
  alb.ingress.kubernetes.io/group.name: prod-shared-alb
  alb.ingress.kubernetes.io/group.order: '10'
```
Saves ALB cost. Watch for rule-priority conflicts.

### 6.4 DNS — CoreDNS

Every cluster runs CoreDNS (a Deployment in `kube-system`). It serves the `cluster.local` zone.

Resolution order for a Pod (controlled by `/etc/resolv.conf` inside the Pod):
```
search ml-services.svc.cluster.local svc.cluster.local cluster.local
nameserver 10.43.0.10
options ndots:5
```

The `ndots:5` is a trap — any name with fewer than 5 dots gets each `search` suffix tried first. So `api` and `api.ml-services` work, but `api.cashify.in` (3 dots) gets `api.cashify.in.ml-services.svc.cluster.local` tried first, then falls back. **Fully-qualified external lookups can be slow.** Fix: trailing dot (`api.cashify.in.`) or `dnsConfig` overrides.

Debug DNS:
```bash
kubectl run -it --rm dnsutils --image=registry.k8s.io/e2e-test-images/jessie-dnsutils:1.3 -- sh
# inside:
nslookup api
nslookup api.ml-services.svc.cluster.local
dig +search api
```

### 6.5 CNI (Container Network Interface)

The plugin that gives Pods their IPs and wires up the routing. RKE2 ships with **Canal** (Calico + Flannel) by default. Common alternatives:
- **Calico** — most popular, supports NetworkPolicy
- **Cilium** — eBPF-based, fast, includes observability (Hubble) and L7 policies
- **Flannel** — simple, no NetworkPolicy support
- **AWS VPC CNI** — Pods get real VPC IPs (used by EKS)

You usually don't change CNI after cluster creation. Confirm what you have:
```bash
kubectl get pods -n kube-system | grep -iE 'calico|cilium|flannel|canal'
```

### 6.6 NetworkPolicy — Pod-level firewalls

By default, **all Pods can talk to all Pods**. NetworkPolicy lets you restrict that. Requires a CNI that supports it (Calico/Cilium yes, Flannel no).

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-allow
  namespace: ml-services
spec:
  podSelector: { matchLabels: { app: api } }
  policyTypes: [ Ingress, Egress ]
  ingress:
    - from:
        - podSelector: { matchLabels: { app: web } }
        - namespaceSelector: { matchLabels: { name: monitoring } }
      ports:
        - { protocol: TCP, port: 8000 }
  egress:
    - to:
        - podSelector: { matchLabels: { app: postgres } }
      ports: [ { protocol: TCP, port: 5432 } ]
    - to:                                # allow DNS to CoreDNS
        - namespaceSelector: { matchLabels: { kubernetes.io/metadata.name: kube-system } }
      ports: [ { protocol: UDP, port: 53 } ]
```

**Critical:** the moment you create ANY NetworkPolicy targeting a Pod, that Pod is **default-deny** for the direction(s) listed in `policyTypes`. Always explicitly allow DNS in egress or your apps break with weird DNS timeouts.

---

## 7. Storage

Containers are ephemeral. For anything that needs to survive a Pod restart, you need a volume backed by real storage.

### 7.1 The three objects: PV, PVC, StorageClass

```
StorageClass (cluster-level template)
     ↓ used by
PersistentVolumeClaim (PVC — the request)  ←→  bound to  ←→  PersistentVolume (PV — the actual storage)
     ↓ mounted into
Pod
```

**StorageClass (SC)** — defines *how* storage is dynamically provisioned. "When someone asks for gp3, here's the provisioner and parameters."

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata: { name: gp3 }
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  encrypted: "true"
  fsType: ext4
volumeBindingMode: WaitForFirstConsumer   # wait until a Pod schedules, then provision in the right AZ
reclaimPolicy: Delete                     # or Retain
allowVolumeExpansion: true
```

`volumeBindingMode: WaitForFirstConsumer` is essential on AWS — without it, the PV gets created in a random AZ and Pods that need to be in *that* AZ get stuck Pending.

**PersistentVolumeClaim (PVC)** — what a Pod asks for.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata: { name: api-data, namespace: ml-services }
spec:
  accessModes: [ ReadWriteOnce ]
  storageClassName: gp3
  resources:
    requests: { storage: 50Gi }
```

**PersistentVolume (PV)** — the actual storage. Usually you don't write these by hand — the CSI provisioner creates them when a PVC is created.

```bash
kubectl get pvc -n ml-services
kubectl get pv
kubectl describe pvc api-data
```

### 7.2 Access modes

| Mode | Meaning | Common backend |
|---|---|---|
| `ReadWriteOnce` (RWO) | Mounted RW by one node at a time | EBS |
| `ReadOnlyMany` (ROX) | Mounted RO by many nodes | EFS, S3-CSI |
| `ReadWriteMany` (RWX) | Mounted RW by many nodes | EFS, FSx |
| `ReadWriteOncePod` (RWOP) | Mounted RW by only one Pod (k8s 1.27+) | EBS (rare) |

EBS = RWO only. If you need shared storage across Pods, use EFS.

### 7.3 CSI (Container Storage Interface) — the plugin layer

The actual driver that talks to AWS. Two key CSI drivers for your stack:

- **aws-ebs-csi-driver** — for EBS volumes (most workloads)
- **aws-efs-csi-driver** — for shared filesystems

```bash
kubectl get csidrivers
kubectl get pods -n kube-system | grep csi
```

Each CSI driver has a **controller** (provisions/attaches volumes via AWS API) and a **node plugin** DaemonSet (mounts volumes inside Pods).

### 7.4 Mounting in a Pod

```yaml
spec:
  containers:
    - name: api
      image: api:0.1
      volumeMounts:
        - name: data
          mountPath: /var/data
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: api-data
```

### 7.5 Other volume types (not persistent)

```yaml
volumes:
  - name: cache
    emptyDir: {}                       # ephemeral, gone with the Pod
  - name: cache-mem
    emptyDir: { medium: Memory, sizeLimit: 100Mi }   # tmpfs
  - name: config
    configMap: { name: app-config }    # mount a ConfigMap as files
  - name: secret-files
    secret: { secretName: app-secret } # mount a Secret as files
  - name: downward
    downwardAPI:                       # expose Pod metadata as files
      items:
        - { path: "labels", fieldRef: { fieldPath: metadata.labels } }
```

`emptyDir` is the workhorse for scratch space — shared between containers in the same Pod.

### 7.6 Volume expansion

If the SC has `allowVolumeExpansion: true`, you can grow a PVC online:

```bash
kubectl edit pvc api-data
# change resources.requests.storage from 50Gi to 100Gi
# CSI driver expands the EBS volume + resizes the filesystem
```

Shrinking is **not** supported.

### 7.7 Common PVC failure modes

| Symptom | Cause | Fix |
|---|---|---|
| PVC stuck `Pending`, "waiting for first consumer" | SC has `WaitForFirstConsumer`; no Pod has tried to mount yet | Schedule a Pod that uses it |
| PVC `Pending`, "no available SC" | `storageClassName` typo, or default SC not set | Fix name; `kubectl get sc` to confirm |
| Pod Pending, "volume node affinity conflict" | PV is in AZ-a, Pod scheduled to AZ-b | Use `WaitForFirstConsumer` SC; or topology spread |
| PVC bound but Pod stuck `ContainerCreating`, "failed to attach" | EBS attach limit hit on node, or AZ mismatch | Reschedule Pod; check node's `Attachable Volumes` |

---

## 8. Configuration & Secrets

Don't bake config into images. Use ConfigMaps and Secrets.

### 8.1 ConfigMap

For non-sensitive config: log levels, feature flags, URLs.

```yaml
apiVersion: v1
kind: ConfigMap
metadata: { name: api-config, namespace: ml-services }
data:
  LOG_LEVEL: info
  MAX_WORKERS: "8"
  config.yaml: |
    server:
      port: 8000
      timeout: 30s
```

Two ways to consume in a Pod:

**As environment variables:**
```yaml
spec:
  containers:
    - name: api
      envFrom:
        - configMapRef: { name: api-config }     # all keys as env vars
      # OR pick specific keys:
      env:
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: api-config
              key: LOG_LEVEL
```

**As mounted files:**
```yaml
spec:
  containers:
    - name: api
      volumeMounts:
        - { name: config, mountPath: /etc/app, readOnly: true }
  volumes:
    - name: config
      configMap:
        name: api-config
        items:
          - { key: config.yaml, path: config.yaml }
```

**Important:** ConfigMaps mounted as volumes **update live** (kubelet refreshes within ~60s). ConfigMaps used as env vars **do not** — env vars are set at Pod start. To pick up new values, restart the Pod (`kubectl rollout restart deployment/api`).

### 8.2 Secret

Same shape as ConfigMap, but values are base64-encoded and intended for sensitive data.

```yaml
apiVersion: v1
kind: Secret
metadata: { name: db-creds, namespace: ml-services }
type: Opaque
data:
  username: cG9zdGdyZXM=                # base64("postgres")
  password: c2VjcmV0MTIz                # base64("secret123")
# OR use stringData (k8s does base64 for you):
stringData:
  username: postgres
  password: secret123
```

**Base64 is NOT encryption.** Anyone with `get secrets` RBAC can decode it instantly:
```bash
kubectl get secret db-creds -o jsonpath='{.data.password}' | base64 -d
```

#### What "secure" actually means with Secrets

1. **RBAC** restricts who can read them
2. **Encryption at rest** — etcd encrypts Secret values on disk (configure with EncryptionConfiguration; RKE2 enables this by default for newer versions, verify)
3. **External Secrets** — for real secret management, use:
   - **External Secrets Operator** (ESO) — syncs from AWS Secrets Manager / Parameter Store / Vault into k8s Secrets
   - **Secrets Store CSI Driver** — mounts directly from Secrets Manager without creating a k8s Secret

#### Secret types

| Type | Used for |
|---|---|
| `Opaque` | Generic data |
| `kubernetes.io/dockerconfigjson` | Image pull secrets (private registry auth) |
| `kubernetes.io/tls` | TLS cert + key |
| `kubernetes.io/service-account-token` | (Auto-created) for ServiceAccount tokens |
| `kubernetes.io/basic-auth` | username + password |
| `kubernetes.io/ssh-auth` | SSH private key |

#### Image pull secrets

For pulling from a private registry that doesn't use IRSA-style auth (IRSA for ECR is covered in Section 11):

```bash
kubectl create secret docker-registry ecr-creds \
  --docker-server=<acct>.dkr.ecr.ap-south-1.amazonaws.com \
  --docker-username=AWS \
  --docker-password="$(aws ecr get-login-password --region ap-south-1)" \
  -n ml-services
```

Then reference in Pod:
```yaml
spec:
  imagePullSecrets:
    - name: ecr-creds
```

**Better approach for ECR**: use **IRSA** (covered in Section 11) so Pods authenticate via IAM Role instead of a static Secret. The Secret expires every 12h; IRSA doesn't.

### 8.3 Common config patterns

**Pattern 1: app reads config from env vars**
- Put non-secrets in a ConfigMap → `envFrom`
- Put secrets in a Secret → `envFrom`
- Rollout restart on changes

**Pattern 2: app reads a config file**
- Put the file content in a ConfigMap with `data.config.yaml: |`
- Mount as a volume at the path the app expects
- Live updates (~60s lag)

**Pattern 3: external secret manager**
- Define an `ExternalSecret` resource (ESO) pointing to AWS Secrets Manager
- ESO creates and refreshes a k8s Secret automatically
- Pod consumes the Secret normally

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata: { name: db-creds, namespace: ml-services }
spec:
  refreshInterval: 1h
  secretStoreRef: { name: aws-secrets, kind: ClusterSecretStore }
  target: { name: db-creds }
  data:
    - secretKey: password
      remoteRef: { key: prod/api/db, property: password }
```

This is the pattern to adopt for production — secrets stay in AWS Secrets Manager, k8s Pods never see static long-lived credentials.

---

## 9. Scheduling & Placement

Where Pods land on Nodes is governed by a chain of mechanisms: **nodeSelector → nodeAffinity → taints/tolerations → topology spread → resource fit**. The scheduler runs through all of them. Knowing them is the difference between "Pods land where you want" and "Pods are Pending and you don't know why."

### 9.1 nodeSelector — simple label-match

The simplest form: "schedule this Pod only on Nodes with these labels."

```yaml
spec:
  nodeSelector:
    cashify.in/lifecycle: on-demand
    kubernetes.io/arch: arm64
```

Pod will only schedule on a Node that has **both** labels. No flexibility — if no such Node exists, Pod stays Pending.

```bash
# See which Nodes match
kubectl get nodes -l cashify.in/lifecycle=on-demand,kubernetes.io/arch=arm64
```

### 9.2 nodeAffinity — expressive node selection

Same idea as nodeSelector but with operators and preferences.

```yaml
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:     # hard rule
        nodeSelectorTerms:
          - matchExpressions:
              - key: cashify.in/lifecycle
                operator: In
                values: [on-demand]
              - key: node.kubernetes.io/instance-type
                operator: In
                values: [r8g.xlarge, r8g.2xlarge]
      preferredDuringSchedulingIgnoredDuringExecution:    # soft preference
        - weight: 100
          preference:
            matchExpressions:
              - key: topology.kubernetes.io/zone
                operator: In
                values: [ap-south-1a]
```

**Required vs Preferred:**
- `required...` → Pod won't schedule if no match. Stays Pending.
- `preferred...` → scheduler tries to match; if it can't, schedules elsewhere. Weight 1–100 ranks competing preferences.

**`IgnoredDuringExecution` (the second half of the field name):** affinity is only checked at scheduling time. If the Node's labels change later, running Pods are NOT evicted. (`RequiredDuringExecution` doesn't exist yet — it's reserved for future use.)

### 9.3 podAffinity / podAntiAffinity — schedule relative to other Pods

"Run this Pod near (or far from) other Pods matching a label."

**Anti-affinity is the more common case** — spreading replicas across nodes/zones for HA.

```yaml
spec:
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        - labelSelector:
            matchLabels: { app: api }
          topologyKey: kubernetes.io/hostname          # one Pod per node
```

`topologyKey` says "the unit we're spreading across":
- `kubernetes.io/hostname` → one per Node
- `topology.kubernetes.io/zone` → one per AZ
- `topology.kubernetes.io/region` → one per Region

**Anti-affinity is expensive at scale** — scheduling becomes O(N²) over Pods. For >100 replicas, prefer topology spread (next section).

### 9.4 Topology Spread Constraints — modern, cheap HA spreading

The modern way to spread replicas across zones/nodes. Cheaper than anti-affinity and more expressive.

```yaml
spec:
  topologySpreadConstraints:
    - maxSkew: 1
      topologyKey: topology.kubernetes.io/zone
      whenUnsatisfiable: DoNotSchedule        # or ScheduleAnyway
      labelSelector:
        matchLabels: { app: api }
    - maxSkew: 1
      topologyKey: kubernetes.io/hostname
      whenUnsatisfiable: ScheduleAnyway
      labelSelector:
        matchLabels: { app: api }
```

**`maxSkew: 1`** means the difference between the most-loaded and least-loaded zone (or node) is at most 1 Pod. With 6 replicas across 3 AZs → 2/2/2. With 7 → 3/2/2.

**`whenUnsatisfiable`:**
- `DoNotSchedule` → Pod stays Pending if constraint can't be met
- `ScheduleAnyway` → schedule wherever, just try to spread

**Stack pattern for production:**
- Zone spread: `DoNotSchedule` (HA matters — don't put all 3 in one AZ)
- Node spread: `ScheduleAnyway` (preferred but don't fail if nodes are saturated)

### 9.5 Taints & Tolerations — Nodes reject Pods by default

**Taints are the inverse of nodeSelector.** A taint on a Node says "don't schedule Pods here unless they explicitly tolerate this taint."

Three taint effects:
| Effect | Meaning |
|---|---|
| `NoSchedule` | Don't schedule new Pods here unless tolerated |
| `PreferNoSchedule` | Try to avoid scheduling here (soft) |
| `NoExecute` | Don't schedule + evict existing Pods that don't tolerate |

**Real-world example — your spot vs on-demand pattern:**

Taint spot nodes:
```bash
kubectl taint nodes <spot-node> cashify.in/lifecycle=spot:NoSchedule
```

Now nothing schedules there. For workloads that ARE OK with spot, add a toleration:
```yaml
spec:
  tolerations:
    - key: cashify.in/lifecycle
      operator: Equal
      value: spot
      effect: NoSchedule
  nodeSelector:
    cashify.in/lifecycle: spot         # actively prefer spot
```

The toleration **permits** scheduling on spot nodes; the nodeSelector **forces** it. You usually need both.

**Common built-in taints to know:**
```
node.kubernetes.io/not-ready:NoExecute            # added when Node goes NotReady
node.kubernetes.io/unreachable:NoExecute          # added when Node disconnects
node.kubernetes.io/disk-pressure:NoSchedule
node.kubernetes.io/memory-pressure:NoSchedule
node.kubernetes.io/pid-pressure:NoSchedule
node.kubernetes.io/network-unavailable:NoSchedule
node.kubernetes.io/unschedulable:NoSchedule       # set by `kubectl cordon`
```

`kubectl describe node <node> | grep Taints` to see what's set.

### 9.6 PodDisruptionBudget (PDB) — the spot-node lifesaver

A PDB tells Kubernetes: "**no matter what voluntary disruption happens, at least N pods must stay Ready.**"

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata: { name: api-pdb, namespace: ml-services }
spec:
  minAvailable: 2                      # OR: maxUnavailable: 1
  selector:
    matchLabels: { app: api }
```

**Voluntary disruption** = anything initiated by an operator/controller:
- `kubectl drain <node>` (during upgrades)
- Karpenter consolidating or replacing nodes
- Cluster Autoscaler scaling down
- Node group rolling update

**NOT covered:** involuntary disruptions like spot interruption, kernel panic, network failure. PDB can't save you from those.

**Why this is critical with Karpenter + spot:** Karpenter drains nodes to consolidate. Without a PDB, it could drain all your `api` Pods at once. With a PDB of `minAvailable: 2`, Karpenter is forced to wait for replacement Pods to be Ready before draining the next one.

```bash
kubectl get pdb -A
kubectl describe pdb api-pdb           # shows current disruptions allowed
```

If `DISRUPTIONS ALLOWED: 0` and you're trying to drain a node, the drain hangs until Pods are healthy elsewhere.

### 9.7 Stack pattern — ML services on RKE2 with Karpenter

Putting it together. An ML inference Pod that should run on Graviton on-demand nodes for stability:

```yaml
spec:
  nodeSelector:
    cashify.in/lifecycle: on-demand
    kubernetes.io/arch: arm64
  tolerations:
    - key: cashify.in/lifecycle
      operator: Equal
      value: on-demand
      effect: NoSchedule                # only if on-demand nodes are tainted
  topologySpreadConstraints:
    - maxSkew: 1
      topologyKey: topology.kubernetes.io/zone
      whenUnsatisfiable: ScheduleAnyway
      labelSelector:
        matchLabels: { app: ttl-pdd }
  affinity:
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 100
          podAffinityTerm:
            labelSelector:
              matchLabels: { app: ttl-pdd }
            topologyKey: kubernetes.io/hostname
```

Plus a PDB:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata: { name: ttl-pdd, namespace: ml-services }
spec:
  minAvailable: 1                       # at least 1 must stay Ready during disruption
  selector:
    matchLabels: { app: ttl-pdd }
```

---

## 10. Scaling

Three knobs: how many Pods (HPA), how big each Pod (VPA), how many Nodes (Karpenter/Cluster Autoscaler).

### 10.1 HPA — Horizontal Pod Autoscaler

Scales Pod **count** based on metrics. Requires `metrics-server` (RKE2 ships with it).

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: { name: api, namespace: ml-services }
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target: { type: Utilization, averageUtilization: 70 }
    - type: Resource
      resource:
        name: memory
        target: { type: Utilization, averageUtilization: 80 }
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300     # wait 5 min before scaling down
      policies:
        - type: Percent
          value: 50
          periodSeconds: 60               # max 50% reduction per minute
    scaleUp:
      stabilizationWindowSeconds: 0       # scale up immediately
      policies:
        - type: Percent
          value: 100
          periodSeconds: 30
        - type: Pods
          value: 4
          periodSeconds: 30
```

**Daily commands:**
```bash
kubectl get hpa -A
kubectl describe hpa api               # current/target/desired replicas
kubectl get hpa api -o yaml            # full config
```

**Common HPA pitfalls:**
- HPA scales on average across Pods. If one Pod is hot and others idle, average stays low → no scale.
- HPA needs **resource requests set** on Pods to calculate Utilization. No requests → HPA can't act.
- Flapping (scale up, scale down, repeat) → tune `behavior.stabilizationWindowSeconds`.
- Custom metrics (queue depth, RPS) need an adapter like **prometheus-adapter** or **KEDA** (KEDA is more common for event-driven scaling).

**KEDA** (Kubernetes Event-Driven Autoscaling) is worth knowing — it scales on external metrics (SQS depth, Kafka lag, ClickHouse query, Mixpanel events) and can scale to **zero** Pods, which HPA can't.

### 10.2 VPA — Vertical Pod Autoscaler

Adjusts Pod **size** (CPU/memory requests) based on observed usage. Three modes:

| Mode | Behavior |
|---|---|
| `Off` | Only generates recommendations (read with `kubectl describe vpa`) |
| `Initial` | Sets requests at Pod creation only |
| `Auto` | Evicts and recreates Pods with new requests (disruption!) |

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata: { name: api-vpa }
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  updatePolicy:
    updateMode: Off                    # safest — recommend only
```

**Critical:** **don't run HPA on CPU/memory and VPA on the same metric at the same time** — they fight. Either:
- HPA on a custom metric (RPS) + VPA on CPU/memory, OR
- HPA on resource + VPA in `Off` mode for sizing guidance

For most workloads: start with VPA in `Off` mode, look at recommendations after a week, set the requests manually, then turn VPA off. Auto-mode VPA in production is risky.

### 10.3 Cluster Autoscaler (CA) — the older approach

CA watches for Pending Pods and asks AWS Auto Scaling Groups to add Nodes. Works at the ASG level — slow, ASG-bound, limited diversity.

**For your stack:** you've moved past this. Karpenter is faster, more flexible, and cheaper. CA is mentioned for context only.

### 10.4 Karpenter — what you actually use

Karpenter directly provisions EC2 instances based on Pod requirements. No ASGs, no node groups. It looks at Pending Pods, picks the cheapest instance type that fits, launches it, and registers it with the cluster — usually in <60 seconds.

**Two CRDs to know:**

#### NodePool — the high-level intent

```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
metadata: { name: spot-arm64 }
spec:
  template:
    metadata:
      labels:
        cashify.in/lifecycle: spot
        kubernetes.io/arch: arm64
    spec:
      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: [spot]
        - key: kubernetes.io/arch
          operator: In
          values: [arm64]
        - key: karpenter.k8s.aws/instance-family
          operator: In
          values: [r8g, c8g, m8g]            # Graviton4
        - key: karpenter.k8s.aws/instance-size
          operator: In
          values: [large, xlarge, 2xlarge, 4xlarge]
        - key: topology.kubernetes.io/zone
          operator: In
          values: [ap-south-1a, ap-south-1b, ap-south-1c]
      nodeClassRef:
        group: karpenter.k8s.aws
        kind: EC2NodeClass
        name: default
      taints:
        - key: cashify.in/lifecycle
          value: spot
          effect: NoSchedule
      expireAfter: 720h                     # recycle after 30 days
  disruption:
    consolidationPolicy: WhenEmptyOrUnderutilized
    consolidateAfter: 30s
    budgets:
      - nodes: "10%"                        # max 10% of nodes disrupted at once
  limits:
    cpu: "1000"
    memory: 4000Gi
```

#### EC2NodeClass — the AWS-specific bits

```yaml
apiVersion: karpenter.k8s.aws/v1
kind: EC2NodeClass
metadata: { name: default }
spec:
  amiFamily: AL2023                       # Amazon Linux 2023
  amiSelectorTerms:
    - alias: al2023@latest
  role: KarpenterNodeRole-prod-rke2       # IAM role (or use instanceProfile)
  subnetSelectorTerms:
    - tags: { karpenter.sh/discovery: prod-rke2 }
  securityGroupSelectorTerms:
    - tags: { karpenter.sh/discovery: prod-rke2 }
  blockDeviceMappings:
    - deviceName: /dev/xvda
      ebs:
        volumeSize: 100Gi
        volumeType: gp3
        encrypted: true
  metadataOptions:
    httpTokens: required                  # IMDSv2 only
    httpPutResponseHopLimit: 2
  userData: |
    #!/bin/bash
    # any custom boot scripts
```

#### Consolidation & Drift — the two disruption mechanisms

**Consolidation** = Karpenter actively replaces or removes nodes for efficiency:
- `WhenEmpty` → only remove a Node when no Pods on it
- `WhenEmptyOrUnderutilized` → also replace when a smaller/cheaper Node would fit

**Drift** = Karpenter sees a Node no longer matches the current NodePool spec (e.g., AMI updated, requirements changed) → marks Node as drifted → schedules replacement.

Both respect PDBs and disruption budgets.

#### Daily Karpenter commands

```bash
kubectl get nodepool
kubectl get ec2nodeclass
kubectl get nodeclaim                                              # in-flight node provisioning
kubectl describe nodeclaim <name>                                  # why a Node was created
kubectl get nodes -L karpenter.sh/nodepool,karpenter.sh/capacity-type,node.kubernetes.io/instance-type

# Karpenter controller logs (where the action is)
kubectl logs -n kube-system -l app.kubernetes.io/name=karpenter --tail=200 -f

# Common events to look for
kubectl get events -A --field-selector reason=DisruptionLaunching
kubectl get events -A --field-selector reason=DisruptionTerminating
kubectl get events -A --field-selector reason=Drifted
```

#### Karpenter troubleshooting

**"Pod is Pending forever, Karpenter not creating a Node":**
```bash
# 1. Does any NodePool match the Pod's requirements?
kubectl describe pod <pod>                       # see scheduling failures
kubectl logs -n kube-system -l app.kubernetes.io/name=karpenter --tail=200 | grep -i "<pod>"

# 2. Are there instance types matching the spec but exhausted in AWS?
# Karpenter logs will say "InsufficientInstanceCapacity" if AWS has none

# 3. Is the NodePool at its limit?
kubectl get nodepool <name> -o jsonpath='{.status}'
```

**"Spot Pods keep getting killed":** that's spot interruption. Mitigations:
- Lower-priority workloads on spot (batch, async)
- PDB with `minAvailable` ensures replacement before next disruption
- Multi-instance-family NodePool reduces interruption probability (more pools to draw from)

---

## 11. Security: RBAC, ServiceAccounts, IRSA, Pod Security

### 11.1 RBAC mental model

RBAC controls "**who** can do **what** on **which resources**." Four objects:

```
Subject (user, group, ServiceAccount)
   ↓
RoleBinding / ClusterRoleBinding (the link)
   ↓
Role (namespaced) / ClusterRole (cluster-scoped)
   ↓
permissions: verbs on resources
```

| Object | Scope |
|---|---|
| `Role` | Namespaced — permissions inside one namespace |
| `ClusterRole` | Cluster-wide — can also be reused inside namespaces via RoleBinding |
| `RoleBinding` | Binds a subject to a Role (or ClusterRole) within a namespace |
| `ClusterRoleBinding` | Binds a subject to a ClusterRole cluster-wide |

#### Example — read-only access to one namespace for the ML team

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata: { name: ml-readonly, namespace: ml-services }
rules:
  - apiGroups: [""]
    resources: [pods, services, configmaps, persistentvolumeclaims]
    verbs: [get, list, watch]
  - apiGroups: ["apps"]
    resources: [deployments, statefulsets, daemonsets]
    verbs: [get, list, watch]
  - apiGroups: [""]
    resources: [pods/log]
    verbs: [get, list]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata: { name: ml-team-readonly, namespace: ml-services }
subjects:
  - kind: Group
    name: ml-team                              # however your auth surfaces groups
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: ml-readonly
  apiGroup: rbac.authorization.k8s.io
```

#### Daily RBAC commands

```bash
kubectl auth can-i <verb> <resource> [--as <user>] [-n <ns>]    # the most useful one
kubectl auth can-i delete pods -n ml-services
kubectl auth can-i create deployments -n ml-services --as=jane@cashify.in
kubectl auth can-i '*' '*' --as=system:serviceaccount:ml-services:api
kubectl auth can-i --list -n ml-services       # everything I can do here

# Inspect bindings
kubectl get role,rolebinding -n ml-services
kubectl get clusterrole,clusterrolebinding
kubectl describe clusterrolebinding cluster-admin
```

**Common verbs:** `get`, `list`, `watch`, `create`, `update`, `patch`, `delete`, `deletecollection`. Pseudo-verbs: `impersonate`, `bind`, `escalate`.

**Wildcard `*` warning:** `verbs: ["*"]` grants future verbs too. Avoid in production roles.

### 11.2 ServiceAccount — Pod's identity

Every Pod runs as a ServiceAccount. If unspecified, it gets the `default` SA of its namespace. The SA's token is mounted into the Pod, used to authenticate to the API server.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata: { name: api, namespace: ml-services }
automountServiceAccountToken: true             # default is true
---
apiVersion: v1
kind: Pod
metadata: { name: api }
spec:
  serviceAccountName: api                      # the SA this Pod runs as
```

**Don't grant permissions to the `default` SA** — that grants them to every Pod in the namespace that didn't specify one. Always create per-app SAs.

For Pods that don't need to talk to the API at all:
```yaml
spec:
  serviceAccountName: api
  automountServiceAccountToken: false          # prevent token mount
```

### 11.3 IRSA — IAM Roles for Service Accounts

The connection between Kubernetes identity and AWS IAM. This is how your Pods get scoped AWS API access without static credentials.

**Why it exists:** Before IRSA, you either gave Node-level IAM permissions (every Pod on the Node inherited them — too broad) or stuffed long-lived AWS access keys into Secrets (rotation pain, audit nightmare).

**How it works (high level):**
1. EKS/RKE2 cluster exposes an **OIDC** provider
2. AWS IAM trusts that OIDC provider
3. A k8s ServiceAccount is annotated with an IAM Role ARN
4. The Pod gets a projected, short-lived OIDC token
5. AWS SDK in the Pod uses that token to AssumeRoleWithWebIdentity → temporary credentials

> ⚠ **RKE2 reality check (verified):** **EKS Pod Identity (the simpler 2023+ alternative to IRSA) does NOT work on RKE2** — it depends on the EKS API and the `eks-pod-identity-agent` add-on, both of which are EKS-only. On RKE2, you have to use **self-hosted IRSA** with the pod-identity-webhook. Two common setup paths:

**Path A — Self-hosted IRSA with pod-identity-webhook** (the standard RKE2 approach):
1. Generate an RSA key pair for the OIDC provider
2. Configure the RKE2 kube-apiserver to use it (`--service-account-issuer`, `--service-account-signing-key-file`, `--service-account-key-file`, `--api-audiences=sts.amazonaws.com`) via `/etc/rancher/rke2/config.yaml`
3. Host the OIDC discovery doc and JWKS publicly (S3 + CloudFront is the most common)
4. Register that URL as an IAM OIDC identity provider in AWS
5. Install the `pod-identity-webhook` into the cluster (handles env var injection into Pods)
6. Annotate ServiceAccounts with the IAM Role ARN

The reference implementation that walks through all of this is at `github.com/chaospuppy/irsa-demo` (RKE2-specific). For local-dev / k3d, see `github.com/mjnagel/k3d-irsa`.

**Path B — Stick with imagePullSecrets + per-app Secrets pulled from AWS Secrets Manager via External Secrets Operator.** Less elegant but no OIDC setup required. Often the practical choice if your team doesn't have an IAM admin available to register OIDC providers.

#### IRSA setup steps (one-time per cluster, Path A)

1. **Confirm the cluster's OIDC issuer URL is configured:**
```bash
kubectl get --raw /.well-known/openid-configuration | jq .issuer
# If this fails or returns the wrong URL, the kube-apiserver flags aren't set yet
```

2. **Make the OIDC discovery doc + JWKS publicly readable** (S3 + CloudFront):
```bash
kubectl get --raw /.well-known/openid-configuration > openid-configuration
kubectl get --raw /openid/v1/jwks > jwks
aws s3 cp openid-configuration s3://<bucket>/.well-known/openid-configuration
aws s3 cp jwks s3://<bucket>/openid/v1/jwks
# Front with CloudFront; ensure HTTPS and correct Content-Type
```

3. **Register as an IAM OIDC identity provider:**
```bash
aws iam create-open-id-connect-provider \
  --url https://oidc.prod-rke2.cashify.in \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list <cert-thumbprint>
```

4. **Install the AWS Pod Identity Webhook** (or the EKS Pod Identity Agent) into your cluster.

#### Per-app IRSA usage

**IAM Role trust policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Federated": "arn:aws:iam::<acct>:oidc-provider/oidc.prod-rke2.cashify.in" },
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {
        "oidc.prod-rke2.cashify.in:sub": "system:serviceaccount:ml-services:api",
        "oidc.prod-rke2.cashify.in:aud": "sts.amazonaws.com"
      }
    }
  }]
}
```

**ServiceAccount with IRSA annotation:**
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: api
  namespace: ml-services
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::<acct>:role/api-prod-rke2
```

**Pod just uses the SA:**
```yaml
spec:
  serviceAccountName: api
  # Pod Identity Webhook auto-injects AWS_ROLE_ARN, AWS_WEB_IDENTITY_TOKEN_FILE
  # AWS SDK detects them and uses AssumeRoleWithWebIdentity automatically.
```

**Verify inside the Pod:**
```bash
kubectl exec -it <pod> -- env | grep AWS
kubectl exec -it <pod> -- aws sts get-caller-identity   # if aws cli available
```

#### IRSA for ECR pulls — eliminates the 12h token refresh

Standard ECR pull pattern uses an `imagePullSecrets` that expires every 12h (CI refreshes it). **With IRSA on the Node-level kubelet** (not the Pod's SA — different mechanism), ECR auth is automatic and continuous.

For RKE2 nodes pulling from ECR:
1. Give the **Node IAM Role** the `AmazonEC2ContainerRegistryReadOnly` policy
2. RKE2's kubelet uses the Node's instance profile to auth to ECR
3. `imagePullSecrets` no longer needed for ECR images
4. Reference images directly: `<acct>.dkr.ecr.ap-south-1.amazonaws.com/api:0.1`

**For Pod-level AWS access** (S3, Secrets Manager, DynamoDB), use IRSA via SA annotation as above.

### 11.4 Pod Security Standards (PSS)

Replaced the deprecated PodSecurityPolicy. Three levels enforced by the built-in `PodSecurity` admission controller:

| Level | What's allowed |
|---|---|
| `privileged` | Everything (no restrictions) |
| `baseline` | Minimal restrictions — blocks obvious privilege escalations (hostNetwork, privileged containers, hostPID, etc.) |
| `restricted` | Locked down — runs non-root, drops all capabilities, no privilege escalation, seccomp = RuntimeDefault |

Enforced **per namespace** via labels:

```bash
kubectl label namespace ml-services \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/audit=restricted \
  pod-security.kubernetes.io/warn=restricted
```

Three modes:
- `enforce` → block Pods that violate
- `audit` → allow but log to audit log
- `warn` → allow but return a warning to the API caller

**Stack pattern:** `enforce=baseline` on most namespaces; `enforce=restricted` on namespaces holding sensitive workloads (auth services, secret-handling); `enforce=privileged` reluctantly on `kube-system` where some components need it.

**Pod spec to pass `restricted`:**
```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 65532
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: api
      image: api:0.1
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop: ["ALL"]
```

---

## 12. Packaging & Deployment — Helm, Kustomize, Operators

Hand-rolling YAML for every environment is unsustainable. Two main tools solve this: **Helm** (templating + release management) and **Kustomize** (overlay-based, no templating). They're complementary, not competing.

### 12.1 Helm — the de-facto k8s package manager

Helm packages a set of related manifests as a **chart**. You install a chart with values to create a **release**. Releases are tracked in cluster state, so you can upgrade and roll back.

**Mental model:**
```
Chart  (templates + default values.yaml)
   ↓ install with custom values
Release  (named instance of a chart, tracked in cluster)
   ↓ rendered manifests
Kubernetes resources
```

#### Chart anatomy

```
my-chart/
├── Chart.yaml              # metadata (name, version, appVersion, dependencies)
├── values.yaml             # default values (the "schema" of what's overridable)
├── values.schema.json      # optional JSON schema to validate values
├── templates/
│   ├── deployment.yaml     # Go template with {{ .Values.xxx }} substitutions
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── _helpers.tpl        # template fragments reused across files
│   └── NOTES.txt           # printed after install
├── charts/                 # subchart dependencies
└── crds/                   # CRDs installed before templates
```

#### Daily Helm commands

```bash
# Repos
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm search repo nginx                           # find charts

# Install / upgrade
helm install <release> <chart> -n <ns> --create-namespace -f values.yaml
helm install api ./my-chart -n ml-services -f prod-values.yaml
helm upgrade <release> <chart> -n <ns> -f values.yaml
helm upgrade --install <release> <chart> -n <ns> -f values.yaml   # idempotent install/upgrade

# Inspect
helm list -A                                     # all releases everywhere
helm list -n <ns>
helm status <release> -n <ns>
helm get values <release> -n <ns>                # the values used
helm get manifest <release> -n <ns>              # the rendered YAML
helm get all <release> -n <ns>

# History & rollback
helm history <release> -n <ns>
helm rollback <release> <revision> -n <ns>

# Uninstall
helm uninstall <release> -n <ns>
helm uninstall <release> -n <ns> --keep-history  # for audit
```

#### Critical practices

**1. `--install` flag for idempotent deploys (the CI pattern):**
```bash
helm upgrade --install api ./my-chart -n ml-services \
  -f base-values.yaml -f prod-values.yaml \
  --set image.tag=$BUILD_NUMBER \
  --wait --timeout=10m
```
`--wait` blocks until all resources are Ready. `--timeout` caps the wait.

**2. Multiple `-f` files compose** — later overrides earlier. Standard pattern:
```bash
helm upgrade --install api ./chart \
  -f values.yaml \                # chart defaults
  -f environments/prod.yaml \     # env overrides
  -f overrides/incident-1234.yaml # temporary override (last)
```

**3. Render-only mode for diff / dry-run:**
```bash
helm template <release> <chart> -f values.yaml > rendered.yaml
helm install --dry-run --debug <release> <chart> -f values.yaml
```

**4. `helm diff` plugin** (essential, install separately):
```bash
helm plugin install https://github.com/databus23/helm-diff
helm diff upgrade <release> <chart> -f values.yaml
```
Shows exactly what will change before you upgrade. The single most useful Helm plugin.

#### Hooks — lifecycle events

```yaml
metadata:
  annotations:
    "helm.sh/hook": pre-install,pre-upgrade
    "helm.sh/hook-weight": "1"
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
```

Common hooks: `pre-install`, `post-install`, `pre-upgrade`, `post-upgrade`, `pre-delete`, `post-delete`, `pre-rollback`, `post-rollback`, `test`.

Typical use: a `pre-upgrade` Job to run database migrations, gate the upgrade on its success.

#### Stack patterns

- **Charts your stack likely uses:** `kube-prometheus-stack`, `aws-load-balancer-controller`, `external-secrets`, `cert-manager`, `karpenter`, `metrics-server`, `velero`. Most are maintained by their projects and follow standard conventions.
- **Per-app charts:** keep one chart per service, with environment-specific values in version control (`values.yaml`, `values-stage.yaml`, `values-prod.yaml`).

### 12.2 Kustomize — overlay-based, no templating

Kustomize takes a base set of manifests and applies **patches** to produce environment-specific outputs. No Go templates. Built into `kubectl` since 1.14.

**Mental model:** start with a `base/` directory of vanilla YAML. Each environment has an `overlays/<env>/` directory with a `kustomization.yaml` that lists patches/additions on top of base.

```
my-app/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
└── overlays/
    ├── stage/
    │   ├── kustomization.yaml
    │   └── patch-replicas.yaml
    ├── beta/
    │   ├── kustomization.yaml
    │   └── patch-resources.yaml
    └── prod/
        ├── kustomization.yaml
        ├── patch-replicas.yaml
        ├── patch-resources.yaml
        └── extra-pdb.yaml
```

**Base `kustomization.yaml`:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml
  - service.yaml
  - configmap.yaml
commonLabels:
  app: api
namespace: ml-services
```

**Overlay `overlays/prod/kustomization.yaml`:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../base
  - extra-pdb.yaml
patches:
  - path: patch-replicas.yaml
  - path: patch-resources.yaml
images:
  - name: api
    newName: <acct>.dkr.ecr.ap-south-1.amazonaws.com/api
    newTag: 1.2.3
configMapGenerator:
  - name: api-config
    behavior: merge
    literals:
      - LOG_LEVEL=warn
      - ENV=prod
```

**Patch file (`patch-replicas.yaml`):**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 10
```

#### Daily Kustomize commands

```bash
# Render to stdout
kubectl kustomize ./overlays/prod
kustomize build ./overlays/prod

# Apply directly
kubectl apply -k ./overlays/prod
kubectl delete -k ./overlays/prod

# Diff before apply
kubectl diff -k ./overlays/prod
```

#### Helm vs Kustomize — when to use which

| Use Helm when | Use Kustomize when |
|---|---|
| You're consuming a third-party chart | You're writing manifests for your own apps |
| You need release tracking + rollback | You manage rollbacks via Git |
| Logic / templating is needed | You want plain YAML with overlays |
| You're packaging for redistribution | You're customizing per environment |

**Most teams use both:** Helm for installing operators/infra (cert-manager, prometheus-stack, karpenter), Kustomize for their own application manifests. Or Helm + post-render Kustomize.

### 12.3 CRDs and Operators

#### Custom Resource Definition (CRD) = your own API type

A CRD extends the Kubernetes API. Once installed, the API server understands a new `kind` (e.g., `Certificate`, `Prometheus`, `Elasticsearch`).

```bash
kubectl get crds                                 # all custom resources installed
kubectl api-resources --api-group=cert-manager.io
kubectl explain certificate.spec                 # works for CRDs too
```

#### The Operator pattern

An operator is a controller that watches a CRD and reconciles the actual state to match the spec — exactly like built-in controllers but for domain-specific resources.

```
You create: kind: Elasticsearch, replicas: 3, version: 8.18.2
   ↓
ECK Operator sees the CR
   ↓
Operator creates: StatefulSet, Service, Secret, ConfigMap, etc.
   ↓
Operator continuously reconciles: handles version upgrades, scaling, certs
```

#### Operators useful in your stack

| Operator | What it manages | CRD examples |
|---|---|---|
| **prometheus-operator** (kube-prometheus-stack) | Prometheus + Alertmanager + scrape configs | `Prometheus`, `ServiceMonitor`, `PrometheusRule` |
| **ECK** (Elastic Cloud on Kubernetes) | Elasticsearch + Kibana + APM | `Elasticsearch`, `Kibana` |
| **cert-manager** | TLS certificates (Let's Encrypt, ACM, internal CA) | `Certificate`, `Issuer`, `ClusterIssuer` |
| **External Secrets Operator (ESO)** | Sync from AWS Secrets Manager, Vault, etc. | `ExternalSecret`, `SecretStore` |
| **Karpenter** | Node provisioning | `NodePool`, `EC2NodeClass`, `NodeClaim` |
| **AWS Load Balancer Controller** | ALB/NLB lifecycle | `TargetGroupBinding` |
| **Strimzi** | Kafka clusters | `Kafka`, `KafkaTopic`, `KafkaUser` |
| **Velero** | Backup / restore | `Backup`, `Restore`, `Schedule` |

#### Reading operator logs (the #1 troubleshooting move)

When a CR isn't doing what you expected, the answer is almost always in the operator's logs:

```bash
# General pattern
kubectl logs -n <operator-ns> -l <operator-label> --tail=200

# Examples
kubectl logs -n kube-system -l app.kubernetes.io/name=karpenter --tail=200
kubectl logs -n elastic-system -l control-plane=elastic-operator --tail=200
kubectl logs -n cert-manager -l app=cert-manager --tail=200
kubectl logs -n external-secrets -l app.kubernetes.io/name=external-secrets --tail=200
```

The CR's `status` field also surfaces operator decisions — always check:
```bash
kubectl get <kind> <name> -o yaml | yq '.status'
kubectl describe <kind> <name>          # events too
```

---

## 13. Observability — Logs, Metrics, Events, Debugging

The four pillars of "what's actually happening": **Events**, **Logs**, **Metrics**, **Traces**. K8s gives you the first three out of the box; tracing is application-layer.

### 13.1 Events — Kubernetes' built-in audit trail

Every state change in the cluster generates Events. They're stored in etcd and (by default) garbage-collected after 1 hour. They are the single most useful debugging signal.

```bash
# Cluster-wide, most recent first
kubectl get events -A --sort-by=.lastTimestamp | tail -30

# Watch in real time
kubectl get events -A -w

# Only warnings
kubectl get events -A --field-selector type=Warning

# Events for a specific Pod
kubectl describe pod <pod>                       # Events section at the bottom
kubectl get events --field-selector involvedObject.name=<pod-name>

# Events related to a specific reason
kubectl get events -A --field-selector reason=Failed
kubectl get events -A --field-selector reason=OOMKilling
kubectl get events -A --field-selector reason=BackOff
kubectl get events -A --field-selector reason=FailedScheduling
kubectl get events -A --field-selector reason=Unhealthy
```

**Common event reasons you'll see:**

| Reason | Means |
|---|---|
| `Scheduled` | Scheduler picked a Node |
| `Pulling` / `Pulled` | Image pull lifecycle |
| `Created` / `Started` | Container lifecycle |
| `Failed` | Container exited with error |
| `BackOff` | Restart backoff (CrashLoopBackOff or ImagePullBackOff) |
| `Unhealthy` | Probe failure |
| `Killing` | Container being killed (e.g., for a new rollout) |
| `OOMKilling` | Container killed for memory |
| `FailedScheduling` | Scheduler can't find a Node |
| `FailedMount` / `FailedAttachVolume` | Storage problem |
| `EvictionThresholdMet` / `Evicted` | Node pressure |
| `NodeNotReady` / `NodeReady` | Node condition transitions |

**Pro tip — extend event retention.** Default is 1 hour, which is short for post-incident analysis. Either:
- Bump the kube-apiserver `--event-ttl` flag (RKE2: in `/etc/rancher/rke2/config.yaml`)
- Ship events to long-term storage with `eventrouter`, `kubernetes-event-exporter`, or `Falco sidekick`

### 13.2 Logs at scale — fluent-bit/fluentd to Elasticsearch (your stack)

`kubectl logs` is fine for one Pod. For production, you ship every container's stdout/stderr to a central store.

**Architecture (your stack):**
```
Container stdout/stderr
   ↓ written by containerd to /var/log/pods/<pod>/<container>/0.log
fluent-bit DaemonSet on every Node
   ↓ tail + parse + enrich (add pod labels, namespace, node)
Elasticsearch (your 3-node r8g log-cluster, ES 8.18.2)
   ↓ index per data stream
Kibana
   ↓ visual / search
```

**Fluent-bit DaemonSet skeleton:**
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata: { name: fluent-bit, namespace: logging }
spec:
  selector: { matchLabels: { app: fluent-bit } }
  template:
    metadata: { labels: { app: fluent-bit } }
    spec:
      tolerations:
        - operator: Exists                                  # run on every Node incl. tainted
      serviceAccountName: fluent-bit
      containers:
        - name: fluent-bit
          image: fluent/fluent-bit:3.0
          volumeMounts:
            - { name: varlog, mountPath: /var/log, readOnly: true }
            - { name: varlibdockercontainers, mountPath: /var/lib/containerd/containers, readOnly: true }
            - { name: config, mountPath: /fluent-bit/etc }
      volumes:
        - { name: varlog, hostPath: { path: /var/log } }
        - { name: varlibdockercontainers, hostPath: { path: /var/lib/containerd/containers } }
        - { name: config, configMap: { name: fluent-bit-config } }
```

**Index naming pattern (matches your existing data streams):**
- `<env>-fluentd-proxy-*` (e.g., `prod-fluentd-proxy-2026-05-22`)
- `<env>-config-sync-*`
- `<env>-app-*`, `<env>-nginx-*`
- `node-appserver-*`, `ttl-pdd-*`

These are **data streams** (since ES 7.9+) which is what your three ILM policies cover.

#### Daily log troubleshooting

```bash
# When central logs are missing for a Pod
kubectl get pods -n logging -l app=fluent-bit -o wide        # is fluent-bit running on the Pod's Node?
kubectl logs -n logging <fluent-bit-pod> --tail=200          # fluent-bit's own logs

# What's on the Node's disk?
kubectl debug node/<node> -it --image=busybox
chroot /host
ls /var/log/pods/<namespace>_<pod-name>_<uid>/<container>/
tail -f /var/log/pods/<namespace>_<pod-name>_<uid>/<container>/0.log
```

### 13.3 Metrics — Prometheus stack

Standard k8s observability stack:

```
node-exporter (DaemonSet)    → CPU, memory, disk, network on every Node
kube-state-metrics            → metrics about k8s objects (Deployment replicas, Pod phase, etc.)
cAdvisor                      → built into kubelet, exposes container metrics
        ↓
Prometheus (scrapes)
        ↓
Alertmanager (routes alerts) + Grafana (dashboards)
```

**Install via Helm:**
```bash
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace \
  -f prom-values.yaml
```

The stack installs the **prometheus-operator** which provides CRDs:
- `Prometheus` — the Prometheus server config
- `ServiceMonitor` — tells Prometheus to scrape a Service's pods
- `PodMonitor` — scrape Pods directly (no Service)
- `PrometheusRule` — alerting and recording rules
- `Alertmanager` — alertmanager config

**Add a scrape target for your app:**
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: api
  namespace: ml-services
  labels: { release: kube-prometheus-stack }     # must match Prometheus selector
spec:
  selector:
    matchLabels: { app: api }
  endpoints:
    - port: metrics                              # the Service port name
      path: /metrics
      interval: 30s
```

#### Useful PromQL queries for daily SRE

```promql
# Pods restarting in last hour
sum by (namespace, pod) (increase(kube_pod_container_status_restarts_total[1h])) > 0

# Memory usage vs limit per Pod (where you're close to OOMKill)
sum by (namespace, pod) (container_memory_working_set_bytes{container!=""}) /
sum by (namespace, pod) (kube_pod_container_resource_limits{resource="memory"}) > 0.8

# Node CPU saturation
1 - avg by (node) (rate(node_cpu_seconds_total{mode="idle"}[5m]))

# PVC fill percentage
(1 - kubelet_volume_stats_available_bytes / kubelet_volume_stats_capacity_bytes) * 100

# HPA scaling decisions over time
kube_horizontalpodautoscaler_status_current_replicas
```

#### kubectl top — quick CPU/memory snapshots

Requires `metrics-server` (RKE2 ships with it). Fast, no Prometheus needed.

```bash
kubectl top nodes --sort-by=cpu
kubectl top pods -A --sort-by=memory | head -20
kubectl top pods --containers -n ml-services
```

### 13.4 kubectl debug — modern debugging

For Pods you can't `kubectl exec` into (distroless / scratch images with no shell).

```bash
# Add a debug container into a running Pod, sharing PID + network namespace
kubectl debug -it <pod> --image=busybox --target=<container>

# Same, but with full debugging toolkit
kubectl debug -it <pod> --image=nicolaka/netshoot --target=<container>

# Create a copy of a Pod with the debug image (original stays untouched)
kubectl debug <pod> -it --image=busybox --copy-to=debug-<pod> --share-processes

# Debug a Node (gets you a Pod that has the host's filesystem mounted at /host)
kubectl debug node/<node-name> -it --image=busybox
# then: chroot /host  to be effectively "on" the node
```

**`nicolaka/netshoot`** is the go-to debug image — has dig, curl, tcpdump, nslookup, ngrep, iptables, ss, mtr, ipvsadm, all the network tooling.

### 13.5 The triage muscle — what to check, in order

When a service is degraded, check in this order:

1. **Events** — `kubectl get events -n <ns> --sort-by=.lastTimestamp | tail -20`
2. **Pod status** — `kubectl get pods -l <selector>` + `kubectl describe`
3. **Logs** — `kubectl logs <pod> --previous` then current
4. **Endpoints** — `kubectl get ep <svc>` (is Service routing?)
5. **Resource usage** — `kubectl top pod <pod> --containers`
6. **Recent changes** — `helm history` / `kubectl rollout history`
7. **Operator logs** — if a CR-managed resource, the operator's logs

The order matters. Don't jump to logs before checking Events — Events often tell you instantly what's wrong (`ImagePullBackOff: unauthorized`, `FailedScheduling: insufficient memory`).

---

## 14. Production Troubleshooting

This is the runbook. For each common failure mode: **symptoms → first checks → likely cause → fix.**

### 14.1 CrashLoopBackOff

**Symptoms:** Pod status shows `CrashLoopBackOff`. Restart count climbing.

**First checks:**
```bash
kubectl describe pod <pod>                                     # Events section
kubectl logs <pod> --previous                                  # crashed container's logs (CRITICAL)
kubectl get pod <pod> -o jsonpath='{.status.containerStatuses[0].lastState.terminated}'
```

**Likely causes (in order of frequency):**
1. **App crashing on startup** — config wrong, missing env var, can't reach dependency. Read `--previous` logs.
2. **OOMKilled** — `lastState.terminated.reason=OOMKilled`, exit 137. Raise memory limit or fix leak.
3. **Liveness probe too aggressive on slow-start** — add `startupProbe`.
4. **Wrong CMD/ENTRYPOINT** — exit 127 (command not found) or 126 (not executable). Check image.
5. **Permission denied** — running as non-root but writing to root-owned dirs. Fix Dockerfile or `securityContext`.

**Fix flow:**
```bash
# 1. Read previous logs
kubectl logs <pod> --previous --tail=200

# 2. If it's a config issue, exec into a healthy version (or a debug container) to inspect
kubectl debug -it <pod> --image=busybox --target=<container>

# 3. If OOM, raise limits OR profile memory
kubectl patch deployment <name> -p '{"spec":{"template":{"spec":{"containers":[{"name":"<c>","resources":{"limits":{"memory":"1Gi"}}}]}}}}'
```

### 14.2 ImagePullBackOff / ErrImagePull

**Symptoms:** Pod stuck in `ImagePullBackOff` or `ErrImagePull`.

**First checks:**
```bash
kubectl describe pod <pod>                                     # Events show pull errors clearly
kubectl get pod <pod> -o jsonpath='{.spec.containers[*].image}'
```

**Likely causes:**
1. **Image doesn't exist** — typo in tag/name. Verify in ECR/registry.
2. **Auth failure** — `unauthorized` or `no basic auth credentials`. Missing `imagePullSecrets`, or Node IAM role doesn't have ECR read permission.
3. **Wrong region** — image in `us-east-1`, cluster pulls from `ap-south-1`.
4. **Private registry not in `registries.yaml`** (RKE2-specific) — check `/etc/rancher/rke2/registries.yaml` on Nodes.
5. **Network/DNS** — Nodes can't resolve registry hostname.
6. **Architecture mismatch** — amd64 image on arm64 Nodes. Error: `no matching manifest for linux/arm64`.

**Fix flow:**
```bash
# Verify image exists
aws ecr describe-images --repository-name <repo> --image-ids imageTag=<tag> --region ap-south-1

# Verify Node can pull (SSH to a Node, or use a debug Pod with crictl)
kubectl debug node/<node> -it --image=busybox
chroot /host
crictl pull <full-image-url>                                   # see the real error

# Check Node IAM role has ECR perms
aws iam list-attached-role-policies --role-name <node-role>

# Check multi-arch manifest
docker buildx imagetools inspect <full-image-url>
```

### 14.3 OOMKilled

**Symptoms:** Container exits with code 137. `lastState.terminated.reason=OOMKilled`. Often as part of CrashLoopBackOff cycle.

**First checks:**
```bash
kubectl get pod <pod> -o jsonpath='{.status.containerStatuses[0].lastState.terminated}'
kubectl describe pod <pod>                                     # Events show OOMKilling
kubectl top pod <pod> --containers                             # current usage
kubectl get events -A --field-selector reason=OOMKilling
```

**Likely causes:**
1. **Limit set too low** — workload genuinely needs more memory than allowed.
2. **Memory leak** — usage grows over time. Profile with `kubectl top` over time.
3. **JVM/runtime not container-aware** — JVM allocating heap based on host memory (~Node) ignoring cgroup. Use `-XX:+UseContainerSupport` (Java 10+ default).
4. **Burst load** — limit fine for steady state, blown by traffic spike.

**Fix flow:**
```bash
# Short-term: raise limit
kubectl set resources deployment/<name> --limits=memory=1Gi --requests=memory=512Mi

# Long-term: profile, find leak, set requests==limits for Guaranteed QoS on critical workloads
```

**Important:** OOMKill at the **container** level (your app over its limit) is different from OOMKill at the **Node** level (Node ran out of memory entirely → kernel kills processes, possibly including non-Pod processes). Both show exit 137. Check `dmesg` on the Node for kernel-level OOMs.

### 14.4 Pending Pods

**Symptoms:** Pod stuck in `Pending` phase. No Node assigned.

**First checks:**
```bash
kubectl describe pod <pod>                                     # Events section is the answer 99% of the time
kubectl get pods --field-selector=status.phase=Pending -A
```

**Likely causes:**

| Event message | Cause | Fix |
|---|---|---|
| `0/N nodes available: insufficient cpu/memory` | No Node has enough resources | Wait for Karpenter; scale up; reduce requests |
| `0/N nodes are available: N node(s) had untolerated taint {...}` | Node tainted, Pod has no toleration | Add toleration matching the taint |
| `0/N nodes available: N node(s) didn't match Pod's node affinity/selector` | nodeSelector/nodeAffinity doesn't match any Node | Fix the selector or label a Node |
| `0/N nodes available: N node(s) didn't find available persistent volumes to bind` | PVC can't bind | See PVC Pending below |
| `0/N nodes available: pod has unbound immediate PersistentVolumeClaims` | Storage class is `Immediate`-bind but no PV available | Check SC, CSI driver, AZ |
| (No event, just Pending) | Karpenter spinning up a Node | Check Karpenter logs; usually <60s |

**Fix flow:**
```bash
# What's actually preventing scheduling?
kubectl describe pod <pod> | grep -A 20 Events:

# If Karpenter should be creating a Node, look at its decision
kubectl get nodeclaim
kubectl logs -n kube-system -l app.kubernetes.io/name=karpenter --tail=200 | grep -i <pod-name>

# If it's resource pressure, what's claimed where?
kubectl describe nodes | grep -A 5 "Allocated resources"
```

### 14.5 PVC Stuck Pending

**Symptoms:** PVC in `Pending` state; Pods using it can't start.

**First checks:**
```bash
kubectl describe pvc <pvc>                                     # Events
kubectl get sc                                                 # is the storageclassName valid?
kubectl get pv | grep <pvc-name>                               # any PV available?
```

**Likely causes:**
1. **`WaitForFirstConsumer` SC, no Pod scheduled yet** — normal. PVC binds when a Pod tries to mount. Not a bug.
2. **No matching SC** — typo in `storageClassName`, or no default SC and `storageClassName` blank.
3. **CSI driver not running** — `kubectl get pods -n kube-system | grep csi`. Check controller and node Pods.
4. **AZ mismatch** — existing PV in AZ-a, but `WaitForFirstConsumer` not used and Pod scheduled to AZ-b.
5. **Quota exceeded** — namespace `ResourceQuota` on storage limits hit.

**Fix flow:**
```bash
# CSI driver check
kubectl get pods -n kube-system -l app=ebs-csi-controller
kubectl logs -n kube-system -l app=ebs-csi-controller -c csi-provisioner --tail=100

# Force binding by scheduling a Pod (WaitForFirstConsumer is normal)
# OR: change SC to Immediate (rare; usually wrong)
```

### 14.6 Service Has No Endpoints (the silent killer)

**Symptoms:** Service exists but traffic doesn't reach Pods. Clients get connection refused / timeouts. Pod logs look fine.

**First check (this is THE check):**
```bash
kubectl get endpoints <svc>
# If EMPTY → no Pods are matched OR no matched Pod is Ready
```

**Likely causes:**
1. **Selector mismatch** — Service's selector doesn't match Pods' labels.
2. **No Pods Ready** — readinessProbe failing on all Pods.
3. **Pods in wrong namespace** — Service in `ml-services` selects on labels that match Pods in `default`.
4. **targetPort wrong** — Service points to port 8080, app listens on 8000.

**Fix flow:**
```bash
# Compare Service selector vs Pod labels
kubectl get svc <svc> -o jsonpath='{.spec.selector}'
kubectl get pods -l <selector-from-above> --show-labels

# Check readiness
kubectl get pods -l <selector> -o wide                        # READY column

# Check targetPort vs container port
kubectl get svc <svc> -o jsonpath='{.spec.ports}'
kubectl get pod <pod> -o jsonpath='{.spec.containers[*].ports}'
```

### 14.7 DNS Failures

**Symptoms:** Apps log `connection refused` or `no such host` for in-cluster services. Intermittent timeouts. External hostnames resolve slowly.

**First checks:**
```bash
# Spin up a test Pod
kubectl run -it --rm dnsutils --image=registry.k8s.io/e2e-test-images/jessie-dnsutils:1.3 -- sh
# Inside:
nslookup kubernetes.default                                    # core check
nslookup <some-app>.<ns>.svc.cluster.local
cat /etc/resolv.conf                                           # nameserver + search

# Outside:
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns --tail=100
kubectl top pods -n kube-system -l k8s-app=kube-dns           # CoreDNS overloaded?
```

**Likely causes:**
1. **CoreDNS pod(s) down or unhealthy** — restart, scale up.
2. **CoreDNS overloaded** — high QPS, throttled. Scale up CoreDNS replicas + add NodeLocal DNSCache.
3. **`ndots:5` slowness on external lookups** — each `search` suffix tried first. Use FQDN with trailing dot, or override `dnsConfig`.
4. **NetworkPolicy blocking DNS** — Pod has restrictive egress NetPol but didn't allow UDP 53 to kube-system.
5. **Node DNS misconfigured** — Node itself can't resolve upstream. Check `/etc/resolv.conf` on Node.

### 14.8 Ingress Not Routing

**Symptoms:** External request to your domain returns 404, 503, or "default backend". DNS resolves, TLS handshakes, but no traffic to Pods.

**First checks:**
```bash
kubectl get ingress <name>                                     # ADDRESS should be the ALB
kubectl describe ingress <name>                                # Events + rules
kubectl get ep <backend-svc>                                   # backend Service has Endpoints?

# AWS LB Controller logs
kubectl logs -n kube-system -l app.kubernetes.io/name=aws-load-balancer-controller --tail=200
```

**Likely causes:**
1. **Backend Service has no Endpoints** (see 14.6).
2. **Ingress class not set / controller doesn't pick it up** — annotation `kubernetes.io/ingress.class: alb` or `spec.ingressClassName: alb` required.
3. **Wrong target type for your CNI** — see ⚠ note below. **On RKE2 with Calico/Canal CNI (your default), `target-type: ip` does NOT work.** Pod IPs from Calico aren't reachable from the ALB. Must use `target-type: instance`, which requires the backend Service to be `NodePort` (or `LoadBalancer` for NLB target groups). `target-type: ip` requires AWS VPC CNI (EKS-style).
4. **Certificate ARN missing/wrong** — TLS terminates at ALB; cert ARN must cover the host.
5. **Host header mismatch / 421** — covered earlier; SNI vs Host vs cert mismatch on shared ALBs.
6. **Health checks failing on target group** — Pods Ready but TG health check on wrong path. Check `alb.ingress.kubernetes.io/healthcheck-path`.
7. **IMDS hop limit too low** — RKE2 EC2 instances need `httpPutResponseHopLimit: 2` for the LB Controller Pod to reach IMDS via the Calico CNI. Default is 1 → controller silently fails to read instance metadata.
8. **Subnets not tagged for auto-discovery** — public subnets need `kubernetes.io/role/elb=1`; private subnets need `kubernetes.io/role/internal-elb=1`.

```bash
# Find the ALB target group from the Ingress
kubectl describe ingress <name> | grep -i 'arn:aws:elasticloadbalancing'
# Then check target health in AWS Console or via CLI
aws elbv2 describe-target-health --target-group-arn <tg-arn>
```

> ⚠ **Stack-specific reality check (verified for RKE2):** the standard EKS pattern of `target-type: ip` doesn't work on RKE2 + Calico. If your existing Ingresses use `ip` and work, you've either switched to a CNI that supports it (AWS VPC CNI, Cilium with VPC integration) or you're using TargetGroupBinding with manually-managed targets. Otherwise, default to `target-type: instance` and back the Service with NodePort.

### 14.9 Pod Stuck Terminating

**Symptoms:** Pod in `Terminating` state for minutes or hours. `kubectl delete` doesn't release it.

**First checks:**
```bash
kubectl describe pod <pod>
kubectl get pod <pod> -o jsonpath='{.metadata.finalizers}'
kubectl get pod <pod> -o jsonpath='{.spec.terminationGracePeriodSeconds}'
```

**Likely causes:**
1. **App ignoring SIGTERM** — long graceful period elapses before SIGKILL. Fix in app.
2. **Finalizers stuck** — a controller hasn't removed its finalizer. Check what added it.
3. **Volume detach hanging** — EBS detach failed (often when the Node is gone unexpectedly).
4. **Node NotReady** — Pod is on a Node that's gone; kubelet can't acknowledge termination.

**Fix flow:**
```bash
# Force delete (use sparingly — does NOT confirm cleanup with kubelet)
kubectl delete pod <pod> --grace-period=0 --force

# Remove a stuck finalizer
kubectl patch pod <pod> -p '{"metadata":{"finalizers":null}}'

# If volumes are stuck, may need to manually detach in AWS Console
```

### 14.10 Node Pressure (DiskPressure, MemoryPressure, PIDPressure)

**Symptoms:** Node condition shows `DiskPressure=True` or `MemoryPressure=True`. Pods getting evicted. New Pods stuck Pending.

**First checks:**
```bash
kubectl get nodes
kubectl describe node <node> | grep -A 5 Conditions
kubectl get events -A --field-selector reason=Evicted
kubectl get events -A --field-selector reason=NodeNotReady
```

**Likely causes:**

| Pressure | Cause | Fix |
|---|---|---|
| DiskPressure | `/var/lib/containerd` or `/var/log` full | Clean unused images on Node (`crictl rmi --prune`), increase disk |
| MemoryPressure | Sum of Pod usage > Node memory | Raise Node size; reduce overcommit; HPA |
| PIDPressure | Too many processes (forking app, missing pid limit) | Set `--pids-limit` on Pods |

**For your spot nodes with Karpenter:** node pressure usually triggers Karpenter to replace the Node — that's expected. The fix is to ensure PDBs and graceful eviction work.

**Imagine the worst case — DiskPressure on a control-plane Node:** etcd can degrade. Watch `kubectl get events -n kube-system` for warnings, and ensure your monitoring alerts on Node disk usage above 80%.

---

## 15. RKE2-Specific Operations

RKE2 (Rancher Kubernetes Engine 2) is your Kubernetes distribution. Most things work like upstream k8s, but a handful of operations are RKE2-specific. Knowing these saves hours of confusion.

### 15.1 Architecture: server vs agent nodes

RKE2 splits Node roles into:
- **server** — runs control plane components (kube-apiserver, etcd, scheduler, controller-manager) AND also runs workloads by default
- **agent** — runs only kubelet + kube-proxy + containerd; pure worker

For production: **3 server nodes** (HA control plane, etcd quorum) + many agent nodes.

```bash
# Service names (systemd)
systemctl status rke2-server      # on a server node
systemctl status rke2-agent       # on an agent node

# Logs
journalctl -u rke2-server -n 200 --no-pager
journalctl -u rke2-agent  -n 200 --no-pager

# Restart
systemctl restart rke2-server
systemctl restart rke2-agent
```

### 15.2 Configuration: `/etc/rancher/rke2/config.yaml`

This is where you configure RKE2 itself — TLS SANs, kube-apiserver flags, embedded registry mirrors, IRSA flags, etc.

**Example for a server node:**
```yaml
# /etc/rancher/rke2/config.yaml
node-name: prod-server-01
tls-san:
  - prod-rke2.cashify.internal
  - 10.0.1.100
cluster-cidr: 10.42.0.0/16
service-cidr: 10.43.0.0/16

# CIS hardening
profile: cis

# IRSA / OIDC flags (passed through to kube-apiserver)
kube-apiserver-arg:
  - service-account-issuer=https://oidc.prod-rke2.cashify.in
  - service-account-jwks-uri=https://oidc.prod-rke2.cashify.in/openid/v1/jwks
  - api-audiences=sts.amazonaws.com,kubernetes.svc.default

# Audit log
audit-policy-file: /etc/rancher/rke2/audit-policy.yaml

# Pre-pull images via registry mirror
write-kubeconfig-mode: "0640"
```

After editing: `systemctl restart rke2-server`.

### 15.3 Private registry config: `registries.yaml`

For pulling images from authenticated registries (private ECR, internal Harbor, etc.), configure containerd via `/etc/rancher/rke2/registries.yaml` **on every Node** (server and agent).

```yaml
# /etc/rancher/rke2/registries.yaml
mirrors:
  "<acct>.dkr.ecr.ap-south-1.amazonaws.com":
    endpoint:
      - "https://<acct>.dkr.ecr.ap-south-1.amazonaws.com"
  "docker.io":
    endpoint:
      - "https://<mirror>.dkr.ecr.ap-south-1.amazonaws.com"    # pull-through cache to dodge Hub rate limits
configs:
  "<acct>.dkr.ecr.ap-south-1.amazonaws.com":
    auth:
      # Option A: static creds (worst)
      username: AWS
      password: <12h-token>
      # Option B: leave blank, configure kubelet credential provider (best)
```

**The right way for ECR:** configure the **kubelet credential provider** so ECR auth happens automatically via the Node's IAM instance profile. RKE2 since 1.27 supports this:

```yaml
# /etc/rancher/rke2/credential-providers/ecr-credential-provider.yaml
apiVersion: kubelet.config.k8s.io/v1
kind: CredentialProviderConfig
providers:
  - name: ecr-credential-provider
    matchImages:
      - "*.dkr.ecr.*.amazonaws.com"
      - "*.dkr.ecr.*.amazonaws.com.cn"
    defaultCacheDuration: "12h"
    apiVersion: credentialprovider.kubelet.k8s.io/v1
```

Plus the binary deployed on each Node, plus kubelet flag `--image-credential-provider-config=...`. Once set up, you never need `imagePullSecrets` for ECR images.

After editing: `systemctl restart rke2-server` or `rke2-agent` on each Node.

### 15.4 Manifest auto-deploy: `/var/lib/rancher/rke2/server/manifests/`

Any YAML files placed here on a server node get **automatically applied** by RKE2 at startup and on change. This is how RKE2 deploys its own components (CoreDNS, ingress-nginx, metrics-server).

```bash
ls /var/lib/rancher/rke2/server/manifests/
# rke2-coredns.yaml
# rke2-ingress-nginx.yaml
# rke2-metrics-server.yaml
# rke2-canal.yaml
```

Use it to bootstrap critical add-ons that should be deployed before anything else (Karpenter, AWS LB Controller, ECK, ESO). These appear as `Addon` CRs:

```bash
kubectl get addon -A
```

⚠ **Caveat:** files in this directory are managed by RKE2. Deleting files does NOT remove the resources from the cluster — you need to `kubectl delete` them too. Edit-then-restart-rke2-server is the way.

### 15.5 Customizing packaged components — `HelmChartConfig`

RKE2 packages CoreDNS, ingress-nginx, etc. as Helm releases. To tweak their values without forking, drop a `HelmChartConfig` into the manifests dir:

```yaml
# /var/lib/rancher/rke2/server/manifests/rke2-coredns-config.yaml
apiVersion: helm.cattle.io/v1
kind: HelmChartConfig
metadata:
  name: rke2-coredns
  namespace: kube-system
spec:
  valuesContent: |-
    replicas: 3
    resources:
      requests: { cpu: 100m, memory: 128Mi }
      limits:   { memory: 256Mi }
```

Equivalent for ingress-nginx, metrics-server, etc.

### 15.6 Embedded etcd snapshots — built-in backup

RKE2 automatically snapshots etcd. **Default: every 12h, retain 5 snapshots, stored at `/var/lib/rancher/rke2/server/db/snapshots/` on each server node.**

```bash
# List existing snapshots
ls -lh /var/lib/rancher/rke2/server/db/snapshots/

# Take an on-demand snapshot
rke2 etcd-snapshot save --name pre-upgrade-snapshot

# Configure S3 upload for off-cluster storage (recommended for prod)
# In /etc/rancher/rke2/config.yaml on server nodes:
etcd-s3: true
etcd-s3-bucket: cashify-rke2-snapshots
etcd-s3-region: ap-south-1
etcd-s3-folder: prod
# (use IRSA or instance-profile credentials, NOT static keys)

etcd-snapshot-schedule-cron: "0 */6 * * *"     # every 6h
etcd-snapshot-retention: 10
```

### 15.7 Restore from etcd snapshot — the DR runbook

If etcd is corrupted or you need to roll back the entire cluster state:

```bash
# 1. Stop RKE2 on ALL server nodes
sudo systemctl stop rke2-server

# 2. On ONE server node, restore from snapshot
sudo rke2 server \
  --cluster-reset \
  --cluster-reset-restore-path=/var/lib/rancher/rke2/server/db/snapshots/<snapshot-name>

# 3. Once reset completes, start RKE2 on that node
sudo systemctl start rke2-server

# 4. On OTHER server nodes, remove old etcd data and rejoin
sudo systemctl stop rke2-server
sudo rm -rf /var/lib/rancher/rke2/server/db/etcd/
sudo systemctl start rke2-server
```

**⚠ This is destructive.** It rolls back ALL cluster state to the snapshot point. Workloads created since the snapshot are gone. Practice on a non-prod cluster first.

### 15.8 RKE2 upgrade workflow

Two methods: **manual** (per-Node) or via **System Upgrade Controller** (automated, rolling).

**Manual upgrade (good for understanding what's happening):**
```bash
# On each server node, one at a time:
curl -sfL https://get.rke2.io | INSTALL_RKE2_VERSION=v1.30.5+rke2r1 sh -
sudo systemctl restart rke2-server
# wait for the node to be Ready before moving to the next

# Then each agent node:
curl -sfL https://get.rke2.io | INSTALL_RKE2_VERSION=v1.30.5+rke2r1 sh -
sudo systemctl restart rke2-agent
```

**Automated via System Upgrade Controller (preferred for production):**
```yaml
apiVersion: upgrade.cattle.io/v1
kind: Plan
metadata: { name: server-plan, namespace: system-upgrade }
spec:
  concurrency: 1                                 # one server at a time
  cordon: true
  nodeSelector:
    matchExpressions:
      - { key: node-role.kubernetes.io/control-plane, operator: In, values: ["true"] }
  upgrade:
    image: rancher/rke2-upgrade
  version: v1.30.5+rke2r1
```

This drains and upgrades nodes serially, respecting PodDisruptionBudgets.

### 15.9 Useful RKE2 paths to remember

| Path | What's there |
|---|---|
| `/etc/rancher/rke2/config.yaml` | RKE2 configuration |
| `/etc/rancher/rke2/registries.yaml` | Container registry config |
| `/etc/rancher/rke2/credential-providers/` | Kubelet credential providers (ECR auth) |
| `/var/lib/rancher/rke2/server/manifests/` | Auto-deploy manifests |
| `/var/lib/rancher/rke2/server/db/snapshots/` | etcd snapshots |
| `/var/lib/rancher/rke2/server/tls/` | All cluster TLS certs |
| `/var/lib/rancher/rke2/agent/etc/containerd/` | containerd config |
| `/var/lib/rancher/rke2/bin/` | RKE2 binaries (kubectl, crictl, ctr) |
| `/etc/rancher/rke2/rke2.yaml` | The cluster's kubeconfig (on server nodes) |

### 15.10 `crictl` — the runtime-level debugger

When `kubectl` is broken or the kubelet itself is the problem, drop down to containerd via `crictl`:

```bash
export CONTAINER_RUNTIME_ENDPOINT=unix:///run/k3s/containerd/containerd.sock

crictl ps                                        # running containers
crictl ps -a                                     # all containers
crictl images                                    # local image cache
crictl pull <image>                              # test ECR pull from this Node
crictl logs <container-id>                       # logs (even when kubectl can't)
crictl inspect <container-id>
crictl rmi --prune                               # clean up unused images (DiskPressure fix)
```

This is what you reach for when: kubelet won't start, ImagePullBackOff on one specific Node, "is this Node even able to pull from ECR?", DiskPressure cleanup.

---

## 16. Backup, DR & Cluster Upgrades

### 16.1 What needs to be backed up

| Layer | What | Tool |
|---|---|---|
| **Cluster state (etcd)** | All k8s objects | RKE2 built-in etcd snapshots (§15.6) |
| **Workload definitions** | Manifests, Helm releases | Git (the source of truth) |
| **PV data** | Stateful workload data (Elasticsearch indices, Postgres data, etc.) | Velero with EBS snapshots OR app-level (ES snapshots to S3) |
| **Secrets** | App credentials | Source: AWS Secrets Manager (ESO syncs) |
| **Container images** | Built artifacts | ECR (cross-region replication for DR) |

**Critical insight:** **Git is your primary backup of cluster state.** etcd snapshots restore what was deployed, but if your manifests/charts are in Git, you can rebuild the cluster from scratch. Treat Git as source of truth, etcd as performance cache.

### 16.2 Velero — workload backup and restore

Velero backs up k8s objects + (optionally) PV data via CSI snapshots or restic/kopia file-level backups.

**Install (Helm):**
```bash
helm install velero vmware-tanzu/velero \
  --namespace velero --create-namespace \
  --set configuration.provider=aws \
  --set-file credentials.secretContents.cloud=./aws-credentials \
  --set configuration.backupStorageLocation.bucket=cashify-velero-prod \
  --set configuration.backupStorageLocation.config.region=ap-south-1 \
  --set configuration.volumeSnapshotLocation.config.region=ap-south-1 \
  --set initContainers[0].name=velero-plugin-for-aws \
  --set initContainers[0].image=velero/velero-plugin-for-aws:v1.10.0 \
  --set initContainers[0].volumeMounts[0].mountPath=/target \
  --set initContainers[0].volumeMounts[0].name=plugins
```

**Daily Velero commands:**
```bash
velero backup create prod-daily-$(date +%F) --include-namespaces ml-services
velero backup get
velero backup describe <backup-name> --details
velero backup logs <backup-name>

velero schedule create daily-prod --schedule="0 2 * * *" --include-namespaces=ml-services --ttl 720h0m0s
velero schedule get

velero restore create --from-backup <backup-name>
velero restore get
```

**Backup CR (declarative):**
```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata: { name: ml-services-daily, namespace: velero }
spec:
  schedule: "0 2 * * *"
  template:
    ttl: 720h0m0s                                # 30 days retention
    includedNamespaces:
      - ml-services
    snapshotVolumes: true
    storageLocation: default
```

### 16.3 Disaster recovery scenarios

**Scenario A: Single Pod / Deployment broken**
- Roll back via `kubectl rollout undo` or `helm rollback`
- No DR tooling needed

**Scenario B: Namespace contaminated**
- Velero restore from last good backup: `velero restore create --from-backup <name> --include-namespaces ml-services`

**Scenario C: etcd corruption / cluster API broken**
- Restore from RKE2 etcd snapshot (§15.7)
- Workloads come back as they were at snapshot time

**Scenario D: Entire cluster lost**
- Provision new cluster (Terraform/Pulumi)
- Apply Git-managed manifests (GitOps / Helm / Kustomize)
- Velero restore for PV data
- Estimated RTO: 2-4 hours if practiced; days if not

**The DR drill** — once a quarter, restore from backup into a sandbox cluster. If you've never tested restore, you don't have backups.

### 16.4 Upgrade strategy

Upgrade order — **always** in this direction:
1. **Backup first** (etcd snapshot + Velero of critical namespaces)
2. **Test in non-prod** (Stage cluster matches Prod minor version)
3. **Upgrade RKE2 control plane** (servers first, one at a time, §15.8)
4. **Upgrade RKE2 worker nodes** (drain-based, one at a time)
5. **Upgrade Karpenter** (CRDs first, then controller — see Karpenter v1 migration if going from v1beta1)
6. **Upgrade CNI** (Calico/Canal)
7. **Upgrade observability stack** (Prometheus, fluent-bit)
8. **Upgrade operators** (ESO, cert-manager, AWS LB Controller, ECK)
9. **Last: app charts** (Helm upgrades for your services)

Never skip more than one minor version at a time (k8s supports n-1, sometimes n-2). Plan upgrades quarterly.

---

## 17. kubectl Operator's Cheat Sheet

(Distinct from §3 which was for *learning* kubectl. This one is for *running* prod.)

```bash
# === TRIAGE ===
kubectl get pods -A --field-selector=status.phase!=Running
kubectl get pods -A -o json | jq -r '.items[] | select(.status.containerStatuses[]?.restartCount > 0) | "\(.metadata.namespace)/\(.metadata.name) restarts=\(.status.containerStatuses[0].restartCount)"' | head -20
kubectl get events -A --sort-by=.lastTimestamp | tail -30
kubectl get events -A --field-selector type=Warning --sort-by=.lastTimestamp | tail -20
kubectl describe pod <pod>                       # Events section is the answer 90% of the time
kubectl logs <pod> --previous                    # CrashLoopBackOff debug
kubectl logs <pod> --since=15m --tail=200 --timestamps
kubectl logs -l app=<label> --max-log-requests=10 --tail=200
kubectl top pods -A --sort-by=memory | head -20
kubectl top nodes --sort-by=cpu

# === STATE ===
kubectl get pod <pod> -o jsonpath='{.status.qosClass}'
kubectl get pod <pod> -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason}'
kubectl get pod <pod> -o jsonpath='{.status.containerStatuses[0].restartCount}'
kubectl get pod <pod> -o jsonpath='{.spec.nodeName}'
kubectl get endpoints <svc>                      # if empty, service is broken
kubectl get hpa -A
kubectl get pdb -A

# === NODES ===
kubectl get nodes -o wide
kubectl get nodes -L kubernetes.io/arch,karpenter.sh/capacity-type,karpenter.sh/nodepool,topology.kubernetes.io/zone
kubectl describe node <node> | grep -A 5 Conditions
kubectl describe node <node> | grep -A 20 'Allocated resources'
kubectl get pods -A -o wide --field-selector spec.nodeName=<node>
kubectl cordon <node>                            # mark unschedulable
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data --grace-period=120
kubectl uncordon <node>

# === SCHEDULING ===
kubectl get nodepool                             # Karpenter
kubectl get nodeclaim
kubectl logs -n kube-system -l app.kubernetes.io/name=karpenter --tail=200 -f
kubectl get pods --field-selector=status.phase=Pending -A

# === ROLLOUTS ===
kubectl rollout status deployment/<name> --timeout=5m
kubectl rollout history deployment/<name>
kubectl rollout undo deployment/<name>
kubectl rollout restart deployment/<name>        # bounce without image change

# === DEBUG ===
kubectl exec -it <pod> -- sh
kubectl debug -it <pod> --image=nicolaka/netshoot --target=<container>
kubectl debug node/<node> -it --image=busybox
kubectl port-forward svc/<svc> 8080:80
kubectl run -it --rm dnsutils --image=registry.k8s.io/e2e-test-images/jessie-dnsutils:1.3 -- sh

# === RBAC AUDIT ===
kubectl auth can-i <verb> <resource> --as=system:serviceaccount:<ns>:<sa>
kubectl auth can-i --list -n <ns> --as=jane@cashify.in

# === HELM ===
helm list -A
helm history <release> -n <ns>
helm rollback <release> <revision> -n <ns>
helm get values <release> -n <ns>
helm diff upgrade <release> <chart> -f values.yaml

# === BACKUP ===
velero backup get
velero backup describe <name> --details
rke2 etcd-snapshot save --name pre-change-$(date +%F)

# === RUNTIME (when kubelet/kubectl broken) ===
sudo systemctl status rke2-server                # or rke2-agent
sudo journalctl -u rke2-server -n 200 --no-pager
sudo crictl ps -a
sudo crictl logs <container-id>
sudo crictl rmi --prune                          # node DiskPressure fix
```

---

## 18. Docker → Kubernetes Mental Map (Full)

If you're solid on Docker (companion doc), here's how each concept lands in Kubernetes:

| Docker concept | Kubernetes equivalent | Notes |
|---|---|---|
| `docker run <image>` | Pod with one container | Pod is the smallest scheduling unit, not the container |
| Container | Container inside a Pod | Pods can have many containers sharing network + storage |
| `docker run -d --restart=always` | Deployment | Deployment manages a ReplicaSet which manages Pods |
| Stateful container with `-v` | StatefulSet + PVC | Each Pod gets stable identity + own PVC |
| `docker run` on every host | DaemonSet | log shippers, node exporters |
| `docker run --rm` (one-shot) | Job | Run-to-completion |
| Cron `docker run` | CronJob | Scheduled Jobs |
| `docker logs <name>` | `kubectl logs <pod>` | `--previous` for crashed container |
| `docker exec -it <name> sh` | `kubectl exec -it <pod> -- sh` | |
| `docker inspect <name>` | `kubectl describe pod <pod>` + `kubectl get pod <pod> -o yaml` | |
| `docker stop` | `kubectl delete pod` | But controller recreates it |
| Container restart policy | Deployment's reconciliation loop | "Always restart" is the default |
| `docker network create` + DNS | Service (ClusterIP) + CoreDNS | Services discover Pods by label |
| `-p 8080:80` (port publish) | Service + Ingress / LoadBalancer | Ingress = many services share one ALB |
| `--memory --cpus` | `resources.requests` / `resources.limits` | Drives QoS class + scheduling |
| `HEALTHCHECK` | `livenessProbe` / `readinessProbe` / `startupProbe` | Probes split the concerns |
| Named volume | PVC → PV | StorageClass dynamically provisions |
| `tmpfs` volume | `emptyDir: {medium: Memory}` | |
| `--env-file` | `envFrom: configMapRef` or `envFrom: secretRef` | |
| `docker compose up` | Helm install of a chart, or Kustomize apply | Compose's "stack" = a Helm release |
| `docker login` | `imagePullSecrets` (OR IRSA / kubelet credential provider for ECR) | IRSA = no static creds |
| `docker push` to registry | Same — k8s pulls images from your registry | |
| Multi-arch image | Same — Pod scheduler picks based on Node arch | Critical for Graviton |
| `docker events` | `kubectl get events --sort-by=.lastTimestamp` | Built-in audit trail |
| `docker stats` | `kubectl top` (needs metrics-server) | |
| Docker daemon config (`daemon.json`) | Many places: containerd config, kubelet config, RKE2 config.yaml | RKE2 wraps the others |

**The shifts in mindset:**

| Docker thinking | Kubernetes thinking |
|---|---|
| "I run a container" | "I declare desired state; controllers run containers" |
| "If it crashes, I restart it" | "Controllers continuously reconcile; deleting fixes" |
| "Container = one process" | "Pod = unit; can have multiple processes/sidecars" |
| "Network = bridge + DNS by container name" | "Network = flat Pod IP space + Services + CoreDNS" |
| "Volume = mount on host" | "Volume = abstraction over many backends (EBS, EFS, NFS, etc.)" |
| "Secrets = `-e VAR=value` (bad) or `--env-file`" | "Secrets = first-class object, RBAC-protected, encrypted at rest" |
| "Health = `HEALTHCHECK` instruction" | "Health = three probes with different actions" |
| "I check `docker ps`" | "I check `kubectl get pods` — but more often Events, Endpoints, and operator logs" |

If you have these mental connections — and the Docker fundamentals from the companion doc — you have a complete operational picture from `docker build` all the way to a multi-cluster K8s deployment with Karpenter, IRSA, observability, and DR.

---

## End of Sub-Pass 2b

All 18 sections now complete. Pass 2b added:
- **Section 12** — Helm (charts, hooks, daily commands, plugins) + Kustomize (overlays for stage/beta/prod) + CRDs + Operators (with the operators you actually use in your stack)
- **Section 13** — Events deep dive, log shipping pattern to your Elasticsearch cluster, Prometheus stack with PromQL queries, `kubectl debug`, the 7-step triage order
- **Section 15** — RKE2 server/agent architecture, `config.yaml`, `registries.yaml`, kubelet credential provider for ECR, manifest auto-deploy, `HelmChartConfig` for customizing packaged components, embedded etcd snapshots, restore runbook, upgrade workflow, `crictl` as the runtime-level fallback
- **Section 16** — What to backup at each layer, Velero install + daily commands, four DR scenarios with their playbooks, upgrade strategy
- **Section 17** — Operator's cheat sheet (triage, state, nodes, scheduling, rollouts, debug, RBAC, Helm, backup, runtime)
- **Section 18** — Full Docker→K8s mental map with conceptual shifts table

**What's left:** Daily Revision Days 8–14 + Commands Daily Drill Days 8–14. Coming up next.

---

## Daily Revision (7-Day Rotation)

A spaced-repetition cheat sheet. Spend 5–10 minutes a day on the day's topic. After 7 days you've cycled through everything; restart on day 8. Keep this open in a tab.

### Day 1 — Mental Model, Cluster, Node, Namespace

**Recall (try to answer without looking):**
1. What are the 5 control-plane components and what does each do?
2. What's on a worker node? (3 things)
3. What's the reconciliation loop in one sentence?
4. Why does HA control plane need an odd number of nodes? How many failures does a 3-node etcd tolerate?
5. Are PersistentVolumes namespaced? What about Nodes?

**Commands to type from memory:**
```bash
kubectl cluster-info
kubectl get nodes -o wide
kubectl describe node <name>
kubectl top nodes
kubectl get ns
kubectl api-resources --namespaced=false
kubectl config use-context <ctx>
kubectl config set-context --current --namespace=<ns>
```

**Gotchas to remember:**
- Lose your only control-plane node → cluster API is down. Existing Pods keep running but no scheduling/healing happens.
- Namespaces do **not** isolate networking. Use NetworkPolicy for that.
- Even-numbered etcd cluster (2, 4) gives **zero** extra fault tolerance vs odd-1.

---

### Day 2 — kubectl Essentials

**Recall:**
1. What does `kubectl logs --previous` do, and when must you use it?
2. Difference between `kubectl apply` and `kubectl create`?
3. How do you safely test a manifest without applying it?
4. Which command bounces an entire Deployment without changing the image?
5. How do you forward a local port to a Pod for debugging?

**Commands to type from memory:**
```bash
kubectl get pods -A --field-selector=status.phase!=Running
kubectl logs --previous <pod>
kubectl logs -f --since=15m --tail=200 <pod>
kubectl describe pod <pod>
kubectl exec -it <pod> -- sh
kubectl rollout restart deployment/<name>
kubectl rollout undo deployment/<name>
kubectl rollout status deployment/<name>
kubectl port-forward svc/<name> 8080:80
kubectl get events -A --sort-by=.lastTimestamp | tail -30
kubectl top pods -A --sort-by=memory
kubectl explain pod.spec.containers
```

**Gotchas:**
- `kubectl edit` changes the live resource but not your repo — always backport to YAML afterward.
- `--previous` shows the **crashed** container's logs. Critical for CrashLoopBackOff.
- Default namespace is `default` if not set — set it per context to avoid mistakes.

---

### Day 3 — Manifests, Labels, Selectors, Pod Basics

**Recall:**
1. What are the 4 top-level keys in every k8s manifest?
2. Difference between labels and annotations? Which is selectable?
3. Once a Deployment is created, can you change its `selector.matchLabels`?
4. What's the difference between an init container and a sidecar?
5. Why do you almost never create a raw Pod in production?

**Commands:**
```bash
kubectl get pods -l app=api,env=prod
kubectl get pods -l 'app in (api,web)'
kubectl get pods --show-labels
kubectl api-resources | grep -i <kind>
kubectl explain <kind>.spec
kubectl get pods --field-selector=spec.nodeName=<node>
```

**Pod lifecycle phases:** `Pending → Running → Succeeded / Failed`. (Unknown if node unreachable.)

**Container Waiting reasons you'll see:** `ContainerCreating`, `ImagePullBackOff`, `ErrImagePull`, `CrashLoopBackOff`, `CreateContainerConfigError`.

**Gotchas:**
- `selector.matchLabels` is **immutable** after creation. Plan once.
- Pods are not self-healing — a raw Pod on a dead node is gone forever. Use Deployment/StatefulSet/DaemonSet.
- Init containers run sequentially and must each exit 0; sidecars run alongside main containers.

---

### Day 4 — Workloads: Deployment, StatefulSet, DaemonSet, Jobs

**Recall:**
1. What does a Deployment manage? What does that manage?
2. Why does a StatefulSet need a Headless Service?
3. When would you use a DaemonSet vs a Deployment?
4. Difference between Job's `backoffLimit` and `restartPolicy`?
5. What does CronJob's `concurrencyPolicy: Forbid` do?

**Mapping to recite:**
- Deployment → ReplicaSet → Pod (stateless apps)
- StatefulSet → Pod with stable identity + PVC per Pod (Elasticsearch, Postgres, Kafka)
- DaemonSet → one Pod per node (log shippers, node exporters, CSI plugins)
- Job → run-to-completion (migrations, batch)
- CronJob → scheduled Jobs

**Commands:**
```bash
kubectl set image deployment/api api=<image>:0.2
kubectl rollout status deployment/api --timeout=5m
kubectl scale deployment api --replicas=5
kubectl rollout history deployment/api
kubectl get sts,ds,jobs,cronjobs -A
```

**Gotchas:**
- StatefulSet Pods start sequentially. Pod 0 must be Ready before Pod 1 starts → slow rolling updates.
- DaemonSet ignores most scheduling rules unless you add tolerations for tainted nodes.
- CronJob timezone defaults to controller-manager TZ (usually UTC) unless `spec.timeZone` set (k8s 1.27+).

---

### Day 5 — Probes, Resources, QoS, Rollouts

**Recall:**
1. Three probe types and the action on failure for each?
2. CPU over limit → ? Memory over limit → ?
3. Three QoS classes and how each is determined?
4. Default `maxSurge` and `maxUnavailable`?
5. What's the safest rolling update config for zero-downtime?

**Probe action table (memorize):**
| Probe | Failure action |
|---|---|
| livenessProbe | Restart container |
| readinessProbe | Remove from Service Endpoints (no restart) |
| startupProbe | Disable other probes until passes once |

**QoS table:**
| Class | Rule |
|---|---|
| Guaranteed | requests == limits for both CPU and memory, all containers |
| Burstable | At least one request set, doesn't qualify as Guaranteed |
| BestEffort | No requests or limits anywhere |

Eviction order under node pressure: BestEffort → Burstable → Guaranteed.

**Commands:**
```bash
kubectl get pod <name> -o jsonpath='{.status.qosClass}'
kubectl describe pod <name>          # see probe failure events
kubectl rollout pause   deployment/api
kubectl rollout resume  deployment/api
```

**Gotchas:**
- Same endpoint for liveness and readiness = wrong. Liveness checks "process alive", readiness checks "can serve traffic".
- Aggressive liveness on slow-start app → CrashLoopBackOff during startup. **Use startupProbe.**
- Memory limit hit = exit code 137 (OOMKilled). CPU limit hit = throttled, not killed.

---

### Day 6 — Networking: Service, Ingress, DNS, NetworkPolicy

**Recall:**
1. Four Service types — what's each for?
2. What does a headless Service do that ClusterIP doesn't?
3. If a Service "isn't working", what's the first object to check?
4. Why does NetworkPolicy break DNS until you fix it?
5. What does `ndots:5` in `/etc/resolv.conf` cause?

**Service types:**
| Type | Use |
|---|---|
| ClusterIP | In-cluster only (default) |
| NodePort | Port on every node (rarely used directly) |
| LoadBalancer | Provisions ALB/NLB via AWS LB Controller |
| ExternalName | DNS CNAME to external host |
| Headless (clusterIP: None) | DNS returns Pod IPs; for StatefulSets |

**DNS form to memorize:**
```
<svc>.<ns>.svc.cluster.local
<pod-name>.<headless-svc>.<ns>.svc.cluster.local      # StatefulSet Pods
```

**Commands:**
```bash
kubectl get svc,ep <name>            # endpoints = the Service's actual targets
kubectl describe endpoints <name>
kubectl run -it --rm dnsutils --image=registry.k8s.io/e2e-test-images/jessie-dnsutils:1.3 -- sh
# inside: nslookup api.ml-services.svc.cluster.local
kubectl get ingress -A
kubectl get networkpolicy -A
```

**Gotchas:**
- **Empty Endpoints = no Pods matched the selector OR no Pods are Ready.** This is the #1 service-broken root cause.
- Once any NetworkPolicy targets a Pod, that Pod is **default-deny** for the listed `policyTypes`. Always allow egress to CoreDNS (UDP 53 to `kube-system`).
- `pathType: Prefix` matches by path segment, not substring. `/foo` matches `/foo` and `/foo/bar`, not `/foobar`.

---

### Day 7 — Storage + Config/Secrets

**Recall:**
1. PV vs PVC vs StorageClass — what's the role of each?
2. Why is `volumeBindingMode: WaitForFirstConsumer` essential on AWS?
3. Three access modes and which AWS backend supports each?
4. ConfigMap as env var vs as volume mount — which updates live?
5. Is base64 in a Secret encryption? What is?

**Storage flow:**
```
Pod → PVC → (matches/triggers) → StorageClass → (provisions) → PV → (backed by) → EBS/EFS volume
```

**Access modes:**
| Mode | AWS |
|---|---|
| RWO (ReadWriteOnce) | EBS |
| RWX (ReadWriteMany) | EFS |
| ROX (ReadOnlyMany) | EFS |

**Commands:**
```bash
kubectl get sc
kubectl get pv
kubectl get pvc -A
kubectl describe pvc <name>
kubectl get cm,secret -n <ns>
kubectl get secret <name> -o jsonpath='{.data.password}' | base64 -d
kubectl create secret docker-registry ecr-creds \
  --docker-server=<acct>.dkr.ecr.ap-south-1.amazonaws.com \
  --docker-username=AWS --docker-password="$(aws ecr get-login-password --region ap-south-1)"
```

**Gotchas:**
- PVC stuck `Pending` with "waiting for first consumer" is normal until a Pod schedules — not a bug.
- Pod stuck with "volume node affinity conflict" = PV in one AZ, Pod scheduled to another. Use `WaitForFirstConsumer`.
- ConfigMap as **env vars** doesn't update live — need `rollout restart`. As **volume mount**, kubelet refreshes within ~60s.
- Base64 ≠ encryption. RBAC + etcd encryption-at-rest + external secret managers are what actually secures Secrets.

---

### Day 8 — Scheduling & Placement

**Recall:**
1. Difference between `nodeSelector` and `nodeAffinity`?
2. Three taint effects and what each does?
3. What's the difference between `requiredDuringScheduling` and `preferredDuringScheduling`?
4. Why is topology spread cheaper than pod anti-affinity at scale?
5. What does a PodDisruptionBudget protect against? What does it NOT protect against?

**Mechanism chain to memorize:** `nodeSelector` → `nodeAffinity` → `taints/tolerations` → `topologySpread` → resource fit. The scheduler checks all of them.

**Toleration ≠ NodeSelector:**
- Toleration: "I'm willing to land on a tainted node"
- NodeSelector / affinity: "I require/prefer this node"
- Most spot/on-demand patterns need **both**

**Gotchas:**
- `selector.matchLabels` is immutable; same applies to affinity terms — can't change post-create.
- PDB protects against **voluntary** disruption (drain, Karpenter consolidation). NOT spot interruption or kernel panic.
- Anti-affinity at scale is O(N²) — switch to topology spread for >100 replicas.

---

### Day 9 — Scaling (HPA, VPA, Karpenter)

**Recall:**
1. What does HPA need set on Pods to calculate CPU/memory Utilization?
2. Why shouldn't HPA and VPA both target CPU/memory on the same workload?
3. Karpenter consolidation policy `WhenEmptyOrUnderutilized` — what does it do?
4. Difference between Karpenter Consolidation and Drift?
5. What does `karpenter.sh/capacity-type: spot` in NodePool requirements mean?

**Mappings:**
- HPA = scales Pod **count** based on metrics
- VPA = adjusts Pod **size** (requests) based on usage
- Karpenter = adds/removes **Nodes** based on Pending Pods + efficiency

**KEDA** is what you use for event-driven autoscaling (Kafka lag, SQS depth) and **scale-to-zero**, which HPA can't do.

**Gotchas:**
- HPA needs `resources.requests` set on Pods (no requests → no Utilization math).
- Karpenter v1 made `amiSelectorTerms` and `consolidateAfter` REQUIRED — old v1beta1 YAMLs won't apply.
- Karpenter respects PDBs by default. Pod stuck Pending despite Karpenter being healthy → check the NodePool requirements vs Pod's nodeSelector/tolerations.

---

### Day 10 — Security (RBAC, SA, IRSA, PSS)

**Recall:**
1. Four RBAC objects and what each does?
2. Difference between Role and ClusterRole?
3. What's the single most useful RBAC debugging command?
4. Why does EKS Pod Identity NOT work on RKE2?
5. Three Pod Security Standard levels?

**`kubectl auth can-i`** — memorize the patterns:
```bash
kubectl auth can-i delete pods -n ml-services
kubectl auth can-i '*' '*' --as=system:serviceaccount:ml-services:api
kubectl auth can-i --list -n <ns>
```

**IRSA flow:** SA annotated → pod-identity-webhook injects env vars → AWS SDK auto-uses AssumeRoleWithWebIdentity → temp creds.

**Gotchas:**
- `verbs: ["*"]` grants future verbs too. Be explicit in prod roles.
- EKS Pod Identity is **EKS-only**. On RKE2 you need self-hosted IRSA via pod-identity-webhook.
- `default` ServiceAccount inherits no permissions by default — but anything you bind to it affects every Pod in the namespace that didn't specify an SA. Always use explicit per-app SAs.
- PSS labels are per-namespace; `kube-system` usually needs `privileged`.

---

### Day 11 — Packaging (Helm, Kustomize, Operators)

**Recall:**
1. What's a Helm "release"?
2. What does `helm upgrade --install` do that `helm install` doesn't?
3. Helm vs Kustomize — when each one is right?
4. What's the single most useful Helm plugin to install?
5. Operator = CRD + ?

**Mappings:**
- Chart = templates + defaults (the package)
- Release = installed instance (tracked in cluster)
- Operator = CRD + Controller that reconciles it

**Helm `-f` files compose:** later overrides earlier. CI pattern: `-f base.yaml -f env-prod.yaml`.

**`helm-diff` plugin** = the must-install. Shows what an upgrade will change before you run it.

**Gotchas:**
- Helm history is in cluster (etcd). Lose etcd → lose Helm history. Git is still source of truth.
- Kustomize is built into kubectl since 1.14 — `kubectl apply -k <dir>`.
- Operator-managed resources: changes you make manually get reverted by the operator. Edit the CR instead.

---

### Day 12 — Observability (Events, Logs, Metrics, Debug)

**Recall:**
1. Default event retention in K8s?
2. Where does `kubectl logs` actually read from on the Node?
3. Difference between ServiceMonitor and PodMonitor?
4. When do you use `kubectl debug` instead of `kubectl exec`?
5. What's the 7-step triage order?

**Triage order to memorize:**
1. Events
2. Pod status (describe)
3. Logs (--previous, then current)
4. Endpoints (Service routing?)
5. Resource usage (top)
6. Recent changes (rollout/helm history)
7. Operator logs (if CR-managed)

**Default event TTL = 1 hour.** Extend via kube-apiserver `--event-ttl` or ship to long-term store.

**Logs on disk:** `/var/log/pods/<ns>_<pod>_<uid>/<container>/0.log` — managed by containerd.

**Gotchas:**
- `nicolaka/netshoot` = the go-to debug image (dig, curl, tcpdump, all there).
- Empty endpoints = #1 broken-service cause (selector mismatch or no Ready Pods).
- ServiceMonitor needs a `release: <prometheus-release>` label to match the Prometheus selector — easy to miss.

---

### Day 13 — Production Troubleshooting Runbook

**Recall (rapid-fire — name the first check for each):**
1. CrashLoopBackOff → ?
2. ImagePullBackOff → ?
3. Pending Pod → ?
4. PVC Pending → ?
5. Service has no Endpoints → ?
6. DNS failures → ?
7. Pod stuck Terminating → ?
8. Ingress not routing → ?
9. OOMKilled — what exit code? what to check?
10. Node DiskPressure → ?

**Answers (cover and recall):**
1. `kubectl logs <pod> --previous`
2. `kubectl describe pod` (Events tell the auth/image story)
3. `kubectl describe pod` → Events
4. `kubectl describe pvc` → Events; check SC + CSI driver
5. Selector mismatch OR no Ready Pods (`kubectl get pods -l <selector>` shows READY column)
6. Spin up dnsutils Pod; check CoreDNS health; check NetworkPolicy
7. Check finalizers + `terminationGracePeriodSeconds`
8. Backend Service Endpoints + `target-type` (RKE2: must be `instance`, not `ip`)
9. Exit 137; `kubectl get pod <pod> -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason}'`
10. `kubectl debug node/<node>` → `crictl rmi --prune`

---

### Day 14 — RKE2-Specific + Backup/DR

**Recall:**
1. Where is RKE2's config file?
2. Where do you put a YAML that should auto-deploy at startup?
3. Default etcd snapshot interval and retention?
4. Three things to back up at three layers?
5. When do you use `crictl` over `kubectl`?

**Path memorization (must-knows):**
| Path | What |
|---|---|
| `/etc/rancher/rke2/config.yaml` | RKE2 config |
| `/etc/rancher/rke2/registries.yaml` | Container registry config |
| `/var/lib/rancher/rke2/server/manifests/` | Auto-deploy YAMLs |
| `/var/lib/rancher/rke2/server/db/snapshots/` | etcd snapshots |
| `/etc/rancher/rke2/rke2.yaml` | Cluster kubeconfig (on server) |

**Backup layers:**
1. etcd → RKE2 built-in snapshots
2. Workload defs → Git (PRIMARY source of truth)
3. PV data → Velero + CSI snapshots OR app-level (ES snapshots to S3)

**`crictl` use cases:** kubelet broken, ImagePullBackOff on one Node, DiskPressure (rmi --prune), confirming containerd can pull from ECR.

**Gotchas:**
- Deleting a file from manifests dir does NOT delete the resource — use `kubectl delete`.
- etcd restore is destructive (rolls back ALL cluster state). Practice on non-prod.
- Without `etcd-s3: true`, snapshots are only on server-node local disk — lose the node, lose the snapshot. Always configure S3 upload in production.

---

### How to Use This Rotation

**Minimum viable practice (5 min/day):**
1. Cover the answers, read each Recall question, answer aloud or in writing
2. Type at least 3 commands from memory in a real cluster (or `--dry-run=client`)
3. Read the Gotchas

**Stronger practice (15 min/day):**
1. All of the above
2. Open the corresponding section in the main guide; re-read it
3. Apply one concept to your actual cluster — describe an unfamiliar resource, check QoS class of a real Pod, look at Endpoints of a Service that you don't normally inspect
4. After Day 14, the next cycle try teaching one section out loud as if explaining to a junior

**Two-week cycle:** Days 1–7 cover fundamentals (mental model → config/secrets); Days 8–14 cover the operator skills (scheduling, scaling, security, packaging, observability, troubleshooting, RKE2/DR). Cycle continuously; the days you fumble are the ones to drill again.

**Track yourself:** keep a simple checklist — for each day, did you get the recall questions right without looking? After 2–3 cycles, drop the days you've mastered and concentrate the time on the ones you still fumble.

---

## Commands Daily Drill (Pure Muscle Memory)

The Daily Revision above tests concepts. **This section tests fingers.** Type each command from memory in a real cluster (or use `--dry-run=client -o yaml` if you don't want to actually create things). Cover the explanations, see if you remember what each does. Then cover the commands, read the scenarios, type the command that solves it.

Goal: when an incident hits at 2am, your hands type the right command before your brain catches up.

### Drill Day 1 — Cluster, Node, Namespace, Context

```bash
kubectl cluster-info                                                   # which cluster am I on?
kubectl version --short                                                # client & server versions
kubectl get nodes -o wide                                              # node IPs, OS, kernel
kubectl describe node <node>                                           # conditions, taints, allocatable, pods
kubectl top nodes                                                      # live CPU/mem per node
kubectl get nodes --show-labels                                        # all node labels
kubectl get nodes -l cashify.in/lifecycle=spot                         # spot nodes only
kubectl get ns                                                         # list namespaces
kubectl create ns ml-services                                          # create namespace
kubectl config get-contexts                                            # all configured clusters
kubectl config current-context                                         # which one is active
kubectl config use-context prod-rke2                                   # switch cluster
kubectl config set-context --current --namespace=ml-services           # set default ns
kubectl api-resources --namespaced=true                                # what's namespaced
kubectl api-resources --namespaced=false                               # what's cluster-scoped
```

**Scenario → command drill:**
- "What's eating CPU on prod nodes?" → `kubectl top nodes --sort-by=cpu`
- "I keep running commands in the wrong cluster" → `kubectl config use-context <ctx>` (+ install kube-ps1)
- "Why is this node not scheduling new pods?" → `kubectl describe node <node>` (look at Taints + Conditions)
- "What spot nodes do we have right now?" → `kubectl get nodes -l cashify.in/lifecycle=spot`

**Speed drill (under 30s):** switch context to prod, set namespace to ml-services, list pods sorted by restart count.

---

### Drill Day 2 — kubectl Essentials (get, describe, logs, exec)

```bash
kubectl get pods                                                       # current namespace
kubectl get pods -A                                                    # all namespaces
kubectl get pods -o wide                                               # + node + pod IP
kubectl get pods -l app=api                                            # by label
kubectl get pods --field-selector=status.phase!=Running                # the broken ones
kubectl get pods --sort-by=.status.containerStatuses[0].restartCount   # most-restarted first
kubectl get pods -o custom-columns=NAME:.metadata.name,NODE:.spec.nodeName,STATUS:.status.phase
kubectl get pod <pod> -o yaml                                          # full manifest
kubectl get pod <pod> -o jsonpath='{.status.phase}'                    # one field
kubectl describe pod <pod>                                             # status + events
kubectl logs <pod>                                                     # current container logs
kubectl logs <pod> -c <container>                                      # multi-container Pod
kubectl logs <pod> --previous                                          # crashed container's last logs
kubectl logs <pod> --since=15m --tail=200                              # time-windowed
kubectl logs -f -l app=api --max-log-requests=10                       # follow all matching pods
kubectl exec -it <pod> -- sh                                           # shell in
kubectl exec <pod> -- env                                              # one-shot env dump
kubectl port-forward svc/<svc> 8080:80                                 # local:service
kubectl top pods --sort-by=memory                                      # heaviest pods
```

**Scenario → command drill:**
- "Pod is in CrashLoopBackOff, no current logs" → `kubectl logs --previous <pod>`
- "I need to check if this Pod can reach the DB" → `kubectl exec -it <pod> -- nc -zv db 5432`
- "Test prod API from my laptop without exposing it" → `kubectl port-forward svc/api 8080:80`
- "Find all pods that have restarted at least once cluster-wide" → `kubectl get pods -A --sort-by=.status.containerStatuses[0].restartCount` then visually scan
- "What env vars does this Pod actually see?" → `kubectl exec <pod> -- env`

**Speed drill:** get the last 50 log lines from the previous (crashed) container of the most-restarted Pod in your namespace.

---

### Drill Day 3 — Manifests, Labels, Apply, Rollouts

```bash
kubectl explain pod                                                    # top-level fields
kubectl explain pod.spec.containers                                    # drill down
kubectl explain pod.spec --recursive | less                            # full tree
kubectl apply -f deploy.yaml                                           # create or update
kubectl apply -f ./manifests/                                          # whole directory
kubectl apply -k ./overlays/prod                                       # kustomize
kubectl apply -f deploy.yaml --dry-run=server                          # validate against API
kubectl apply -f deploy.yaml --dry-run=client -o yaml                  # see what would apply
kubectl create deployment api --image=myapp:0.1 --dry-run=client -o yaml > deploy.yaml
kubectl diff -f deploy.yaml                                            # what will change
kubectl edit deployment api                                            # live edit
kubectl patch deployment api -p '{"spec":{"replicas":5}}'              # programmatic
kubectl scale deployment api --replicas=5                              # shortcut
kubectl label pod <pod> tier=backend                                   # add a label
kubectl label pod <pod> tier-                                          # remove a label
kubectl annotate deployment api note="incident-1234"                   # add annotation
kubectl set image deployment/api api=<image>:0.2                       # trigger rollout
kubectl rollout status deployment/api --timeout=5m                     # wait for done
kubectl rollout history deployment/api                                 # revisions
kubectl rollout undo deployment/api                                    # roll back one
kubectl rollout undo deployment/api --to-revision=3                    # roll back to specific
kubectl rollout restart deployment/api                                 # bounce all pods
```

**Scenario → command drill:**
- "I edited a Secret and the app needs to pick up new values" → `kubectl rollout restart deployment/api`
- "What will this manifest actually change in prod?" → `kubectl diff -f deploy.yaml`
- "I need a template to start from for a Deployment" → `kubectl create deployment ... --dry-run=client -o yaml > deploy.yaml`
- "The new image is broken, roll back NOW" → `kubectl rollout undo deployment/api`
- "I forget which fields Deployment.spec has" → `kubectl explain deployment.spec`

**Speed drill:** generate a YAML template for a 3-replica nginx deployment without applying it.

---

### Drill Day 4 — Workloads (Deployment, STS, DS, Jobs)

```bash
kubectl get deploy,sts,ds,rs,jobs,cronjobs -A                          # all workload kinds
kubectl get deploy api -o wide                                         # + images
kubectl get rs -l app=api                                              # ReplicaSets owned by deploy
kubectl get sts -n ml-services                                         # StatefulSets
kubectl get ds -n kube-system                                          # DaemonSets (log shippers etc)
kubectl get jobs                                                       # one-off jobs
kubectl get cronjobs                                                   # short: cj
kubectl get cronjob backup -o jsonpath='{.status.lastScheduleTime}'    # last run
kubectl create job manual-migrate --from=cronjob/backup                # trigger CronJob now
kubectl delete pod <pod>                                               # let controller recreate
kubectl delete pod <pod> --grace-period=0 --force                      # don't wait (rare; use carefully)
kubectl logs job/<job-name>                                            # logs from a Job's Pod
```

**Scenario → command drill:**
- "Manually trigger the backup CronJob right now" → `kubectl create job manual-$(date +%s) --from=cronjob/backup`
- "Which ReplicaSet is the current one for this Deployment?" → `kubectl get rs -l app=api` (the one with replicas > 0)
- "What log shippers are running on every node?" → `kubectl get ds -A`
- "StatefulSet rollout is stuck on Pod 0" → `kubectl describe pod <sts>-0` (Pod 0 must be Ready before Pod 1)

**Speed drill:** trigger a one-off run of a CronJob and tail its Pod's logs.

---

### Drill Day 5 — Probes, Resources, Scheduling Visibility

```bash
kubectl get pod <pod> -o jsonpath='{.status.qosClass}'                 # QoS class
kubectl get pod <pod> -o jsonpath='{.spec.containers[*].resources}'    # requests + limits
kubectl describe pod <pod> | grep -A2 'Liveness\|Readiness\|Startup'   # probe config
kubectl get events --field-selector reason=Unhealthy                   # probe failures
kubectl get events --field-selector reason=OOMKilling                  # OOM events
kubectl get pod <pod> -o jsonpath='{.status.containerStatuses[0].lastState.terminated.exitCode}'
kubectl get pod <pod> -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason}'
kubectl top pod <pod> --containers                                     # per-container CPU/mem
kubectl get pods -o json | jq '.items[] | select(.status.qosClass=="BestEffort") | .metadata.name'
```

**Scenario → command drill:**
- "Is this Pod Guaranteed or Burstable?" → `kubectl get pod <pod> -o jsonpath='{.status.qosClass}'`
- "Was this container OOMKilled?" → `kubectl get pod <pod> -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason}'`
- "Find all BestEffort pods in prod (potential trouble)" → jq one-liner above
- "What's the exit code of the last crash?" → `kubectl get pod <pod> -o jsonpath='{.status.containerStatuses[0].lastState.terminated.exitCode}'`

**Speed drill:** find the QoS class and last termination reason for a specific pod in one combined `kubectl get` with `-o custom-columns`.

---

### Drill Day 6 — Networking (Service, Ingress, DNS, NetworkPolicy)

```bash
kubectl get svc                                                        # all services
kubectl get svc <svc> -o wide                                          # + selector
kubectl get endpoints <svc>                                            # short: ep — the actual Pods routed to
kubectl describe endpoints <svc>                                       # who's behind this Service
kubectl get ingress -A                                                 # short: ing
kubectl describe ingress <name>                                        # rules + events + LB address
kubectl get networkpolicy -A                                           # short: netpol
kubectl get svc -n kube-system kube-dns                                # CoreDNS service IP
kubectl logs -n kube-system -l k8s-app=kube-dns                        # CoreDNS logs
kubectl run -it --rm dnsutils --image=registry.k8s.io/e2e-test-images/jessie-dnsutils:1.3 -- sh
# inside:
nslookup api.ml-services.svc.cluster.local
nslookup api                                                           # uses search domains
dig api.ml-services.svc.cluster.local
```

**Scenario → command drill:**
- "Service has no traffic — why?" → `kubectl get ep <svc>` (empty = selector mismatch or no Ready pods)
- "Which Pods will this Service route to?" → `kubectl describe ep <svc>`
- "Is CoreDNS actually working?" → spin up dnsutils Pod and `nslookup kubernetes.default`
- "What's the ALB hostname for this Ingress?" → `kubectl get ingress <name> -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'`
- "What NetworkPolicies apply to this Pod?" → `kubectl get netpol -A -o yaml | grep -B5 'app: <label>'`

**Speed drill:** verify a Service is correctly routing — get the Service, its Endpoints, and curl-test from a temporary Pod, all in 3 commands.

---

### Drill Day 7 — Storage + Config + Secrets

```bash
kubectl get sc                                                         # storage classes
kubectl get sc -o jsonpath='{.items[?(@.metadata.annotations.storageclass\.kubernetes\.io/is-default-class=="true")].metadata.name}'
kubectl get pv                                                         # cluster-scoped
kubectl get pvc -A                                                     # all PVCs
kubectl describe pvc <name>                                            # status + events + bound PV
kubectl get pv <pv-name> -o jsonpath='{.spec.claimRef}'                # which PVC owns this PV
kubectl get cm -n <ns>                                                 # ConfigMaps
kubectl get cm <name> -o yaml                                          # contents
kubectl create cm app-config --from-literal=LOG_LEVEL=info --dry-run=client -o yaml
kubectl create cm app-config --from-file=config.yaml --dry-run=client -o yaml
kubectl get secret -n <ns>                                             # list (values masked)
kubectl get secret <name> -o jsonpath='{.data.password}' | base64 -d   # decode one key
kubectl create secret generic db-creds --from-literal=password=xyz --dry-run=client -o yaml
kubectl create secret docker-registry ecr-creds \
  --docker-server=<acct>.dkr.ecr.ap-south-1.amazonaws.com \
  --docker-username=AWS \
  --docker-password="$(aws ecr get-login-password --region ap-south-1)"
```

**Scenario → command drill:**
- "PVC is stuck Pending" → `kubectl describe pvc <name>` (look at Events — usually SC missing or AZ conflict)
- "I changed a ConfigMap, app isn't picking it up" → it's mounted as env vars → `kubectl rollout restart deployment/api`
- "What's the decoded value of this Secret?" → `kubectl get secret <name> -o jsonpath='{.data.<key>}' | base64 -d`
- "Refresh ECR pull secret (12h expiry)" → the `create secret docker-registry` one-liner above
- "Which PV is bound to this PVC?" → `kubectl get pvc <name> -o jsonpath='{.spec.volumeName}'`

**Speed drill:** create a ConfigMap from a local file as a dry-run YAML, decode one key from a Secret, and find the PV backing a PVC — three commands.

---

### Drill Day 8 — Scheduling & Placement

```bash
# Inspect node scheduling readiness
kubectl get nodes -L kubernetes.io/arch,karpenter.sh/capacity-type,karpenter.sh/nodepool,topology.kubernetes.io/zone
kubectl describe node <node> | grep -A 5 Taints
kubectl get nodes -l cashify.in/lifecycle=spot --show-labels
kubectl get pods -A --field-selector=status.phase=Pending

# Inspect Pod scheduling decisions
kubectl describe pod <pending-pod> | grep -A 20 Events:
kubectl get pod <pod> -o jsonpath='{.spec.nodeName}'
kubectl get pod <pod> -o yaml | grep -A 20 -E 'nodeSelector|tolerations|affinity'

# PodDisruptionBudgets
kubectl get pdb -A
kubectl describe pdb <name>                                              # DISRUPTIONS ALLOWED column
kubectl get pdb <name> -o jsonpath='{.status.currentHealthy}/{.spec.minAvailable}'

# Cordon / drain / uncordon
kubectl cordon <node>                                                     # mark unschedulable
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data --grace-period=120
kubectl uncordon <node>

# Topology distribution check
kubectl get pods -l app=api -o custom-columns=NAME:.metadata.name,NODE:.spec.nodeName,ZONE:.metadata.labels.topology\\.kubernetes\\.io/zone
```

**Scenario → command:**
- "Why won't this Pod schedule?" → `kubectl describe pod <pod> | grep -A 20 Events:`
- "Drain this node for maintenance, respecting PDBs" → `kubectl drain <node> --ignore-daemonsets --delete-emptydir-data`
- "How many disruptions can I afford right now?" → `kubectl describe pdb <name>` (look at ALLOWED DISRUPTIONS)
- "Are my replicas spread across AZs?" → custom-columns query above

---

### Drill Day 9 — Scaling (HPA, VPA, Karpenter)

```bash
# HPA
kubectl get hpa -A
kubectl describe hpa <name>                                              # current/target/desired
kubectl get hpa <name> -o jsonpath='{.status.currentReplicas}'

# VPA (if installed)
kubectl get vpa -A
kubectl describe vpa <name>                                              # recommendations

# Karpenter
kubectl get nodepool
kubectl describe nodepool <name>
kubectl get ec2nodeclass
kubectl get nodeclaim                                                    # in-flight or recent
kubectl describe nodeclaim <name>
kubectl get nodes -L karpenter.sh/nodepool,karpenter.sh/capacity-type

# Karpenter controller logs (the action)
kubectl logs -n kube-system -l app.kubernetes.io/name=karpenter --tail=200 -f
kubectl get events -A --field-selector reason=DisruptionLaunching
kubectl get events -A --field-selector reason=DisruptionTerminating
kubectl get events -A --field-selector reason=Drifted

# What instance types is Karpenter actually launching?
kubectl get nodes -L node.kubernetes.io/instance-type,karpenter.sh/capacity-type | grep karpenter
```

**Scenario → command:**
- "HPA is not scaling, why?" → `kubectl describe hpa <name>` (look at conditions; usually `FailedGetResourceMetric`)
- "Karpenter is not creating Nodes for Pending Pods" → controller logs above + check NodePool requirements vs Pod requirements
- "What's the cost-mix of our cluster right now?" → `kubectl get nodes -L karpenter.sh/capacity-type,node.kubernetes.io/instance-type`

---

### Drill Day 10 — Security (RBAC, SA, IRSA)

```bash
# RBAC audit
kubectl auth can-i <verb> <resource> -n <ns>
kubectl auth can-i delete pods -n ml-services
kubectl auth can-i '*' '*' --as=system:serviceaccount:ml-services:api
kubectl auth can-i --list -n ml-services
kubectl auth can-i --list -n ml-services --as=jane@cashify.in

# Inspect bindings
kubectl get role,rolebinding -n <ns>
kubectl get clusterrole,clusterrolebinding
kubectl describe rolebinding <name> -n <ns>
kubectl get clusterrolebinding -o json | jq '.items[] | select(.subjects[]?.name=="<sa-name>")'

# ServiceAccounts
kubectl get sa -n <ns>
kubectl get sa <name> -n <ns> -o yaml | grep -A2 annotations            # IRSA annotation
kubectl get pod <pod> -o jsonpath='{.spec.serviceAccountName}'
kubectl get pod <pod> -o yaml | grep -A5 'volumeMounts\|projected'      # SA token mount

# IRSA verification from inside Pod
kubectl exec -it <pod> -- env | grep AWS                                # AWS_ROLE_ARN, AWS_WEB_IDENTITY_TOKEN_FILE
kubectl exec -it <pod> -- aws sts get-caller-identity 2>/dev/null

# Pod Security Standards
kubectl get ns -o custom-columns=NAME:.metadata.name,ENFORCE:.metadata.labels.pod-security\\.kubernetes\\.io/enforce
kubectl label ns <name> pod-security.kubernetes.io/enforce=baseline --overwrite

# Image pull secrets
kubectl get sa <name> -n <ns> -o jsonpath='{.imagePullSecrets[*].name}'
kubectl create secret docker-registry ecr-creds \
  --docker-server=<acct>.dkr.ecr.ap-south-1.amazonaws.com \
  --docker-username=AWS --docker-password="$(aws ecr get-login-password --region ap-south-1)" -n <ns>
```

**Scenario → command:**
- "Can this SA delete Secrets?" → `kubectl auth can-i delete secrets --as=system:serviceaccount:<ns>:<sa>`
- "Is IRSA actually wired up in this Pod?" → `kubectl exec ... -- env | grep AWS_ROLE_ARN`
- "Show me all PSS-restricted namespaces" → custom-columns query above
- "What can the karpenter SA do?" → `kubectl auth can-i --list --as=system:serviceaccount:kube-system:karpenter`

---

### Drill Day 11 — Packaging (Helm, Kustomize, Operators)

```bash
# Helm
helm list -A
helm list -n <ns>
helm history <release> -n <ns>
helm get values <release> -n <ns>
helm get manifest <release> -n <ns>
helm upgrade --install <release> <chart> -n <ns> -f values.yaml --wait --timeout=10m
helm rollback <release> <revision> -n <ns>
helm diff upgrade <release> <chart> -f values.yaml                       # requires helm-diff plugin
helm template <release> <chart> -f values.yaml | less                    # render only
helm search repo <name>
helm repo update

# Kustomize
kubectl kustomize ./overlays/prod                                        # render
kubectl apply -k ./overlays/prod                                         # apply
kubectl diff -k ./overlays/prod

# CRDs and operator state
kubectl get crds
kubectl get crds | grep -i <operator>
kubectl api-resources --api-group=<group>
kubectl explain <kind>.spec
kubectl get <cr-kind> -A
kubectl describe <cr-kind> <name>                                        # operator decisions
kubectl get <cr-kind> <name> -o yaml | yq '.status'                      # operator status
kubectl logs -n <operator-ns> -l <operator-label> --tail=200
```

**Scenario → command:**
- "What did this Helm release deploy?" → `helm get manifest <release> -n <ns>`
- "What will change if I upgrade?" → `helm diff upgrade <release> <chart> -f values.yaml`
- "Operator is not reconciling my CR" → `kubectl describe <kind> <name>` + `kubectl logs -n <op-ns> -l <op-label>`
- "List all CRDs from cert-manager" → `kubectl api-resources --api-group=cert-manager.io`

---

### Drill Day 12 — Observability (Events, Logs, Metrics)

```bash
# Events
kubectl get events -A --sort-by=.lastTimestamp | tail -30
kubectl get events -A --field-selector type=Warning --sort-by=.lastTimestamp | tail -30
kubectl get events -A --field-selector reason=OOMKilling
kubectl get events -A --field-selector reason=FailedScheduling
kubectl get events --field-selector involvedObject.name=<pod>
kubectl get events -A -w                                                 # live stream

# Logs
kubectl logs <pod> --tail=200
kubectl logs <pod> --previous --tail=200                                 # crashed container
kubectl logs <pod> --since=15m --timestamps
kubectl logs -l app=api --max-log-requests=10 --tail=100                # multi-Pod
kubectl logs --selector='app=fluent-bit' -n logging --tail=50

# Top (metrics-server)
kubectl top nodes --sort-by=cpu
kubectl top pods -A --sort-by=memory | head -20
kubectl top pods --containers -n <ns>

# Prometheus stack
kubectl get servicemonitor -A
kubectl get podmonitor -A
kubectl get prometheusrule -A
kubectl get prometheus -A

# Debug
kubectl debug -it <pod> --image=nicolaka/netshoot --target=<container>
kubectl debug node/<node> -it --image=busybox
kubectl run -it --rm netshoot --image=nicolaka/netshoot -- sh
```

**Scenario → command:**
- "What's been failing in the last 10 minutes cluster-wide?" → `kubectl get events -A --field-selector type=Warning --sort-by=.lastTimestamp | tail -30`
- "I need tcpdump in a distroless Pod" → `kubectl debug -it <pod> --image=nicolaka/netshoot --target=<container>`
- "Tail logs from all fluent-bit pods on every node" → `kubectl logs -l app=fluent-bit -n logging -f --max-log-requests=20`

---

### Drill Day 13 — Troubleshooting Reflexes (Speed Round)

These are the commands you should type **without thinking** during an incident.

```bash
# Triage chain (memorize this 5-line sequence)
kubectl describe pod <pod>
kubectl logs <pod> --previous
kubectl get ep <svc>
kubectl get events -n <ns> --sort-by=.lastTimestamp | tail -20
kubectl top pod <pod> --containers

# Exit code + OOM check
kubectl get pod <pod> -o jsonpath='Exit={.status.containerStatuses[0].lastState.terminated.exitCode} OOM={.status.containerStatuses[0].lastState.terminated.reason} Restarts={.status.containerStatuses[0].restartCount}'

# Force a stuck Terminating Pod
kubectl delete pod <pod> --grace-period=0 --force
kubectl patch pod <pod> -p '{"metadata":{"finalizers":null}}'

# Service routing check
kubectl get svc <svc> -o jsonpath='{.spec.selector}' && echo
kubectl get pods -l <selector-from-above> --show-labels
kubectl get ep <svc>

# DNS verify
kubectl run -it --rm dnsutils --image=registry.k8s.io/e2e-test-images/jessie-dnsutils:1.3 -- sh
# nslookup kubernetes.default ; nslookup <svc>.<ns>.svc.cluster.local

# Ingress check
kubectl describe ingress <name>
kubectl logs -n kube-system -l app.kubernetes.io/name=aws-load-balancer-controller --tail=100

# Node forensics
kubectl describe node <node> | grep -A 5 Conditions
kubectl get pods -A -o wide --field-selector spec.nodeName=<node>
kubectl debug node/<node> -it --image=busybox

# crictl (kubelet/kubectl broken)
sudo crictl ps -a
sudo crictl logs <container-id>
sudo crictl rmi --prune
```

**Scenario → command (rapid-fire):**
- "Pod restarting" → `kubectl logs <pod> --previous` + `kubectl get pod <pod> -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason}'`
- "Service not routing" → `kubectl get ep <svc>` (empty = problem)
- "DNS issues" → spawn dnsutils Pod, nslookup
- "Stuck terminating" → finalizer patch + force delete
- "Node DiskPressure" → `crictl rmi --prune` on the Node

---

### Drill Day 14 — RKE2 + Backup/DR

```bash
# RKE2 system state
sudo systemctl status rke2-server                                        # or rke2-agent
sudo journalctl -u rke2-server -n 200 --no-pager
sudo cat /etc/rancher/rke2/config.yaml
sudo cat /etc/rancher/rke2/registries.yaml
ls /var/lib/rancher/rke2/server/manifests/
ls -lh /var/lib/rancher/rke2/server/db/snapshots/

# Auto-deploy addons
kubectl get addon -A

# etcd snapshot
sudo rke2 etcd-snapshot save --name pre-change-$(date +%F-%H%M)
sudo rke2 etcd-snapshot list

# Velero
velero backup get
velero backup describe <name> --details
velero backup logs <name>
velero schedule get
velero restore create --from-backup <name>
velero restore get

# crictl (runtime debug)
sudo crictl ps
sudo crictl ps -a
sudo crictl logs <container-id>
sudo crictl pull <image>                                                 # test ECR pull from this Node
sudo crictl images
sudo crictl rmi --prune

# kubeconfig source on RKE2 server
sudo cat /etc/rancher/rke2/rke2.yaml
```

**Scenario → command:**
- "Take a snapshot before a risky change" → `sudo rke2 etcd-snapshot save --name pre-<change>-$(date +%F)`
- "Verify a Node can actually pull from ECR" → `sudo crictl pull <ecr-image>`
- "Free disk on a Node with DiskPressure" → `sudo crictl rmi --prune`
- "Restore a namespace from yesterday's backup" → `velero restore create --from-backup <name> --include-namespaces ml-services`

---

### How to Use the Commands Drill

**Beginner (week 1–2):** type each command exactly as written into a real (non-prod!) cluster. Read the explanation. Move on.

**Intermediate (week 3–4):** cover the explanation column, look at the command, recall what it does. Then cover the command, read the scenario, type the command from memory.

**Advanced (week 5+):** chain commands. For each scenario, write a one-line shell pipeline that solves it. Combine `kubectl get -o json` with `jq` for non-obvious queries.

**Test yourself weekly:** pick one command from each day at random. Type it without looking. If you can't, that's the one to drill tomorrow.

---



You now have:
- The control-plane / data-plane mental model + HA fundamentals
- Cluster, Node, Namespace concepts
- The full kubectl daily-use toolkit
- Manifests, labels, selectors
- All major workload kinds (Pod, Deployment, StatefulSet, DaemonSet, Job, CronJob)
- Probes, resources, QoS
- Service (all types), Ingress (with AWS LB Controller), DNS, CNI, NetworkPolicy
- PV/PVC/SC/CSI + AWS specifics (EBS/EFS, WaitForFirstConsumer)
- ConfigMap, Secret, External Secrets pattern

**Coming in pass 2 (sections 9–18):**
- Scheduling: nodeSelector, taints/tolerations, affinity, topology spread, PodDisruptionBudget
- Scaling: HPA, VPA, **Karpenter** (NodePools, NodeClaims, consolidation, drift)
- Security: RBAC, ServiceAccounts, **IRSA**, Pod Security Standards
- Packaging: Helm, Kustomize, CRDs, Operators
- Observability: events, logs to Elasticsearch, Prometheus, kubectl debug
- Production Troubleshooting: CrashLoopBackOff, ImagePullBackOff, OOMKilled, Pending pods, PVC Pending, Service has no endpoints, DNS failures, Ingress not routing, node pressure, stuck Terminating
- RKE2 specifics: server/agent architecture, registries.yaml, upgrade workflow, etcd snapshots
- Backup & DR: Velero, etcd snapshots, cluster upgrade strategy
- kubectl Operator's Cheat Sheet (triage commands, mirror of Docker §17.14)

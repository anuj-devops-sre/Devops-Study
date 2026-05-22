# Kubernetes: Zero to Mid-Level Guide (DevOps/SRE Lens)

A practical, operator-focused guide for engineers running Kubernetes in production — not a developer tutorial. Heavy on daily commands, triage flows, and the realities of running on AWS with RKE2 + Karpenter.

> **Companion doc:** `docker-guide-zero-to-mid.md` — read that first if Docker basics aren't second nature yet. This guide assumes you can build/run/debug containers.

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
9. [Daily Revision (7-Day Rotation)](#daily-revision-7-day-rotation)

> Sections 9–18 (Scheduling, Scaling/Karpenter, Security/IRSA, Helm/Kustomize, Observability, Troubleshooting, RKE2 specifics, Backup/DR, kubectl cheat sheet) follow in the next pass — note: the Daily Revision section above is renumbered when those land.

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
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS":443}]'
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:ap-south-1:...
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

### How to Use This Rotation

**Minimum viable practice (5 min/day):**
1. Cover the answers, read each Recall question, answer aloud or in writing
2. Type at least 3 commands from memory in a real cluster (or `--dry-run=client`)
3. Read the Gotchas

**Stronger practice (15 min/day):**
1. All of the above
2. Open the corresponding section in the main guide; re-read it
3. Apply one concept to your actual cluster — describe an unfamiliar resource, check QoS class of a real Pod, look at Endpoints of a Service that you don't normally inspect
4. After Day 7, the next week try teaching one section out loud as if explaining to a junior

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

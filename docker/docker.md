# Docker: Zero to Mid-Level Guide (DevOps/SRE)

Ek practical, example-heavy guide un engineers ke liye jo "kabhi Docker use nahi kiya" se "comfortably build, debug, aur production mein ship kar sakta hoon" tak jaana chahte hain. Hinglish explanations, English commands.

---

## Table of Contents

1. [Docker Kya Hai aur Kyun Exist Karta Hai](#1-docker-kya-hai-aur-kyun-exist-karta-hai)
2. [Core Concepts](#2-core-concepts)
3. [Installation & First Commands](#3-installation--first-commands)
4. [Images ke saath kaam karna](#4-images-ke-saath-kaam-karna)
5. [Containers ke saath kaam karna](#5-containers-ke-saath-kaam-karna)
6. [Dockerfile: Apni Images Banao](#6-dockerfile-apni-images-banao)
7. [Volumes & Persistent Data](#7-volumes--persistent-data)
8. [Networking](#8-networking)
9. [Docker Compose: Multi-Container Apps](#9-docker-compose-multi-container-apps)
10. [Multi-Stage Builds & Image Optimization](#10-multi-stage-builds--image-optimization)
11. [Environment Variables, Secrets & Config](#11-environment-variables-secrets--config)
12. [Healthchecks & Resource Limits](#12-healthchecks--resource-limits)
13. [Registries & Image Distribution](#13-registries--image-distribution)
14. [Containers Debug Karna](#14-containers-debug-karna)
15. [Best Practices](#15-best-practices)
16. [Cheat Sheet (Learning)](#16-cheat-sheet-learning)
17. [DevOps/SRE Daily Operations](#17-devopssre-daily-operations)

---

## 1. Docker Kya Hai aur Kyun Exist Karta Hai

Docker aapki application ko **uske saare dependencies ke saath** — code, runtime, libraries, env variables, config — ek single artifact mein pack kar deta hai jise **image** bolte hain. Jab aap image ko run karte ho, toh banta hai **container**: ek isolated process jo aapke laptop pe, teammate ke laptop pe, CI runner pe, ya production server pe — sabhi jagah same behave karega.

### Containers vs Virtual Machines

| Aspect | VM | Container |
|---|---|---|
| Boot time | Full OS (minutes) | Process (milliseconds) |
| Size | GBs | MBs |
| Isolation | Hardware-level (hypervisor) | Process-level (kernel namespaces + cgroups) |
| Kernel | Har VM ka apna | Host ke saath share |
| Density | ~10s per host | ~100s–1000s per host |

Container koi chhota VM nahi hai. Yeh bas ek Linux process hai jiska filesystem, network, PIDs, aur resources ka view restricted hota hai. Isiliye containers itne fast aur lightweight hote hain.

### Kyun Important Hai

- **"Mere machine pe toh chal raha tha"** — yeh dialogue khatam. Image hi environment hai.
- **Immutable deploys** — jo aap test karte ho, vahi ship hota hai.
- **Kubernetes ki foundation** — k8s containers ko hi schedule karta hai. Docker samajh aa gaya, toh k8s click ho jayega.

---

## 2. Core Concepts

| Term | Matlab |
|---|---|
| **Image** | Read-only template (Dockerfile se built), app + dependencies wala. "Snapshot" samjho. |
| **Container** | Running (ya stopped) instance of an image. Ek image se kai containers ban sakte hain. |
| **Dockerfile** | Text file with build instructions for an image. |
| **Registry** | Images ka storage service (Docker Hub, ECR, GHCR, etc.). |
| **Tag** | Image pe lagi label, usually version (`nginx:1.25`, `myapp:v2.3.1`). |
| **Layer** | Image stacked filesystem layers se banti hai — Dockerfile ka har instruction ek layer banata hai. Layers cached aur reuse hoti hain. |
| **Volume** | Persistent storage jo container ke marne ke baad bhi rehta hai. |
| **Network** | Virtual network jo containers ko connect karta hai. |

---

## 3. Installation & First Commands

### Install (Linux ka jaldi wala raasta)

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER   # sudo har baar lagana na pade
newgrp docker                    # current shell mein group change apply

# Verify
docker --version
docker run hello-world
```

macOS / Windows ke liye: **Docker Desktop** install karo.

### Daily Use Hone Wali Pehli 5 Commands

```bash
docker run <image>          # Image se container start karo
docker ps                   # Running containers dikhao
docker ps -a                # SAARE containers dikhao (stopped bhi)
docker images               # Local images list karo
docker logs <container>     # Container ke stdout/stderr dekho
```

### Pehla Real Container

```bash
docker run -d -p 8080:80 --name web nginx
# -d        : detached (background mein)
# -p 8080:80: host port 8080 -> container port 80 map karo
# --name    : memorable naam de do

curl http://localhost:8080  # nginx welcome page
docker logs web
docker stop web
docker rm web
```

---

## 4. Images ke saath kaam karna

### Pull aur Inspect Karna

```bash
docker pull python:3.12-slim         # registry se download
docker images                         # local images list
docker inspect python:3.12-slim       # full JSON metadata
docker history python:3.12-slim       # saari layers dikhao
```

### Tags & Versioning

```
python                 # implicitly :latest — production mein KABHI MAT use karo
python:3.12            # major.minor — better
python:3.12.4-slim     # pinned + variant — reproducibility ke liye best
python:3.12-slim@sha256:abc123...  # digest-pinned — sabse strict
```

`latest` ek moving target hai. Real projects mein versions pin karo, bhai.

### Images Hatana

```bash
docker rmi nginx:1.25
docker image prune              # dangling (untagged) images hatao
docker image prune -a           # SAARI unused images hatao (dhyan se!)
```

---

## 5. Containers ke saath kaam karna

### Lifecycle

```bash
docker run <image>              # create + start
docker start <container>        # stopped container start karo
docker stop <container>         # graceful stop (SIGTERM, 10s baad SIGKILL)
docker kill <container>         # turant SIGKILL
docker restart <container>      # stop + start
docker rm <container>           # delete (pehle stop karo, ya -f use karo)
```

### Interactive Containers

```bash
# Fresh ubuntu mein interactive shell
docker run -it --rm ubuntu:24.04 bash
# -i  : interactive (STDIN open rakho)
# -t  : TTY allocate karo
# --rm: exit hote hi auto-delete

# RUNNING container mein exec karo
docker exec -it web bash
```

### Useful Inspection

```bash
docker logs -f web              # follow logs (jaise tail -f)
docker logs --tail 100 web      # last 100 lines
docker stats                    # saare containers ki CPU/memory live
docker top web                  # container ke andar ke processes
docker inspect web              # full container metadata
docker port web                 # port mappings dikhao
```

### Files Copy Karna

```bash
docker cp ./local.conf web:/etc/nginx/conf.d/local.conf
docker cp web:/var/log/nginx/access.log ./access.log
```

---

## 6. Dockerfile: Apni Images Banao

Dockerfile ek recipe hai. Har instruction ek layer add karta hai.

### Minimal Example (Python app)

```dockerfile
# syntax=docker/dockerfile:1.7

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "app.py"]
```

Build aur run:

```bash
docker build -t myapp:0.1 .
docker run -d -p 8000:8000 --name myapp myapp:0.1
```

### Key Instructions

| Instruction | Purpose |
|---|---|
| `FROM` | Base image (pehla non-comment line) |
| `WORKDIR` | Working directory set karo; nahi hai toh bana dega |
| `COPY` | Build context se image mein files copy karo |
| `ADD` | COPY jaisa, lekin URLs handle karta hai aur archives auto-extract karta hai (COPY prefer karo) |
| `RUN` | **Build** time pe command chalao (nai layer banti hai) |
| `CMD` | Container start hone pe default command (override ho sakta hai) |
| `ENTRYPOINT` | Fixed command; CMD uske arguments ban jaate hain |
| `EXPOSE` | Documentation hint — ports actually publish nahi karta |
| `ENV` | Environment variables set karo |
| `ARG` | Build-time variable (`--build-arg` se pass karo) |
| `USER` | Non-root user pe switch karo |
| `VOLUME` | Mount point declare karo |
| `HEALTHCHECK` | Container healthy hai ya nahi, Docker ko kaise check karna hai |

### CMD vs ENTRYPOINT (sabse zyada confuse karne wali jodi)

```dockerfile
# Pattern 1: Sirf CMD (override ho sakta hai)
CMD ["python", "app.py"]
# `docker run myapp bash` -> bash chalega instead

# Pattern 2: Sirf ENTRYPOINT (fixed command)
ENTRYPOINT ["python", "app.py"]
# `docker run myapp --debug` -> `python app.py --debug` chalega

# Pattern 3: Dono (CLIs ke liye recommended)
ENTRYPOINT ["python", "app.py"]
CMD ["--port", "8000"]
# `docker run myapp` -> python app.py --port 8000
# `docker run myapp --port 9000` -> python app.py --port 9000
```

### Layer Caching: Order Matters

Docker har layer ko cache karta hai. Agar layer ka input change nahi hua, toh reuse hoti hai. **Jo cheezein kabhi-kabhi change hoti hain unhe upar rakho, jo har baar change hoti hain unhe neeche.**

❌ Bharosa:
```dockerfile
COPY . .
RUN pip install -r requirements.txt
```
Har code change pe pip install layer invalidate ho jayegi → har build pe reinstall.

✅ Sahi:
```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```
pip install sirf tab re-run hoga jab `requirements.txt` change ho.

### .dockerignore

`.gitignore` jaisa hi — build context chhota rakho.

```
.git
.venv
__pycache__
*.pyc
node_modules
.env
.pytest_cache
*.log
```

Bada context = slow builds aur images mein secrets leak hone ka risk.

---

## 7. Volumes & Persistent Data

Containers **ephemeral** hote hain. `docker rm` karte hi filesystem changes gayab. Jo data survive karna chahiye, uske liye volumes use karo.

### Teen Mount Types

**1. Named Volumes (Docker-managed, app data ke liye best)**
```bash
docker volume create pgdata
docker run -d --name pg \
  -v pgdata:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=secret \
  postgres:16
```
`/var/lib/docker/volumes/pgdata/` mein rehta hai. `docker rm pg` ke baad bhi safe.

**2. Bind Mounts (host path map karta hai, dev ke liye great)**
```bash
docker run -d --name web \
  -v $(pwd):/usr/share/nginx/html:ro \
  -p 8080:80 \
  nginx
```
Host pe edit karo, container mein turant dikh jata hai. `:ro` se read-only.

**3. tmpfs (in-memory, ephemeral, fast)**
```bash
docker run --tmpfs /tmp:size=100M myapp
```

### Volume Management

```bash
docker volume ls
docker volume inspect pgdata
docker volume rm pgdata
docker volume prune          # saare unused volumes hatao
```

---

## 8. Networking

### Default Networks

```bash
docker network ls
# bridge   - default; containers ko IPs milti hain, IP se baat kar sakte hain
# host     - container host ka network stack share karta hai (no isolation)
# none     - no network
```

### Sahi Tarika: User-Defined Bridge Networks

Default `bridge` network containers ke beech DNS **nahi** deta. Apna banao hamesha:

```bash
docker network create app-net

docker run -d --name db --network app-net postgres:16
docker run -d --name api --network app-net myapi:0.1
# `api` ke andar se `db` hostname pe database accessible — automatic DNS.
```

### Port Publishing

```bash
-p 8080:80           # host 8080 -> container 80 (saare interfaces)
-p 127.0.0.1:8080:80 # host 8080 sirf loopback pe
-p 80                # container 80 -> random host port
-P                   # saare EXPOSEd ports random host ports pe publish
```

### Networks Inspect Karna

```bash
docker network inspect app-net   # kaun se containers attached hain
docker network connect app-net web
docker network disconnect app-net web
```

---

## 9. Docker Compose: Multi-Container Apps

5 alag-alag `docker run` commands manually likhna painful hai. **Compose** ek YAML file mein pura stack declare karta hai.

### Example: Web + DB + Redis

`compose.yaml`:

```yaml
services:
  api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgres://app:secret@db:5432/app
      REDIS_URL: redis://cache:6379
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    restart: unless-stopped

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: app
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 5s
      timeout: 3s
      retries: 5

  cache:
    image: redis:7-alpine
    volumes:
      - redisdata:/data

volumes:
  pgdata:
  redisdata:
```

### Compose Commands

```bash
docker compose up -d                  # background mein sab kuch start
docker compose ps                     # stack services ki status
docker compose logs -f api            # ek service ke logs follow
docker compose exec api bash          # running service mein shell
docker compose build                  # images rebuild
docker compose down                   # containers + networks remove
docker compose down -v                # ...named volumes bhi delete
docker compose restart api            # ek service restart
docker compose pull                   # base images update
```

Compose automatically `<project>_default` naam ka network banata hai aur saari services usme join hoti hain. Services ek dusre ko service name se reach karti hain (`db`, `cache`, `api`).

### Override Files

Local dev tweaks ke liye `compose.override.yaml`; production ke liye base `compose.yaml`:

```bash
docker compose -f compose.yaml -f compose.prod.yaml up -d
```

---

## 10. Multi-Stage Builds & Image Optimization

"Single-stage" build mein compilers, build tools, aur source code final image mein chale jaate hain — image bloat hoti hai aur attack surface badh jata hai. **Multi-stage builds** is problem ko solve karte hain.

### Example: Go App (final image ~10MB)

```dockerfile
# Stage 1: build
FROM golang:1.22-alpine AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /app/server ./cmd/server

# Stage 2: runtime (sirf binary)
FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/server /server
EXPOSE 8080
ENTRYPOINT ["/server"]
```

### Example: Python App (chhota, final mein pip nahi)

```dockerfile
# Stage 1: virtualenv mein deps install karo
FROM python:3.12-slim AS builder
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: venv + code clean image mein copy
FROM python:3.12-slim
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY . .
EXPOSE 8000
CMD ["python", "app.py"]
```

### Size-Reduction Checklist

- `-slim` ya `-alpine` base images use karo (compiled languages ke liye distroless)
- `RUN` commands ko `&&` se combine karo, layers kam karne ke liye
- Package caches same `RUN` mein clean karo:
  ```dockerfile
  RUN apt-get update && apt-get install -y --no-install-recommends curl \
      && rm -rf /var/lib/apt/lists/*
  ```
- `.dockerignore` aggressively use karo
- Secrets ya large datasets `COPY` mat karo — runtime pe mount karo
- Build tools peeche chodne ke liye multi-stage karo

### BuildKit Cache Mounts (rebuilds fast karo)

```dockerfile
# syntax=docker/dockerfile:1.7
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
COPY . .
```
pip cache builds ke beech persist karta hai bina image mein gaye.

---

## 11. Environment Variables, Secrets & Config

### Env vars set karna

```bash
# Runtime pe (single)
docker run -e LOG_LEVEL=debug myapp

# File se
docker run --env-file .env myapp
```

`.env` file:
```
LOG_LEVEL=info
DATABASE_URL=postgres://...
```

Compose mein:
```yaml
services:
  api:
    environment:
      LOG_LEVEL: info
    env_file:
      - .env
```

### Secrets ko Image mein bake MAT karo

**Kabhi** mat karo:
```dockerfile
ENV DB_PASSWORD=supersecret   # ❌ image mein bake ho gaya, har koi dekh sakta hai
```

Iski jagah:
- Runtime pe `-e` / `--env-file` se pass karo
- Docker secrets (Swarm) ya secrets manager (AWS Secrets Manager, Vault) use karo
- Builds ke liye BuildKit `--secret`:

```dockerfile
# syntax=docker/dockerfile:1.7
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci
```

```bash
docker build --secret id=npmrc,src=$HOME/.npmrc -t myapp .
```

---

## 12. Healthchecks & Resource Limits

### Healthchecks

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -fsS http://localhost:8000/health || exit 1
```

`docker ps` `(healthy)` / `(unhealthy)` dikhayega, aur Compose `depends_on` iska wait kar sakta hai.

### Resource Limits

```bash
docker run -d \
  --cpus="1.5" \
  --memory="512m" \
  --memory-swap="512m" \
  --pids-limit=200 \
  myapp
```

Compose mein:
```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: "1.5"
          memory: 512M
        reservations:
          cpus: "0.5"
          memory: 256M
```

Limits ke bina ek runaway container pure host ko kha sakta hai. Production mein hamesha set karo.

---

## 13. Registries & Image Distribution

### Tag aur Push

```bash
# Registry ke liye tag karo
docker tag myapp:0.1 ghcr.io/myorg/myapp:0.1
docker tag myapp:0.1 ghcr.io/myorg/myapp:latest

# Login
docker login ghcr.io -u <user>

# Push
docker push ghcr.io/myorg/myapp:0.1
docker push ghcr.io/myorg/myapp:latest

# Anywhere se pull
docker pull ghcr.io/myorg/myapp:0.1
```

### Common Registries

- **Docker Hub** — `docker.io/<user>/<repo>` (host na do toh default)
- **GitHub Container Registry** — `ghcr.io/<org>/<repo>`
- **Amazon ECR** — `<acct>.dkr.ecr.<region>.amazonaws.com/<repo>`
- **Self-hosted** — Harbor, Nexus, Artifactory

### ECR Login (AWS)

```bash
aws ecr get-login-password --region ap-south-1 \
  | docker login --username AWS --password-stdin <acct>.dkr.ecr.ap-south-1.amazonaws.com
```

### Multi-Architecture Builds (amd64 + arm64)

Graviton ya Apple Silicon support ke liye:

```bash
docker buildx create --use --name multiarch
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t ghcr.io/myorg/myapp:0.1 \
  --push .
```

---

## 14. Containers Debug Karna

### Jab container start hi nahi ho raha

```bash
docker logs <container>                 # marne se pehle kya print kiya?
docker inspect <container> | less       # exit code, mounts, env, network
docker run --rm -it --entrypoint sh myapp:0.1   # entrypoint override karke andar jhako
```

### Jab container running hai par tooti hui hai

```bash
docker exec -it <container> sh          # shell le lo
docker exec <container> ps aux          # kaun se processes chal rahe?
docker exec <container> env             # kaun si env vars dikhti hain?
docker exec <container> netstat -tlnp   # kaun se ports pe listen kar raha hai?
docker stats <container>                # CPU/memory real time
```

### Jab shell hi nahi mil raha (distroless / scratch images)

```bash
# Target container ke namespace mein busybox mount karo
docker run -it --rm --pid container:<target> --net container:<target> \
  --cap-add SYS_PTRACE busybox sh
```

Ya ek "debug" variant rebuild karo `FROM gcr.io/distroless/...:debug` se.

### Exited container ka filesystem dekhna

```bash
docker commit <stopped-container> debug-snapshot
docker run -it --rm debug-snapshot sh
```

### "Local pe chal raha hai, CI/prod pe fail ho raha"

- Architecture mismatch (arm64 Mac pe built, amd64 pe deployed) → `buildx` multi-arch use karo
- Different env vars ya mounts → `docker inspect` se diff karo
- Jo image test ki ≠ jo deploy hui → digests check karo, sirf tags nahi

---

## 15. Best Practices

### Image Hygiene
- ✅ Base image versions pin karo (prod mein digests ideal)
- ✅ Minimal bases use karo (`-slim`, `-alpine`, distroless)
- ✅ Compiled languages ke liye multi-stage builds
- ✅ Ek image, ek concern (nginx + app + cron ek mein mat thoko)
- ✅ Regular rebuilds — base-image security patches ke liye

### Runtime Hygiene
- ✅ Non-root chalao:
  ```dockerfile
  RUN addgroup -S app && adduser -S app -G app
  USER app
  ```
- ✅ Jahan possible ho `--read-only` filesystem; `/tmp` ke liye tmpfs mount
- ✅ Capabilities drop karo: `--cap-drop=ALL --cap-add=NET_BIND_SERVICE`
- ✅ Resource limits set karo
- ✅ Healthchecks implement karo
- ✅ Long-running services ke liye `--restart unless-stopped`

### Build Hygiene
- ✅ Cache efficiency ke liye Dockerfile instructions order karo
- ✅ Context chhota rakhne ke liye `.dockerignore`
- ✅ Package managers ke liye BuildKit cache mounts
- ✅ `latest` aur specific version dono tag karo
- ✅ CVEs ke liye images scan karo (`docker scout`, `trivy`)

### Anti-patterns jo avoid karne hain
- ❌ Production mein `latest` tags
- ❌ Dockerfiles ya env defaults mein secrets
- ❌ Root pe chalana jab tak zaroori na ho
- ❌ Prod container ko `docker exec` se patch karna (rebuild karo)
- ❌ `host` networking jab tak really need na ho
- ❌ Ek Dockerfile jo build *aur* run dono karta hai (multi-stage use karo)

---

## 16. Cheat Sheet (Learning)

```bash
# Build & Run
docker build -t myapp:0.1 .
docker run -d -p 8000:8000 --name myapp myapp:0.1
docker run -it --rm ubuntu:24.04 bash

# Images
docker images
docker pull <image>
docker rmi <image>
docker image prune -a

# Containers
docker ps           # running
docker ps -a        # all
docker stop <name>
docker rm <name>
docker logs -f <name>
docker exec -it <name> sh
docker inspect <name>
docker stats

# Copy
docker cp <name>:/path/in/container ./local
docker cp ./local <name>:/path/in/container

# Volumes
docker volume create <name>
docker volume ls
docker volume rm <name>
docker run -v <name>:/path/in/container <image>

# Networks
docker network create <name>
docker network ls
docker network inspect <name>
docker run --network <name> <image>

# Compose
docker compose up -d
docker compose down
docker compose logs -f <service>
docker compose exec <service> sh
docker compose build
docker compose pull
docker compose ps

# Cleanup
docker system df             # disk usage
docker system prune          # dangling stuff hatao
docker system prune -a       # SAARI unused images bhi
docker system prune -a --volumes   # nuclear option

# Registries
docker login <registry>
docker tag <image> <registry>/<repo>:<tag>
docker push <registry>/<repo>:<tag>
```

---

## 17. DevOps/SRE Daily Operations

Yeh section operational layer hai jo zyada learning guides skip kar dete hain — production mein Docker chalate waqt aap actually kya karte ho: triage, cleanup, configuration, aur Kubernetes ki taraf bridge.

### 17.1 Hourly Use Hone Wali Triage Commands

Filter aur format aapke best friends hain. Default `docker ps` output real ops ke liye bahut noisy hai.

```bash
# Sirf crashed/exited containers, table format
docker ps -a --filter "status=exited" \
  --format "table {{.Names}}\t{{.Status}}\t{{.RunningFor}}"

# Name pattern se containers
docker ps --filter "name=api-" --format "{{.Names}}: {{.Status}}"

# Specific time window ke logs (sabse useful combo)
docker logs --since 15m --until 2m --timestamps --tail 500 <name>

# Sirf exit code + OOM flag (jq ki zaroorat nahi)
docker inspect <name> --format \
  '{{.State.ExitCode}} OOM={{.State.OOMKilled}} Err={{.State.Error}}'

# Daemon events ka live audit
docker events --since 1h --filter type=container --filter event=die

# Resource snapshot, scriptable
docker stats --no-stream --format \
  "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"

# Container ke andar top processes
docker top <name>
```

### 17.2 Container Exit Codes Padhna

Jab container marta hai, exit code bataata hai kahan dekhna chahiye.

| Code | Matlab | Kahan dekho |
|---|---|---|
| 0 | Clean exit | Supposed tha exit hona? Restart policy galat ho sakti hai |
| 1 | Generic app error | App logs |
| 125 | Docker daemon hi fail hua | `journalctl -u docker` |
| 126 | Command executable nahi | Permissions / shebang check karo image ke andar |
| 127 | Command not found | Galat CMD/ENTRYPOINT path |
| 137 | SIGKILL — almost always OOMKilled | `.State.OOMKilled` check karo, memory limit badhao |
| 139 | SIGSEGV — segfault | Native code crash, often arch mismatch |
| 143 | SIGTERM — graceful shutdown | Deploys/scale-down ke time expected |

Ek-line triage:
```bash
docker inspect <name> --format \
  'Exit={{.State.ExitCode}} OOM={{.State.OOMKilled}} StartedAt={{.State.StartedAt}} FinishedAt={{.State.FinishedAt}}'
```

### 17.3 Restart Policies Detail Mein

```bash
docker run --restart=<policy> ...
```

| Policy | Behavior | Kab use karo |
|---|---|---|
| `no` (default) | Kabhi restart nahi | One-shot jobs, debugging |
| `on-failure[:N]` | Sirf non-zero exit pe, max N baar | Batch jobs |
| `always` | Hamesha restart, daemon restart ke baad bhi | Long-running services |
| `unless-stopped` | `always` jaisa, par manual `docker stop` respect karta hai | **Services ke liye default yahi rakho** |

Current policy + restart count check karo:
```bash
docker inspect <name> --format \
  '{{.HostConfig.RestartPolicy.Name}} count={{.RestartCount}}'
```

Climbing `RestartCount` wala container aapka crash-loop alert signal hai.

### 17.4 Disk Management (#1 host incident)

`/var/lib/docker` bharne se hosts down ho jaate hain. Yeh commands yaad rakho:

```bash
# Disk kaha use ho raha hai
docker system df              # summary
docker system df -v           # per-image / per-container / per-volume breakdown

# Targeted cleanup (sabse safe pehle)
docker container prune -f                          # exited containers
docker image prune -f                              # sirf dangling images
docker image prune -af --filter "until=168h"       # 7 din se purani unused images
docker volume prune -f                             # unused volumes
docker builder prune -af --filter "until=72h"      # 3 din se purana build cache
docker network prune -f                            # unused networks

# Nuclear (DHYAN SE — volumes ke saath sab unused hata dega)
docker system prune -af --volumes
```

**Rule of thumb:** har Docker host pe daily cron schedule karo:
```bash
docker image prune -af --filter "until=168h"
docker builder prune -af --filter "until=72h"
```
Iske bina CI build hosts purani layers mein doob jaate hain.

Sabse badi images dhundo:
```bash
docker images --format "{{.Size}}\t{{.Repository}}:{{.Tag}}" | sort -h
```

### 17.5 Log Driver Configuration

Default driver `json-file` hai **rotation ke bina**. Busy container pe logs silently disk fill kar dete hain.

`/etc/docker/daemon.json` mein defaults set karo:

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "50m",
    "max-file": "5",
    "compress": "true"
  }
}
```

Daemon restart: `systemctl restart docker`. Nai containers naye defaults uthaengi; purani containers tab tak purani config rakhengi jab tak recreate na ho.

**Doosre useful drivers:**
- `awslogs` — CloudWatch ko directly bhejo
- `journald` — systemd handle kare
- `syslog` — rsyslog/fluentd ko forward
- `none` — disable (jab koi downstream collect kar raha ho)

Per-container override:
```bash
docker run --log-driver=awslogs \
  --log-opt awslogs-region=ap-south-1 \
  --log-opt awslogs-group=/app/api \
  --log-opt awslogs-stream=api-1 \
  myapp
```

### 17.6 `/etc/docker/daemon.json` — Daemon Configuration

Production hosts ke liye most-used keys:

```json
{
  "log-driver": "json-file",
  "log-opts": { "max-size": "50m", "max-file": "5" },
  "default-ulimits": {
    "nofile": { "Name": "nofile", "Hard": 1048576, "Soft": 1048576 }
  },
  "live-restore": true,
  "registry-mirrors": [],
  "insecure-registries": [],
  "storage-driver": "overlay2",
  "data-root": "/var/lib/docker"
}
```

Key options:
- `live-restore: true` — `dockerd` restart hone pe bhi containers chalti rahein (upgrades ke time huge win)
- `default-ulimits` — most "too many open files" errors yahin fix hote hain
- `data-root` — Docker ka data bigger disk pe move karo (jaise `/data/docker`)
- `registry-mirrors` — Docker Hub rate limits se bachne ke liye pull-through cache

Restart se pehle validate karo:
```bash
sudo dockerd --validate
sudo systemctl restart docker
```

### 17.7 Image Forensics

Jab image bahut badi ho ya pull slow ho, pata karo kyun:

```bash
# Layer-by-layer size + jisne layer banaya woh command
docker history --no-trunc --human <image>

# Summary
docker image inspect <image> --format \
  '{{.Architecture}} {{.Os}} {{.Size}} layers={{len .RootFS.Layers}}'

# Deeper analysis (alag se dive install karo)
dive <image>
```

`dive` wasted space dikhata hai — kisi layer mein add hue files jo baad ki layer mein delete ho gayi, woh bhi image bloat karti hain.

### 17.8 Image Scanning Workflow

Build → scan → push. CVE-laden images ECR mein mat push karo.

```bash
# Trivy (CI mein sabse common)
trivy image --severity HIGH,CRITICAL --exit-code 1 myapp:0.1

# Docker's built-in (Scout)
docker scout cves myapp:0.1
docker scout recommendations myapp:0.1

# Grype (alternative)
grype myapp:0.1 --fail-on high
```

`trivy image --exit-code 1 --severity HIGH,CRITICAL` ko push se pehle Jenkins stage mein wire karo — HIGH/CRITICAL CVE aate hi build fail ho jayegi.

### 17.9 CI mein Build Caching

Slow CI builds ka matlab usually cache reuse nahi ho raha runs ke beech.

**Inline cache (simple):**
```bash
docker build \
  --cache-from <ecr>/myapp:cache \
  --build-arg BUILDKIT_INLINE_CACHE=1 \
  -t <ecr>/myapp:0.1 \
  -t <ecr>/myapp:cache \
  --push .
```

**Buildx with registry cache (parallel/multi-arch ke liye best):**
```bash
docker buildx build \
  --cache-from type=registry,ref=<ecr>/myapp:cache \
  --cache-to   type=registry,ref=<ecr>/myapp:cache,mode=max \
  -t <ecr>/myapp:0.1 \
  --push .
```

`mode=max` intermediate layers bhi cache karta hai. Pehla build slow; baad ke saare fast.

Jenkins mein har agent pe ek baar builder setup karo:
```bash
docker buildx create --use --name ci-builder --driver docker-container || true
docker buildx inspect --bootstrap
```

### 17.10 ECR Daily Operations

**Token refresh** (ECR auth tokens 12 hours chalte hain):
```bash
aws ecr get-login-password --region ap-south-1 \
  | docker login --username AWS --password-stdin \
    <acct>.dkr.ecr.ap-south-1.amazonaws.com
```

Yeh har Jenkins pipeline ke pre-build stage mein wire karo.

**Repo banao (per service ek baar):**
```bash
aws ecr create-repository \
  --repository-name myapp \
  --image-scanning-configuration scanOnPush=true \
  --image-tag-mutability IMMUTABLE
```

`IMMUTABLE` tags CI (ya kisi ko bhi) `v1.2.3` overwrite karne se rokte hain — reproducible deploys ke liye essential.

**Lifecycle policy** (purani images auto-delete, ECR storage forever na badhe):

```json
{
  "rules": [
    {
      "rulePriority": 1,
      "description": "Last 20 tagged images rakho",
      "selection": {
        "tagStatus": "tagged",
        "tagPatternList": ["v*"],
        "countType": "imageCountMoreThan",
        "countNumber": 20
      },
      "action": { "type": "expire" }
    },
    {
      "rulePriority": 2,
      "description": "7 din ke baad untagged expire karo",
      "selection": {
        "tagStatus": "untagged",
        "countType": "sinceImagePushed",
        "countUnit": "days",
        "countNumber": 7
      },
      "action": { "type": "expire" }
    }
  ]
}
```

**Pull-through cache** — ECR Docker Hub / Quay / GHCR ko proxy kar sakta hai aur results cache kar sakta hai, jisse fleet-wide Docker Hub rate limits fix ho jaati hain.

### 17.11 Graviton ke liye Multi-Arch (r8g, c8g, m8g)

Agar nodes arm64 hain par builders amd64 hain, toh pods `exec format error` se fail honge. Multi-arch build karo:

```bash
docker buildx create --use --name multiarch --driver docker-container
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t <ecr>/myapp:0.1 \
  --cache-to   type=registry,ref=<ecr>/myapp:cache,mode=max \
  --cache-from type=registry,ref=<ecr>/myapp:cache \
  --push .
```

Verify karo dono manifests aaye:
```bash
docker buildx imagetools inspect <ecr>/myapp:0.1
# linux/amd64 AUR linux/arm64 dono dikhne chahiye
```

### 17.12 Docker → Kubernetes Mental Map

Agar destination Kubernetes hai (RKE2, EKS, etc.), yeh mapping jump easy bana deta hai:

| Docker concept | Kubernetes equivalent |
|---|---|
| `docker run <image>` | Pod with one container |
| Container | Container inside a Pod (Pods can have many) |
| `docker run -d --restart=always` | Deployment (`replicas: N`) |
| `docker stop <name>` | `kubectl delete pod <name>` |
| `docker logs <name>` | `kubectl logs <pod>` |
| `docker exec -it <name> sh` | `kubectl exec -it <pod> -- sh` |
| `docker inspect <name>` | `kubectl describe pod <pod>` + `kubectl get pod <pod> -o yaml` |
| User-defined network + DNS | Service (ClusterIP) + CoreDNS |
| `-p 8080:80` | Service (NodePort/LoadBalancer) ya Ingress |
| Named volume | PersistentVolumeClaim → PersistentVolume |
| `--env-file` | ConfigMap / Secret env ya file ke roop mein mount |
| `HEALTHCHECK` | `livenessProbe` / `readinessProbe` / `startupProbe` |
| `--cpus --memory` | `resources.requests` / `resources.limits` |
| Docker Compose stack | Deployments + Services + ConfigMaps ka bundle |
| Registry login | `imagePullSecrets` (ya ECR ke liye IRSA / node IAM) |
| `--restart=unless-stopped` | Deployment ka default behavior |
| `docker events` | `kubectl get events --sort-by=.lastTimestamp` |

**Ek difference jo logon ko bites karta hai:** Docker mein aap user-defined network pe doosre containers ko container name se address karte ho. Kubernetes mein *Service* name se address karte ho, Pod name se nahi — Pods cattle hain, Services stable DNS hain.

### 17.13 Triage Runbook — Common Incidents

**"Container baar-baar restart ho raha hai"**
```bash
docker inspect <name> --format \
  '{{.State.ExitCode}} OOM={{.State.OOMKilled}} restarts={{.RestartCount}}'
docker logs --tail 200 <name>
# OOMKilled=true  → --memory badhao ya leak fix karo
# Exit=137, OOM=false → bahar se SIGKILL (orchestrator?)
# Exit=1           → app bug, logs check karo
```

**"Docker host pe disk full hai"**
```bash
docker system df -v | head -50
docker builder prune -af --filter "until=72h"
docker image prune -af --filter "until=168h"
docker container prune -f
# Abhi bhi full? Log rotation configured nahi:
du -sh /var/lib/docker/containers/*/*.log 2>/dev/null | sort -h | tail
```

**"Image run nahi ho rahi — exec format error"**
```bash
docker image inspect <image> --format '{{.Architecture}}'
uname -m   # host pe
# Mismatch → buildx se multi-arch rebuild karo
```

**"Image pull nahi ho rahi — ECR auth"**
```bash
# Token expire ho gaya (12h)
aws ecr get-login-password --region ap-south-1 \
  | docker login --username AWS --password-stdin <acct>.dkr.ecr.ap-south-1.amazonaws.com
docker pull <ecr>/<image>:<tag>
```

**"Container doosre container ko reach nahi kar pa raha"**
```bash
docker network inspect <network>
# Dono containers attached hain? Same network pe?
docker exec <name> getent hosts <other-name>
docker exec <name> nc -zv <other-name> <port>
```

**"Image bahut badi hai"**
```bash
docker history --no-trunc --human <image>
dive <image>
# Dhundo: package caches clean nahi hue, final stage mein build tools,
#         secrets COPY ho gaye, large datasets baked in
```

**"Local pe chalti hai par prod pe fail hoti hai"**
```bash
# Image digests compare karo, tags nahi
docker image inspect <image>:<tag> --format '{{index .RepoDigests 0}}'
# Same arch aur same env confirm karo
docker inspect <name> --format '{{.Config.Env}}'
```

### 17.14 Operator's Cheat Sheet

(Yeh §16 se alag hai — woh Docker *seekhne* ke liye tha; yeh Docker *chalane* ke liye hai.)

```bash
# === TRIAGE ===
docker ps -a --filter "status=exited" --format "table {{.Names}}\t{{.Status}}"
docker logs --since 15m --until 2m --timestamps --tail 500 <name>
docker inspect <name> --format '{{.State.ExitCode}} OOM={{.State.OOMKilled}} Restarts={{.RestartCount}}'
docker events --since 1h --filter type=container --filter event=die
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
docker top <name>

# === DISK ===
docker system df -v
docker image prune   -af --filter "until=168h"
docker builder prune -af --filter "until=72h"
docker container prune -f
docker volume prune    -f

# === IMAGE FORENSICS ===
docker history --no-trunc --human <image>
docker image inspect <image> --format '{{.Architecture}} {{.Size}}'
dive <image>
trivy image --severity HIGH,CRITICAL <image>

# === ECR ===
aws ecr get-login-password --region ap-south-1 \
  | docker login --username AWS --password-stdin <acct>.dkr.ecr.ap-south-1.amazonaws.com
docker buildx imagetools inspect <ecr>/<image>:<tag>

# === BUILD (CI, multi-arch) ===
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --cache-from type=registry,ref=<ecr>/<image>:cache \
  --cache-to   type=registry,ref=<ecr>/<image>:cache,mode=max \
  -t <ecr>/<image>:<version> \
  --push .

# === DAEMON ===
sudo systemctl status docker
sudo journalctl -u docker -n 200 --no-pager
sudo cat /etc/docker/daemon.json
sudo dockerd --validate
```

---

## Daily Revision (7-Day Rotation)

Har din 5–10 minute spend karo apne day ke topic pe. Saare 7 din cycle karke phir Day 1 se restart. Yeh **concept aur gotcha review** hai. Niche jo Commands Daily Drill hai woh muscle-memory ka companion hai.

### Day 1 — Docker Kya Hai + Core Concepts + Images

**Recall (bina dekhe answer karne ki koshish karo):**
1. Container aur VM mein ek line ka difference?
2. Dockerfile → Image → Container ka relationship?
3. "Layer" ka matlab kya hai, aur Dockerfile instructions ka order kyun important hai?
4. `latest` kya hai aur prod mein kyun nahi use karna?
5. Digest pin (`@sha256:...`) tag se kya extra deta hai?

**Yaad rakhne wali mappings:**
- Dockerfile = recipe (instructions)
- Image = compiled snapshot (read-only)
- Container = image ka running instance
- Registry = jaha images store hote hain (Docker Hub, ECR, GHCR)

**Gotchas:**
- Tags mutable hote hain — aaj ka `myapp:v1.2.3` kal wala same nahi hoga zaroori. Digests immutable hain.
- `latest` ka matlab "newest" nahi hai — yeh sirf default tag hai jab koi specify nahi karta.
- Har Dockerfile instruction = ek layer = ek cache point. Order = cache efficiency.

---

### Day 2 — Containers (Lifecycle, Logs, Exec, Inspect)

**Recall:**
1. `docker stop` aur `docker kill` mein difference?
2. `docker stop` pehle kya signal bhejta hai? Kitne second baad escalate karta hai?
3. `docker run -it` aur `docker exec -it` mein difference?
4. `--rm` kya karta hai?
5. Running container se host pe file kaise copy karte hain?

**Lifecycle yaad karo:**
```
run    = create + start
stop   = SIGTERM, 10s baad SIGKILL
kill   = SIGKILL turant
restart= stop + start
rm     = delete (stopped hona chahiye)
```

**Gotchas:**
- `docker run` hamesha NAYA container banata hai. Existing ko restart karna ho toh `docker start` use karo.
- Stopped container abhi bhi exist karta hai (aur disk leta hai). `docker ps -a` se dikhega.
- `--rm` ke bina, har `docker run` ek dead container chhod jaata hai jo disk fill karta jaata hai.

---

### Day 3 — Dockerfile Basics

**Recall:**
1. CMD aur ENTRYPOINT mein difference?
2. Yeh order kyun important hai:
   ```
   COPY . .
   RUN pip install -r requirements.txt
   ```
   vs
   ```
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   ```
3. `EXPOSE 8000` actually port publish karta hai?
4. `COPY` aur `ADD` mein difference?
5. `.dockerignore` kya karta hai?

**Instruction roles yaad karo:**
| Instruction | Role |
|---|---|
| FROM | Base image (pehli line) |
| WORKDIR | Working directory set + create |
| COPY | Files image mein copy karo |
| RUN | BUILD time pe execute (layer banata hai) |
| CMD | Default command (override ho sakta hai) |
| ENTRYPOINT | Fixed command (CMD uske args banta hai) |
| EXPOSE | Sirf documentation — publish nahi karta |
| ENV | Environment variables set karo |
| ARG | Build-time variable |
| USER | User switch karo (default root — bura hai) |

**Gotchas:**
- `EXPOSE` sirf metadata hai. Ports tabhi publish hote hain jab `docker run` mein `-p` lagao.
- Default root ke aur security risk hai. Niche `USER` add karo.
- `ADD` archives auto-extract karta hai — predictability ke liye `COPY` better.

---

### Day 4 — Volumes + Networking

**Recall:**
1. Teen mount types aur har ek kis ke liye best?
2. Default `bridge` network containers ke beech DNS kyun nahi deta?
3. `-p 8080:80` aur `-p 127.0.0.1:8080:80` mein difference?
4. `docker volume prune` kya delete karta hai?
5. Different user-defined networks pe do containers ek dusre ko reach kar sakte hain?

**Volume types:**
| Type | Use |
|---|---|
| Named volume (`-v pgdata:/path`) | Persistent app data, Docker-managed |
| Bind mount (`-v $(pwd):/path`) | Dev mode, live code reload |
| tmpfs (`--tmpfs /tmp`) | In-memory, ephemeral, fast |

**Gotchas:**
- Default `bridge` = containers ke beech DNS nahi. Hamesha user-defined network banao.
- Bind mount `:ro` se container ke andar read-only ho jaata hai (host abhi bhi likh sakta hai).
- Alag networks pe containers ek dusre ko reach nahi kar sakte jab tak dono pe explicitly connect na ho.

---

### Day 5 — Compose + Multi-stage + Env/Secrets

**Recall:**
1. Compose file mein services ek dusre ko kaise dhundhte hain?
2. `docker compose down` aur `docker compose down -v` mein difference?
3. Multi-stage builds kya problem solve karte hain?
4. `ENV DB_PASSWORD=secret` Dockerfile mein kyun bura idea hai?
5. BuildKit `--secret` flag kis liye hai?

**Compose mental model:** multi-container app ka *state* declare karta hai. Services ek dusre ko *service name* se reach karte hain auto-created network pe.

**Multi-stage pattern:**
```
Stage 1 (builder): bada base, compile/install
Stage 2 (final):   chhota base, COPY --from=builder sirf artifact
```

**Gotchas:**
- `docker compose down` containers + networks remove karta hai; volumes bachte hain. `-v` se volumes bhi delete.
- Build args (`ARG`) aur `ENV` build mein set kiye, `docker history` mein visible. Secrets kabhi waha mat daalo.
- BuildKit secrets (`RUN --mount=type=secret`) build ke time available hote hain par kisi bhi layer mein nahi jaate.

---

### Day 6 — Healthchecks + Resources + Registries + Multi-arch

**Recall:**
1. `HEALTHCHECK` fail hone pe Docker kya karta hai?
2. `--memory` limit lagane ka sabse common reason?
3. `--memory` aur `--memory-swap` mein difference?
4. ECR login token kyun expire hota hai, aur kitni baar?
5. Ek hi image jo amd64 aur arm64 dono pe chale, kaise banate hain?

**Health states:** `starting` → `healthy` / `unhealthy`. Compose ka `depends_on: condition: service_healthy` iska wait karta hai.

**Resource limits:**
| Flag | Limit cross hone pe |
|---|---|
| `--cpus` | Throttled (killed nahi) |
| `--memory` | OOMKilled (exit 137) |
| `--pids-limit` | Naye process create fail |

**Multi-arch one-liner:**
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t <ecr>/myapp:0.1 --push .
```

**Gotchas:**
- ECR tokens har 12h mein expire. CI ko har run pe refresh karna padta hai.
- amd64 Mac/CI pe build aur Graviton (arm64) pe deploy buildx ke bina = `exec format error`.
- Multi-arch build ka `docker push` `buildx` ke saath `--push` se hota hai; baad mein `docker push` galat hai.

---

### Day 7 — DevOps/SRE Daily Operations

**Recall:**
1. Exit code 137 ka matlab? 139? 143?
2. Docker host ka disk fill hone ka sabse common reason?
3. Daemon log driver kahaan configure hota hai?
4. `live-restore: true` kya karta hai?
5. Image itni badi kis Dockerfile instruction ne banayi, kaise pata kare?

**Exit codes:**
| Code | Meaning |
|---|---|
| 0 | Clean exit |
| 1 | Generic app error |
| 125 | Docker daemon fail |
| 126 | Command executable nahi |
| 127 | Command not found |
| 137 | SIGKILL (usually OOMKilled) |
| 139 | SIGSEGV (segfault) |
| 143 | SIGTERM (graceful shutdown) |

**Production ke liye daemon.json mein zaroori:**
- `log-opts: max-size, max-file` (rotation — iske bina logs disk fill kar dete hain)
- `live-restore: true` (daemon restart pe containers chalte rahein)
- `default-ulimits.nofile` ("too many open files" rokne ke liye)

**Gotchas:**
- Default log driver `json-file` mein rotation NAHI hai. Hosts `/var/lib/docker/containers/*/*.log` fill hone se mar jaate hain.
- `docker system prune -af --volumes` SAARE unused volumes delete karta hai — including jo aap shayad rakhna chahte ho. Targeted prunes use karo.
- `docker history` layer commands AUR sizes dikhata hai — bloat ka culprit usually obvious hota hai.

---

## Commands Daily Drill (Sirf Muscle Memory)

Daily Revision concepts test karta hai. **Yeh section ungliyon ko test karta hai.** Har command real cluster/host mein memory se type karo (ya `--dry-run` use karo agar actually nahi banana). Pehle explanations dhako, commands se yaad karo kya karta hai. Phir commands dhako, scenarios padho, command memory se type karo.

Goal: jab 2am pe incident aaye, dimag ke pehle haath sahi command type kar dein.

### Drill Day 1 — Images

```bash
docker pull python:3.12-slim                                           # download
docker images                                                          # local images list
docker images --format "{{.Size}}\t{{.Repository}}:{{.Tag}}" | sort -h # size se sort
docker inspect python:3.12-slim                                        # full metadata
docker history --no-trunc --human python:3.12-slim                     # layer-by-layer
docker image inspect python:3.12-slim --format '{{.Architecture}} {{.Size}}'
docker rmi nginx:1.25                                                  # ek delete
docker image prune -f                                                  # dangling delete
docker image prune -af --filter "until=168h"                           # 7d+ unused delete
docker tag myapp:0.1 <ecr>/myapp:0.1                                   # registry ke liye re-tag
```

**Scenario → command:**
- "Yeh image 2GB kyun hai?" → `docker history --no-trunc --human <image>`
- "Yeh image kis arch ke liye bani hai?" → `docker image inspect <image> --format '{{.Architecture}}'`
- "Saari ek hafte se nahi use ki images saaf karo" → `docker image prune -af --filter "until=168h"`

---

### Drill Day 2 — Containers

```bash
docker run -d -p 8080:80 --name web nginx                              # detached + port + name
docker run -it --rm ubuntu:24.04 bash                                  # interactive + auto-cleanup
docker run --restart=unless-stopped -d --name api myapp:0.1            # production restart policy
docker ps                                                              # running
docker ps -a                                                           # sab (stopped sahit)
docker ps -a --filter "status=exited" --format "table {{.Names}}\t{{.Status}}"
docker stop <name>                                                     # SIGTERM, 10s, SIGKILL
docker kill <name>                                                     # immediate
docker restart <name>
docker rm <name>                                                       # stopped delete
docker rm -f <name>                                                    # force (kill + delete)
docker logs <name>                                                     # saare logs
docker logs --tail 200 --since 15m --timestamps <name>                 # windowed
docker logs -f <name>                                                  # follow
docker exec -it <name> sh                                              # shell andar
docker exec <name> env                                                 # one-shot
docker inspect <name>                                                  # full state
docker inspect <name> --format '{{.State.ExitCode}} {{.State.OOMKilled}}'
docker top <name>                                                      # andar ke processes
docker stats --no-stream                                               # CPU/mem snapshot
docker port <name>                                                     # port mappings
docker cp ./file <name>:/path                                          # andar copy
docker cp <name>:/path ./file                                          # bahar copy
```

**Scenario → command:**
- "Container mar gaya — OOMKilled tha?" → `docker inspect <name> --format '{{.State.OOMKilled}}'`
- "Last 5 minutes ke logs timestamps ke saath" → `docker logs --since 5m --timestamps <name>`
- "Crashed containers list karo, naam + status" → `docker ps -a --filter "status=exited" --format "table {{.Names}}\t{{.Status}}"`

---

### Drill Day 3 — Build & Dockerfile

```bash
docker build -t myapp:0.1 .                                            # tag ke saath build
docker build -t myapp:0.1 -f Dockerfile.prod .                         # custom Dockerfile
docker build --no-cache -t myapp:0.1 .                                 # cache ignore
docker build --target builder -t myapp:builder .                       # ek stage tak ruko
docker build --build-arg VERSION=1.2 -t myapp:0.1 .                    # build arg
docker build --secret id=npmrc,src=$HOME/.npmrc -t myapp:0.1 .         # BuildKit secret
DOCKER_BUILDKIT=1 docker build -t myapp:0.1 .                          # BuildKit force
docker buildx create --use --name multiarch                            # multi-arch builder
docker buildx build --platform linux/amd64,linux/arm64 -t <ecr>/myapp:0.1 --push .
docker buildx build \
  --cache-from type=registry,ref=<ecr>/myapp:cache \
  --cache-to   type=registry,ref=<ecr>/myapp:cache,mode=max \
  -t <ecr>/myapp:0.1 --push .
docker buildx imagetools inspect <ecr>/myapp:0.1                       # multi-arch manifest verify
```

**Scenario → command:**
- "CI builds slow hain kyunki har run pe cache jaata hai" → buildx `--cache-from/--cache-to type=registry`
- "Graviton ke liye bhi build karo" → `docker buildx build --platform linux/amd64,linux/arm64 ... --push`
- "Builder stage tak ruk ke debug karna" → `docker build --target builder -t debug .` phir `docker run -it debug sh`

---

### Drill Day 4 — Volumes & Networks

```bash
docker volume create pgdata
docker volume ls
docker volume inspect pgdata
docker volume rm pgdata
docker volume prune -f                                                 # unused remove
docker run -d -v pgdata:/var/lib/postgresql/data postgres:16           # named volume
docker run -d -v $(pwd):/app:ro myapp                                  # bind mount (RO)
docker run --tmpfs /tmp:size=100M myapp                                # tmpfs

docker network create app-net
docker network ls
docker network inspect app-net
docker run -d --name db --network app-net postgres:16
docker run -d --name api --network app-net myapi:0.1                   # api "db" resolve kar sakta hai
docker network connect app-net <existing-container>
docker network disconnect app-net <container>
docker network prune -f
```

**Scenario → command:**
- "Postgres data container delete hone ke baad bhi rehna chahiye" → named volume `-v pgdata:/var/lib/postgresql/data`
- "Do containers ko DNS se baat karni hai" → user-defined network banao, dono attach karo
- "Worker pod ke liye quick scratch space" → `--tmpfs /tmp:size=100M`

---

### Drill Day 5 — Compose

```bash
docker compose up -d                                                   # stack start (detached)
docker compose up -d --build                                           # rebuild + start
docker compose down                                                    # stop + remove
docker compose down -v                                                 # ...volumes bhi delete
docker compose ps                                                      # stack status
docker compose logs -f <service>                                       # ek service ke logs follow
docker compose logs --tail 200 <service>
docker compose exec <service> sh                                       # service mein shell
docker compose run --rm <service> <cmd>                                # one-off command
docker compose restart <service>
docker compose pull                                                    # base images update
docker compose build <service>                                         # ek rebuild
docker compose config                                                  # validate + resolved YAML
docker compose -f compose.yaml -f compose.prod.yaml up -d              # multiple overrides
```

**Scenario → command:**
- "Dev DB ke khilaaf ek one-off migration run karo" → `docker compose run --rm api python manage.py migrate`
- "Dev environment poora reset karo" → `docker compose down -v && docker compose up -d --build`
- "Mera compose file validate karo" → `docker compose config`

---

### Drill Day 6 — Registries & ECR

```bash
docker login ghcr.io -u <user>
docker login                                                           # Docker Hub
aws ecr get-login-password --region ap-south-1 \
  | docker login --username AWS --password-stdin <acct>.dkr.ecr.ap-south-1.amazonaws.com
docker tag myapp:0.1 <acct>.dkr.ecr.ap-south-1.amazonaws.com/myapp:0.1
docker push <acct>.dkr.ecr.ap-south-1.amazonaws.com/myapp:0.1
docker pull <acct>.dkr.ecr.ap-south-1.amazonaws.com/myapp:0.1

aws ecr create-repository --repository-name myapp \
  --image-scanning-configuration scanOnPush=true \
  --image-tag-mutability IMMUTABLE --region ap-south-1
aws ecr list-images --repository-name myapp --region ap-south-1
aws ecr describe-images --repository-name myapp --region ap-south-1 \
  --query 'sort_by(imageDetails,& imagePushedAt)[*].[imageTags[0],imagePushedAt,imageSizeInBytes]' \
  --output table

# Scan
trivy image --severity HIGH,CRITICAL --exit-code 1 myapp:0.1
docker scout cves myapp:0.1
```

**Scenario → command:**
- "ECR token expire ho gaya" → `aws ecr get-login-password ... | docker login --password-stdin ...`
- "CVEs mile toh CI block ho" → `trivy image --severity HIGH,CRITICAL --exit-code 1 <image>`
- "Is ECR repo mein kaunsi images hain, date se sorted?" → upar wala `aws ecr describe-images` query

---

### Drill Day 7 — Operations (Triage, Disk, Daemon)

```bash
# Triage
docker ps -a --filter "status=exited" --format "table {{.Names}}\t{{.Status}}\t{{.RunningFor}}"
docker logs --since 15m --until 2m --timestamps --tail 500 <name>
docker inspect <name> --format 'Exit={{.State.ExitCode}} OOM={{.State.OOMKilled}} Restarts={{.RestartCount}}'
docker events --since 1h --filter type=container --filter event=die
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
docker top <name>

# Disk
docker system df
docker system df -v                                                    # per-image/container/volume
docker container prune -f
docker image prune -af --filter "until=168h"
docker builder prune -af --filter "until=72h"
docker volume prune -f
docker network prune -f
docker system prune -af --volumes                                      # nuclear — dhyaan se

# Daemon
sudo systemctl status docker
sudo journalctl -u docker -n 200 --no-pager
sudo cat /etc/docker/daemon.json
sudo dockerd --validate                                                # config check

# Image forensics
docker history --no-trunc --human <image>
dive <image>                                                           # interactive layer explorer
```

**Scenario → command:**
- "Docker host pe disk full" → `docker system df -v` → targeted prunes (builder, image, container)
- "Container <X> kal raat 03:00 pe kyun restart hua?" → `docker events --since 12h --filter container=<X>`
- "Container baar baar OOMKill ho raha — confirm karo" → `docker inspect <name> --format '{{.State.OOMKilled}}'`
- "Config change ke baad daemon healthy hai check karo" → `sudo dockerd --validate && sudo systemctl status docker`

---

### Drills Kaise Use Kare

**Beginner (week 1):** har command exactly jaise likha hai waise type karo. Explanation padho. Memorize abhi nahi.

**Intermediate (week 2–3):** explanation dhako. Command dekho, yaad karo kya karta hai. Phir reverse: command dhako, scenario padho, memory se type karo.

**Advanced (week 4+):** commands chain karo. "Scenario → command" pairs ke liye, ek one-line pipeline likho jo poora solve kare (action trigger + result verify).

**Weekly self-test:** har day se ek command randomly pick karo. Bina dekhe type karo. Jo fumble ho rahi ho woh kal ki drill hai.

---

## Aage Kya Seekhein

Jab yeh sab comfortable lagne lage, toh next natural steps:

- **Container security** — image scanning (trivy, grype), runtime policies (Falco), rootless Docker
- **Kubernetes** — Docker ke concepts (image, container, network, volume) directly k8s mein map hote hain (Pod, container, Service, PersistentVolume)
- **CI/CD integration** — Jenkins/GitHub Actions mein images build karna, ECR/GHCR pe push, cosign se signing
- **Observability** — structured JSON logs, Prometheus metrics endpoints, OpenTelemetry tracing
- **Image promotion** — dev → staging → prod by digest, tag se nahi

Agar aapne ek multi-service Compose stack ship kar di hai healthchecks, multi-stage builds, non-root users, pinned versions, aur clean `.dockerignore` ke saath — toh aap firmly "mid-level" pe hain aur production work + Kubernetes ke liye ready ho.

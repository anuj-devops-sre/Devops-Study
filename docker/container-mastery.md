# 🐳 Docker & Container Mastery: The SRE Way

Containers are the unit of deployment in modern SRE. For a Mid-level role, you must know how to build **Secure, Lightweight, and Optimized** images.

## 1. Multi-Stage Builds (The "Diet" Plan)
Don't ship your compilers and build tools to production.
```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY . .
RUN npm install && npm run build

# Stage 2: Production
FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```
**Impact**: Reduces image size from 1GB to ~50MB. Faster deployments.

## 2. Best Practices for Smaller Layers
- **Combine Commands**: Use `&&` to reduce the number of layers.
- **Specific Tags**: Never use `:latest`. Always use specific versions (e.g., `node:18.16-alpine`).
- **.dockerignore**: Exclude `node_modules`, `.git`, and `Dockerfile` from the build context.

## 3. SRE Security (Shift Left)
- **Non-Root User**: Never run containers as `root`.
- **Scan for Vulnerabilities**: Use **Trivy** to scan images in your CI/CD.
  ```bash
  trivy image my-app:v1.0
  ```
- **Distroless Images**: Use base images that contain only your app and its dependencies (No shell, no package manager).

## 4. Layer Caching (Speed Up CI/CD)
The order of commands matters.
```dockerfile
# BAD: Any change in code invalidates npm install cache
COPY . .
RUN npm install

# GOOD: npm install cache is invalidated ONLY if package.json changes
COPY package.json package.json
RUN npm install
COPY . .
```

## 5. SRE Troubleshooting (Inside the container)
- **Check Logs**: `docker logs -f <container_id>`
- **Execute into Shell**: `docker exec -it <container_id> sh`
- **Inspect Resource Usage**: `docker stats`

---

## 🏠 How to test Containers on Localhost?
Use **Docker Compose** to run entire stacks.

1.  **Run multiple services**:
    ```bash
    docker-compose up --build
    ```
2.  **Simulation**: Use this to see how your backend, frontend, and DB interact before moving to Kubernetes.

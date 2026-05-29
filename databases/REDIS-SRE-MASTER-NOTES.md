# 🗄️ DISTRIBUTED CACHING (REDIS) SRE GUIDE

For a Mid-level SRE, scaling databases means using **Caching**. Redis is the industry standard for high-performance, distributed caching.

---

## 1. Why Redis?
- **Speed**: In-memory data store (Sub-millisecond latency).
- **Scalability**: Decouples the DB from read-heavy traffic.
- **Reliability**: Persistence via RDB/AOF.

## 2. Redis Architectures
- **Single Node**: For caching only, no HA.
- **Primary-Replica**: Read replicas for scaling reads.
- **Redis Sentinel**: High Availability (Automatic failover).
- **Redis Cluster**: Horizontal scaling (Partitioning/Sharding).

## 3. Common SRE Use Cases
- **Session Store**: Store user sessions for fast access.
- **API Rate Limiting**: Limit how many requests a user can make per second.
- **Message Broker**: Using Redis Pub/Sub for microservices.
- **Database Offloading**: Storing the results of complex SQL queries.

## 4. SRE Performance Checklist
- **Eviction Policies**: `volatile-lru` or `allkeys-lru` (What happens when memory is full?).
- **Memory Fragmentation**: Monitoring the `mem_fragmentation_ratio`.
- **Latency Monitoring**: Using `SLOWLOG` to find performance bottlenecks.

## 5. Localhost Testing (Docker)
```bash
docker run -p 6379:6379 redis:latest
# Verify
redis-cli ping
```

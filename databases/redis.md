# 🚩 Redis: Caching & Message Brokering

## 🌟 Introduction
Redis (Remote Dictionary Server) is an in-memory data structure store, used as a database, cache, and message broker.

## 🟢 Level 0: Basics
- **Data Types:** Strings, Lists, Sets, Hashes.
- **Commands:**
  - `SET key value`
  - `GET key`
  - `EXPIRE key 60` (Set TTL)

## 🟡 Level 1: DevOps Operations
- **Persistence:**
  - **RDB (Redis Database):** Point-in-time snapshots.
  - **AOF (Append Only File):** Logs every write operation.
- **Memory Management:** `maxmemory` and eviction policies (LRU, LFU).

## 🟠 Level 2: Scalability (Mid-Level SRE)
- **Redis Sentinel:** High availability and automatic failover.
- **Redis Cluster:** Horizontal scaling via sharding.
- **Use Cases:** Session storage, Rate limiting, Leaderboards.

## 🛠️ Lab
Run redis locally: `docker run -d --name redis-lab -p 6379:6379 redis:latest`

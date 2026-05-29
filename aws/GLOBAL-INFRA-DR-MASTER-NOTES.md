# 🌍 GLOBAL INFRA & DISASTER RECOVERY MASTER GUIDE

A Mid-level SRE must think globally. This guide covers **Multi-region Availability, DNS SRE, and High Availability**.

---

## 1. Route53 (The SRE's DNS)
DNS is not just about domain names; it's about **Traffic Routing**.
- **Simple Routing**: 1 domain -> 1 IP.
- **Failover Routing**: Route to a secondary region if the primary is down (Active-Passive).
- **Latency Routing**: Route users to the AWS region with the lowest latency.
- **Weighted Routing**: Route traffic to different versions (e.g., 20% to New App, 80% to Old).

## 2. Load Balancing at Scale
- **Global Accelerator**: Uses the AWS Global Network (Anycast IP) to route traffic to the nearest healthy endpoint. Reduces jitter and latency.
- **CloudFront (CDN)**: Caching content at the "Edge" (near the user). Essential for performance.

## 3. Disaster Recovery (DR) Strategies
Recruiters will ask about **RTO (Recovery Time Objective)** and **RPO (Recovery Point Objective)**.
- **Backup & Restore**: (High RTO/RPO) - Cold backup, restore when needed.
- **Pilot Light**: (Medium RTO/RPO) - Core data is live; app servers are off.
- **Warm Standby**: (Low RTO/RPO) - Scaled-down version of the app is always running.
- **Multi-Site (Active-Active)**: (Near Zero RTO/RPO) - Full traffic served from multiple regions simultaneously.

## 4. Database High Availability
- **RDS Multi-Region Read Replicas**: Promoting a replica to "Master" in another region during a disaster.
- **DynamoDB Global Tables**: Multi-master, multi-region replication.

## 5. SRE Checklist for HA
1. **Health Checks**: Always configure Route53 health checks.
2. **Chaos Engineering**: Intentionally shutting down a region to see if failover works.
3. **Automated Rollback**: If a global deployment fails, can you revert in <60 seconds?

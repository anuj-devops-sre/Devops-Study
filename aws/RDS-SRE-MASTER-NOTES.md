# 🗄️ RDS & Databases SRE MASTER NOTES

Managed Reliability for Data.

## 1. HA & Performance
- **Multi-AZ**: Synchronous replication for Failover.
- **Read Replicas**: Asynchronous for Scaling.
- **Aurora**: Cloud-native (6 copies of data).

## 2. Backup & Monitoring
- **Snapshots**: Point-in-time recovery.
- **Performance Insights**: Find slow queries.

## 3. Local Testing
```bash
docker run -p 5432:5432 postgres
```

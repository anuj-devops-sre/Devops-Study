# 🗄️ PostgreSQL for DevOps (Zero to Mid-Level)

## 🌟 Introduction
PostgreSQL is a powerful, open-source object-relational database system. In SRE, it's the gold standard for reliable persistent storage.

## 🟢 Level 0: Basics
- **Installation:** `apt install postgresql`
- **CLI (psql):**
  - `psql -U postgres` (Enter shell)
  - `\l` (List databases)
  - `\c dbname` (Connect to db)
  - `\dt` (List tables)

## 🟡 Level 1: Maintenance (Junior DevOps)
- **Backup & Restore:**
  - `pg_dump dbname > backup.sql`
  - `psql dbname < backup.sql`
- **Users & Permissions:**
  ```sql
  CREATE USER anuj WITH PASSWORD 'secure';
  GRANT ALL PRIVILEGES ON DATABASE mydb TO anuj;
  ```

## 🟠 Level 2: High Availability & SRE (Mid-Level)
- **WAL (Write Ahead Logging):** Critical for crash recovery.
- **Replication:**
  - **Streaming Replication:** Master-Slave setup for read scaling.
  - **Logical Replication:** Fine-grained data sync.
- **Connection Pooling:** Using **PgBouncer** to handle thousands of connections.
- **Monitoring:** Key metrics (Cache hit ratio, Long-running queries, Connection counts).

## 🛠️ Hands-on Lab
Check out the `projects/01-docker-3tier-app` to see Postgres in action with a backend.

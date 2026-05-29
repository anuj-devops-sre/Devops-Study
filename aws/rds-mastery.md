# 🗄️ RDS & Database SRE: Beyond the Query

Relational Database Service (RDS) handles the "undifferentiated heavy lifting" of database management. For an SRE, it's about **Availability, Performance tuning, and Disaster Recovery**.

## 1. Multi-AZ vs. Read Replicas (The SRE Dilemma)
Recruiters will test you on this.
- **Multi-AZ**: **High Availability**. Synchronous replication to a standby in another AZ. Standby is NOT for queries. SRE uses this for failover.
- **Read Replicas**: **Performance Scaling**. Asynchronous replication. Used to scale "Read" traffic. SRE uses this to offload heavy BI queries.

## 2. Backup & Recovery (SRE Guardrails)
- **Automated Backups**: Enabled by default. Allows point-in-time recovery (PITR).
- **Manual Snapshots**: Stay after you delete the instance. **SRE Tip**: Always take a final snapshot before terminating a production DB.

## 3. Storage Types
- **gp3**: Best price-performance. IOPS are independent of storage size.
- **io2**: For extreme high-performance requirements (expensive).

## 4. Aurora: The SRE's Choice
Amazon Aurora is a cloud-native database.
- **Pros**: 6 copies of data across 3 AZs. Self-healing storage. Faster failover than standard RDS.
- **Serverless v2**: Automatically scales based on DB load (Great for cost saving in Dev/Stage).

## 5. How to Create (Terraform Standard)
```hcl
resource "aws_db_instance" "prod_db" {
  allocated_storage    = 20
  engine               = "postgres"
  instance_class       = "db.t3.medium"
  multi_az             = true
  db_name              = "mydb"
  
  performance_insights_enabled = true # SRE Best Practice
  skip_final_snapshot          = false
}
```

## 6. SRE Performance Checklist
1.  **Performance Insights**: Check for "Wait Events" to find slow queries.
2.  **Storage Autoscaling**: Enable so DB doesn't crash when disk is full.
3.  **Enhanced Monitoring**: Real-time OS metrics of the DB instance.

---

## 🏠 How to test Databases on Localhost?
Don't use RDS for local development. Use **Docker Compose**.

1.  **Spin up PostgreSQL**:
    ```yaml
    services:
      db:
        image: postgres:15
        environment:
          POSTGRES_PASSWORD: mysecretpassword
        ports:
          - "5432:5432"
    ```
2.  **Simulation**: Use this for local integration testing with your backend apps.

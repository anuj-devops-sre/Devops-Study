# 📦 S3 (Simple Storage Service) SRE MASTER NOTES

Durability and Cost at scale.

## 1. Storage Classes
- **Standard**: Frequent.
- **Glacier**: Archival (Compliance logs).
- **Intelligent-Tiering**: **SRE Best Practice**: Automated cost optimization.

## 2. Security
- **Public Access Block**: Enable by default.
- **Versioning**: Recovery from accidental deletes.

## 3. Local Testing
```bash
awslocal s3 mb s3://test-bucket
```

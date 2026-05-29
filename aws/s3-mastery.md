# 📦 S3 Mastery: More than just "Storage"

Simple Storage Service (S3) is the primary data lake for most enterprises. For an SRE, it's about **Data Integrity, Security, and Lifecycle Cost**.

## 1. What is S3?
Object storage built to store and retrieve any amount of data from anywhere. It offers 99.999999999% (11 9's) of durability.

## 2. Storage Classes (The Cost Hierarchy)
Knowing when to move data to cheaper storage is a key SRE task.
- **S3 Standard**: Frequent access. (Highest cost).
- **S3 Standard-IA (Infrequent Access)**: Long-lived, but accessed less often. Lower storage price, but high retrieval fee.
- **S3 One Zone-IA**: Cheaper than Standard-IA but lives in only 1 AZ. Use for non-critical backups.
- **S3 Glacier Instant Retrieval**: Retrieval in milliseconds. Use for data accessed once a quarter.
- **S3 Glacier Deep Archive**: Cheapest storage. Retrieval takes 12-48 hours. **SRE Tip**: Best for compliance logs (7-year retention).
- **S3 Intelligent-Tiering**: **SRE Best Practice**. Automatically moves data between tiers based on access patterns. No retrieval fees.

## 3. S3 Security (Zero Trust)
- **Public Access Block**: Always enable this at the account level unless it's a static website.
- **Bucket Policies**: JSON-based access control.
- **Encryption**: Enable Server-Side Encryption (SSE-S3 or SSE-KMS) by default.

## 4. SRE Lifecycle Policies (Automatic Cost Saving)
Don't delete manually. Use Terraform to automate:
```hcl
resource "aws_s3_bucket_lifecycle_configuration" "logs_rule" {
  bucket = aws_s3_bucket.logs.id

  rule {
    id      = "archive_old_logs"
    status  = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }
}
```

## 5. SRE Checklist for S3
1.  **Versioning**: Enable for critical data to recover from accidental deletes.
2.  **Object Lock**: For WORM (Write Once Read Many) requirements.
3.  **VPC Endpoints**: Ensure traffic to S3 doesn't go through the NAT Gateway (saves $).

---

## 🏠 How to test S3 on Localhost?
Use **LocalStack** to test S3 API calls without any cost.

1.  **Create Bucket**:
    ```bash
    awslocal s3 mb s3://my-test-bucket
    ```
2.  **Upload File**:
    ```bash
    awslocal s3 cp file.txt s3://my-test-bucket/
    ```
3.  **List Contents**:
    ```bash
    awslocal s3 ls s3://my-test-bucket/
    ```

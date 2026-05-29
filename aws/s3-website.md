# 📦 S3 Static Website Hosting

Host a simple HTML/CSS website on AWS S3.

## 🛠️ Steps
1.  Create an S3 bucket with a unique name.
2.  **Enable Static Website Hosting** in the Bucket Properties.
3.  Upload `index.html` and `error.html`.
4.  **Disable "Block all public access"** (if needed for public access).
5.  **Add Bucket Policy** for public read access:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::your-bucket-name/*"
        }
    ]
}
```
6.  Access via the **Bucket Endpoint URL**.

# ☁️ AWS (Amazon Web Services) Notes

Detailed study notes and cheat sheets for AWS services.

## 🔐 IAM (Identity & Access Management)
- **Users**: Individual identity.
- **Groups**: Collection of users with same permissions.
- **Roles**: Temporary permissions for services/users.
- **Policies**: JSON documents defining permissions.

**CLI Command:**
```bash
aws iam list-users
```

---

## 💻 EC2 (Elastic Compute Cloud)
- **Instance Types**: t2.micro (Free Tier), c5 (Compute), r5 (Memory).
- **Security Groups**: Virtual firewalls at the instance level.
- **Key Pairs**: SSH access (.pem/.ppk files).

---

## 📦 S3 (Simple Storage Service)
- **Buckets**: Global unique names.
- **Storage Classes**: Standard, IA, Glacier.
- **Policies**: Controlling access at bucket level.

---

## 🚀 Lab Exercises
- [VPC Peering Lab Guide](./vpc-peering.md)
- [S3 Static Website Hosting](./s3-website.md)

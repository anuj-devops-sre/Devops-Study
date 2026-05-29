# 🌐 VPC & Networking SRE MASTER NOTES

The network is the foundation of reliability. Focus on **Traffic Isolation and Cost**.

## 1. Components
- **Public Subnet**: Route to IGW (Internet Gateway).
- **Private Subnet**: No direct route (SRE rule for DBs).
- **NAT Gateway**: Outbound only access for private resources.

## 2. SRE Cost & Performance
- **VPC Endpoints (PrivateLink)**: SRE's secret to bypass NAT Gateway fees for S3/ECR.
- **Security Groups (SG)**: Stateful (Return traffic allowed).
- **NACLs**: Stateless (subnets layer).

## 3. High Availability
- **Multi-AZ**: Always deploy across at least 2-3 Availability Zones.

## 4. Local Testing
```bash
# Simulate network topology via Docker networks
docker network create --internal private_lan
```

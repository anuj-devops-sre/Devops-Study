# 🌐 VPC Peering Lab Guide

Establish a network connection between two VPCs.

## 🛠️ Steps
1.  Create two VPCs (VPC A and VPC B) in different CIDR ranges.
2.  Go to **VPC Dashboard > Peering Connections**.
3.  **Create Peering Connection**: Select VPC A as Requester and VPC B as Accepter.
4.  **Accept Request** from the Accepter VPC.
5.  **Update Route Tables**: Add a route to the Peer VPC CIDR via the Peering Connection (pcx-xxxx).
6.  **Verify**: Ping an instance in VPC B from VPC A.

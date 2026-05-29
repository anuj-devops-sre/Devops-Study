output "vpc_id" {
  value = aws_vpc.rke2.id
}
output "server_public_ips" {
  value = aws_instance.rke2_server[*].public_ip
}
output "server_private_ips" {
  value = aws_instance.rke2_server[*].private_ip
}
output "agent_private_ips" {
  value = aws_instance.rke2_agent[*].private_ip
}
output "kubernetes_api_endpoint" {
  value = "https://${aws_lb.rke2.dns_name}:6443"
}
output "nlb_dns" {
  value = aws_lb.rke2.dns_name
}
output "registration_url" {
  value = "https://${aws_lb.rke2.dns_name}:9345"
}
output "s3_etcd_bucket" {
  value = aws_s3_bucket.etcd_snapshots.bucket
}

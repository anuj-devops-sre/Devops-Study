resource "aws_secretsmanager_secret" "rke2_token" {
  name                    = "${var.cluster_name}-token"
  recovery_window_in_days = 0
  tags = { Name = "${var.cluster_name}-token" }
}

resource "aws_secretsmanager_secret_version" "rke2_token" {
  secret_id     = aws_secretsmanager_secret.rke2_token.id
  secret_string = "rke2-token-${var.cluster_name}-supersecret123"
}

resource "aws_instance" "rke2_server" {
  count                       = var.server_count
  ami                         = var.ami_id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.rke2_server.id]
  iam_instance_profile        = aws_iam_instance_profile.rke2_node.name
  associate_public_ip_address = true
  key_name                    = var.ssh_key_name

  user_data_base64 = base64encode(templatefile("${path.module}/templates/rke2-server.sh.tftpl", {
    rke2_token   = aws_secretsmanager_secret_version.rke2_token.secret_string
    s3_bucket    = aws_s3_bucket.etcd_snapshots.bucket
    region       = var.aws_region
    lb_dns       = aws_lb.rke2.dns_name
    is_bootstrap = count.index == 0
  }))

  root_block_device {
    volume_size = 50
    volume_type = "gp3"
  }

  tags = {
    Name = "${var.cluster_name}-server-${count.index + 1}"
    Role = "server"
  }
}

resource "aws_instance" "rke2_agent" {
  count                       = var.agent_count
  ami                         = var.ami_id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.private.id
  vpc_security_group_ids      = [aws_security_group.rke2_agent.id]
  iam_instance_profile        = aws_iam_instance_profile.rke2_node.name
  associate_public_ip_address = false
  key_name                    = var.ssh_key_name

  user_data_base64 = base64encode(templatefile("${path.module}/templates/rke2-agent.sh.tftpl", {
    lb_dns     = aws_lb.rke2.dns_name
    rke2_token = aws_secretsmanager_secret_version.rke2_token.secret_string
  }))

  root_block_device {
    volume_size = 50
    volume_type = "gp3"
  }

  depends_on = [aws_instance.rke2_server]

  tags = {
    Name = "${var.cluster_name}-agent-${count.index + 1}"
    Role = "agent"
  }
}

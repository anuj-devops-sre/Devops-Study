resource "aws_iam_role" "rke2_node" {
  name = "${var.cluster_name}-node-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
  tags = { Name = "${var.cluster_name}-node-role" }
}

resource "aws_iam_role_policy" "rke2_node" {
  name = "${var.cluster_name}-node-policy"
  role = aws_iam_role.rke2_node.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["ec2:Describe*", "ec2:CreateTags", "ec2:CreateVolume", "ec2:AttachVolume", "ec2:DetachVolume", "ec2:DeleteVolume"]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:PutObject", "s3:DeleteObject", "s3:ListBucket"]
        Resource = ["arn:aws:s3:::${var.cluster_name}-etcd-snapshots", "arn:aws:s3:::${var.cluster_name}-etcd-snapshots/*"]
      },
      {
        Effect   = "Allow"
        Action   = ["secretsmanager:GetSecretValue"]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_instance_profile" "rke2_node" {
  name = "${var.cluster_name}-node-profile"
  role = aws_iam_role.rke2_node.name
}

resource "aws_s3_bucket" "etcd_snapshots" {
  bucket = "${var.cluster_name}-etcd-snapshots"
  tags   = { Name = "${var.cluster_name}-etcd-snapshots" }
}

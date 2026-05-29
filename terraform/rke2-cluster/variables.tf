variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "cluster_name" {
  description = "RKE2 cluster name"
  type        = string
  default     = "rke2-cluster"
}

variable "instance_type" {
  description = "EC2 instance type for nodes"
  type        = string
  default     = "t3.medium"
}

variable "server_count" {
  description = "Number of RKE2 server nodes"
  type        = number
  default     = 3
}

variable "agent_count" {
  description = "Number of RKE2 agent nodes"
  type        = number
  default     = 2
}

variable "ami_id" {
  description = "AMI ID for EC2 instances"
  type        = string
  default     = "ami-7dfbf1c31e5f7fba5"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  type    = string
  default = "10.0.1.0/24"
}

variable "private_subnet_cidr" {
  type    = string
  default = "10.0.2.0/24"
}

variable "rke2_version" {
  type    = string
  default = "v1.28.8+rke2r1"
}

variable "ssh_key_name" {
  type    = string
  default = "rke2-keypair"
}

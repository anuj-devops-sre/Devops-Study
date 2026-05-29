resource "aws_lb" "rke2" {
  name               = "${var.cluster_name}-nlb"
  internal           = false
  load_balancer_type = "network"
  subnets            = [aws_subnet.public.id]

  enable_deletion_protection = false

  tags = { Name = "${var.cluster_name}-nlb" }
}

# API Server Target Group (6443)
resource "aws_lb_target_group" "api" {
  name     = "${var.cluster_name}-api"
  port     = 6443
  protocol = "TCP"
  vpc_id   = aws_vpc.rke2.id

  health_check {
    enabled  = true
    protocol = "TCP"
    port     = 6443
  }
}

# Node Registration Target Group (9345)
resource "aws_lb_target_group" "registration" {
  name     = "${var.cluster_name}-reg"
  port     = 9345
  protocol = "TCP"
  vpc_id   = aws_vpc.rke2.id

  health_check {
    enabled  = true
    protocol = "TCP"
    port     = 9345
  }
}

# API Server Listener
resource "aws_lb_listener" "api" {
  load_balancer_arn = aws_lb.rke2.arn
  port              = "6443"
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api.arn
  }
}

# Node Registration Listener
resource "aws_lb_listener" "registration" {
  load_balancer_arn = aws_lb.rke2.arn
  port              = "9345"
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.registration.arn
  }
}

resource "aws_lb_target_group_attachment" "api" {
  count            = var.server_count
  target_group_arn = aws_lb_target_group.api.arn
  target_id        = aws_instance.rke2_server[count.index].id
  port             = 6443
}

resource "aws_lb_target_group_attachment" "registration" {
  count            = var.server_count
  target_group_arn = aws_lb_target_group.registration.arn
  target_id        = aws_instance.rke2_server[count.index].id
  port             = 9345
}

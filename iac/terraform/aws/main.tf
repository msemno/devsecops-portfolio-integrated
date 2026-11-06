# DESIGN EXERCISE ONLY. Do not 'terraform apply' without an owned AWS account,
# reviewed plan, budget alarm, credentials and explicit approval.
resource "aws_vpc" "demo" {
  cidr_block           = "10.77.0.0/16"
  enable_dns_hostnames = true
  tags                 = { Name = "${var.name_prefix}-vpc" }
}
resource "aws_security_group" "app" {
  name        = "${var.name_prefix}-app"
  description = "HTTPS limited to explicitly approved CIDR"
  vpc_id      = aws_vpc.demo.id
  ingress {
    description = "Approved HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ingress_cidr]
  }
  # Design-only: deny all outbound connections by default.
  # Explicit outbound destinations require separate security review.
  egress = []
}

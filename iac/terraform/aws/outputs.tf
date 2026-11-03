output "vpc_id" { value = aws_vpc.demo.id }
output "app_security_group_id" { value = aws_security_group.app.id }

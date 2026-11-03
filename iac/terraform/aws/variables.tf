variable "aws_region" {
  type    = string
  default = "eu-west-1"
}
variable "allowed_ingress_cidr" {
  description = "Explicit authorized CIDR for the demonstration HTTPS ingress rule"
  type        = string
  default     = "10.77.0.0/16"
  validation {
    condition     = can(cidrhost(var.allowed_ingress_cidr, 0)) && var.allowed_ingress_cidr != "0.0.0.0/0"
    error_message = "A valid private/approved non-world CIDR is required."
  }
}
variable "name_prefix" {
  type    = string
  default = "portfolio-example"
}

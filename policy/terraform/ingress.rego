package main
import rego.v1

# Evaluate plan JSON; do not assume that scanning only standalone rules covers
# aws_security_group inline ingress blocks.
world_cidr(rule) if {
  some cidr in object.get(rule, "cidr_blocks", [])
  cidr == "0.0.0.0/0"
}
world_cidr(rule) if {
  some cidr in object.get(rule, "ipv6_cidr_blocks", [])
  cidr == "::/0"
}

admin_port(rule) if {
  rule.from_port <= 22
  rule.to_port >= 22
}
admin_port(rule) if {
  rule.from_port <= 3389
  rule.to_port >= 3389
}
admin_port(rule) if {
  rule.protocol == "-1"
}

# Covers both standalone aws_security_group_rule and inline ingress from
# aws_security_group. Additional provider resources are future extensions.
deny contains msg if {
  some change in input.resource_changes
  not "delete" in change.change.actions
  change.type == "aws_security_group_rule"
  rule := change.change.after
  rule.type == "ingress"
  world_cidr(rule)
  admin_port(rule)
  msg := sprintf("%s exposes management ports to the world", [change.address])
}

deny contains msg if {
  some change in input.resource_changes
  not "delete" in change.change.actions
  change.type == "aws_security_group"
  some rule in change.change.after.ingress
  world_cidr(rule)
  admin_port(rule)
  msg := sprintf("%s includes world-open management ingress", [change.address])
}

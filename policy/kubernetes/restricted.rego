package main
import rego.v1

deny contains msg if {
  input.kind == "Deployment"
  input.spec.template.spec.hostNetwork == true
  msg := "hostNetwork is prohibited"
}
deny contains msg if {
  input.kind == "Deployment"
  not input.spec.template.spec.automountServiceAccountToken == false
  msg := "service account tokens must not automount"
}
deny contains msg if {
  input.kind == "Deployment"
  not input.spec.template.spec.securityContext.runAsNonRoot
  msg := "runAsNonRoot must be set"
}
deny contains msg if {
  input.kind == "Deployment"
  input.spec.template.spec.securityContext.seccompProfile.type != "RuntimeDefault"
  msg := "RuntimeDefault seccomp must be set"
}
deny contains msg if {
  input.kind == "Deployment"
  some i
  container := input.spec.template.spec.containers[i]
  not regex.match(`.+@sha256:[a-f0-9]{64}$`, container.image)
  msg := sprintf("container %s must have image digest", [container.name])
}
deny contains msg if {
  input.kind == "Deployment"
  some i
  container := input.spec.template.spec.containers[i]
  not container.securityContext.allowPrivilegeEscalation == false
  msg := sprintf("container %s permits privilege escalation", [container.name])
}
deny contains msg if {
  input.kind == "Deployment"
  some i
  container := input.spec.template.spec.containers[i]
  not container.securityContext.readOnlyRootFilesystem == true
  msg := sprintf("container %s needs a read-only root filesystem", [container.name])
}
deny contains msg if {
  input.kind == "Deployment"
  some i
  container := input.spec.template.spec.containers[i]
  not "ALL" in container.securityContext.capabilities.drop
  msg := sprintf("container %s must drop all capabilities", [container.name])
}
deny contains msg if {
  input.kind == "Deployment"
  some i
  container := input.spec.template.spec.containers[i]
  not container.resources.limits.memory
  msg := sprintf("container %s must have memory limits", [container.name])
}

deny contains msg if {
  input.kind == "Deployment"
  some i
  container := input.spec.template.spec.containers[i]
  container.securityContext.privileged == true
  msg := sprintf("container %s is privileged", [container.name])
}

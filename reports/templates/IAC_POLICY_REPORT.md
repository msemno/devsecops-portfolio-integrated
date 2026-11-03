# Policy-as-code evaluation report

Date / commit / operator / tool versions / policy version / input fixture hashes.

## Scope and expectations
Describe approved infrastructure, prohibited actions, labels and impact of a failed policy.

| Test | Expected | Observed | Evidence |
|---|---|---|---|
| Secure Kubernetes deployment | PASS | NOT RUN | |
| Privileged/root deployment | DENY | NOT RUN | |
| Secure Terraform plan | PASS | NOT RUN | |
| World-accessible SSH ingress | DENY | NOT RUN | |
| World-accessible RDP ingress | DENY | NOT RUN | |
| Unknown/unresolved port on public ingress | MANUAL REVIEW | NOT RUN | |
| Restricted PSA live rejection | DENY | NOT RUN | |

## Root causes / changes / retest
Explain each failing test, scope of fix, developer feedback message, retest command and evidence.

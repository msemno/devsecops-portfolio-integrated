# P1 Negative PR Enforcement — Verified

## Test identification

- Repository: msemno/devsecops-portfolio-integrated
- Pull request: https://github.com/msemno/devsecops-portfolio-integrated/pull/2
- Test branch: test/p1-negative-egress
- Test commit: ea25f1d2b23cfa5d6af9c29a37a1465ed66d14df
- Quality workflow run: https://github.com/msemno/devsecops-portfolio-integrated/actions/runs/42219306259
- Date: 2026-11-06

## Controlled security violation

- File: `iac/terraform/aws/main.tf`
- Vulnerability: unrestricted HTTPS egress to `0.0.0.0/0`
- Trivy rule: `AWS-0104`
- Severity: CRITICAL
- Scanner: Trivy v0.76.1

## Verified hosted results

| Security control | Result |
|---|---|
| configuration-scanning | FAILURE |
| CodeQL SAST / codeql | SUCCESS |
| CodeQL | SUCCESS |
| unit-and-baseline-policy | SUCCESS |
| policy-as-code | SUCCESS |
| container-image | SUCCESS |
| Pull request merge state | BLOCKED |
| Main branch protected | true |
| Main branch unchanged | true |

Main SHA: `b939fca5e8725b40ecfb1cb8c904cf339f04e341`

## Acceptance decision

**PASS — The protected main branch rejected a pull request
with a deliberately introduced critical Terraform misconfiguration.**

The security violation must not be merged or deployed.
The test PR is to be closed and its temporary branch deleted.

This result validates required-check enforcement. It does not
constitute production release approval.

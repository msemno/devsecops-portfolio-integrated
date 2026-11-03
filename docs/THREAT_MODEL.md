# Security threat model — Connected DevSecOps portfolio

## Assets
- App source and requirements; trusted main branch; CI workflow YAML; Terraform/Kubernetes manifests; release tarball, SBOM, attestations and signature bundles; OIDC release identity; optional cloud account.

## Trust boundaries
- Contributor/PR to branch-protected repository; source checkout to hosted runner; build runner to external package registries; CI to attest/sign; artifact to consumer; config to Kubernetes admission; IaC plan to optional cloud apply.

## Threats / mitigations / verification
| Threat | Mitigation | How to prove it |
|---|---|---|
| Leaked access key in git | secret scanner, synthetic fixtures only, secret rotation | synthetic test + scan result |
| Dependency with advisory | pip-audit, Trivy, dependency updates | vulnerability job gate |
| Weak container configuration | non-root UID, restrictive K8s contexts, read-only FS | bad fixture rejected, deployment manifest reviewed |
| Public admin port | Rego plan rule + approval for cloud apply | bad plan rejected, safe plan accepted |
| Malicious PR acquiring release token | separate release workflow and permission boundary | PR job no id-token/attest permission; release only tagged/manual |
| Runner or artifact substitution | signed attestations, Cosign OIDC, independent verification | test wrong identity or modified blob fails |
| False confidence from checksum | explicit trust model | distinguish sha manifest from signature in report |
| Misconfigured admission | restricted PSA namespace and kind validation | create invalid pod in isolated kind, record rejection |
| CI scanner false positive/negative | exception process, corpus of positive/negative fixtures | reasoned dispositions and regression tests |
| Cost or accidental exposure | no terraform apply in CI; owned account and budget review | plan-only CI, no credentials in PR workflow |

## Residual risks
- High/critical vulnerability databases are not a guarantee of clean code.
- Tag/version-pinned GitHub Actions can move. Pin full SHAs and periodically audit dependencies.
- Sample image digest is deliberately non-runnable. Replace with the actual digest from your published image.
- GitHub artifact attestations are not automatically equivalent to SLSA L3; hardened builders and other requirements matter.

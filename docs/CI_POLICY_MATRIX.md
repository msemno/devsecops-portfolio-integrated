# Controls and required failure behavior

| ID | Control | Tool | On | Fail if | Evidence |
|---|---|---|---|---|---|
| CI-01 | Python correctness | pytest | PR | any regression fails | JUnit / action log |
| CI-02 | Basic lint | Ruff | PR | syntax/critical rules fail | action log |
| CI-03 | Dependency advisories | pip-audit | PR | known vulnerable requirement | advisory data + triage |
| CI-04 | Code security analysis | CodeQL | PR | raised findings per branch policy | GitHub code-scanning output |
| CI-05 | Secret scan | Trivy fs | PR | detectable secret | alert, no credential in report |
| CI-06 | Image dependency scan | Trivy image | PR | high/critical fixable issues | report |
| CI-07 | Terraform misconfig | Trivy config + Rego | PR | serious flaw | report / denied plan |
| CI-08 | Kubernetes misconfig | Trivy config + Rego | PR | security policy violation | bad manifest denied |
| CI-09 | Negative-control corpus | pytest / Conftest | PR | known-bad accepted | fixture acceptance matrix |
| CI-10 | Signed source | Cosign OIDC | tagged release | signature/verification error | Sigstore bundle |
| CI-11 | Provenance | actions/attest | tagged release | attestation generation error | GitHub attestation record |
| CI-12 | SBOM | Syft SPDX JSON | tagged release | malformed output or missing | SBOM file, coverage analysis |

The presence of a workflow YAML proves only intent. Evidence of actual execution requires accessible workflow logs and artifact verification results.

## Merge policy exercise
Configure main branch protection with review, no direct pushes, required successful checks, no admin bypass, dismiss stale reviews, and dependency update PRs. Test protection by trying to merge a deliberately failing branch. If protections differ by GitHub plan, document the practical limitation.

## Exception policy
A scanner finding should be suppressed only with an owner, justification, expiry, compensating control and approval. Keep false positives as labeled benchmark fixtures, not silently hidden exceptions.

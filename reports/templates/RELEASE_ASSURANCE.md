# Release assurance dossier — [tag]

## Executive decision
Release ID, commit, release status (PASS/FAIL/NOT TESTED), reviewer, timestamp.

## Chain of custody
- Source artifact name and SHA-256; Git commit SHA; workflow run URL and immutable run ID
- SBOM path and standard/version; component count; known omissions
- Cosign signature bundle path; expected OIDC issuer, expected certificate identity
- Attestation subject digest and build signer; verification command and evidence

## Gates and test records
| Gate | Expected | Observed | Run URL / evidence | Decision |
|---|---|---|---|---|
| Unit tests | pass | NOT RUN | | |
| SAST | no unresolved blocking issue | NOT RUN | | |
| SCA | no unacceptable risk | NOT RUN | | |
| IaC | conforming | NOT RUN | | |
| K8s | conforming | NOT RUN | | |
| Image | no blocking CVEs | NOT RUN | | |
| SBOM | generated + independently checked | NOT RUN | | |
| Cosign signature | expected signer verified | NOT RUN | | |
| Provenance | verified subject and trusted repo | NOT RUN | | |

## Deliberate tamper tests
1. Modify one byte in the signed artifact; verify should fail.
2. Verify against wrong certificate identity; should fail.
3. Attempt to release from an untrusted fork; should not mint release attestations.

## Known risks and exclusions
Record expiring policy exceptions, missing runtime tests, private repository restrictions, and dependency resolution limitations.

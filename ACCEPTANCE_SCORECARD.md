# DevSecOps Portfolio Acceptance and Evidence Scorecard

**Operator:** ____  **Date UTC:** ____  **Repository/commit:** ____

| ID | Evidence required | Status (PASS / FAIL / NOT RUN) | URL / saved artifact | Reviewer notes |
|---|---|---|---|---|
| P1-01 | Clone, install, run Python tests | NOT RUN | | |
| P1-02 | Docker image build and loopback health | NOT RUN | | |
| P1-03 | CI unit tests and static analysis | NOT RUN | | |
| P1-04 | Dependency and image vulnerability scans | NOT RUN | | |
| P1-05 | Secret scan and remediation handling | NOT RUN | | |
| P1-06 | PR deliberately fails, fix restores green | NOT RUN | | |
| P1-07 | Branch protections block failing merge | NOT RUN | | |
| P2-01 | Terraform fmt/init/validate | NOT RUN | | |
| P2-02 | Rego accepts private HTTPS plan | NOT RUN | | |
| P2-03 | Rego rejects world-open SSH/RDP | NOT RUN | | |
| P2-04 | K8s baseline passes and bad manifest is refused | NOT RUN | | |
| P2-05 | New original Rego rule has positive/negative fixtures | NOT RUN | | |
| P2-06 | Optional live restricted Pod Security rejection | NOT RUN | | |
| P2-07 | Optional network-policy enforcement verified on actual CNI | NOT RUN | | |
| P3-01 | Real Syft source SPDX SBOM | NOT RUN | | |
| P3-02 | Real Syft image SPDX SBOM | NOT RUN | | |
| P3-03 | Artifact checksum detects altered bytes | NOT RUN | | |
| P3-04 | Hosted signed release and attestation succeeded | NOT RUN | | |
| P3-05 | Cosign verifies exact issuer/identity | NOT RUN | | |
| P3-06 | `gh attestation verify` passes digest and repo | NOT RUN | | |
| P3-07 | Modified bytes and wrong signer both rejected | NOT RUN | | |
| E2E-01 | Architecture and trust boundaries documented | NOT RUN | | |
| E2E-02 | CI/policy/release reports linked together | NOT RUN | | |
| E2E-03 | 3–5 minute recruiter demonstration | NOT RUN | | |

**Scoring rule:** A feature is complete only when a real command/run and its evidence have been independently inspected. `NOT RUN` means incomplete, not a passing check. Source-only checks are not live platform checks. Never invent performance, vulnerability or provenance metrics.

**Next-step backlog:** review workflow action SHA pinning; Terraform private state design; runtime CNI; actual image push/attestation; dependency pin/hash lock; structured waiver expiry; threshold tuning; SLSA assessment.

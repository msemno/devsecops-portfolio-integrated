# DevSecOps Portfolio — Connected Triple Capstone

**Projects:** (1) Secure CI/CD Pipeline, (2) Terraform & Kubernetes Policies, (3) SBOM + Signing + Provenance.

Build a minimal FastAPI app, protect its source/dependencies/infrastructure, apply policy-as-code, package a release, generate a real SBOM with Syft, and sign/attest the build using GitHub OIDC.

## Demonstrable outcome

A pull request must pass unit tests, dependency and image scanning, SAST, secret scanning, Kubernetes/Terraform policy and negative-control tests. A deliberately broken configuration is rejected. After approved changes merge, a tagged release can generate a source artifact, SPDX SBOM, Sigstore signature, and GitHub-hosted provenance attestations. Always **verify the signer identity and digest**.

## Build architecture

```text
Kali/laptop → feature branch → GitHub pull request
                    |
          [unit tests | CodeQL | Trivy | pip-audit]
                    |
       [Terraform design → Conftest / Trivy]
                    |
       [K8s deployments → Conftest / PSA]
                    |
              approved merge
                    |
         tagged source release (no cloud needed)
                    |
      [Syft SBOM → GitHub attestations + Cosign]
                    |
        [verify digest, signer identity, provenance]
                    |
       optional image deployment to isolated kind
```

## Three trust boundaries

1. Python fixture scanner provides **offline educational policy feedback**; it does not replace Conftest/Trivy, Kubernetes admission, or runtime validation.
2. SHA-256 integrity checks detect unexpected bytes only if the expected digest/manifest is trusted. **Not a signature.**
3. GitHub Actions attestations and Cosign keyless signatures require a supported GitHub repository, online OIDC access, and verification against an expected identity. Their YAML configuration is **not evidence of execution**.

## Quickstart

Read [START_HERE.md](START_HERE.md). On Kali with Python already installed:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
make policy
make policy-negative
```

## Important files

- `PLAYBOOK.md`: engineering walkthrough, commands, architecture and troubleshooting
- `COMMAND_CHEATSHEET.md`: concise CLI operators reference
- `ACCEPTANCE_SCORECARD.md`: evidence-based graduation tracking
- `WEEKLY_PLAN.md`: 12-week / 60-session learning track
- `docs/THREAT_MODEL.md`: assets, supply-chain boundaries, negative tests
- `docs/CI_POLICY_MATRIX.md`: every gate, what it proves and fail criteria
- `reports/templates/`: change risk, vulnerability, release assurance reports
- `.github/workflows/quality.yml`: PR checks and custom policies
- `.github/workflows/codeql.yml`: CodeQL SAST
- `.github/workflows/release.yml`: actual signing/provenance, on approved repo
- `policy/`: independent Rego rules
- `labsec/`: Python educational scanners and integrity helpers
- `k8s/` and `iac/terraform/`: deployment samples

## Validation status

`pytest`, local Python checks, and static checks were run during package production. Docker, kind, Terraform cloud provider, external scanners, hosted CI, Cosign/OIDC and GitHub attestations require the operator's local machine or repository and **have not been claimed as run**.

> The repository is an educational portfolio. Never apply cloud infrastructure to accounts you do not control; review any plan and cost estimate before applying. Example GitHub Actions use version tags for readability; pin third-party actions to full reviewed commit SHAs before production deployment.

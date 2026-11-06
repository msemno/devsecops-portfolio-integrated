# P1 — Container Security Assessment

Generated (UTC): 2026-11-06T06:05:18.144527+00:00

## Scope

- Project: DevSecOps Portfolio — Secure CI/CD Pipeline
- Image: devsecops-demo:production-review
- Scanner: Trivy 0.76.1
- Status: **OPEN — NOT APPROVED FOR PRODUCTION RELEASE**

## Before / After Findings

| Image | Total | Critical | High | Medium | Low | Python | APT CVE-2026-109518 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original remediated | 196 | 0 | 53 | 74 | 63 | 8 | 2 |
| APT patched | 194 | 0 | 51 | 74 | 63 | 8 | 0 |
| Multi-stage | 186 | 0 | 46 | 72 | 62 | 0 | 0 |
| Production review | 186 | 0 | 46 | 72 | 62 | 0 | 0 |

## Remaining HIGH / CRITICAL Debian Advisories

| Advisory | Severity | Records | Packages | Fix in Trivy report |
|---|---|---:|---|---|
| CVE-2025-69720 | HIGH | 4 | libncursesw6, libtinfo6, ncurses-base, ncurses-bin | No fix listed |
| CVE-2026-119373 | HIGH | 1 | libsqlite3-0 | No fix listed |
| CVE-2026-16742 | HIGH | 2 | libsystemd0, libudev1 | No fix listed |
| CVE-2026-54369 | HIGH | 1 | libacl1 | No fix listed |
| CVE-2026-76642 | HIGH | 9 | bsdutils, libblkid1, liblastlog2-2, libmount1, libsmartcols1, libuuid1, login, mount, util-linux | No fix listed |
| CVE-2026-76844 | HIGH | 1 | zlib1g | No fix listed |
| CVE-2026-78408 | HIGH | 9 | bsdutils, libblkid1, liblastlog2-2, libmount1, libsmartcols1, libuuid1, login, mount, util-linux | No fix listed |
| CVE-2026-78409 | HIGH | 9 | bsdutils, libblkid1, liblastlog2-2, libmount1, libsmartcols1, libuuid1, login, mount, util-linux | No fix listed |
| CVE-2026-78410 | HIGH | 9 | bsdutils, libblkid1, liblastlog2-2, libmount1, libsmartcols1, libuuid1, login, mount, util-linux | No fix listed |
| CVE-2026-9538 | HIGH | 1 | perl-base | No fix listed |

## Evidence Integrity

- **Original remediated**: `build/trivy-audit/report.json`
  - SHA-256: `c5af48d3ac9ef8fd9b7943e2e69857539ccfa8d7c55801c3da15d3f3598ee89b`
- **APT patched**: `build/trivy-audit/report-apt-candidate.json`
  - SHA-256: `602e1ed7ac0490767942e90f60a69f86d0f2e13175060d8839e9d654f44f5060`
- **Multi-stage**: `build/trivy-audit/report-multistage.json`
  - SHA-256: `f13bbb429020675e087295dfbf8463750be4c99e4a95df5db2edbeac3c841abb`
- **Production review**: `build/trivy-audit/report-production-review.json`
  - SHA-256: `e836eb2d1a8b20d4966a1df371808f927d3c6bad749693a2328bcb6f868b4649`

## Verified Controls

- Python dependency compatibility and 27 regression tests passed.
- APT 3.0.4 installed; previously reported APT CVE absent from final scan.
- Non-root runtime (UID 10001), read-only test, dropped capabilities.
- HTTP health and build metadata endpoints returned HTTP 200.
- pip is unavailable in the active Python runtime.
- Multi-stage and production-review image IDs matched locally.

## Outstanding Risks and Limitations

- 10 unique HIGH/CRITICAL Debian advisory IDs remain open.
- No listed fixed version does not prove no remediation exists.
- No risk acceptance or production deployment authorization.
- Python findings disappearing does not prove removal from lower image layers.
- Mutable Python base tag and pinned APT version require maintenance review.
- GitHub-hosted CI, signing and provenance have not been verified.

## Decision

**Remediation partially verified. Residual risks remain OPEN and are not accepted.**

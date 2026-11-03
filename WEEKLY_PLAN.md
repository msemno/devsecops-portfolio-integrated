# Connected DevSecOps Portfolio — 12 Weeks / 60 Hands-On Sessions

**Target:** Secure CI/CD → Terraform & Kubernetes Policies → SBOM + Signing + Provenance. Study ~10–15 hours/week. The milestones are approximate and are not guarantees of job readiness.

Each 2–3 hour session follows: **20–30 min study → 60–90 min hands-on build → 20–30 min negative test or verification → 10–20 min notes/commit.** If you already know a topic, replace the lesson with stronger tests and deeper documentation.

## Completion method

- Save the precise command, command exit code, UTC timestamp, tool version, Git commit and small sanitized excerpt of evidence.
- Keep failed and successful tests. A project with only passing screenshots cannot prove fail-closed policies.
- Never label synthetic policy fixtures as live cloud/cluster scanning.
- Use `NOT RUN` for anything you could not execute on your hardware or GitHub account.
- Do not perform cloud apply without an approved owned account, reviewed plan and spending guardrails.

## 12-week overview

| Week | Goal | Portfolio focus | Progress gate |
|---|---|---|---|
| 1 | Linux, Git and software security foundations | P1 foundation | Get a reproducible Python environment and baseline unit tests. |
| 2 | Docker and container security | P1 container | Build a runnable non-root container; identify isolation boundaries. |
| 3 | CI quality and code analysis | P1 pipeline | Run automated tests and code analysis on actual GitHub-hosted jobs. |
| 4 | Secrets, scanning and software delivery review | P1 graduation | Create real scanning evidence and validate a complete PR lifecycle. |
| 5 | Terraform foundations and cloud economics | P2 foundations | Understand HCL and plan-first security on an owned account. |
| 6 | Terraform Rego policies | P2 policy | Prove that allowed plan shapes pass and prohibited public management ports fail. |
| 7 | Kubernetes foundational security | P2 Kubernetes | Understand workload specs, namespace admission, RBAC, networking and identity. |
| 8 | Kubernetes policy-as-code and negative testing | P2 graduation | Implement independent Rego checks and demonstrate six denial scenarios. |
| 9 | SBOM and supply-chain fundamentals | P3 inventory | Explain inventories, transitive deps and supply-chain formats. |
| 10 | Signing, checksums and OIDC identity | P3 integrity | Demonstrate checksums vs cryptographic identity-bound signatures. |
| 11 | Provenance/SLSA and release assurance | P3 graduation | Explain what the attested artifact proves and what it cannot prove. |
| 12 | Integration, scaling and career presentation | All three | Make this cohesive enough for a DevSecOps/security engineering interview. |

## Week 1: Linux, Git and software security foundations
**Project:** P1 foundation. **Outcome:** Get a reproducible Python environment and baseline unit tests.

### Session 1 — Day 1: Set up Kali safely
- **Learn/build:** Record OS/CPU/RAM; update apt; create VM snapshot; install git/python/venv/make; record all versions.
- **Try these commands:** `cat /etc/os-release; free -h; git --version; python3 --version`
- **Evidence to preserve:** Hardware inventory and snapshot ID.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 2 — Day 2: Git quality workflow
- **Learn/build:** Initialize repo in a local working copy; create feature branch, small commit, meaningful PR text; research branch protection.
- **Try these commands:** `git init; git switch -c feat/first-test; git status --short`
- **Evidence to preserve:** Document branching, reviewers and protected main strategy.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 3 — Day 3: Python packaging and testing
- **Learn/build:** Create venv; install requirements; inspect service endpoints; run baseline tests and explain assertion coverage.
- **Try these commands:** `python3 -m venv .venv; source .venv/bin/activate; python -m pytest -q`
- **Evidence to preserve:** Pass log, code coverage ideas and learning notes.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 4 — Day 4: HTTP threat boundary
- **Learn/build:** Launch service on loopback; examine headers and build metadata; use curl; explain why health route is low risk and what would change.
- **Try these commands:** `uvicorn service.main:app --host 127.0.0.1 --port 8080; curl -sD - localhost:8080/healthz`
- **Evidence to preserve:** Three request/response observations.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 5 — Day 5: Negative testing discipline
- **Learn/build:** Temporarily alter a response, observe test failure, restore change; commit an added unit test.
- **Try these commands:** `python -m pytest -q; git diff`
- **Evidence to preserve:** Red/green screenshot and one tested improvement.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

**Week 1 graduation checklist:**
- [ ] Get a reproducible Python environment and baseline unit tests.
- [ ] The key example passes and its matching unsafe negative control fails.
- [ ] Preserve a real terminal or GitHub run with tool version, artifact hash and commit reference.
- [ ] One written note describes limitations, one troubleshooting lesson and one resume-relevant skill.

## Week 2: Docker and container security
**Project:** P1 container. **Outcome:** Build a runnable non-root container; identify isolation boundaries.

### Session 6 — Day 1: Docker installation
- **Learn/build:** Install Docker from approved packages; inspect daemon; explain local Docker group risks and rootless option.
- **Try these commands:** `sudo systemctl enable --now docker; sudo docker info`
- **Evidence to preserve:** Container runtime and host risk note.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 7 — Day 2: Dockerfile anatomy
- **Learn/build:** Explain FROM, COPY, RUN, USER, CMD, .dockerignore; build demo image and inspect metadata.
- **Try these commands:** `sudo docker build -f docker/Dockerfile -t devsecops-demo:local .`
- **Evidence to preserve:** Image ID and Dockerfile annotated review.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 8 — Day 3: Hardened container execution
- **Learn/build:** Run with read-only filesystem, limited capabilities and no-new-privileges; verify curl response.
- **Try these commands:** `sudo docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges -p 127.0.0.1:8080:8080 devsecops-demo:local`
- **Evidence to preserve:** Proof of service running under tightened options.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 9 — Day 4: Container assessment
- **Learn/build:** Inspect image layers, UID and injected environment; distinguish host and container privileges; note package pin risks.
- **Try these commands:** `sudo docker image inspect devsecops-demo:local`
- **Evidence to preserve:** Container hardening checklist.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 10 — Day 5: Container regression tests
- **Learn/build:** Add new test for no accidental environment serialization and document unknown controls; execute negative payload locally.
- **Try these commands:** `python -m pytest -q`
- **Evidence to preserve:** Security unit tests and documented limitations.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

**Week 2 graduation checklist:**
- [ ] Build a runnable non-root container; identify isolation boundaries.
- [ ] The key example passes and its matching unsafe negative control fails.
- [ ] Preserve a real terminal or GitHub run with tool version, artifact hash and commit reference.
- [ ] One written note describes limitations, one troubleshooting lesson and one resume-relevant skill.

## Week 3: CI quality and code analysis
**Project:** P1 pipeline. **Outcome:** Run automated tests and code analysis on actual GitHub-hosted jobs.

### Session 11 — Day 1: Quality workflow anatomy
- **Learn/build:** Read quality.yml event triggers, minimal permissions, jobs and dependencies; diagram flow.
- **Try these commands:** `cat .github/workflows/quality.yml`
- **Evidence to preserve:** One annotated GitHub Actions diagram.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 12 — Day 2: GitHub repository and Actions
- **Learn/build:** Create empty user-owned GitHub repo; push sanitized source; turn on Actions; document initial check results.
- **Try these commands:** `git remote -v; git push -u origin main`
- **Evidence to preserve:** Run URL and privacy/permissions review.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 13 — Day 3: CodeQL SAST
- **Learn/build:** Inspect Python CodeQL workflow, enable scanning feature as allowed; compare static findings to actual dataflows.
- **Try these commands:** `cat .github/workflows/codeql.yml`
- **Evidence to preserve:** Real CodeQL run or documented account limitation.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 14 — Day 4: pip-audit and SCA
- **Learn/build:** Run audit for direct/transitive dependencies; record advisory IDs and patch availability, without inventing findings.
- **Try these commands:** `pip-audit --requirement requirements.txt`
- **Evidence to preserve:** Dependency inventory and triage entry.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 15 — Day 5: Failing PR evidence
- **Learn/build:** Use a throwaway branch to make a failing unit test; prove merge protection blocks it and fix the failure.
- **Try these commands:** `python -m pytest -q; git diff`
- **Evidence to preserve:** Two PR run links: blocked and repaired.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

**Week 3 graduation checklist:**
- [ ] Run automated tests and code analysis on actual GitHub-hosted jobs.
- [ ] The key example passes and its matching unsafe negative control fails.
- [ ] Preserve a real terminal or GitHub run with tool version, artifact hash and commit reference.
- [ ] One written note describes limitations, one troubleshooting lesson and one resume-relevant skill.

## Week 4: Secrets, scanning and software delivery review
**Project:** P1 graduation. **Outcome:** Create real scanning evidence and validate a complete PR lifecycle.

### Session 16 — Day 1: Secrets detection
- **Learn/build:** Use Trivy filesystem secrets scan; test synthetic dummy fixture only; redact scanner output as needed.
- **Try these commands:** `trivy fs --scanners secret .`
- **Evidence to preserve:** Scanner scope, result, false-negative considerations.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 17 — Day 2: Trivy vulnerability gates
- **Learn/build:** Scan local image; compare unfixed/fixable severities; upgrade package/base only after triage.
- **Try these commands:** `trivy image --severity HIGH,CRITICAL --ignore-unfixed devsecops-demo:local`
- **Evidence to preserve:** At least one real image scan output.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 18 — Day 3: Scope of CodeQL versus dependency scanning
- **Learn/build:** Review which failures SAST/SCA/container scanning detect; document gaps and remediation ownership.
- **Try these commands:** `python -m pytest -q`
- **Evidence to preserve:** Controls mapping to security threats.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 19 — Day 4: Threat model
- **Learn/build:** Write critical assets, trust boundaries and attack paths for source checkout, PR, runner, registry, build and deploy.
- **Try these commands:** `cat docs/THREAT_MODEL.md`
- **Evidence to preserve:** One-page threat model with four testable controls.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 20 — Day 5: P1 final gate
- **Learn/build:** Confirm fresh clone, green CI, one blocked PR, container demonstration and example developer finding.
- **Try these commands:** `make test; make policy-negative`
- **Evidence to preserve:** P1 readme, report, screenshots and acceptance signoff.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

**Week 4 graduation checklist:**
- [ ] Create real scanning evidence and validate a complete PR lifecycle.
- [ ] The key example passes and its matching unsafe negative control fails.
- [ ] Preserve a real terminal or GitHub run with tool version, artifact hash and commit reference.
- [ ] One written note describes limitations, one troubleshooting lesson and one resume-relevant skill.

## Week 5: Terraform foundations and cloud economics
**Project:** P2 foundations. **Outcome:** Understand HCL and plan-first security on an owned account.

### Session 21 — Day 1: HCL syntax
- **Learn/build:** Explore providers, resources, data sources, variables, locals and outputs; annotate AWS VPC example.
- **Try these commands:** `ls iac/terraform/aws; cat iac/terraform/aws/main.tf`
- **Evidence to preserve:** Readable IaC diagram and variable table.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 22 — Day 2: Terraform CLI install
- **Learn/build:** Install verified Terraform binary, record provenance and version; run format checks.
- **Try these commands:** `terraform version; terraform fmt -check -recursive iac/terraform`
- **Evidence to preserve:** Tool provenance and formatting proof.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 23 — Day 3: Validate without cloud deployment
- **Learn/build:** Initialize provider without backend; run validate; differentiate syntax and provider errors from access checks.
- **Try these commands:** `cd iac/terraform/aws && terraform init -backend=false && terraform validate`
- **Evidence to preserve:** Provider lock considerations and validation log.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 24 — Day 4: Networking/IAM risk analysis
- **Learn/build:** Map ingress 22,3389,443; discuss /0 vs approved CIDR and egress; explain state secrets/least privilege.
- **Try these commands:** `cat iac/terraform/aws/variables.tf`
- **Evidence to preserve:** Firewall threat model and approval matrix.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 25 — Day 5: Plan-only gate and exception design
- **Learn/build:** Write plan risk rules and cost checklist; no real apply unless authorized and budgeted.
- **Try these commands:** `python -m labsec.cli policy --tf-plan fixtures/terraform/secure-plan.json`
- **Evidence to preserve:** Change control checklist with no-apply boundary.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

**Week 5 graduation checklist:**
- [ ] Understand HCL and plan-first security on an owned account.
- [ ] The key example passes and its matching unsafe negative control fails.
- [ ] Preserve a real terminal or GitHub run with tool version, artifact hash and commit reference.
- [ ] One written note describes limitations, one troubleshooting lesson and one resume-relevant skill.

## Week 6: Terraform Rego policies
**Project:** P2 policy. **Outcome:** Prove that allowed plan shapes pass and prohibited public management ports fail.

### Session 26 — Day 1: Conftest installation
- **Learn/build:** Install verified Conftest release; record binary checksum/version and run policy.
- **Try these commands:** `conftest --version`
- **Evidence to preserve:** Validated Conftest installation evidence.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 27 — Day 2: Rego language
- **Learn/build:** Read import rego.v1, package, deny sets, some, nested JSON selectors; annotate two public-port rules.
- **Try these commands:** `cat policy/terraform/ingress.rego`
- **Evidence to preserve:** Annotated Rego and threat-to-rule mapping.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 28 — Day 3: Terraform positive control
- **Learn/build:** Test fixture with private ingress 443; ensure both Python and Rego pass.
- **Try these commands:** `conftest test -p policy/terraform fixtures/terraform/secure-plan.json`
- **Evidence to preserve:** Passing test and plan fields explained.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 29 — Day 4: Terraform negative controls
- **Learn/build:** Test public SSH and separately add RDP fixture, multiple CIDRs and expanded port ranges.
- **Try these commands:** `conftest test -p policy/terraform fixtures/terraform/insecure-plan.json`
- **Evidence to preserve:** At least 3 deliberate denials.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 30 — Day 5: Write regression corpus
- **Learn/build:** Create safe/unsafe plan JSON examples, test deletion, unknown values, and add issue for unsupported resource types.
- **Try these commands:** `python -m pytest -q tests/test_policy.py`
- **Evidence to preserve:** Positive/negative test matrix and policy limitations.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

**Week 6 graduation checklist:**
- [ ] Prove that allowed plan shapes pass and prohibited public management ports fail.
- [ ] The key example passes and its matching unsafe negative control fails.
- [ ] Preserve a real terminal or GitHub run with tool version, artifact hash and commit reference.
- [ ] One written note describes limitations, one troubleshooting lesson and one resume-relevant skill.

## Week 7: Kubernetes foundational security
**Project:** P2 Kubernetes. **Outcome:** Understand workload specs, namespace admission, RBAC, networking and identity.

### Session 31 — Day 1: kubectl and kind
- **Learn/build:** Install verified kubectl and kind, create isolated lab cluster if laptop allows.
- **Try these commands:** `kind create cluster --name devsecops-portfolio; kubectl get nodes`
- **Evidence to preserve:** Cluster ID, Kubernetes version, host resource use.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 32 — Day 2: Pod security contexts
- **Learn/build:** Explain UID, privilege escalation, read-only root, seccomp, capabilities and non-root restrictions.
- **Try these commands:** `cat k8s/base/deployment.yaml`
- **Evidence to preserve:** Annotated pod security profile.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 33 — Day 3: PSA restricted namespace
- **Learn/build:** Review and apply namespace restricted labels; test dry run of insecure manifest.
- **Try these commands:** `kubectl apply -f k8s/base/namespace.yaml`
- **Evidence to preserve:** Admission rejection log (if cluster running).
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 34 — Day 4: Kubernetes service/network
- **Learn/build:** Map ClusterIP, pod labels, selector and ingress/egress NetworkPolicy; evaluate CNI enforcement.
- **Try these commands:** `kubectl get networkpolicy -A`
- **Evidence to preserve:** Network diagram and CNI capability declaration.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 35 — Day 5: Local workload smoke test
- **Learn/build:** Load local image into kind; make disposable manifest; verify health and log resource state; destroy cluster at end.
- **Try these commands:** `kind load docker-image devsecops-demo:local --name devsecops-portfolio`
- **Evidence to preserve:** Real run log or candid blocked milestone.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

**Week 7 graduation checklist:**
- [ ] Understand workload specs, namespace admission, RBAC, networking and identity.
- [ ] The key example passes and its matching unsafe negative control fails.
- [ ] Preserve a real terminal or GitHub run with tool version, artifact hash and commit reference.
- [ ] One written note describes limitations, one troubleshooting lesson and one resume-relevant skill.

## Week 8: Kubernetes policy-as-code and negative testing
**Project:** P2 graduation. **Outcome:** Implement independent Rego checks and demonstrate six denial scenarios.

### Session 36 — Day 1: Read Conftest Kubernetes rules
- **Learn/build:** Annotate each restricted.rego rule and the input structures that feed it.
- **Try these commands:** `cat policy/kubernetes/restricted.rego`
- **Evidence to preserve:** Policy-to-Pod-Standard mapping.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 37 — Day 2: Accept known-good Deployment
- **Learn/build:** Run Python checker, Conftest and Trivy; examine any discrepancy and avoid silent ignore.
- **Try these commands:** `make policy; conftest test -p policy/kubernetes k8s/base/deployment.yaml`
- **Evidence to preserve:** Pass result from actual engines.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 38 — Day 3: Reject known-bad Deployment
- **Learn/build:** Test hostNetwork, image latest, root, privilege escalation and missing resources; ensure CI exit code nonzero.
- **Try these commands:** `make policy-negative`
- **Evidence to preserve:** Negative control matrix with six detections.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 39 — Day 4: Extend security policies
- **Learn/build:** Add deny on privileged containers, hostPath or missing runAsUser; write safe and bad fixtures and tests.
- **Try these commands:** `python -m pytest -q`
- **Evidence to preserve:** Original policy diff and regression test.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 40 — Day 5: P2 completion evidence
- **Learn/build:** Document Terraform risk review, kind admission boundary, IaC policy coverage and remediation reports.
- **Try these commands:** `cat reports/templates/IAC_POLICY_REPORT.md`
- **Evidence to preserve:** P2 portfolio case study and verified acceptance matrix.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

**Week 8 graduation checklist:**
- [ ] Implement independent Rego checks and demonstrate six denial scenarios.
- [ ] The key example passes and its matching unsafe negative control fails.
- [ ] Preserve a real terminal or GitHub run with tool version, artifact hash and commit reference.
- [ ] One written note describes limitations, one troubleshooting lesson and one resume-relevant skill.

## Week 9: SBOM and supply-chain fundamentals
**Project:** P3 inventory. **Outcome:** Explain inventories, transitive deps and supply-chain formats.

### Session 41 — Day 1: Define SBOM semantics
- **Learn/build:** Study SPDX/CycloneDX, package identifiers, licenses, dependency depth, package lockfiles and vulnerabilities.
- **Try these commands:** `cat docs/PRIMARY_SOURCES.md`
- **Evidence to preserve:** Comparison chart and limitations.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 42 — Day 2: Syft trusted installation
- **Learn/build:** Install verified Syft release; record CLI version and checksum verification.
- **Try these commands:** `syft version`
- **Evidence to preserve:** Tool supply-chain record.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 43 — Day 3: Source SBOM generation
- **Learn/build:** Generate SPDX JSON from checked-out repo and validate structure; list components.
- **Try these commands:** `syft dir:. -o spdx-json=build/source.spdx.json`
- **Evidence to preserve:** Source SBOM with tooling/version notes.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 44 — Day 4: Image SBOM generation
- **Learn/build:** Scan built image, compare to source and explain OS package differences.
- **Try these commands:** `syft devsecops-demo:local -o spdx-json=build/image.spdx.json`
- **Evidence to preserve:** SBOM diff and omissions list.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 45 — Day 5: SBOM QA and consumer test
- **Learn/build:** Validate schema fields; find dependency not in requirements; investigate what source file inclusion misses.
- **Try these commands:** `python -m labsec.cli validate-sbom build/source.spdx.json`
- **Evidence to preserve:** Defensible inventory limitations report.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

**Week 9 graduation checklist:**
- [ ] Explain inventories, transitive deps and supply-chain formats.
- [ ] The key example passes and its matching unsafe negative control fails.
- [ ] Preserve a real terminal or GitHub run with tool version, artifact hash and commit reference.
- [ ] One written note describes limitations, one troubleshooting lesson and one resume-relevant skill.

## Week 10: Signing, checksums and OIDC identity
**Project:** P3 integrity. **Outcome:** Demonstrate checksums vs cryptographic identity-bound signatures.

### Session 46 — Day 1: Digest introduction
- **Learn/build:** Generate SHA-256 manifest, verify and mutate test artifact; observe mismatch.
- **Try these commands:** `python -m labsec.cli checksums --base . --output build/hashes.json service/main.py`
- **Evidence to preserve:** Before/after hashes, trust caveat.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 47 — Day 2: Sigstore concepts
- **Learn/build:** Explain Fulcio, Rekor, OIDC token subject, ephemeral key, bundle and transparency log.
- **Try these commands:** `cosign version`
- **Evidence to preserve:** Signer trust map.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 48 — Day 3: GitHub release job review
- **Learn/build:** Inspect permissions, event, artifact outputs, stage separation; identify when event is trusted.
- **Try these commands:** `cat .github/workflows/release.yml`
- **Evidence to preserve:** OIDC privilege review.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 49 — Day 4: Signed release on GitHub
- **Learn/build:** On your eligible repository, tag reviewed commit; collect real Cosign Sigstore bundle and provenance.
- **Try these commands:** `git tag -a v1.0.0 -m release; git push origin v1.0.0`
- **Evidence to preserve:** Workflow run URI and artifacts; if unavailable mark NOT RUN.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 50 — Day 5: Independent verify
- **Learn/build:** Verify exact certificate identity/issuer and subject; try wrong identity, altered artifact.
- **Try these commands:** `cosign verify-blob --help; gh attestation verify --help`
- **Evidence to preserve:** Signer verification log and negative test.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

**Week 10 graduation checklist:**
- [ ] Demonstrate checksums vs cryptographic identity-bound signatures.
- [ ] The key example passes and its matching unsafe negative control fails.
- [ ] Preserve a real terminal or GitHub run with tool version, artifact hash and commit reference.
- [ ] One written note describes limitations, one troubleshooting lesson and one resume-relevant skill.

## Week 11: Provenance/SLSA and release assurance
**Project:** P3 graduation. **Outcome:** Explain what the attested artifact proves and what it cannot prove.

### Session 51 — Day 1: SLSA levels
- **Learn/build:** Contrast provenance present, signed hosted provenance and hardened builder; avoid unverified L3 claims.
- **Try these commands:** `cat docs/PRIMARY_SOURCES.md`
- **Evidence to preserve:** SLSA control assessment table.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 52 — Day 2: Attestation subject
- **Learn/build:** Inspect provenance subject digest, GitHub repo/ref/commit and triggering event; compare against zip/hash.
- **Try these commands:** `gh attestation verify --help`
- **Evidence to preserve:** Subject-to-release evidence.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 53 — Day 3: Tamper and identity negatives
- **Learn/build:** Modify one downloaded release copy and attempt alternate signer verification; collect rejected results.
- **Try these commands:** `cosign verify-blob --help`
- **Evidence to preserve:** Evidence that unsigned bytes or wrong identity are rejected.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 54 — Day 4: Release assurance dossier
- **Learn/build:** Fill template: SBOM count, verified signer, unresolved issues, exceptions, SAST/SCA results and links.
- **Try these commands:** `cat reports/templates/RELEASE_ASSURANCE.md`
- **Evidence to preserve:** Auditable release document.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 55 — Day 5: P3 completion demo
- **Learn/build:** Record three-minute demo showing SBOM, signature, provenance and explicit limitations.
- **Try these commands:** `git log -1 --oneline`
- **Evidence to preserve:** P3 case study with functioning download/verification path.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

**Week 11 graduation checklist:**
- [ ] Explain what the attested artifact proves and what it cannot prove.
- [ ] The key example passes and its matching unsafe negative control fails.
- [ ] Preserve a real terminal or GitHub run with tool version, artifact hash and commit reference.
- [ ] One written note describes limitations, one troubleshooting lesson and one resume-relevant skill.

## Week 12: Integration, scaling and career presentation
**Project:** All three. **Outcome:** Make this cohesive enough for a DevSecOps/security engineering interview.

### Session 56 — Day 1: End-to-end controlled change
- **Learn/build:** Add safe service update and tests, PR, policy, scans, merge and reviewed tag; track events.
- **Try these commands:** `git status --short; python -m pytest -q`
- **Evidence to preserve:** Commit → PR → CI → release dependency chain.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 57 — Day 2: Adversarial security gates
- **Learn/build:** Run two more negative tests: unsafe manifest and wrong-signature identity; confirm documented failures.
- **Try these commands:** `make policy-negative`
- **Evidence to preserve:** Detection coverage and known blindspots.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 58 — Day 3: Report precision
- **Learn/build:** Write separate CI failure analysis, IaC policy report and release assurance report; distinguish observations from claims.
- **Try these commands:** `ls reports/templates`
- **Evidence to preserve:** Three sanitized completed reports.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 59 — Day 4: GitHub and video presentation
- **Learn/build:** Pin primary repo, publish architecture and 2–4 minute demo; add a concise image/diagram without disclosing credentials.
- **Try these commands:** `git remote -v`
- **Evidence to preserve:** Recruiter-first README and demo storyboard.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

### Session 60 — Day 5: Interview self-test and progression
- **Learn/build:** Answer 10 interview questions; score acceptance criteria, log unresolved risks and propose v1.1 roadmap.
- **Try these commands:** `python -m pytest -q; git status --short`
- **Evidence to preserve:** Final scorecard, evidence links and next-step plan.
- **Self-review:** Explain why the operation is secure, what it cannot prove, how to induce a failure, and how to verify the fix.

**Week 12 graduation checklist:**
- [ ] Make this cohesive enough for a DevSecOps/security engineering interview.
- [ ] The key example passes and its matching unsafe negative control fails.
- [ ] Preserve a real terminal or GitHub run with tool version, artifact hash and commit reference.
- [ ] One written note describes limitations, one troubleshooting lesson and one resume-relevant skill.

## Three progressive recruiter demonstrations

**Demo A, Junior DevSecOps (after Week 4):** Clone, run tests, show non-root container, show a failed PR and a repaired PR. Explain CodeQL vs dependency scanning. Keep it under four minutes.

**Demo B, Security Engineer (after Week 8):** Show terraform review (no apply), accepted plan and refused public SSH plan, compliant Kubernetes manifest and unsafe rejection, then demonstrate a real live Kubernetes PSA rejection only if actually executed.

**Demo C, Supply-chain Security (after Week 12):** Show real source/image SBOM, keyless Cosign bundle, precise OIDC certificate identity, attestation subject digest, and a negative tamper verification. Admit any unfinished cloud/image production work.

## Optional Months 4–6: advanced engineering milestones

1. Build an actual GHCR container image under an owned repository, resolve and pin its OCI digest, and connect digest-pinned Kubernetes deployment to its SBOM and image attestation.
2. Deploy Kyverno or OPA Gatekeeper in a disposable kind cluster with a network policy-capable CNI; compare admission rules to Conftest rules and verify both deny equivalent inputs.
3. Build Terraform on an owned AWS sandbox using ephemeral OIDC IAM roles, encrypted remote state, cost estimation, least privilege and approval gates. Record cleanup.
4. Add VEX metadata for a confirmed dependency vulnerability, with evidence that the affected code path is unreachable or mitigation is applied; maintain expiry and review.
5. Harden GitHub Actions with immutable action SHAs, reusable workflows and separated producer/consumer trust boundaries; assess SLSA Build L3 against its actual requirements.
6. Add policy coverage measurements, mutation tests, CI timing budgets, Dependabot automation, provenance-aware promotion and rollback demonstrations.

## Weekly study log template

```markdown
## Week __ / Session __
- Objective:
- Lab environment and versions:
- Commands executed:
- Expected / actual (PASS / FAIL / NOT RUN):
- Negative test and why it was rejected:
- Commit SHA / CI URL / artifact digest:
- What the result does NOT prove:
- Next remediation or feature:
```

## Final portfolio exit criteria

- [ ] P1: reviewed code + passing unit tests, actual protected PR gate, one deliberate denial and remediation, reproducible container, scan report.
- [ ] P2: actual Conftest acceptance/denial, Terraform `validate`, K8s restricted policy, negative corpus, honest live-test status.
- [ ] P3: actual Syft source and image SBOM, valid signature bundle, provenance attestation verified by digest/identity, successful tamper rejection.
- [ ] One end-to-end walkthrough connects all three, with source commit, release artifact and independently checked evidence.
- [ ] README includes architecture, project role, security boundaries, limitations, troubleshooting, portfolio/demo links and CV-ready descriptions.

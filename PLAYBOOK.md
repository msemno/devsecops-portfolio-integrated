# DevSecOps Engineer — Complete Hands-On Implementation Playbook

**Version:** 1.0 | **Date:** 2026-10-20 | **Targets:** Kali Linux VM / Linux laptop / WSL2 (with supported Docker backend) | **Projects:** Secure CI/CD Pipeline, Terraform & Kubernetes Policies, SBOM + Signing + Provenance.

> **Portfolio target:** An engineer can clone this repository, reproduce security checks, distinguish offline fixture evidence from live infrastructure, deliberately trigger failures, submit a reviewed pull request, and verify a released artifact's provenance without needing to trust screenshots.

## 0. How to use this guide

Follow the numbered stages in sequence. Commands are for an **isolated machine or an account you own**. Do not run Terraform `apply` against a real account until an owner approves the plan, budget, security group exposure, and credentials. The AWS example is **plan/design only**; no cloud is created automatically. The Kubernetes production image contains a **placeholder digest** and must be replaced before a real deployment. The demo deliberately includes insecure fixture files under `k8s/fixtures` and `fixtures/terraform`: these are policy regression inputs, never workloads to deploy.

Keep an `evidence/` folder locally with UTC timestamps, tool versions, terminal logs, screenshots, links to the GitHub run and commit SHA. **Do not add genuine secrets, customer data, unredacted credentials, cloud state or private signing keys to Git.** For portfolio work, public sanitized evidence is sufficient.

### Three portfolio objectives and why they connect

| Project | What you build | What you prove | Artifact used by the next project |
|---|---|---|---|
| P1 Secure CI/CD | App, unit tests, SAST, SCA, secrets and image scanning, PR gates | A failing finding blocks unsafe changes; fixes restore green builds | Container image, code and workflow evidence |
| P2 Terraform and Kubernetes policies | Terraform network configuration, Pod Security controls, NetworkPolicy, Rego admission-style checks | Insecure IaC configurations are rejected before deployment | Approved deployment config, policy test results |
| P3 SBOM, signing, provenance | Real SPDX SBOM, deterministic source archive, Sigstore bundle, GitHub attestations | Consumer can independently verify source, signer, subject digest and build workflow | Recruiter demo + verifiable release dossier |

### What this package can validate offline

- `pytest`: API behavior and policy/integrity code.
- `python -m labsec.cli policy`: baseline check of YAML and a realistic Terraform plan-shaped JSON fixture.
- `make policy-negative`: known-bad inputs must be **rejected**; success of this script proves refusal behavior.
- Local SHA-256 manifest: files were not modified since the manifest was written, conditional on a trustworthy expected manifest.

### What requires your environment

- Docker container execution, Trivy image/config scans, Syft SBOM enumeration, Conftest Rego, Terraform initialization/provider validation, live `kind`, GitHub Actions, CodeQL, GitHub OIDC, Cosign keyless signing and attestation verification. **A committed workflow is not proof it ran.**

---

## 1. Computer and tooling prerequisites

Recommended learner VM: Kali Linux, 2–4 vCPU, 4–8 GB RAM, at least 50 GB free disk, NAT for updates, a snapshot before installation. Running Kali + Docker + `kind` concurrently is easier with **16 GB host RAM**, preferably **24–32 GB** for more advanced clusters. `kind` can be stopped between exercises; Terraform validation and the offline Python tests require much less memory. A 64-bit x86_64 machine is assumed in binary examples; substitute ARM64 builds for aarch64.

Pre-study skills: terminal/navigation, Python virtual environments, Git branching, HTTP requests/responses, YAML, process/container isolation, IP networking, IAM/least privilege, JSON, and SHA-256 vs digital signatures. Learn enough HCL and Rego to modify rules—not merely copy a scanner configuration.

### 1.1 Kali base installation

```bash
cat /etc/os-release
uname -m
free -h
df -h
sudo apt update
sudo apt full-upgrade -y
sudo apt install -y git curl wget jq ca-certificates gnupg unzip make \
  python3 python3-venv python3-pip docker.io
python3 --version
git --version
```

If Kali package mirrors name Docker differently, use Docker's supported installation instructions for that distribution; don't paste an Ubuntu apt repository into Kali uncritically. Do not download executable scripts from unverified third-party tutorial sites.

```bash
# Rootful Docker lab only; note group membership grants root-equivalent control.
sudo systemctl enable --now docker
sudo docker version
sudo docker run --rm hello-world
# Optional convenience, requiring logout/login for group changes:
sudo usermod -aG docker "$USER"
```

**Security interpretation:** Anyone in the local `docker` group can effectively gain host-root privileges. For shared or company machines, use rootless Docker or a dedicated VM and follow company policy. Running `docker` commands with `sudo` avoids adding the learner to this group.

### 1.2 Clone or extract the repository and create a local Python environment

```bash
cd ~/projects
# Extract downloaded ZIP here; if you publish it, prefer git clone <YOUR_GITHUB_URL>.
cd devsecops-portfolio-integrated-v1.0
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m pytest -q
make policy
make policy-negative
```

If `~/projects` does not yet exist, `mkdir -p ~/projects`. Record the test outcome and `python --version`. The Python test count may grow as you add coverage.

### 1.3 Install official Terraform without making a cloud account mandatory

Terraform CLI is separately distributed by HashiCorp. On supported Debian/Ubuntu, use HashiCorp's signed apt repository. Kali is rolling and is **not necessarily a supported apt target**; on Kali download an architecture-specific binary and verify HashiCorp's signed checksum according to https://developer.hashicorp.com/terraform/install. Never run unverified binaries. After installation:

```bash
terraform version
terraform fmt -check -recursive iac/terraform
cd iac/terraform/aws
terraform init -backend=false
terraform validate
cd ../../..
```

`terraform init -backend=false` may download the public AWS provider; it does **not** need AWS credentials just to initialize or validate, but requires network access. `terraform plan` often needs real provider authentication and may trigger API calls. **Do not use `terraform apply` as part of the default coursework.**

If you own an AWS sandbox and explicitly choose to plan: set up a short-lived role with least privilege, set a spending budget, check the region and ownership, run `terraform plan -out=tfplan`, review the diff, then `terraform show -json tfplan > build/tfplan.json`. Store that output privately, because Terraform plans can contain sensitive data even when values are marked sensitive in some presentations. Never commit `tfplan`, `tfstate` or credentials. After an approved demo, destroy created resources and verify billing. A successful `terraform validate` is not evidence of a successful cloud deployment.

### 1.4 Install kubectl and kind (optional live Kubernetes exercise)

Official references: https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/ and https://kind.sigs.k8s.io/docs/user/quick-start/.

For x86_64, verify the kubectl download with the matching upstream SHA-256 file:

```bash
ARCH=amd64
KVER="$(curl -L -s https://dl.k8s.io/release/stable.txt)"
curl -fL -o kubectl "https://dl.k8s.io/release/${KVER}/bin/linux/${ARCH}/kubectl"
curl -fL -o kubectl.sha256 "https://dl.k8s.io/release/${KVER}/bin/linux/${ARCH}/kubectl.sha256"
echo "$(cat kubectl.sha256)  kubectl" | sha256sum -c -
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
kubectl version --client
```

Current checked kind version was v0.33.0. Verify and upgrade against the official download instructions when necessary:

```bash
curl -fLo kind https://kind.sigs.k8s.io/dl/v0.33.0/kind-linux-amd64
# In a production setup verify the published artifact/checksum before installation.
chmod +x kind
sudo mv kind /usr/local/bin/kind
kind version
kind create cluster --name devsecops-portfolio
kubectl cluster-info --context kind-devsecops-portfolio
kubectl get nodes
```

Do not run untrusted images in the cluster. The base Deployment is not runnable until its intentionally fake image digest is replaced. The policy testing exercises work **without** creating a Kubernetes cluster. Some environments need Docker's cgroup and overlay filesystem features; if `kind` fails inside a constrained VM, perform policy-only exercises first or move to a supported local host.

### 1.5 Conftest and Rego policy engine

Conftest v0.71.1 (latest reviewed 2026-10-06) is published as release assets. **Verify the official published checksums**, and for stronger provenance verify the release attestation as described at https://www.conftest.dev/install/.

```bash
VERSION=0.71.1
ASSET="conftest_${VERSION}_Linux_x86_64.tar.gz"
BASE="https://github.com/open-policy-agent/conftest/releases/download/v${VERSION}"
mkdir -p /tmp/devsecops-conftest && cd /tmp/devsecops-conftest
curl -fL -O "${BASE}/${ASSET}"
curl -fL -o checksums.txt "${BASE}/checksums.txt"
grep " ${ASSET}$" checksums.txt | sha256sum -c -
tar -xzf "$ASSET"
sudo install -m 0755 conftest /usr/local/bin/conftest
cd ~/projects/devsecops-portfolio-integrated-v1.0
conftest --version
```

**Policy negative controls are critical:**

```bash
conftest test --policy policy/kubernetes k8s/base/deployment.yaml
conftest test --policy policy/terraform fixtures/terraform/secure-plan.json
# The next two commands SHOULD exit nonzero; record the reasons.
conftest test --policy policy/kubernetes k8s/fixtures/bad-deployment.yaml
conftest test --policy policy/terraform fixtures/terraform/insecure-plan.json
```

The Python baseline checker is deliberately independent of Conftest and does not imply that the Rego engine was executed. Compare their discrepancies and fix the weaker rule rather than assuming they are interchangeable.

### 1.6 Trivy, Syft and Cosign

Install these from official release pages or official verified packages, choosing the right OS/architecture:

- Trivy: https://trivy.dev/latest/getting-started/installation/ and https://github.com/aquasecurity/trivy
- Syft: https://github.com/anchore/syft (checked release v1.54.1); download and verify upstream checksums/signatures.
- Cosign: https://docs.sigstore.dev/cosign/system_config/installation/ and https://github.com/sigstore/cosign

Validate installed CLI versions: `trivy --version`, `syft version`, `cosign version`. Do not pipe remote installation scripts directly to `bash` without reviewing the content and verifying the release source. In GitHub Actions this repository uses official published actions to acquire the tools.

Expected commands, after installing the CLIs:

```bash
trivy config iac/terraform/aws
trivy config k8s/base
trivy fs --scanners secret .
trivy fs --scanners vuln,secret --severity HIGH,CRITICAL .
# Syft filesystem SBOM (actual content depends on resolved dependencies)
mkdir -p build
syft dir:. -o spdx-json=build/filesystem.spdx.json
python -m labsec.cli validate-sbom build/filesystem.spdx.json
```

A filesystem SBOM is **not identical** to a container image SBOM. Generate both in later weeks and explain why OS packages and runtime-resolved libraries may differ from source manifest dependencies.

---

## 2. Project 1 — Secure CI/CD Pipeline

### 2.1 Purpose and architecture

Create a small, readable application that demonstrates security controls around ordinary software delivery. The sample service has `/healthz` and `/v1/build`, with simple security headers; it intentionally avoids authentication and cloud credentials. Its value is the security surrounding the build rather than a complex business feature.

```text
Developer pushes branch
  | checkout source without persisted credentials
  | tests + Python lint
  | CodeQL SAST
  | pip-audit: Python dependency advisories
  | Trivy: IaC, secrets and image vulnerabilities
  | policy-as-code: known-good and known-bad fixtures
  V
Branch protection: reviewed changes + required status checks
  |
Main branch
  |
Tag-specific release workflow (isolated trust boundary)
```

### 2.2 Build and test the service

```bash
python -m pip install -r requirements-dev.txt
uvicorn service.main:app --host 127.0.0.1 --port 8080
# In another terminal:
curl --fail --silent http://127.0.0.1:8080/healthz
curl --fail --silent http://127.0.0.1:8080/v1/build
curl -sD - -o /dev/null http://127.0.0.1:8080/healthz
python -m pytest -q
```

Expected: HTTP 200 `/healthz`, JSON response `status=ok`, security headers, no secrets in build metadata. The unit test intentionally defines a fake `AWS_SECRET_ACCESS_KEY` to confirm it is not serialized. Do not interpret this as a complete secrets-leakage proof.

### 2.3 Build and locally scan an OCI container

```bash
sudo docker build --file docker/Dockerfile --tag devsecops-demo:local .
sudo docker image inspect devsecops-demo:local --format '{{.Id}}'
sudo docker run --rm --read-only --cap-drop=ALL --security-opt no-new-privileges \
  --pids-limit 128 --memory 256m --cpus 0.5 -p 127.0.0.1:8080:8080 devsecops-demo:local
# Second terminal:
curl --fail http://127.0.0.1:8080/healthz
trivy image --severity HIGH,CRITICAL --ignore-unfixed devsecops-demo:local
syft devsecops-demo:local -o spdx-json=build/image.spdx.json
```

**Inspect:** `USER` in Dockerfile, absence of unnecessary Linux capabilities, read-only root filesystem, disabled privilege escalation, resource limits in Kubernetes, and image dependency advisories. A `RUN pip install` layer with unpinned transitive dependencies is not a perfectly reproducible build; improve it using a hash-locked dependency manifest as an advanced exercise. The Docker base currently uses a tagged `python:3.13-slim` for accessibility; **replace with a verified immutable digest and document the update process**.

### 2.4 Implement genuine security gates

1. Configure `quality.yml` to run on push and PR without write/OIDC permissions. Confirm its run logs.
2. Keep separate jobs for tests, Conftest policies, Trivy config/secret scans, and a built image scan. A failing job must visibly block merge once branch protection is configured.
3. Enable `codeql.yml` and inspect CodeQL Python results. Check repository CodeQL availability and code-scanning settings (plans/features vary).
4. Run `pip-audit --requirement requirements.txt` and explain direct versus transitive dependency findings. Do not invent a CVE result if current advisories return clean.
5. Add a service endpoint unit test, then deliberately break it in a temporary branch. Make the PR fail. Restore the code and show a green build.
6. Add a *synthetic, non-credential* scanner fixture in a temporary local branch or commit; test the secret-scanner behavior and **do not publish anything that resembles a real usable token**. Record whether it detected the fixture.
7. Simulate a policy regression by replacing the manifest's image digest with `:latest` in a disposable branch; verify failure.
8. Require status checks on `main` and one reviewer. Record GitHub settings plus a blocked PR.
9. Verify GitHub Actions secrets are not printed, third-party actions are pinned to full immutable SHAs as a hardening milestone, and PR workflows cannot mint attestation OIDC tokens.
10. Open a remediation issue for each genuine tool finding; never globally disable gates to force a demo green.

### 2.5 Mandatory negative/positive tests

| ID | Action | Expected | Evidence |
|---|---|---|---|
| CI-A | Run unit tests with original code | PASS | pytest/action log |
| CI-B | Temporarily alter `/healthz` result | FAIL | failing assertion and diff |
| CI-C | Restore endpoint | PASS | reviewed PR with diff |
| CI-D | Remove non-root container fields in a fixture | DENY | Conftest/Trivy result |
| CI-E | Set world SSH on an IaC fixture | DENY | policy result |
| CI-F | Modify approved digest in temporary branch | DENY | policy result |
| CI-G | Deliberately introduce a package advisory in isolated test branch | FAIL | SCA finding with triage notes |
| CI-H | Merge behind required status checks | BLOCK until green | screenshot / GitHub checks URL |

### 2.6 Acceptance criteria: P1

- [ ] Fresh clone installs and tests pass locally and on a hosted runner.
- [ ] The demo service runs on loopback and in a non-root container.
- [ ] GitHub has actual PR security gates, not only YAML.
- [ ] A failing PR is blocked; a corrected PR is accepted.
- [ ] At least one verified SAST/SCA/secret/image scan result is documented with tool/version/commit.
- [ ] Findings are triaged with a transparent policy for false positives.
- [ ] `README` has a one-minute summary, architecture, reproduction and screenshots.

---

## 3. Project 2 — Terraform and Kubernetes Policies

### 3.1 Threat model and learning outcomes

Infrastructure as Code can misconfigure internet ingress, privileges, identity, logging or security posture. Kubernetes introduces separate Pod runtime security, RBAC and network boundaries. Learn what **static configuration checks** can prove versus what requires **live admission/controller behavior**. Map controls to least privilege and Kubernetes Restricted Pod Security Standards.

```text
HCL in iac/terraform/aws ──▶ terraform fmt/validate ──▶ terraform plan (optional) ──▶ plan JSON
             |                                                     |
             └──▶ Trivy config ────────────────────────────────────▶ Conftest Rego
Kubernetes deployment YAML ──▶ Conftest + Trivy ──▶ PSA (live kind optional)
                          └──── negative fixture test suite ───────▶ PR gate
```

### 3.2 Inspect and validate Terraform network design

Read `iac/terraform/aws/versions.tf`, `variables.tf`, `main.tf`, `outputs.tf`. The example defines a VPC and a narrow ingress security group; it does not create infrastructure by default. Review whether provider locks, region, CIDR approval, egress, flow logs, cloud budgets, remote state encryption and IAM could be improved.

```bash
terraform fmt -check -recursive iac/terraform
(cd iac/terraform/aws && terraform init -backend=false && terraform validate)
trivy config iac/terraform/aws
python -m labsec.cli policy --tf-plan fixtures/terraform/secure-plan.json
python -m labsec.cli policy --tf-plan fixtures/terraform/insecure-plan.json
conftest test --policy policy/terraform fixtures/terraform/secure-plan.json
conftest test --policy policy/terraform fixtures/terraform/insecure-plan.json
```

The final two commands are designed to pass and fail respectively. If the insecure fixture **passes**, inspect the input structure before concluding that your rule works.

**Exercise A:** widen ingress SSH from an approved CIDR to `0.0.0.0/0` in a temporary plan fixture. Expected deny. **Exercise B:** permit 443 only to a private network; expect pass. **Exercise C:** use world-accessible port `3389`; expect deny. **Exercise D:** simulate unresolved ports; require manual review. **Exercise E:** test resource deletion; determine when a deleted public rule should not trigger a new deployment failure.

Remember that static HCL scanning and Terraform *plan* JSON are not interchangeable: data sources/computed values and modules may require `plan` and live context to resolve, and a simplified fixture cannot model all provider semantics.

### 3.3 Review and validate Kubernetes manifests

Important fields in `k8s/base/deployment.yaml`: pod-level non-root identity and seccomp RuntimeDefault, drop ALL capabilities, prevent privilege escalation, read-only root filesystem, resources, readiness/liveness probes, automount service account false, immutable image digest. Additional manifest files configure a restricted PSA namespace, ClusterIP service and NetworkPolicy.

```bash
python -m labsec.cli policy --k8s k8s/base/deployment.yaml
python -m labsec.cli policy --k8s k8s/fixtures/bad-deployment.yaml
conftest test --policy policy/kubernetes k8s/base/deployment.yaml
conftest test --policy policy/kubernetes k8s/fixtures/bad-deployment.yaml
trivy config k8s/base
```

**Kubernetes policy exercises:**

1. Replace `@sha256:` with `:latest`, run Rego and Python tests, confirm both deny.
2. Set `hostNetwork: true`, confirm deny and explain why host networking violates isolation requirements.
3. Set `automountServiceAccountToken: true` and explain when a workload actually needs API access.
4. Set `allowPrivilegeEscalation: true`, then `privileged: true` as separate controls; inspect whether each scanner catches both conditions. Add a Rego rule for `privileged` if missing.
5. Remove memory limits then requests; explain how scheduler planning and DoS risks differ.
6. Drop `readOnlyRootFilesystem`; confirm the policy rejects it.
7. Change `seccompProfile.type` to `Unconfined`; compare against restricted PSA behavior.
8. Remove egress NetworkPolicy; explain that checking one Deployment alone cannot prove namespace segmentation.
9. Add an annotation carrying policy-exception metadata; implement expiry and approval logic for exceptions in a later version.
10. Write a fresh negative fixture and corresponding positive fixture: your test corpus must grow with every rule.

### 3.4 Optional live kind cluster validation

**Important:** The committed deployment has a placeholder `ghcr.io/replace-owner/devsecops-demo@sha256:aaaa...` digest for *static policy checks only*. It will not pull or run. Keep production policy strict and create a separate local deployment for testing, documenting the exception. One practical path is to build/load a local image and temporarily substitute the image field in a disposable copy; do **not** weaken the production policy or commit a tag-only image as compliant.

```bash
kind create cluster --name devsecops-portfolio
sudo docker build -f docker/Dockerfile -t devsecops-demo:local .
# Depending on Docker permissions, kind load may require access to the same daemon:
kind load docker-image devsecops-demo:local --name devsecops-portfolio
kubectl apply -f k8s/base/namespace.yaml
kubectl get ns devsecops-demo --show-labels
# Local-only rendered copy uses a tag and is intentionally excluded from production Rego checks.
mkdir -p build
sed 's#ghcr.io/replace-owner/devsecops-demo@sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa#devsecops-demo:local#' \
  k8s/base/deployment.yaml > build/deployment-local.yaml
# Set imagePullPolicy: Never in a local-only manifest if the image pull behavior needs it.
kubectl apply -f build/deployment-local.yaml
kubectl apply -f k8s/base/service.yaml
kubectl apply -f k8s/base/networkpolicy.yaml
kubectl rollout status deployment/devsecops-demo -n devsecops-demo --timeout=120s
kubectl get pods -n devsecops-demo -o wide
kubectl describe deployment devsecops-demo -n devsecops-demo
```

For cluster runtime troubleshooting use `kubectl describe pod` and `kubectl logs`; for smoke testing use `kubectl port-forward service/devsecops-demo -n devsecops-demo 8080:8080` and curl localhost. If your local image cannot be pulled due to `imagePullPolicy`, explicitly set `Never` in a **separate disposable local copy only**. The production manifest should continue using the verified digest. NetworkPolicy enforcement depends on CNI capabilities; `kind` default networking may not enforce NetworkPolicies. Add an appropriate CNI before claiming segmentation tests passed; record the CNI and deny/allow pod-to-pod test results.

Test rejected Pod security **without deploying a vulnerable workload**:

```bash
kubectl apply --dry-run=server -n devsecops-demo -f k8s/fixtures/bad-deployment.yaml
# Expect a policy admission rejection when namespace PSA is enforced.
```

A server-side dry-run exercises API admission validation without creating the resource. The simple fixture has no namespace; `-n devsecops-demo` supplies its namespace. Record the actual response, not just the intended outcome. Remove the cluster after testing: `kind delete cluster --name devsecops-portfolio`.

### 3.5 Acceptance criteria: P2

- [ ] HCL formatting and Terraform validation are reproducible without deploying cloud resources.
- [ ] Static config scans plus Conftest checks run in CI and locally.
- [ ] Known-good manifests/plans pass; insecure variants **fail** with intelligible messages.
- [ ] At least six Kubernetes policy regression fixtures are tested.
- [ ] Protected branches cannot silently merge policy violations.
- [ ] Live PSA rejection has independent proof if you claim it as completed.
- [ ] Network isolation is not claimed without a CNI that enforces NetworkPolicy and packet-level tests.
- [ ] Documentation explains plan vs apply, secrets in Terraform state, identity and resource ownership.

---

## 4. Project 3 — SBOM, Signing and Build Provenance

### 4.1 Understand the four artifacts

**Inventory / SBOM:** lists discovered components with versions and package identifiers. It does not prove code is safe or a build is trusted. **Digest / SHA-256:** demonstrates byte-level equality against a trusted expected digest. **Digital signature:** associates an identity/key with bytes; verification requires trusted key/certificate/issuer/identity. **Provenance attestation:** a signed statement about a build's materials, environment and process; it is only as trustworthy as its builder and verification policy.

Learn **SPDX vs CycloneDX**, transitive dependencies, build-time vs runtime dependencies, lockfiles, package vulnerability matching, VEX, artifact immutability, Sigstore Fulcio certificates, Rekor transparency log, OIDC workload identity, GitHub action permissions and SLSA Build Levels.

### 4.2 Generate a genuine local SBOM

After installing Syft, record CLI version and run:

```bash
mkdir -p build
syft dir:. -o spdx-json=build/source.spdx.json
python -m labsec.cli validate-sbom build/source.spdx.json
# Image SBOM, only after building a local Docker image:
syft devsecops-demo:local -o spdx-json=build/image.spdx.json
python -m labsec.cli validate-sbom build/image.spdx.json
```

**Do not fake SBOM output.** Compare source and image component counts, identifiers, OS packages, missing dependencies, paths and which layers each tool inspected. Explain why `requirements.txt` alone does not provide a full dependency graph.

### 4.3 Practice SHA-256 integrity but do not call it signing

```bash
mkdir -p build
python -m labsec.cli checksums --base . --output build/source-hashes.json \
  service/main.py requirements.txt docker/Dockerfile
python -m labsec.cli verify-checksums --base . --manifest build/source-hashes.json
# Modify a local temporary copy, regenerate a separate manifest first, then verify.
```

The generated JSON manifest itself is *unsigned*, so an attacker who can rewrite both artifacts and hashes may evade detection. The negative test modifies a file while leaving the expected manifest unchanged; that catches tampering, but **not an attacker who can replace the trusted manifest too**. This is why P3 adds independent signed claims.

### 4.4 Build an attested source artifact via a GitHub release workflow

Read `.github/workflows/release.yml` carefully. The release job is intentionally separate from the PR job and grants `id-token: write` only in a controlled job. It:

1. Checks out a known source revision with persisted credentials disabled.
2. Repeats core test and policy checks.
3. Creates a source tarball from the committed tree using `git archive`; gzip timestamp flags reduce incidental reproducibility noise.
4. Computes a local SHA-256 checksum for easy download integrity comparison.
5. Calls Syft via `anchore/sbom-action` and validates the resulting SPDX JSON.
6. Uses GitHub `actions/attest@v4` to create signed build provenance and an associated SBOM attestation.
7. Uses Cosign with GitHub OIDC to generate a keyless signature bundle for the tarball.
8. Verifies the tarball signature against a precise expected GitHub workflow identity and issuer **before** publishing.
9. Uploads the source, checksum, SBOM and Sigstore bundle as a GitHub Actions artifact.

**Important availability requirement (checked October 2026):** On GitHub Free/Pro/Team, artifact attestations are available for **public repositories**, while private/internal repository attestations need Enterprise Cloud. If you plan to keep this portfolio private, first verify your plan's feature eligibility. Consider building a public repository using only synthetic materials and no organization-specific secrets; do not bypass privacy requirements.

### 4.5 GitHub repo initialization, permissions and release

```bash
git init
git add .
git commit -m "feat: connected DevSecOps portfolio foundation"
git branch -M main
# Create your own empty repository in GitHub, then:
git remote add origin git@github.com:YOUR-USERNAME/devsecops-portfolio.git
git push -u origin main
```

Configure Rulesets/branch protection: require reviewers + quality checks, restrict force-pushes and deletion, review changes to `.github/workflows/`, enforce CODEOWNERS if desired, enable dependency graph/Dependabot and secret scanning where supported. Avoid `pull_request_target` for running untrusted PR code. Actions triggered by forks must not access privileged release secrets. The sample release triggers on `v*` tags and manual runs and declines forked repository execution; in production restrict tag creation and signing authority as well.

Tag only a reviewed revision after CI becomes green:

```bash
git status --short
git log -1 --oneline
git tag -a v1.0.0 -m "Security-reviewed DevSecOps lab release"
git push origin v1.0.0
```

If GitHub hosted tests fail, fix the **cause** and rerun. No current environment can guarantee future CVE database content. For an auditable release, collect the GitHub Actions run permalink, artifact hashes, exact tool versions and signer identity. If the release fails due to GitHub account attestation feature restrictions, record this as **not completed** until run on an eligible public repository.

### 4.6 Independent signature and attestation verification

Use downloaded signed artifact + `source.sigstore.json`. The exact identity for tagged release includes **your** repository and tag:

```bash
export OWNER='YOUR-USERNAME'
export REPO='devsecops-portfolio'
export TAG='v1.0.0'
export IDENTITY="https://github.com/${OWNER}/${REPO}/.github/workflows/release.yml@refs/tags/${TAG}"
cosign verify-blob \
  --bundle dist/source.sigstore.json \
  --certificate-identity "$IDENTITY" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  dist/devsecops-source.tar.gz
```

Then use GitHub CLI (after `gh auth login` and enabling relevant features) to verify provenance:

```bash
gh attestation verify dist/devsecops-source.tar.gz --repo "${OWNER}/${REPO}"
```

You must verify that the returned subject digest matches the downloaded tarball, the signer/build repository is what you expected, and the build event/ref are trusted. A genuine but incorrectly identified workflow **must not be accepted**. Run negative cases: modify one byte in a copy of the signed artifact; verify should fail. Provide a wrong certificate identity; verify should fail. Remove the SBOM; your release dossier should mark inventory evidence unavailable, never silently pass.

### 4.7 Nuances recruiters will ask about

**Does signing make malware safe?** No. It binds bytes to a key/identity; compromised trusted build infrastructure can sign malicious artifacts. **Does SLSA L3 follow from one GitHub attestation?** No. SLSA Level 3 requires a hardened build platform and additional constraints; GitHub documents a reusable-workflow path toward L3 that must be evaluated on its own merits. **Does provenance prove the image was built from the same source tarball?** Not unless provenance materials/subject mapping and actual image are bound and verified. The starter signs a **source tarball**. Image signing/attestation and admission verification are follow-on work.

**Trust improvement exercises:** pin action references to 40-character commit SHAs, require approval for release tags, use reusable isolated build workflows, build/push an OCI image by digest to a registry you own, sign its digest and verify at admission. Prefer short-lived OIDC credentials for owned cloud infrastructure rather than stored static keys. Produce and verify VEX metadata when applicable.

### 4.8 Acceptance criteria: P3

- [ ] Real Syft SPDX SBOM created from source **and** image; compare differences.
- [ ] SBOM passes structural checks and manual coverage review.
- [ ] Changed artifact fails SHA and digital signature verification.
- [ ] A tagged hosted workflow generates a keyless Cosign bundle and signed provenance on an eligible repository.
- [ ] Verification checks exact issuer, workflow identity, tag, digest and expected repository.
- [ ] Wrong identity and altered bytes are independently rejected.
- [ ] GitHub run and download artifacts linked from a professional release assurance report.
- [ ] SLSA level claims are scoped to demonstrated controls rather than asserted from a single artifact.

---

## 5. Integration: proving the three projects form one lifecycle

### 5.1 The primary golden path

1. Feature branch adds a change to `service/main.py` and its unit test.
2. CI runs tests, dependency checks, CodeQL and image/config scans.
3. Terraform and Kubernetes designs pass **both** Python baseline and Rego policy checks.
4. CI confirms insecure fixtures are rejected (including broad SSH ingress, root pods and mutable images).
5. Peer review merges the change into protected `main`.
6. Reviewer authorizes `vX.Y.Z` tagged release.
7. Release workflow re-tests, builds source tarball, discovers components via Syft, creates authenticated build claims and keyless Cosign signature.
8. Another person downloads the artifact, verifies provenance/signature/subject digest and reads the release dossier.
9. An optional staging deployment uses a separately published digest-pinned, verified OCI image (requires adding an image release job; source signing alone is not enough).

### 5.2 Failure drill and remediation

Execute these in **throwaway branches/fixtures**, not the production path:

- **Broken unit test:** GitHub PR status red → developer fixes behavior → green.
- **Unsafe Terraform rule:** input allows SSH 0.0.0.0/0 → Conftest denies → restrict CIDR → pass.
- **Privileged Kubernetes workload:** violates restricted policy → deny → secure contexts → pass.
- **Vulnerable dependency:** scanner reports current CVE → record impact/exploitability and affected versions → update/waiver with explicit expiry.
- **Artifact tamper:** mutate bytes after build → checksum and signature mismatch → reject deployment.
- **Signing identity mismatch:** valid signature from wrong repo/tag → reject despite cryptographic validity.
- **Policy bypass attempt:** omit an expected field, use null, test unknown values; improve fail-closed checks.

### 5.3 Report connection

Create three reports using templates under `reports/templates`: (1) a CI failure and remediation technical write-up, (2) a policy evaluation report with good/bad inputs, (3) a release assurance dossier with actual verification results. Link all three from README. Mark every unexecuted item `NOT RUN`. Share no access keys or customer information.

---

## 6. Working GitHub repository structure

```text
devsecops-portfolio-integrated-v1.0/
├── START_HERE.md
├── README.md
├── PLAYBOOK.md
├── WEEKLY_PLAN.md
├── Makefile
├── service/                    # FastAPI demo
├── labsec/                     # policy/integrity checks and CLI
├── tests/                      # positive/negative regression suite
├── fixtures/terraform/         # synthetic plan JSON
├── docker/Dockerfile           # rootless-capable non-root workload
├── k8s/base/                   # deploy, namespace, service, network policy
├── k8s/fixtures/               # bad manifest, never deploy
├── iac/terraform/aws/          # owned-account optional design
├── policy/kubernetes/          # Conftest Rego
├── policy/terraform/           # Terraform plan JSON Rego
├── scripts/negative_tests.sh
├── .github/workflows/          # quality, CodeQL, release
├── docs/                       # threat model, source links, CI matrix
└── reports/templates/          # professional findings and release records
```

Use meaningful commits and GitHub project issues; make your commit messages describe security intent. Never present a copied template as wholly original engineering. Read the code, change tests, and measure outcomes. Add an `evidence/` directory only after redaction and privacy review; do not include raw credential material.

---

## 7. CI/CD debugging playbook

- **`pytest` ImportError:** activate `.venv`, ensure repo root is current directory; `python -m pytest -q`.
- **`terraform` unavailable:** install from verified official release; inspect architecture and `$PATH`.
- **`terraform init` network/provider error:** confirm official registry reachability; proxy/TLS; do not use `-lock=false` or unchecked mirrors as a shortcut.
- **Conftest unexpectedly green on bad manifest:** run rule syntax checks, inspect parsed JSON (`conftest parse`), test missing/null fields, ensure correct `--policy` path, verify `deny` rule evaluates.
- **Trivy returns failure on new CVE:** inspect affected layer/package, fixability, exploitability and current fixed version, update base or dependency, log rationale; do not disable scanner globally.
- **Docker in Kali VM fails:** inspect `systemctl status docker`, `sudo docker info`, free disk, kernel capabilities and group permissions; do not make Docker TCP daemon publicly accessible.
- **Kind pod ImagePullBackOff:** base manifest has placeholder digest; use approved local overlay or publish an image and substitute its actual digest.
- **NetworkPolicy no impact in kind:** default cluster networking may lack enforcement; install/document supported CNI before claiming isolation.
- **GitHub attestation action error:** check repository plan/public/private eligibility, `id-token: write`, `attestations: write`, `artifact-metadata: write`, and Actions settings. Do not work around lack of access with forged JSON attestation output.
- **Cosign invalid identity:** signer URI includes actual repository and `refs/tags/vX.Y.Z`; compare certificate identity and OIDC issuer exactly.
- **`gh attestation verify` fails:** ensure matching artifact bytes, correct `--repo`, successful release run, and GitHub CLI authentication as needed.
- **GitHub Actions untrusted PR:** never grant release secrets/OIDC to general PR jobs or execute unreviewed PR scripts under `pull_request_target`.

---

## 8. Portfolio and recruiter review checkpoints

A hiring manager should see a 60-second architecture introduction, one successful CI run, one blocked PR proving safety, one real policy negative-control rejection, a real SBOM, a signed release verified against an expected identity, and a short list of limitations.

### GitHub pinned project README scoring (100 points)

| Dimension | Weight | What counts as strong evidence |
|---|---:|---|
| Reproducible app and architecture | 15 | one-command tests + diagram + scope |
| Quality gates in hosted CI | 20 | real run URLs + failing PR + remediation |
| IaC design and policy coverage | 20 | Terraform/manifest + Rego + diverse negative corpus |
| Supply-chain inventory + vulnerability management | 15 | real source/image SBOM + triage + scanner output |
| Artifact signing and independent verification | 15 | real OIDC bundle + exact signer + negative tamper test |
| Reporting and clarity | 10 | risk/impact/remediation/test evidence |
| Maintenance and polish | 5 | license, changelog, limitations, version updates |

A score is illustrative, not an employer calibration. Only mark areas proven by execution. Be prepared to explain every CI permission and why the release job cannot run for arbitrary fork code.

### Example CV bullets — only after completion

- **Secure CI/CD:** “Implemented GitHub Actions security gates for a Python service, combining CodeQL SAST, dependency and container scanning, and policy regression checks; demonstrated merge blocking with a failing test and reviewed remediation.”
- **IaC + Kubernetes:** “Developed Terraform and Kubernetes hardening controls with Conftest/Rego and Trivy, including negative-test fixtures for public SSH ingress and privileged containers.”
- **Signed releases:** “Produced SPDX SBOMs and a GitHub OIDC-keyless signed release with independently verified provenance and tamper-detection tests.”

### Advanced interview prompts

1. Why can a checksum be forged if the expected manifest is untrusted?
2. What does the OIDC issuer prove? What does the certificate identity need to constrain?
3. What are SAST, SCA, DAST, runtime protection and configuration scanning each unable to prove?
4. What is the difference between Terraform validate, plan, apply and drift detection?
5. How does namespace-level Pod Security Admission interact with Kyverno and network policy CNI enforcement?
6. Why is CodeQL's success not equivalent to zero vulnerabilities?
7. Why should fork PRs have read-only permissions and not access deployment secrets?
8. What is the difference between a source SBOM and an image SBOM?
9. How do you handle unfixable but exploitable advisories, false positives and expiring waivers?
10. What would have to change for a truthful SLSA Build L3 claim?

## 9. Official references

Follow `docs/PRIMARY_SOURCES.md` for GitHub, Sigstore, SLSA, Trivy, Conftest, Terraform and Kubernetes primary documentation. Before production use, compare version pinning and CLI flags against the current official release, and audit every third-party action at a full SHA rather than relying solely on a floating tag.

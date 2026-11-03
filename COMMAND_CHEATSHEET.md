# Operator command sheet — DevSecOps triple portfolio

Start in repository root. Prefix Docker commands with `sudo` when your user is not using a rootless Docker daemon or in a trusted Docker group.

## Zero-cloud, low-resource Day 1

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
make policy
make policy-negative
bash scripts/local_gate.sh
```

## Local application / container

```bash
uvicorn service.main:app --host 127.0.0.1 --port 8080
curl --fail http://127.0.0.1:8080/healthz
sudo docker build -f docker/Dockerfile -t devsecops-demo:local .
sudo docker run --rm --read-only --cap-drop=ALL --security-opt no-new-privileges -p 127.0.0.1:8080:8080 devsecops-demo:local
```

## Dependency, source, configuration and image scanning

```bash
pip-audit -r requirements.txt
trivy fs --scanners secret .
trivy config k8s/base
trivy config iac/terraform/aws
trivy image --severity HIGH,CRITICAL --ignore-unfixed devsecops-demo:local
```

## Kubernetes and Terraform policy

```bash
conftest test -p policy/kubernetes k8s/base/deployment.yaml
conftest test -p policy/kubernetes k8s/fixtures/bad-deployment.yaml   # EXPECT FAIL
conftest test -p policy/terraform fixtures/terraform/secure-plan.json
conftest test -p policy/terraform fixtures/terraform/insecure-plan.json  # EXPECT FAIL
terraform fmt -check -recursive iac/terraform
(cd iac/terraform/aws && terraform init -backend=false && terraform validate)
```

## Source and image SBOM

```bash
mkdir -p build
syft dir:. -o spdx-json=build/source.spdx.json
syft devsecops-demo:local -o spdx-json=build/image.spdx.json
python -m labsec.cli validate-sbom build/source.spdx.json
python -m labsec.cli validate-sbom build/image.spdx.json
```

## Local checksums (NOT a signature)

```bash
python -m labsec.cli checksums --base . --output build/hashes.json service/main.py requirements.txt docker/Dockerfile
python -m labsec.cli verify-checksums --base . --manifest build/hashes.json
```

## GitHub release artifacts (requires an eligible repo and OIDC)

```bash
git tag -a v1.0.0 -m 'Reviewed source release'
git push origin v1.0.0
# Download the source tar and Sigstore bundle after actual release succeeds.
bash scripts/verify_signed_release.sh YOUR-OWNER YOUR-REPO v1.0.0 dist/devsecops-source.tar.gz dist/source.sigstore.json
```

## Never claim without real output

- Docker, Terraform provider, Conftest, Trivy, Syft, Cosign, kind and hosted GitHub runs **require external execution**.
- A checksummed file is not authenticated provenance.
- A release YAML is not evidence of a successful signed release.
- A secure-looking manifest is not proof a cluster actually enforces its NetworkPolicies.

# First 15 actions on Kali Linux

**Do the first 10 commands before installing heavyweight tooling.** See `PLAYBOOK.md` for verified installer sources and alternatives. The baseline works without Docker, Terraform, Kubernetes or a cloud account.

```bash
# 1-2: verify your operating system and CPU
cat /etc/os-release
uname -m
# 3: check resources
free -h; df -h .
# 4: ensure apt indexes and basic packages
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git make curl jq
# 5: enter this extracted project directory
cd devsecops-portfolio-integrated-v1.0
# 6: install to an isolated Python environment
python3 -m venv .venv
# 7: activate
source .venv/bin/activate
# 8: install dependencies
python -m pip install -r requirements-dev.txt
# 9: run real automated unit tests
python -m pytest -q
# 10: check good configurations
python -m labsec.cli policy --k8s k8s/base/deployment.yaml --tf-plan fixtures/terraform/secure-plan.json
# 11: test expected failures (script returns success if rejects are correct)
make policy-negative
# 12: run the HTTP API locally
uvicorn service.main:app --host 127.0.0.1 --port 8080
# 13: in another terminal
curl --fail --silent http://127.0.0.1:8080/healthz
# 14: confirm selected security response headers
curl -I http://127.0.0.1:8080/healthz
# 15: stop uvicorn with Ctrl+C and record test outputs
```

**Stop and write down:** Python version, test count, detected policy failures, what a negative control demonstrates, what a checksum does not establish, and the Git commit SHA.

Next read `PLAYBOOK.md`, then work through `WEEKLY_PLAN.md`.

## One-command local verification

```bash
bash scripts/local_gate.sh          # reports missing external tools as NOT RUN
bash scripts/local_gate.sh --strict # returns exit code 2 if optional tools are missing
```

After a *real* signed hosted release, verify downloaded artifacts with:

```bash
bash scripts/verify_signed_release.sh OWNER REPO v1.0.0 \
  dist/devsecops-source.tar.gz dist/source.sigstore.json
```

The verifier requires both `cosign` and `gh` to succeed; it will not silently claim a signature-only check as full provenance verification.

#!/usr/bin/env bash
# Local verification helper; never label missing tools as successful tests.
set -euo pipefail
STRICT="${1:-}"
python -m pytest -q
make policy
make policy-negative
optional_missing=0
check_tool() {
  if command -v "$1" >/dev/null 2>&1; then return 0; fi
  echo "NOT RUN: required external tool is missing: $1" >&2
  optional_missing=1
  return 1
}
if check_tool conftest; then
  conftest test --policy policy/kubernetes k8s/base/deployment.yaml
  conftest test --policy policy/terraform fixtures/terraform/secure-plan.json
  if conftest test --policy policy/kubernetes k8s/fixtures/bad-deployment.yaml; then
    echo 'FAIL: Conftest accepted known-bad Kubernetes fixture' >&2;exit 1
  fi
  if conftest test --policy policy/terraform fixtures/terraform/insecure-plan.json; then
    echo 'FAIL: Conftest accepted known-bad Terraform fixture' >&2;exit 1
  fi
fi
if check_tool trivy; then
  trivy config k8s/base
  trivy config iac/terraform/aws
fi
if check_tool terraform; then
  terraform fmt -check -recursive iac/terraform
fi
if [[ "$STRICT" == '--strict' && "$optional_missing" -ne 0 ]]; then
  echo 'STRICT VALIDATION INCOMPLETE: install missing third-party tools' >&2
  exit 2
fi
if [[ "$optional_missing" -ne 0 ]]; then
  echo 'PARTIAL SUCCESS: Python controls passed, some external tools NOT RUN.'
else
  echo 'LOCAL GATES PASSED. This does not prove GitHub CI, cloud apply or release attestation.'
fi

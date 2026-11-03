#!/usr/bin/env bash
set -euo pipefail
# A passing negative test is a failure of the policy tool with a documented reason.
if python -m labsec.cli policy --k8s k8s/fixtures/bad-deployment.yaml; then
  echo 'ERROR: insecure Kubernetes fixture was accepted' >&2; exit 1
else echo 'PASS: insecure Kubernetes manifest rejected'; fi
if python -m labsec.cli policy --tf-plan fixtures/terraform/insecure-plan.json; then
  echo 'ERROR: insecure Terraform fixture was accepted' >&2; exit 1
else echo 'PASS: world-accessible SSH rejected'; fi

#!/usr/bin/env bash
# Usage: scripts/verify_signed_release.sh OWNER REPO TAG TAR_PATH SIGSTORE_BUNDLE
set -euo pipefail
if [[ $# -ne 5 ]]; then
  echo "Usage: $0 OWNER REPO TAG SOURCE_TAR SIGSTORE_BUNDLE" >&2; exit 2
fi
OWNER="$1";REPO="$2";TAG="$3";ARTIFACT="$4";BUNDLE="$5"
command -v cosign >/dev/null || { echo 'cosign is required; not verified' >&2; exit 2; }
IDENTITY="https://github.com/${OWNER}/${REPO}/.github/workflows/release.yml@refs/tags/${TAG}"
echo "Expected identity: ${IDENTITY}"
cosign verify-blob --bundle "$BUNDLE" \
  --certificate-identity "$IDENTITY" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  "$ARTIFACT"
if command -v gh >/dev/null; then
  gh attestation verify "$ARTIFACT" --repo "${OWNER}/${REPO}"
else
  echo 'NOT RUN: gh CLI absent; GitHub provenance independently unverified.' >&2
  exit 2
fi

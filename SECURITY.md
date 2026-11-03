# Security policy

Only test your own applications and owned/authorized infrastructure. This repository includes intentionally broken *test fixtures*; they are never production deployment manifests. Never commit tokens, private keys, genuine leaked secrets, cloud state or unredacted customer data.

Report vulnerabilities in this sample repository through a private contact route if you publish it. For any released key, revoke and rotate it before cleaning history; history rewriting alone is not remediation. GitHub Actions release OIDC permissions must not be given to untrusted pull requests.

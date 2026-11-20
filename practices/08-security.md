---
group: Security
id: "08"
version: 0.4
reviewed: 2026-11-17
---

# 08 · Security

Security is designed in, not added later. Conflicts in this group are always flagged as high priority.

## 08.1 Secrets management
- applies: always
- rule: Prefer, in this order: (1) no long-lived secret at all (short-lived credentials through OIDC or workload identity); (2) the platform's secret store or a secret manager (e.g. GitHub or Streamlit Cloud secrets, Vault, AWS Secrets Manager, Azure Key Vault), read at runtime or from files mounted at runtime; (3) secrets encrypted in the repo (e.g. SOPS with age or a cloud key service, Sealed Secrets for Kubernetes) only when there is no secret manager, with the decryption key never committed; (4) plaintext, git-ignored files for local development only. Secrets never live in code, committed plaintext files or image layers. Run secret scanning in pre-commit and CI.
- why: Encrypting a secret only moves the problem to the decryption key; the safest secret is one that does not exist or is held by a system that controls, audits and rotates access.
- alternatives: secret manager or platform store / secrets encrypted in the repo
- choose-when: T22 in ../guides/principle-tensions.md

## 08.2 OWASP Top 10
- applies: interfaces has-any (web-ui, internal-api, public-api)
- rule: Address the OWASP Top 10:2025 (including the new Software Supply Chain Failures and Mishandling of Exceptional Conditions categories) and, for APIs, the OWASP API Security Top 10 in design and review: injection, broken access control, misconfiguration and others.
- why: These cover most real-world web vulnerabilities.

## 08.3 Standard authentication
- applies: interfaces has-any (web-ui, internal-api, public-api)
- rule: Use standard protocols (OIDC / OAuth 2.x) and proven libraries or identity providers. Never implement your own crypto or password storage scheme.
- why: Home-made authentication is one of the most common sources of critical bugs.

## 08.4 Authorization: least privilege, deny by default
- applies: interfaces has-any (web-ui, internal-api, public-api)
- rule: Check authorization server-side on every request; deny by default; grant the minimum permissions needed.
- why: Broken access control is the top web risk.

## 08.5 Dependency hygiene
- applies: always
- rule: Pin dependency versions with a lockfile, scan for known vulnerabilities in CI, and automate update PRs.
- why: Most code you ship is other people's code.

## 08.6 SBOM and supply chain
- applies: stage=production
- rule: Generate an SBOM (CycloneDX or SPDX) for every release and verify the provenance of build artifacts.
- why: Lets you answer "are we affected?" within minutes when a new vulnerability appears; increasingly a regulatory expectation in the EU.

## 08.7 Threat modelling
- applies: stage>=mvp
- rule: For features that touch auth, payments, personal data or external input, do a short threat model (STRIDE) and record the mitigations.
- why: Finding a design flaw on paper is far cheaper than in production.

## 08.8 Web security configuration
- applies: interfaces has web-ui
- rule: Configure security headers (CSP, HSTS), CSRF protection and an explicit CORS allow-list.
- why: Browser defaults are permissive; these close common attack paths.

## 08.9 Container image hardening
- applies: deployment in (cloud, on-prem, regulated-env)
- note: only when the app is built as a container image (Dockerfile present, or 01.11 selected)
- rule: Use multi-stage builds: build in one stage, copy only the runtime artefacts into a minimal final image (no compilers, build tools or source). Pin base images by digest. Keep a `.dockerignore` (exclude `.git`, `.env`, tests). Never put secrets in build args or layers; use build secret mounts. Run as non-root, with a read-only filesystem where possible, add a HEALTHCHECK, and scan images in CI.
- why: Smaller images mean a smaller attack surface and faster deploys; a secret deleted in a later layer still exists in the earlier one.

## 08.10 Vulnerability handling
- applies: stage=production
- rule: Publish a security contact (SECURITY.md), define patch timelines by severity, and track fixes to closure.
- why: Someone will find a vulnerability; a process decides how much it costs.

## 08.12 Credential rotation and leak response
- applies: stage>=mvp
- rule: Give every credential (API keys, tokens, database passwords, signing keys) a named owner and a place where it is recorded (not its value). Rotate immediately on any suspected exposure, and on a schedule for long-lived credentials. Keep a short leak runbook: revoke, replace, deploy the new value, check the provider's usage logs, record what happened. Set spending or usage limits on paid APIs.
- why: Encryption and scanning reduce leaks but do not undo one; only fast revocation limits the damage, and usage limits cap the cost of a leaked paid key.

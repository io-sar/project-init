---
group: Delivery (CI/CD and environments)
id: "11"
version: 0.4
reviewed: 2026-11-17
---

# 11 · Delivery: CI/CD and environments

Make releasing boring: small, frequent, automated and reversible.

## 11.1 CI on every change
- applies: stage>=mvp
- rule: Every PR runs format check, lint, type check, tests and security scans. Main is always releasable.
- why: Problems are found minutes after they are introduced, not weeks.

## 11.2 Build once, promote
- applies: deployment in (cloud, on-prem, regulated-env)
- rule: Build one immutable artifact (e.g. container image) per commit and promote that same artifact through all environments.
- why: What you tested is exactly what you release.

## 11.3 Infrastructure as Code
- applies: deployment=cloud
- rule: Define infrastructure as code (Terraform, Pulumi, Bicep or similar), reviewed and applied via the pipeline. No manual console changes.
- why: Environments become reproducible and changes auditable.

## 11.4 Environment parity
- applies: deployment in (cloud, on-prem, regulated-env)
- rule: Keep dev, staging and production as similar as possible (same containers, same backing service types).
- why: Differences between environments are where "but it worked in staging" comes from.

## 11.5 Feature flags
- applies: stage=production
- rule: Separate deploying from releasing with feature flags; remove flags once a feature is fully released.
- why: Enables trunk-based development and instant rollback of a feature without a deploy.

## 11.6 Safe rollouts and rollback
- applies: stage=production AND scale>=moderate
- rule: Roll out with blue-green or canary deployments and an automated, tested rollback.
- why: Limits the blast radius of a bad release.

## 11.7 DORA metrics
- applies: team>=small AND stage=production
- rule: Track deployment frequency, lead time for changes, change failure rate and time to restore service.
- why: Research-backed indicators of delivery performance; they show where the pipeline hurts.

## 11.8 Affected-only CI in monorepos
- applies: repo=monorepo
- rule: CI builds, tests and deploys only the projects affected by a change, following the dependency graph (a change in a shared library triggers its consumers), with build caching. Choose the tool by stack and size using ../guides/repo-strategy.md and record it in an ADR. Run the full pipeline on a schedule (e.g. nightly) as a safety net.
- why: Without it, every change runs everything and CI time grows with the repo; path filters alone miss dependency changes.

## 11.9 Isolated CI environments
- applies: stage>=mvp AND (data>=stored OR shared=yes)
- rule: Each pipeline run starts its own temporary dependencies (database in a container built from the migrations with the same version and extensions, queues, caches). CI never depends on a shared, long-lived environment that others can change.
- why: Isolation means one person's change cannot break everyone else's pipeline, and failures are reproducible.

## 11.10 Lightweight change management (change management as code)
- applies: shared=yes OR (stage=production AND team>=small) OR regulation has nis2
- rule: Run change management through the repository: the PR is the change request; labels set the change type (standard = pre-approved low risk, merge after green CI; normal = owner review; emergency = allowed, reviewed afterwards); the PR template has risk, impact and rollback sections; CODEOWNERS enforce approval on high-risk paths (migrations, infrastructure, auth); merged changes to shared or production systems are announced automatically to the affected teams.
- why: Keeps the intent of ITIL change management (risk assessment, approval, record, back-out plan) without meetings that slow a fast team down.

## 11.11 Pipelines as code, fast feedback
- applies: stage>=mvp
- rule: Pipelines are code in the repo, reviewed like code, reused through shared templates or reusable workflows. Order stages to fail fast (format and lint → unit tests → build → integration → E2E); keep the PR pipeline under ~10 minutes with dependency caching and parallel jobs; set a timeout on every job; cancel superseded runs on the same branch.
- why: Slow pipelines get bypassed; fail-fast ordering gives the cheapest signal first.

## 11.12 Pipeline security
- applies: stage>=mvp
- rule: Treat CI actions and plugins as third-party dependencies: pin them to a full commit SHA (with a version comment) and let Dependabot/Renovate update the pins. Default the CI token to read-only and grant extra permissions per job. Use OIDC federation to cloud providers instead of long-lived cloud secrets. Never run untrusted fork code with secrets (e.g. `pull_request_target` + checkout of the PR). Protect production deploys with environment approvals. CODEOWNERS cover the pipeline folder.
- why: The CI system holds the keys to production; a compromised or moved action tag can steal secrets from every repo that uses it.

## 11.13 Automated pipeline checks
- applies: stage>=mvp
- rule: Check the pipelines themselves automatically: a workflow linter (e.g. actionlint for GitHub Actions; the platform's CI lint for GitLab/Azure), a workflow security scanner (e.g. zizmor, poutine), and a repository posture check (OpenSSF Scorecard) on a schedule. Fix or explicitly accept every finding.
- why: Pipeline misconfigurations are invisible in normal reviews; tools catch unpinned actions, broad token permissions and injection risks.

## 11.14 Flaky tests are quarantined, not ignored
- applies: stage>=mvp
- rule: A test that fails intermittently is moved to a quarantine job within a day, gets an issue with an owner, and is fixed or deleted within an agreed time. Never "just re-run" as a habit.
- why: Flaky tests teach the team to ignore red builds, which hides real failures.

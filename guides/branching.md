# Branching strategy guide

Used for practice 01.4 and profile D11. The release model decides the branching model.

| Model | How it works | Choose when |
|---|---|---|
| **Trunk-based** | Short-lived branches (≤ 2 days) merged to `main`; `main` always releasable; feature flags hide unfinished work | `release=continuous`: web apps, SaaS, internal services. Default. |
| **GitHub flow** | Trunk-based with a PR per branch and deploy from `main` | Same as trunk-based; the most common lightweight form |
| **Release branches** | Trunk-based development, plus a `release/x.y` branch cut for each release; fixes cherry-picked | `release=scheduled` with a stabilisation period, or `multi-version` |
| **Gitflow** | `main` (releases, tagged), `develop` (integration), `feature/*` from develop, `release/*` to stabilise, `hotfix/*` from main | `release=scheduled` with formal approval (CAB, release windows), on-prem or packaged software, regulated releases |

## Notes
- Atlassian now describes Gitflow as a legacy workflow that has largely given way to trunk-based development: its long-lived branches cause drift and merge conflicts and fit poorly with CI/CD. It still suits projects with scheduled release cycles.
- Whatever the model: protected `main`, PR review, green CI before merge, tags for releases.
- Record the choice and the release model behind it in an ADR.

Source: Atlassian, Gitflow workflow (https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow).

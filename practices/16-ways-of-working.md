---
group: Ways of working (team and delivery)
id: "16"
version: 0.4
reviewed: 2026-11-17
---

# 16 · Ways of working

The process side that makes engineering practices stick.

## 16.1 Definition of Ready and Done
- applies: team>=small
- rule: Agree a Definition of Ready (clear acceptance criteria, dependencies known) and a Definition of Done (code reviewed, tests green, docs updated, deployed) and keep them in `docs/`.
- why: Shared expectations prevent half-finished work being called done.

## 16.2 Traceable work
- applies: tracker!=none
- rule: Every change links to an issue. Use the tracker's convention everywhere: branch `<type>/<KEY>-short-description`, commit message footer `Refs: <KEY>` (keep the Conventional Commits scope for the code area, 01.5), PR title starting with the key. Jira: issue keys (`ABC-123`, smart commits for transitions); GitHub: `Closes #12` in the PR to close on merge; Azure Boards: `AB#123`.
- why: Anyone can trace why a line of code exists, and the tracker updates itself from the code flow.

## 16.3 Small batches
- applies: always
- rule: Break work into slices that can be merged within one or two days.
- why: Small batches reduce risk, review effort and merge conflicts.

## 16.4 Documentation as code
- applies: always
- rule: Keep docs in the repo next to the code, in Markdown, reviewed in the same PRs.
- why: Docs in a separate wiki drift out of date.

## 16.5 Onboarding guide
- applies: team>=small
- rule: Maintain `docs/onboarding.md` so a new developer can set up, run and ship a small change in their first day.
- why: Onboarding time is a direct measure of how understandable the project is.

## 16.6 Design review before building
- applies: team>=small OR horizon in (splits, high-scale)
- rule: For significant features (new module or service, new external dependency, data model change, cross-team impact), write a short design doc or RFC in `docs/design/` and get it reviewed before coding; outcomes become ADRs.
- why: Aligns people on goals and dependencies early, when changing direction is cheap.

## 16.7 Tracker integration and automation
- applies: tracker!=none
- rule: Connect the repository to the tracker (Jira–GitHub/Bitbucket integration, GitHub Projects, Azure Boards app) so branches, PRs, builds and deploys appear on the issue. Automate transitions: PR opened → In review, merged → Done (or Ready to deploy), deployed → Released. Keep issue templates in the repo (bug, feature, tech debt) with acceptance criteria and Definition of Done (16.1). Labels match the change types in 11.10.
- why: Status stays accurate without manual updates; managers see progress from the tracker, engineers stay in the code.

## 16.8 Tool selection with explicit criteria
- applies: always
- rule: Choose tools and services with ../guides/tool-selection.md: compare total cost of ownership (licence, hosting, operations, people time), licence type and relicensing risk, lock-in and exit cost, open standards, support and compliance needs. Record choices that are costly to reverse in an ADR.
- why: "Free" tools can cost more in people time; paid tools can lock you in. Explicit criteria make the trade-off visible.
- alternatives: open-source / self-hosted vs paid / managed
- choose-when: T15 in ../guides/principle-tensions.md

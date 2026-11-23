# Practice proposals (inbox)

Not loaded by the skill. Ideas and lessons waiting to be reviewed; nothing here is in the catalogue yet. Process them in the monthly review (MAINTENANCE.md) or the next version. When the skill has its own repo, move these to issues with the "practice proposal" template.

## P1 · Closing keywords and Gitflow (source: author, real project, 2026-11-19)
- **Problem:** GitHub only honours closing keywords (`Closes #12`) when the pull request targets the repository's **default branch**. With Gitflow, pull requests go to `develop` while `main` is the default, so issues never close automatically and the PR shows no linked issues.
- **Verified:** GitHub docs: keywords in a PR description are interpreted only when the PR targets the default branch; for any other branch they are ignored and no links are created. https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
- **Detect:** default branch (`gh repo view --json defaultBranchRef -q .defaultBranchRef.name`), integration branch exists (`git ls-remote --heads origin develop`), where recent PRs go (`gh pr list --state all --limit 30 --json baseRefName -q '.[].baseRefName' | sort | uniq -c`).
- **Symptom:** merged PRs with zero `closingIssuesReferences`; PR bodies using `Refs #n`; PR template or CLAUDE.md saying "close by hand".
- **Decision rule:** if most PRs target a non-default branch and closing references are empty, recommend making the integration branch the default (`gh repo edit --default-branch develop`) and switching the PR template to `Closes #n`. It is a repo setting: ask first. Alternative if the default must stay `main`: close issues by hand or with a small workflow on PR merge.
- **Proposed home:** `guides/branching.md` (Gitflow notes), practices 16.2 / 16.7, detection D15.

## P2 · Waiting on CI without hanging (source: author, real project, 2026-11-19)
- **Problem:** an agent waiting on CI with `gh pr checks --watch` or `gh run watch` can hang indefinitely, or judge by an older or stuck run.
- **Rule:** judge only runs for the PR's head commit (`gh pr view <n> --json headRefOid`, then `gh run list --commit <sha>`); wait with a time limit (e.g. poll every 15 s for up to 5 minutes, or wrap a watch in `timeout 300`); at the limit, report what passed and what is pending, then ask. Some agent environments block foreground `sleep`; there, use the harness's background or monitor tool.
- **Proposed home:** group 15 (new practice "Bounded waits on CI and long commands") and the CLAUDE.md template workflow line.
- **To verify:** `gh run list --commit` and `closingIssuesReferences` field availability in the installed gh version.

## P3 · Negative and boundary test design (source: review, 2026-11-19)
- **Gap:** the catalogue says "tests with every change" (03.2) and lists test types, but never says *which cases* to test. Nothing requires invalid-input, boundary or failure-path cases.
- **Proposal:** new 03.12 "Positive, negative and boundary cases" (always), 03.13 "Failure-path tests for dependencies" (stage>=mvp AND (ai!=none OR interfaces has-any (internal-api, public-api) OR data>=stored)), and a "Test design techniques" section in `guides/testing-strategy.md` (equivalence partitioning, boundary value analysis, negative testing, error guessing, state transitions, decision tables).
- **Status:** adopted in v0.7.0 (03.12, 03.13, testing-strategy guide).

## P4 · Exploratory testing (source: author question, 2026-11-19)
- **Gap:** exploratory testing was only a row in the testing guide's table, with no practice or method.
- **Status:** adopted in v0.7.0 (03.14 exploratory sessions, 15.9 agent-run sessions in safe mode, Session-Based Test Management section in the testing guide).

## P5 · Encrypting secrets (source: author question, 2026-11-19)
- **Question:** should secrets be encrypted?
- **Answer adopted:** encryption moves the problem to the decryption key. Ranking: no long-lived secret (OIDC, workload identity) > secret manager or platform store > encrypted in the repo (SOPS, Sealed Secrets) > plaintext git-ignored for local only. A leaked secret is fixed only by rotation.
- **Status:** adopted in v0.8.0 (08.1 rewritten with the ranking, tension T22, new 08.12 credential rotation and leak response).

## P6 · Agent autonomy (source: author's local settings and M5 approval, 2026-11-19)
- **Question:** are there best practices for letting AI tools run on their own?
- **Findings on a real setup:** broad allows such as `Bash(uv *)` and `Bash(gh *)` permit arbitrary code and destructive commands; a "push to main" ask pattern misses forms like `HEAD:main` or `--all`; a milestone approval kept only in memory is not enforced; a public issue board is untrusted input.
- **Status:** adopted in v0.9.0 (15.10 graduated autonomy enforced outside the agent, 15.11 external text is data, ask rules in the settings template, autonomy line in the CLAUDE.md template, branch-protection recommendation in the summary).

## P7 · Upgrade asked all questions again (source: author's upgrade run, 2026-11-19)
- **Problem:** the profile was never saved in full, and "always asked" questions were not exempted in upgrade mode.
- **Status:** fixed in v0.10.0 (docs/standards/profile.md written on every run; upgrade asks only missing, changed or open dimensions and confirms once).

## P8 · Read planning docs (source: author, 2026-11-23)
- **Request:** a "Planning docs" step in detection for new and existing projects: read PLAN.md, SPEC.md, ROADMAP.md, README and `docs/*.md` to pre-fill profile answers (confirmed once, marked "detected from PLAN.md") and to detect milestones in new projects too.
- **Status:** adopted in v0.11.0, extended with: explicit statements only, quotes as evidence, conflicts between docs asked, decisions already made linked instead of new ADRs, non-goals respected.


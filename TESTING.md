# Testing and improving the project-init skill

Not loaded by the skill. Use these prompts in Claude Code after installing the skill in `~/.claude/skills/project-init/`.

## Test scenarios (fixture projects)
| ID | Scenario | Key profile values | Must happen |
|---|---|---|---|
| A | Empty repo, prototype, solo | new, prototype, data=none, stays-small | KISS over SOLID (T1); few rule files; no ADRs beyond 0001–0002; no Docker unless needed |
| B | New Python API, MVP, personal data, cloud | new, mvp, personal, internal-api, gdpr | GDPR rules (09.x incl. 09.10), RFC 9457 errors, migrations, containers, CI security |
| C | Existing Streamlit app using an LLM, solo | existing, mvp, web-ui, uses-llm | Gap analysis with CURRENT/PROPOSED/RESULT labels; 14.x incl. async (14.7) and evals; no code changes; generated block inside project-init markers; settings.json proposed |
| D | Monorepo with 3 apps and a shared library | repo=monorepo | 11.8 affected-only CI and a tool ADR; repo-strategy guide used |
| E | Several apps sharing one Postgres, small team | shared=yes, team=small | 06.12, 06.13, 11.9, 11.10 selected |
| F | On-prem product with scheduled releases | deployment=on-prem, release=scheduled | Q8 asked; Gitflow or release branches chosen (T4) with an ADR |
| G | Existing repo with an existing CLAUDE.md that conflicts | existing | Conflicts shown one at a time; default KEEP CURRENT; nothing overwritten without a yes |
| H | Multi-tenant AI platform with plugins | tenancy=multi, platform=yes, shared=yes, ai-act | 04.10, 04.14, 04.17, 06.13, 11.10, 09.8; tenancy and style ADRs |
| O | New project with a plan | new repo with PLAN.md (stage, data, hosting, milestones M0-M3, a non-goal) | Answers stated in PLAN.md are not asked, shown as `detected from PLAN.md` with a quote; milestones found and used for the upgrade path; a practice that contradicts the non-goal is dropped or flagged; nothing inferred beyond the text |
| N | Upgrade without re-asking | project set up with an earlier version | Answered questions are not asked again; only new, changed or open dimensions are asked; the full profile is shown once; docs/standards/profile.md is written or updated |
| M | Agent autonomy | any project, public repo with an issue tracker | 15.10 and 15.11 selected; settings.json proposes ask rules for destructive git/gh commands, merges and paid scripts; no broad `Bash(uv *)`-style allows; CLAUDE.md has an Autonomy line; summary recommends branch protection |
| L | Testing depth | any stage>=mvp project with a web UI and an LLM | 03.12 (negative and boundary cases), 03.13 (failure paths with fake clients) and 03.14 / 15.9 (exploratory sessions, safe mode) selected; testing rules mention negative cases and failure paths |
| K | Secret-file hook (when proposed) | sandbox unavailable | Blocked (exit 2): `cat .env`, `type .streamlit\secrets.toml`, `cp .env.local x`, `cat .env.production`, `cat .env.example.local`. Allowed (exit 0): `cat .env.example`, `ls .venv`, `python -c "import os; os.environ"`, `cat .envrc`, the test command |
| J | Streamlit app on Streamlit Community Cloud | deployment=paas | No IaC, container image, health endpoint or build-once-promote practices; data residency (09.6) still selected when data>=personal |
| I | Open-source library accepting contributions | openness=community | Group 17 incl. licence ADR, SECURITY.md, DCO/CLA; single-maintainer risk flagged |

## Prompt 1 · Dry run on a real project
```
Run /project-init on this repository in DRY-RUN mode.
Go through every step, but do not write or change any file.
At the end, show:
1. The profile you built and the evidence for each value.
2. Every file you would create or change, with its full proposed content.
3. For existing conventions: the conflict list with CURRENT / PROPOSED / RESULT.
4. Your own critique of the run: questions that were unclear, practices that seem wrong
   for this project, tensions resolved badly, anything confusing in the skill's instructions.
Then propose concrete changes to the skill files as diffs, without applying them.
```

## Prompt 2 · Evaluate with fixtures (uses the skill-creator skill)
```
Use the skill-creator skill to evaluate and improve ~/.claude/skills/project-init.
1. Create the fixture repositories for scenarios A to I from TESTING.md in a temp folder.
2. Run project-init on each in dry-run mode (the case folders in evals/ already cover several scenarios), answering the questions with the profile
   values listed for that scenario.
3. Grade each run against the "Must happen" column and these general checks:
   - only application-code-free changes (golden rule 1)
   - generated CLAUDE.md block under 120 lines and all rule files under 250 lines; non-negotiables not repeated in rule files
   - rule files contain no catalogue IDs, no ../guides links, no alternatives/choose-when text and no Backlog section
   - the questions stay within the tool limits (max 4 questions per round, max 4 options each)
   - every selected practice's applies-tag is really true for the profile
   - no tension applied on both sides
   - CURRENT / PROPOSED / RESULT labels used for every comparison
4. Report pass/fail per scenario and check, with the evidence.
5. Propose improvements to SKILL.md, the description, questions, practices or guides as diffs.
Do not modify the skill until I approve the diffs.
```

## Prompt 3 · Review the catalogue itself
```
Review the practices and guides in ~/.claude/skills/project-init without running it.
Find: contradictions between practices, applies-tags that select a practice where it
does not make sense (or miss where it should apply), practices with no clear rule,
outdated tools, versions or standards, and important gaps for a senior engineering baseline.
Verify anything time-sensitive (standards, tool status, regulations) with web search and cite sources.
Output a table: practice ID, issue, evidence, proposed fix. Do not edit files.
```

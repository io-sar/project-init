# Roadmap to v1.0

Not loaded by the skill. Status of the project-init skill and what is left before v1.0.
Last updated: 2026-11-23 (v0.11.0).

**v1.0 means:** proven on real projects, stable structure (changes to the profile, tag syntax or file layout after v1.0 need v2.0), and shareable.

## Status
| # | Item | Status | Notes |
|---|---|---|---|
| 1 | Writing run on a real project, reviewed like a PR | ✅ Done | AI Project Troubleshooter (Streamlit, existing CLAUDE.md), worktree `test/skill-trial`, v0.4.1. All runtime checks passed: CLAUDE.md only appended, 3 always-loaded rule files, path-scoped rules on matching files, `.env` read blocked, formatter hook on Windows, secret-file Bash hook (8/8 cases). Committed on the trial branch. |
| 2 | Upgrade mode tested | 🔶 In progress | First upgrade run (v0.9) re-asked all questions; fixed in v0.10 (saved profile). Re-test with v0.10. | Install v0.6 in Claude Code, run upgrade mode in the same worktree; expect only small diffs (mainly removing rules that repeat the project's own CLAUDE.md). Then PR `test/skill-trial` into `develop`. |
| 3 | Two more real projects | ⬜ | One brand-new project (new mode) and one different existing repo (other stack or team project). Dry run first, then a writing run. |
| 4 | Automated evals with skill-creator | ⬜ | 6 cases in `evals/` plus scenarios in TESTING.md (A to K). Run with and without the skill; all must pass. Add cases for upgrade mode and an existing CLAUDE.md with markers. |
| 5 | Proofreading by the author | ⬜ | Read the handbook PDF; send remarks as `ID: remark` lines. Goes into the next version. |
| 6 | Freeze the structure | ⬜ | Declare profile dimensions, tag syntax, practice fields and file layout stable. |
| 7 | Tune the trigger description | ⬜ | skill-creator description optimisation; needs Claude Code CLI on the author's machine. |
| 8 | Shareable repo | 🔶 In progress | Public GitHub repo with MIT licence, README and .gitignore prepared in v0.10.1; each PC clones into ~/.claude/skills/project-init and updates with git pull. | Own GitHub repo with README, a deliberate licence (17.1), CHANGELOG; `~/.claude/skills/project-init` as a clone of it. |
| 9 | First monthly review | ⬜ Scheduled | Runs 1 December 2026, 09:59 Athens time, suggestions only. Attach the repo (item 8) so it can check files too. |

## Inbox
Open practice proposals are in `PROPOSALS.md` (open: P1 closing keywords and Gitflow, P2 bounded CI waits; adopted: P3 negative and boundary tests and P4 exploratory testing in v0.7, P5 secrets ranking and rotation in v0.8, P6 agent autonomy in v0.9, P7 upgrade re-asking fixed in v0.10, P8 planning docs in v0.11).

## Suggested path
- v0.7: upgrade-mode findings (item 2) and the author's proofreading (item 5).
- v0.8: evals green (item 4), second and third real projects (item 3).
- v0.9: frozen structure, tuned description, public repo (items 6 to 8).
- v1.0: after the December review is triaged and the third project runs cleanly.

## Out of scope for v1.0
Language extensions (Python, TypeScript...) come as v1.1+ add-ons to the language-agnostic core.

## How to continue in a new session
Attach `project-init.zip` (or the repo), say "continue the project-init skill from ROADMAP.md", and share any new findings.

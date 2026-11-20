---
name: project-init
description: Set up senior-level engineering standards for a software project, new or existing. Detects the stack and current conventions, asks a few questions about stage, data, growth and regulation, then writes a short CLAUDE.md, topic rules in .claude/rules/, on-demand standards docs, ADRs, a proposed .claude/settings.json and (for existing projects) a milestone-based adoption plan, chosen from a curated catalogue of 175+ best practices (architecture, APIs, data, distributed systems, multi-tenancy, security, GDPR and EU regulation, testing, CI/CD, AI/LLM, open source, Claude Code). Use this whenever the user runs /project-init, starts or bootstraps a new project or repo, asks to set up CLAUDE.md or project rules, wants best practices or engineering standards applied to a codebase, or asks to audit an existing repo against best practices, even if they don't name the skill. Not for answering a single best-practice question in conversation.
---

# Project init · v0.10.1

Turn a catalogue of senior engineering practices into standards that fit THIS project: only what applies, with trade-offs resolved and recorded, written where Claude Code will follow them, and loaded only when they are needed.

## Ground rules, and why
1. **Write documentation and configuration only; never change application code.** Standards are adopted gradually through reviewed changes; a setup tool that rewrites code produces huge, unreviewable diffs and breaks trust.
2. **Always ask about data sensitivity and regulation; never infer them.** A wrong guess either misses legal obligations or buries a simple project in compliance work.
3. **Show before you write, and get a yes.** Existing files may hold deliberate decisions; the user decides what changes.
4. **Label every comparison CURRENT, PROPOSED and RESULT** (never "old/new"). Fixed labels remove any doubt about which side is which.
5. **Keep what loads every session small.** Everything in CLAUDE.md and in rule files without `paths:` is loaded at the start of every session; the more there is, the less reliably each rule is followed. Put detail on demand and scope rules to folders.

## Modes
- **Normal**: all steps; writes files after confirmation.
- **Dry run** (the user says "dry run" or asks to preview): all steps, but write nothing anywhere, including this skill's `feedback/` folder, and skip the write confirmation. Show CLAUDE.md, rule files, settings.json, ADRs and the adoption plan in full; show `docs/standards/*` as headings plus one sample section unless the user asks for all.
- **Upgrade**: if CLAUDE.md contains `project-init:start`, this is an upgrade. Load the saved profile from `docs/standards/profile.md`; for projects set up before v0.10, rebuild it from the CLAUDE.md profile line, the ADRs and `docs/standards/`, and say which values were rebuilt. Run detection (Step 1) to spot changes. In Step 2 ask **only** about dimensions that are missing from the saved profile (e.g. added in a newer skill version), that detection shows have changed, or that were left open; never repeat answered questions, even the ones marked "always asked". Then show the full profile once (Step 3) with a single question: "Anything changed?". Steps 4 to 7 then propose only the differences, as CURRENT / PROPOSED / RESULT. Use it when the project reaches a new stage or milestone, or after installing a new skill version.

## Files in this skill
| File | Read it in |
|---|---|
| `profile.md` | all steps: dimensions, tag syntax, practice fields |
| `detection.md` | Step 1 |
| `questions.md` | Steps 2 and 3 (in upgrade mode, only for missing, changed or open dimensions) |
| `practices/TAGS.md`, then the selected practices in `practices/NN-*.md` | Steps 4 and 5 (the catalogue) |
| `guides/principle-tensions.md` | Step 4, resolving `alternatives:` |
| `guides/architecture-styles.md` | Step 4 and ADR 0002 (quality attributes, style, tenancy, gateway) |
| `guides/branching.md`, `repo-strategy.md`, `database-selection.md`, `testing-strategy.md`, `tool-selection.md`, `llm-evaluation.md` | Step 4 when a selected practice points to them, and Step 6 for ADRs and standards docs |
| `templates/*.tmpl` | Step 6 |

`README.md`, `LICENSE`, `TESTING.md`, `MAINTENANCE.md`, `ROADMAP.md`, `PROPOSALS.md`, `CHANGELOG.md`, `tools/` and `feedback/` are for the repository and for maintaining the skill; you do not need them during a run.

## Step 1 · Detect
Follow `detection.md`. Record every detected value with its evidence (file path), because the user confirms the profile from that evidence in Step 3. Never open `.env` or key files. In an existing project, also collect existing conventions with file and line (Step 5 compares against them), and note any existing CLAUDE.md, AGENTS.md, `.claude/rules/` and `.claude/settings.json`.

## Step 2 · Ask
Follow `questions.md`: Round 1 (4 questions, always), Round 2 (up to 4, skipping what was detected), and the single follow-up only when its condition is met. Stay within the question tool's limits so no option is silently dropped.

## Step 3 · Confirm
Show the confirmation screen from `questions.md`, including how many practices the profile selects. Continue only after the user confirms or corrects it; everything downstream depends on this profile.

## Step 4 · Select
1. Read `practices/TAGS.md` (one line per practice: ID, title, applies tag, flags) and evaluate every tag against the profile. Then read only the selected practices in the group files; skip groups with no selected practice. Practices with `opt-in: yes` are only suggested in the summary.
2. Resolve every practice with `alternatives:` using `guides/principle-tensions.md` in its stated order (auto tensions resolved from the profile; advisory tensions get the default and are listed for the user). A practice with `alternatives:` but no row in the tensions table is advisory: write the practice's own rule and list the alternative in the summary. Write only the chosen side; both sides would give contradictory instructions.
3. Keep a list of practices skipped only because of `stage`: the upgrade path.

## Step 5 · Gap analysis (existing projects only)
Give each selected practice one status, comparing with the conventions from Step 1:
- **enforced**: a tool, CI step or test checks it
- **documented only**: written somewhere, nothing checks it
- **missing**: not found
- **conflicting**: the project does it differently

Present conflicts so each decision is easy:
- **Security (08) and privacy (09) conflicts: one at a time**, marked HIGH PRIORITY, each needing an explicit choice, because silently keeping a weak rule there can cause real harm.
- **All other conflicts: one table**, with KEEP CURRENT pre-selected; the user changes only the rows they want.

```
Conflict 2 of 3 (HIGH PRIORITY) · Security · Secrets management

| Label                                          | Rule text                          | Where it comes from |
|------------------------------------------------|------------------------------------|---------------------|
| CURRENT  (in your project today)               | "Store API keys in config.yaml"     | README.md, line 40  |
| PROPOSED (from the catalogue, not yet applied) | "Secrets only from a secret manager or env; never in committed files" | catalogue 08.1 |

Impact if replaced: <one line>
Recommendation: REPLACE WITH PROPOSED, because <one line>
Your choice: [K] keep CURRENT · [R] replace with PROPOSED · [M] merge
```
On [M], add a row `RESULT (what will be written)` and ask for confirmation. After all conflicts, show one summary table: ID · CURRENT · RESULT · decision. The default is KEEP CURRENT: an existing convention is often a deliberate choice, and consistency inside a codebase matters more than a marginally better rule.
- **KEEP CURRENT** writes nothing new: the existing rule stays where it is, and the decision is recorded in `docs/standards/`. Never repeat a rule that already exists outside the generated block.
- **REPLACE or MERGE of a line outside the project-init markers** (e.g. in a hand-written CLAUDE.md) is the only edit allowed outside the markers: show exactly that line as CURRENT / RESULT and change it only after an explicit yes.

Map statuses for Step 6:
- enforced, or a REPLACE/MERGE decision → **Enforced** (rule files); KEEP CURRENT → nothing new written
- documented only, or missing but cheap to apply to new code → **Adopting** (rule files: new code follows it, existing code keeps its local pattern)
- missing and needing real work on existing code → **planned**, assigned to a milestone in the adoption plan (never in rule files)

In a new project every selected rule is **Enforced**.

## Step 6 · Write
First list every file that will be created or changed and get a yes (skip this in dry run). For any file that already exists, show CURRENT vs RESULT before writing it. Template comments are instructions for you: strip them from written files, except the project-init markers and the one-line "Generated by" note, so no catalogue IDs or skill wording end up in the project.

**Three loading tiers.** Decide for each selected practice where it lives:
1. **Always loaded** (CLAUDE.md and rule files without `paths:`): the non-negotiables and rules that apply to any file.
2. **Loaded by path** (rule files with `paths:`): add `paths:` for groups 03, 05, 06, 13 and 14 whenever their code can be located (tests, API, models/migrations, UI, AI code). With a flat layout, scope to the specific files that clearly hold that code (e.g. `app.py`, `db.py`); if none can be identified, load the rule always and count it against the budget.
3. **On demand** (`docs/standards/<group>.md`): the full rule, reason and resolved trade-off for every selected practice of the group; CLAUDE.md says when to read each file.

**Budget.** The generated CLAUDE.md block stays under 120 lines and the whole CLAUDE.md under 200 lines (warn the user above that); all always-loaded rule files together stay under 250 lines. Write one short line per rule; add a reason only where it is not obvious. If the budget is exceeded, keep in rule files the security, privacy and testing rules and the ones that change Claude's day-to-day coding; move the rest to `docs/standards/` only.

**Rule text hygiene.** Rule files and CLAUDE.md must stand on their own in the project: no catalogue IDs, no links to this skill's guides, no `alternatives` or `choose-when` text, no references to practices that were not selected. Write each resolved trade-off as one plain sentence.

**No repeats.** Before writing a rule, check the project's existing instructions (CLAUDE.md outside the markers, AGENTS.md, existing rule files, CONTRIBUTING.md) for a rule with the same intent. If one exists, do not write it again; if the catalogue rule adds something, write only the addition, phrased as extending the existing rule. Judge by meaning, not by heading names: a "Code design" section can cover structure, a "Rules that must not break" section can cover secrets.

Files:
1. `CLAUDE.md` from `templates/CLAUDE.md.tmpl`. New file: the full block. Existing file without markers: append the block at the end, headed `## Project standards`, and leave out every section whose content the file already covers, judged by meaning rather than heading (title, description, commands, structure or code layout, workflow); preserve everything else exactly, including notes and roadmaps. Existing file with markers: update only inside them. If AGENTS.md exists, import it (`@AGENTS.md`) rather than duplicating it. Non-negotiables (max 8) live only here.
2. `.claude/rules/<group>.md` from `templates/rule-file.md.tmpl`, named after the group file without its number (e.g. `security.md`), Enforced and Adopting rules only.
3. `docs/standards/<group>.md` from `templates/standard-doc.md.tmpl`, one per group with selected practices.
4. `.claude/settings.json` proposal from `templates/settings.json.tmpl` for practices with `kind: setup` (15.3, 15.4) and the autonomy model (15.10): deny reading secret files and force pushes (best effort), ask for destructive git and gh commands, merges, releases, repository settings and paid scripts, keep allow rules narrow, allow each routine command both bare and with arguments (`Bash(cmd)` and `Bash(cmd *)`), and a formatter hook only if the repository is already formatted (otherwise the first edit would reformat whole files; list "format the codebase" as a planned item instead). Deny the real secret files by name but keep `.env.example` readable, since it documents the variables without values. If Claude Code's sandbox is not available (e.g. native Windows), also propose the optional PreToolUse hook that blocks shell commands mentioning secret files; say that it matches text (so a command that only mentions the name is blocked too), can be bypassed with globs or split strings, and fails open if its interpreter breaks. Test it with sample commands before reporting, without touching real secret files. Merge with any existing settings as CURRENT / RESULT; never remove existing entries without asking.
5. `docs/adr/` from `templates/adr.md.tmpl`: if the folder exists, continue its numbering and format; otherwise start with 0001 (record architecture decisions). Then: quality attributes and architecture style (new projects), one per resolved tension that matters here, one per REPLACE decision (existing projects). If a decision is already documented elsewhere in the project (CLAUDE.md, a spec, an existing ADR, the README), do not write a new ADR: link to the existing record in `docs/standards/` and propose an ADR only if that record lacks the reasoning.
6. `docs/standards/profile.md` from `templates/profile.md.tmpl`: every dimension with its value, source (answered, detected with evidence, or default) and date; open questions; confirmed milestones. Upgrade mode reads it, so answered questions are never asked twice.
7. `docs/standards-adoption.md` from `templates/standards-adoption.md.tmpl` (existing projects): planned items grouped by milestone, security and privacy first, plus the upgrade path. Use only current or future milestones the user confirmed in Step 3 (never a milestone that is already done); if the project has none, propose M1/M2/next stage.

## Step 7 · Summarise
Report, in this order:
1. Files written (or, in dry run, files that would be written) and the line counts of CLAUDE.md and the rule files against the budget.
2. Practices selected per group, and which tier each group went to.
3. Existing projects: enforced / adopting / planned counts and the items of the first milestone.
4. Opt-in suggestions, advisory tensions left at their default, regulations marked "not sure", and the upgrade path. If the repository is hosted on GitHub or a similar platform, recommend server-side branch protection for the main and integration branches (a repository setting: the user decides). Note that permission deny rules are best effort (e.g. `cat .env` through the shell is not a Read call) and recommend Claude Code's sandbox for stronger isolation.
5. Open questions (e.g. regulation "not sure") and commands left as TODO.
6. Overrides, for improving the skill: one line per user override (rejected practice, KEEP CURRENT, overridden tension) as `date · ID · chosen instead · reason`, with no project names, paths or personal data. Show these lines; append them to `feedback/overrides.md` in this skill's folder only if the user says yes, the folder is writable and this is not a dry run.

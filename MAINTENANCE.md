# Maintaining the project-init skill

Not loaded by the skill. How the catalogue stays current.

## 1. Version everything
- The skill lives in its own git repository; `~/.claude/skills/project-init` is a clone or symlink of it.
- Semantic versioning in `SKILL.md` (`# Project init · vX.Y`) and `CHANGELOG.md`:
  - PATCH: wording fixes, sources, typos
  - MINOR: new practices, guides or questions
  - MAJOR: changed profile dimensions, tag syntax or output structure
- Every generated CLAUDE.md records the skill version, so projects created with an old version can be found and upgraded (re-run `/project-init`, upgrade mode).

## 2. Inbox for new ideas
- Any idea, link or lesson learned goes into an issue in the skill repo using the "practice proposal" template: what, why, source, which group, proposed applies-tag.
- Nothing goes straight into the catalogue; proposals are processed in the monthly review.

## 3. Monthly review (scheduled)
A scheduled task runs once a month and opens a PR or report with:

- **Staleness**: groups whose `reviewed:` date is older than 12 months.
- **Radar**: new editions or changes of the standards and tools the catalogue names (e.g. OWASP Top 10 lists, WCAG, EU regulations and their dates, RFCs, CI and container tooling, monorepo tools, LLM eval tools), licence changes of named tools, deprecated actions or services.
- **Inbox**: open practice proposals, triaged.
- **Usage feedback**: overrides recorded in `feedback/` (see 4), grouped by practice.
Each finding comes with a source and a proposed diff; a human approves before merge.

Suggested review prompt:
```
Run the monthly review of the project-init skill as described in MAINTENANCE.md.
Use web search for every time-sensitive item and cite sources.
Output: findings table (item, change found, source, proposed diff, priority).
Do not edit the skill; prepare the diffs for my approval.
```

## 4. Learn from real runs
- At the end of each run the skill appends one line per user override to `feedback/overrides.md` in the SKILL folder (date, practice or tension ID, what was chosen instead, reason given). No project names, no personal data.
- Practices that are overridden often are wrong, badly tagged or badly worded: fix them first.

## 5. Tool rings (for guides that name tools)
Mark tools with a ring, inspired by technology radars: **adopt** (default recommendation), **trial** (use where it fits, still proving itself), **assess** (watch), **hold** (do not start new work with it). The monthly review moves tools between rings.

## 6. Validation
Run `python3 tools/validate_catalogue.py` after every change: it checks required fields, unique IDs, every applies-tag against the profile dimensions, and tension references, and rebuilds practices/INDEX.md.

## 7. Proofreading
Run `python3 tools/build_handbook.py <output-folder>` from the skill root to build one readable handbook (Markdown, HTML and, if pandoc and Chrome are installed, PDF) with every practice and guide in reading order and a review checklist.

## 8. Regression check before every release of the skill
Run Prompt 2 from TESTING.md (fixture scenarios). A new version ships only if all scenarios still pass.

## 9. Release message
The repository is the source of truth; each PC has a clone at `~/.claude/skills/project-init`. End every release message with the update line:

```powershell
git -C "$HOME\.claude\skills\project-init" pull
```

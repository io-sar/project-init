# project-init

A [Claude Code](https://code.claude.com) skill that sets up senior-level engineering standards for a software project, new or existing, and keeps them up to date.

It looks at the repository, asks a few short questions (stage, data, growth, regulation, hosting), and picks the practices that fit **this** project from a catalogue of 180+ language-agnostic best practices. It then writes them where Claude Code follows them, loading each rule only when it is needed.

**Status:** pre-1.0 (see [ROADMAP.md](ROADMAP.md)). Tested on a real existing project; feedback welcome.

## What it does
- **Detects** the stack, hosting, tests, CI, existing conventions and milestones from the repository.
- **Asks** only what it cannot detect: one or two short rounds of multiple-choice questions.
- **Selects** practices by profile: a solo prototype gets a light setup, while a multi-tenant production platform with personal data gets architecture, security, GDPR and operations rules. Trade-offs such as SOLID vs YAGNI, Gitflow vs trunk-based, or monolith vs microservices are resolved from the profile and recorded as decisions (ADRs).
- **Respects existing projects:** it never changes application code, keeps your CLAUDE.md content, shows every conflict as CURRENT / PROPOSED / RESULT, and plans the rest by milestone instead of refactoring.
- **Writes, after your approval:**
  - a short generated block in `CLAUDE.md`
  - `.claude/rules/*.md` (a few always loaded, the rest only for matching folders)
  - `docs/standards/*.md` (full reasons, read on demand) and `docs/standards/profile.md`
  - a proposed `.claude/settings.json` (blocks secret files and force pushes, asks before destructive or paid actions)
  - ADRs in `docs/adr/`, and for existing projects `docs/standards-adoption.md`

The catalogue covers foundations, code quality, testing (including negative, boundary, failure-path and exploratory testing), architecture, APIs, data, distributed systems, security, EU privacy and regulation (GDPR, NIS2, AI Act, CRA, EAA), operations, CI/CD, performance and cost, frontend, AI/LLM features, working with Claude Code (including agent autonomy), ways of working, and open-source maintenance.

## Install
Clone the repository into your personal Claude Code skills folder, so it is available in every project.

**Windows (PowerShell)**
```powershell
git clone https://github.com/YOUR-GITHUB-USERNAME/project-init "$HOME\.claude\skills\project-init"
```

**macOS / Linux**
```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/project-init ~/.claude/skills/project-init
```

Restart Claude Code, type `/` and check that **project-init** appears.

## Update
```powershell
git -C "$HOME\.claude\skills\project-init" pull
```
Then restart Claude Code, and run upgrade mode in your projects (see below).

## Use
In Claude Code, inside your project:

| Goal | Prompt |
|---|---|
| Preview without writing anything | `Run /project-init in DRY-RUN mode.` |
| Set up standards | `/project-init` |
| Update an existing setup after a new version or a new milestone | `Run /project-init in upgrade mode. Propose only the differences. Don't write anything until I approve.` |

Tip: try it first in a separate git worktree or branch, and review the result like a pull request.

## Repository layout
| Path | What it is |
|---|---|
| `SKILL.md` | The workflow Claude follows |
| `profile.md`, `questions.md`, `detection.md` | Project profile, questions and detection rules |
| `practices/` | The catalogue: one file per group, plus a generated index (`TAGS.md`, `INDEX.md`) |
| `guides/` | Decision guides: trade-offs, architecture styles, testing, databases, repos, branching, tools, LLM evaluation |
| `templates/` | Templates for the files the skill writes |
| `evals/`, `TESTING.md` | Test cases and prompts for evaluating the skill |
| `tools/` | `validate_catalogue.py` (checks every rule) and `build_handbook.py` (one readable PDF/HTML handbook) |
| `ROADMAP.md`, `PROPOSALS.md`, `CHANGELOG.md`, `MAINTENANCE.md` | Status, ideas inbox, history and how the catalogue stays current |

## Contributing
Issues with proposals, corrections or real-run findings are welcome. For a new or changed practice, include the rule, why it matters, when it should apply, and a source. Run `python3 tools/validate_catalogue.py` before opening a pull request.

## Disclaimer
The privacy and regulation practices are engineering guidance, not legal advice.

## Licence
[MIT](LICENSE)

# Detection map (language-agnostic)

Detection only SUGGESTS values. Every detected value is shown on the profile confirmation screen with its evidence, and the user can correct it.
Read file names, manifests and config, plus the planning docs below. Never read `.env` or secret files.

## Planning docs (both new and existing projects, run first)
Read the project's own planning documents, if present: `PLAN.md`, `SPEC.md`, `ROADMAP.md`, `README*`, and the Markdown files directly in `docs/` (`docs/*.md`; similar names such as `DESIGN.md`, `ARCHITECTURE.md` or `BRIEF.md` count too). Skip files this skill generated (`docs/standards/`, `docs/standards-adoption.md`).

Use them to:
1. **Pre-fill profile answers.** Take a value only from an explicit statement, never from a guess, and record the source with a short quote, e.g. `detected from PLAN.md: "public demo for recruiters, no accounts"`. Typical statements: stage (prototype, MVP, production, "live"), users and interfaces (web app, API, CLI), data ("stores no personal data", "user accounts", "health records"), hosting ("Streamlit Community Cloud", "AWS", "installed at customers"), growth and team, regulation named in the text (GDPR, AI Act...), open-source intent, multi-tenancy or a plugin platform.
2. **Detect milestones,** in new projects too: headings or lists such as `M0`…`Mn`, "Milestone", "Phase", "Sprint", "Release v…", with any status words or checkboxes (done, current, next). Record each as done, current or future.
3. **Find decisions already made** (architecture, stack, database, hosting, branching, licence, testing approach). Link to them instead of writing a new ADR (Step 6.5).
4. **Note non-goals and constraints** ("no accounts", "no native packages", "no paid services"), so no practice proposes what the plan excludes; list such clashes in the summary.

Rules:
- If two documents disagree, do not pick one: show both quotes and ask.
- Pre-filled answers are not asked again in Step 2; they are confirmed once on the confirmation screen, with their source.
- Data sensitivity and regulation may be pre-filled only from an explicit statement in these documents, and stay visible for confirmation (ground rule 2).

## D0 · mode
| Signal | Suggests |
|---|---|
| No source files, or only scaffolding (README, LICENSE, .gitignore) | `new` |
| Source files present, or more than ~10 commits in git history | `existing` |

## D10 · stack (language and framework)
| File | Language / ecosystem |
|---|---|
| `pyproject.toml`, `requirements*.txt`, `setup.py`, `Pipfile` | Python |
| `package.json` (+ `tsconfig.json` → TypeScript) | JavaScript / TypeScript |
| `go.mod` | Go |
| `pom.xml`, `build.gradle*` | Java / Kotlin |
| `*.csproj`, `*.sln` | .NET |
| `Cargo.toml` | Rust |
| `Gemfile` | Ruby |
| `composer.json` | PHP |

Framework = the main web/UI/CLI dependency found in the manifest (e.g. FastAPI, Django, Flask, Streamlit, Express, NestJS, Next.js, React, Spring Boot, ASP.NET). Report it by name; do not judge it.

## D4 · interfaces (multi-select)
| Signal | Suggests |
|---|---|
| UI framework dependency (React, Vue, Angular, Streamlit, Django templates...) or `templates/`, `static/` | `web-ui` |
| Web/API framework dependency, `openapi.*`, `*.proto`, route/controller folders | `internal-api` (ask if public) |
| Console entry points in manifest, `bin/`, `cli/` folder | `cli` |
| Message broker clients (Kafka, RabbitMQ, SQS, Pub/Sub, NATS), `asyncapi.*` | `events` |

## D5 · data
| Signal | Suggests |
|---|---|
| DB drivers / ORMs (SQLAlchemy, psycopg, Prisma, TypeORM, Hibernate, Mongo, Redis), `migrations/`, `alembic/`, DB services in `docker-compose*` | at least `stored` |
| Anything else | nothing: personal / special-category is ALWAYS asked, never inferred |

## D3 · architecture
| Signal | Suggests |
|---|---|
| One deployable unit | `monolith` (recommend modular monolith, 04.1) |
| Several deployable apps (multiple Dockerfiles / services in compose / k8s manifests / `services/*`) | `services` |

## D7 · deployment
| Signal | Suggests |
|---|---|
| `Dockerfile`, `docker-compose*` only | `local` or `cloud` (ask) |
| `Procfile`, `render.yaml`, `vercel.json`, `netlify.toml`, `app.yaml` (App Engine), `railway.json`, a Streamlit app with no Dockerfile or IaC, or a hosting note in the README/spec naming such a platform | `paas` (confirm) |
| `*.tf`, `*.bicep`, Pulumi, CDK, `serverless.*`, `k8s/`, `helm/` | `cloud` |
| Installer configs (e.g. MSI/pkg builders), Helm charts or compose files meant for customers, `release/*` branches | `on-prem` (confirm) |
| Nothing | not detected: ask Q10 |

## D8 · ai
| Signal | Suggests |
|---|---|
| LLM SDKs (anthropic, openai, google-genai, mistral), frameworks (LangChain, LlamaIndex, Semantic Kernel) | `uses-llm` |
| Agent / tool-calling frameworks, MCP servers or clients | `agentic` (confirm) |

## D2 · team
| Signal | Suggests |
|---|---|
| Distinct human commit authors in the last 90 days (exclude bots such as dependabot, renovate, github-actions): 1 | `solo` |
| 2 or more | `small` |
| CODEOWNERS lists 2 or more teams | `multi-team` (otherwise confirm with the user before choosing multi-team) |
| No git history | ask |

## D11 · release
| Signal | Suggests |
|---|---|
| `develop` branch and/or `release/*` branches | `scheduled` (Gitflow-style) |
| Several maintained `release/x.y` or `support/*` branches | `multi-version` |
| Only `main` + short-lived branches, frequent tags or deploys | `continuous` |

## D13 · repo
| Signal | Suggests |
|---|---|
| `.gitmodules` | `submodules` |
| `nx.json`, `turbo.json`, `moon.yml` / `.moon/`, `pants.toml`, `MODULE.bazel` / `WORKSPACE`, `pnpm-workspace.yaml`, `lerna.json`, `rush.json`, `go.work`, Cargo `[workspace]`, Gradle multi-project, several app manifests under `apps/` or `packages/` | `monorepo` (record the tool) |
| None of the above | `single` |

## D15 · tracker
| Signal | Suggests |
|---|---|
| Commit messages or branch names with keys like `ABC-123`, Jira smart commits, an Atlassian MCP server configured | `jira` |
| `Closes #12` / `Fixes #12` in commits, `.github/ISSUE_TEMPLATE/` | `github` |
| `AB#123` in commits, `azure-pipelines.yml` | `azure-boards` |
| `.gitlab/issue_templates/` | `gitlab` |
| None | ask if team>=small, otherwise `none` |

## D16 · openness
| Signal | Suggests |
|---|---|
| `LICENSE` with an OSI-approved licence (MIT, Apache-2.0, BSD, MPL, GPL, AGPL, LGPL...) | at least `published` (confirm in Q7b) |
| Plus `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, issue/PR templates, or a public package registry config (e.g. `publishConfig`, PyPI classifiers) | `community` (confirm) |
| Proprietary licence, or no licence file | `closed`, counted as detected: skip Q7b (a missing licence means "all rights reserved", not open source) |

## Existing conventions (mode = existing)
Collect, with file path, for the gap analysis:

- AI instructions: `CLAUDE.md`, `CLAUDE.local.md`, `.claude/rules/`, `.claude/settings.json`, `AGENTS.md`, `.cursor/rules/`, `.github/copilot-instructions.md`
- Tooling: formatter, linter and type-checker configs; `.pre-commit-config.yaml`; `.editorconfig`
- CI: `.github/workflows/`, `.gitlab-ci.yml`, `azure-pipelines.yml`, `Jenkinsfile`, `bitbucket-pipelines.yml` (and which checks they run)
- Docs: `CONTRIBUTING.md`, `SECURITY.md`, `docs/adr/`, `CHANGELOG.md`, `LICENSE`
- Commands: scripts in the manifest, `Makefile`, `Taskfile.yml`, `justfile`
- Milestones: roadmap headings (M0…Mn, "Roadmap", "Milestones") in CLAUDE.md, README or ROADMAP.md, and tracker milestones; record each with whether it looks done, current or future, and confirm in Step 3
- Formatter state: whether a formatter is configured, and whether the codebase is already formatted (ask the user, or run a read-only check such as `ruff format --check` / `prettier --check` with permission)

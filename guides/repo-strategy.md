# Repository strategy guide

Used for profile D13 and the repo ADR. Choose by how code changes together, not by fashion.

## Monorepo vs polyrepo vs submodules
| Option | Choose when | Watch out for |
|---|---|---|
| **Single repo** (one app) | One deployable, one team | Nothing special |
| **Monorepo** | Several apps/libs that share code and change together; one team or a few closely working ones | Needs tooling to avoid running everything on every change; clear ownership (CODEOWNERS) |
| **Polyrepo** | Independent teams, independent release cycles, little shared code | Shared code must become versioned packages; cross-repo changes need coordination |
| **Git submodules** | Embedding another repo pinned at an exact commit that rarely changes: vendored and patched third-party code, shared firmware/SDK, shared specs/protos, docs theme | Clones need `--recursive`; easy to forget updates (detached HEAD); CI must fetch submodules; a cross-repo change needs two PRs and a pointer bump |

Prefer these over submodules when possible:

- **Versioned package** in a registry (npm, PyPI, Maven, NuGet) for shared libraries: cleanest.
- **git subtree**: copies code in; nothing extra to clone.
- **Monorepo**: if the code genuinely changes together.

## Monorepo tooling: run only what changed
Tools work out which projects a change affects (dependency graph + git diff), cache outputs, and run independent tasks in parallel.

| Tier | Tools | Fits | Limitation |
|---|---|---|---|
| Lightweight | CI path filters (GitHub Actions `paths:`, GitLab `rules: changes:`, Azure Pipelines path triggers) | 2 to 5 independent apps, little shared code | Does not follow dependencies: a change in a shared lib does not trigger its consumers unless listed by hand |
| Task runner + cache | **Turborepo** (simple, fast), **Nx** (feature-rich, generators, enterprise), **Moon** (polyglot, reproducible) | JS/TS-first monorepos; Nx and Moon also handle other languages | Remote caching may use a paid service |
| Full build system | **Bazel**, **Buck2**, **Pants** (strong for Python/JVM) | Large polyglot repos needing exact, hermetic builds | Steep learning curve; BUILD files everywhere |
| Language-native | Gradle (JVM), Cargo workspaces (Rust), Go workspaces, pnpm/npm/yarn workspaces | Single-language monorepos | Affected detection is limited or manual |

Rule for the skill: recommend by stack and size; do not propose a full build system to a small team when a task runner solves the bottleneck. Record the choice in an ADR (practice 11.8).

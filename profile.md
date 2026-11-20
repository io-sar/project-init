# Project profile: the decision dimensions

Every practice in the catalogue is tagged with `applies:` conditions built from these dimensions.
At init, the skill fills this profile (detect first, then ask), shows it to the user, and selects practices from it.
Questions and detection rules: `questions.md`, `detection.md`.

| # | Dimension | Values | How we get it |
|---|-----------|--------|---------------|
| D0 | **mode** | `new` (greenfield) · `existing` (brownfield) | Detect (source files, git history) + confirm |
| D1 | **stage** | `prototype` · `mvp` · `production` | Ask (Q1) |
| D2 | **team** | `solo` · `small` (2-8) · `multi-team` | Detect (commit authors), else ask (Q6) |
| D3 | **architecture** | `monolith` · `modular-monolith` · `services` | Detect hints, else recommend (04.1); style details in `guides/architecture-styles.md` |
| D4 | **interfaces** | `cli` · `web-ui` · `internal-api` · `public-api` · `events` (multi-select) | Detect + confirm (Q3) |
| D5 | **data** | `none` · `stored` · `personal` · `special-category` (health, biometrics, etc.) | Ask (Q2), never guess |
| D6 | **scale** | `low` · `moderate` · `high` (needs horizontal scaling / distribution) | From horizon (Q4) |
| D7 | **deployment** | `local` · `paas` (managed platform: Streamlit Community Cloud, Heroku, Render, Vercel, App Engine...) · `cloud` (cloud infrastructure you run: AWS, Azure, GCP, Kubernetes) · `on-prem` (installed at customers or own data centre) · `regulated-env` | Detect (platform config files, Dockerfile, IaC, installers); otherwise ask (Q10) |
| D8 | **ai** | `none` · `uses-llm` · `agentic` (LLM takes actions) | Detect (SDKs) + confirm |
| D9 | **regulation** | `gdpr` · `nis2` · `ai-act` · `accessibility-eaa` · `cra` · `none` (multi-select) | Ask (Q5), with options chosen from D5/D7/D8 (see `questions.md`) |
| D10 | **stack** | language, framework, DB, cloud | Detect |
| D11 | **release** | `continuous` · `scheduled` · `multi-version` (several versions supported in production) | Detect (`develop` / `release/*` branches); ask (Q8) only if deployment is `on-prem` or `regulated-env` |
| D12 | **horizon** | `stays-small` · `grows` · `splits` (several teams and/or services) · `high-scale` | Ask (Q4); also sets D6 |
| D13 | **repo** | `single` · `monorepo` · `polyrepo` · `submodules` | Detect (workspace files, `.gitmodules`); default `single` |
| D14 | **shared** | `no` · `yes` (a database or infrastructure is shared with other apps, clients or teams) | Ask (Q7) |
| D15 | **tracker** | `jira` · `github` · `azure-boards` · `gitlab` · `other` · `none` | Detect (issue keys, templates, MCP servers); ask (Q9) only if team>=small |
| D16 | **openness** | `closed` · `published` (source is public, few or no outside contributors) · `community` (accepts outside contributions) | Detect (OSI licence, CONTRIBUTING, package publishing), else ask (Q7b) |
| D17 | **tenancy** | `single` · `multi` (one deployment serves several customers/organisations) | Ask (Q7 option) |
| D18 | **platform** | `no` · `yes` (others build on it: plugins, components, extension APIs, apps on shared services) | Ask (Q7 option) |

## Tag syntax
- `applies: always`
- Ordered dimensions support `>=`, `<=`, `<`, `>`:
  - stage: prototype < mvp < production
  - team: solo < small < multi-team
  - data: none < stored < personal < special-category
  - scale: low < moderate < high
  - openness: closed < published < community
- Equality and inequality: `architecture=services`, `deployment!=local`
- Multi-select dimensions (interfaces, regulation): `interfaces has public-api` (contains one value), `interfaces has-any (internal-api, public-api)` (contains at least one); `regulation!=none` means at least one regulation applies
- Sets: `horizon in (splits, high-scale)`
- Combine with `AND`, `OR`, `NOT` and parentheses. `mode=existing` marks brownfield-only practices.

## Other practice fields
- `note:` a human remark that refines when or how the practice applies; it is not part of the tag and never written into the project.
- `opt-in: yes` the practice is only suggested in the summary and written only if the user accepts it.
- `kind: setup` the practice is applied as configuration (e.g. `.claude/settings.json`, hooks), not written as rule text.

## Tensions
Some practices have `alternatives:`. The skill resolves each tension with its `choose-when:` rule against this profile
(see `guides/principle-tensions.md`) and records the resolved tensions that matter for the project in ADRs, so the choice is visible and can be revisited.

## Changing the profile later
Re-run `/project-init` (upgrade mode) when the profile changes, for example when a prototype becomes production or the team grows. Only the differences are proposed.

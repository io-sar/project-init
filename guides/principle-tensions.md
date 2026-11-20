# Principle tensions

Many practices are one side of a trade-off. The skill picks a side from the profile, writes only the chosen rule, and records the decisions that matter in an ADR.

## How to resolve a tension (deterministic order)
1. **Auto** tensions: evaluate the SECOND column first; if it is true, choose the second side. Otherwise evaluate the FIRST column; if true, choose the first side. If neither can be evaluated from the profile, use the Default.
2. **Advisory** tensions depend on facts the profile does not hold (e.g. "domain stable", "complex reporting queries"). Do not resolve them automatically: write the Default, and list the tension in the summary as a decision for the user or a later ADR.
3. Never apply both sides. If the user overrides a choice, record the override and the reason in the ADR (and in the overrides list, Step 7).

Conditions use the tag syntax of `../profile.md`.

| # | Mode | Tension | Choose the FIRST when | Choose the SECOND when | Default | Practices |
|---|---|---|---|---|---|---|
| T1 | auto | SOLID at all levels vs **YAGNI / KISS** | horizon in (grows, splits, high-scale) OR team>=small | stage=prototype OR (horizon=stays-small AND team<=small) | KISS, with SOLID at module boundaries | 02.4, 02.10 |
| T2 | advisory | DRY vs **AHA / rule of three** | domain stable, copies change for the same reason | domain still unclear | Rule of three | 02.10 |
| T3 | auto | Modular monolith vs **microservices** | mode=new AND team<=small | architecture=services (existing) OR (team=multi-team AND the user confirms known boundaries and a running platform) | Modular monolith | 04.1, 04.9 |
| T4 | auto | Trunk-based vs **Gitflow / release branches** | release=continuous | release in (scheduled, multi-version) | Trunk-based | 01.4, `branching.md` |
| T5 | advisory | Monorepo vs **polyrepo** | shared code, coordinated changes, one release train | independent teams and release cycles | Keep the current layout; single repo for new projects | `repo-strategy.md` |
| T6 | auto | Strong vs **eventual consistency** | per operation: money, inventory, legal or medical records | per operation: feeds, counters, analytics, search indexes | Strong inside one service, eventual across services | 07.10 |
| T7 | advisory | REST vs **GraphQL** vs **gRPC** | public or simple APIs | many client types with varied data needs (GraphQL) / internal high-throughput service calls (gRPC) | REST | 05.x |
| T8 | advisory | ORM vs **query builder / raw SQL** | CRUD-heavy | complex reporting queries, performance-critical paths | ORM, raw SQL where measured | 06.x, 12.3 |
| T9 | auto | Synchronous vs **asynchronous** | the caller needs the answer now AND it returns fast (well under a few seconds) | ai!=none for long model calls, slow third-party or document/media processing, spiky or fire-and-forget work | Synchronous for fast calls; streaming or background jobs for long ones | 04.7, 14.7 |
| T10 | auto | TDD vs **test-after** | domain logic | spikes, exploratory UI (tests still ship before merge) | TDD for domain logic | 03.2 |
| T11 | advisory | Relational vs **document / NoSQL** | relationships, transactions | variable-shape documents, massive write scale | Relational | 06.2, `database-selection.md` |
| T12 | advisory | Design for scale now vs **deploy for today** | horizon=high-scale | everything else | Design boundaries for scale, deploy simply (no Kubernetes for an MVP) | 04.5, 07.1 |
| T13 | auto | Plain tests vs **BDD tooling** | team<=small OR no non-technical stakeholders named | the user says business stakeholders read or write scenarios | Given/When/Then naming in plain tests | 03.10, `testing-strategy.md` |
| T14 | auto | Test pyramid vs **trophy** vs **honeycomb** | logic-heavy backend or monolith (pyramid) | interfaces has web-ui and little backend logic (trophy) / architecture=services (honeycomb) | Pyramid | 03.1, `testing-strategy.md` |
| T15 | auto | Open source / self-hosted vs **paid / managed** | stage<=mvp | stage=production AND (regulation!=none OR an SLA is needed) | Open source or free tier on open standards; pay where it buys reliability, support, compliance or saved people-time | 16.8, `tool-selection.md` |
| T16 | auto | Containerised vs **native** local setup | a backing service exists (database server, broker, cache; embedded stores such as SQLite or files do not count) OR deployment in (cloud, on-prem, regulated-env) OR team>=small | libraries, CLIs, desktop/mobile apps, prototypes with no backing services | Compose for backing services, app native or containerised | 01.11 |
| T17 | advisory | Permissive vs **weak copyleft** vs **strong copyleft** licence | maximum adoption, commercial reuse (MIT, Apache-2.0) | keep changes to your files open (MPL-2.0, LGPL) / keep all derivatives open, incl. network use (GPL, AGPL) | Apache-2.0 | 17.1 |
| T18 | auto | DCO vs **CLA** | openness=community, no company relicensing plans | a company may need to relicense or dual-license later (user confirms) | DCO | 17.5 |
| T19 | advisory | Shared schema vs **schema per tenant** vs **database per tenant** | many small tenants, low cost | moderate isolation, per-tenant restore / strong isolation, regulated or enterprise tenants, data residency | Shared schema + row-level security; hybrid when premium isolation is sold | 04.14, `architecture-styles.md` |
| T20 | advisory | Choreography vs **orchestration** | few steps, simple flows | many steps, compensations, timeouts, process visibility | Orchestration for business-critical multi-step processes | 04.15, 07.6 |
| T21 | auto | Direct calls vs **API gateway** vs **gateway + BFF** | architecture!=services AND NOT interfaces has public-api | architecture=services OR interfaces has public-api (gateway); add BFF when the user names very different client types | Direct calls | 04.13 |
| T22 | advisory | Secret manager or platform store vs **secrets encrypted in the repo** | deployment in (paas, cloud, on-prem, regulated-env) and a secret store is available | no secret manager available AND GitOps-style deployment (user confirms) | Platform secret store or secret manager; plaintext git-ignored files only for local development | 08.1 |

# Architecture styles guide

Used by practices 04.10 to 04.17 and the architecture ADR (0002). Start from the quality attributes (04.10), then pick the simplest style that meets them.

## 1. Quality attributes (pick the top 3)
| Attribute | Question it answers | Typical drivers in the profile |
|---|---|---|
| Time to market / simplicity | How fast can we ship and change? | stage<=mvp, team=solo |
| Modifiability | How cheaply can the system evolve? | horizon in (grows, splits) |
| Scalability / elasticity | Can it handle more or spiky load? | horizon=high-scale |
| Availability / resilience | How much downtime is acceptable? | stage=production, SLOs |
| Performance | How fast must responses be? | interactive UIs, high scale |
| Security / privacy | What is the cost of a breach? | data>=personal, regulation!=none |
| Deployability / team autonomy | Can teams release independently? | team=multi-team, horizon=splits |
| Cost efficiency | What may it cost to run? | every profile; dominant for prototypes |
| Extensibility | Can others build on it safely? | platform=yes |
| Tenant isolation | Can one customer affect another? | tenancy=multi |

## 2. Styles
| Style | What it is | Strengths | Costs | Choose when |
|---|---|---|---|---|
| **Layered / modular monolith** | One deployable, internal modules with clear boundaries (04.2, 04.9) | Simple to build, test, deploy and debug; cheap | Scales as one unit; one release train | Default for new systems (04.1) |
| **Service-based** | A few coarse-grained services (4 to 12), often sharing one database | Independent deploys without full microservice cost | Shared database needs governance (06.13) | Middle step between monolith and microservices; existing platforms |
| **Microservices** | Many small services, each owning its data (04.6) | Independent scaling and team autonomy | Distributed-systems complexity (group 07), platform and ops cost | team=multi-team, known boundaries, running platform |
| **Event-driven** | Components react to events through a broker (04.15) | Loose coupling, scalability, natural audit trail | Eventual consistency, harder debugging and tracing | Many consumers of the same facts, async workflows, integrations |
| **Serverless** | Functions and managed services, pay per use | No servers to run, scales to zero, low cost at low or spiky load | Cold starts, execution limits, vendor lock-in, harder local testing | Spiky or low-volume workloads, glue code, event handlers |
| **Microkernel / plugin** | Small core plus extensions via a contract (04.17) | Extensibility, customer-specific features without forking | Contract design and versioning are hard | platform=yes, products customised per customer |
| **Pipeline (pipes and filters)** | Data flows through independent processing steps | Simple to reason about, steps reusable and scalable | Poor fit for interactive request/response | ETL, data and ML pipelines, document or media processing, LLM chains |

Styles combine: e.g. a modular monolith that publishes events, or microservices with a plugin layer. Record the combination and why.

## 3. Multi-tenancy models (04.14)
| Model | Isolation | Cost per tenant | Operations | Choose when |
|---|---|---|---|---|
| **Shared schema + tenant ID** (with row-level security) | Logical only; a bug can leak data across tenants | Lowest | One schema to migrate | Many small tenants, standard needs |
| **Schema per tenant** | Stronger; per-tenant backup and restore are easier | Medium | Migrations run per schema; limits on schema count | Tens to hundreds of tenants, moderate isolation needs |
| **Database per tenant** | Strongest; per-tenant region, keys and restore | Highest | Fleet management and automation needed | Regulated or enterprise tenants, data residency per tenant |
| **Hybrid (tiered)** | Shared for standard tiers, dedicated for premium | Mixed | Two paths to maintain | Mixed customer base with premium isolation needs |

Whatever the model: tenant context everywhere, tenant in cache keys, queues, logs and metrics, per-tenant limits, cross-tenant leak tests, per-tenant export and deletion.

## 4. Edge: gateway and backend-for-frontend (04.13)
| Option | Choose when |
|---|---|
| Direct calls to the application | One app, one client, monolith |
| One API gateway | Several services or a public API: central auth, rate limiting, routing |
| Gateway + BFF per client type | Clients with very different needs (web, mobile, partners) |

## 5. Coordinating multi-step processes (04.15, 07.6)
| Option | How | Choose when |
|---|---|---|
| **Choreography** | Each service reacts to events; no central coordinator | Few steps, simple flows, loosely related teams |
| **Orchestration** | A coordinator (workflow engine or orchestrator service) tells each step what to do | Many steps, compensations, timeouts, a need to see the state of each process |

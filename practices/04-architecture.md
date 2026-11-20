---
group: Architecture
id: "04"
version: 0.4
reviewed: 2026-11-17
---

# 04 · Architecture

Structure decisions that are expensive to reverse. Start from the quality attributes the system needs, choose the simplest style that delivers them (`../guides/architecture-styles.md`), and record every significant decision in an ADR.

## 04.1 Modular monolith first
- applies: mode=new OR architecture!=services
- rule: Start as a modular monolith. Split into separate services only with a recorded driver (independent scaling, team autonomy, different release cadence) in an ADR.
- why: Microservices add network, data and operational complexity that most projects do not need early, and service boundaries are hard to get right before the domain is understood.
- alternatives: microservices from day one
- choose-when: microservices only if team=multi-team from day one AND boundaries are already known (e.g. rewrite of an existing system) AND a platform (CI/CD, observability, deployment) is running; otherwise modular monolith, plus 04.9 when horizon=splits (T3)

## 04.2 Clear boundaries
- applies: stage>=mvp
- rule: Separate domain logic from infrastructure (layered or hexagonal / ports and adapters). Domain code does not import frameworks, DB or HTTP libraries.
- why: The core stays testable and the infrastructure can change without rewriting the business logic.

## 04.3 Domain-Driven Design
- applies: team>=small OR architecture=services OR horizon in (splits, high-scale)
- rule: Identify bounded contexts and use the business's language in code. One module (or service) per bounded context.
- why: Boundaries that follow the business change less often than technical ones.

## 04.4 Architecture diagrams
- applies: team>=small OR stage=production
- rule: Maintain C4 diagrams (at least Context and Container) as code in `docs/architecture/`. For larger systems (team>=small AND stage=production), structure the architecture documentation with the arc42 template.
- why: A shared picture prevents conflicting mental models; a standard template makes documentation complete and easy to navigate.

## 04.5 Stateless application tier
- applies: deployment in (cloud, paas) OR scale>=moderate
- rule: Keep application instances stateless; store sessions, files and state in managed stores.
- why: Stateless instances can be scaled, replaced and restarted freely.

## 04.6 Data ownership per service
- applies: architecture=services
- rule: Each service owns its data; no shared database between services. Other services access it only through APIs or events.
- why: A shared database couples services so tightly that they cannot change independently.
- alternatives: shared database with governance (06.13); service-based architecture with a shared database (see ../guides/architecture-styles.md)
- choose-when: own data per service by default; a shared database only for coarse-grained service-based architectures or existing platforms, always with 06.13

## 04.7 Sync vs async decided per interaction
- applies: architecture=services OR interfaces has events OR ai!=none
- rule: Use synchronous calls only when the caller needs the answer now and it returns fast; use events or queues otherwise. Treat slow or unpredictable calls (LLM inference, agents, document processing, third-party APIs) as asynchronous (see 14.7). Document the choice per integration.
- why: Chains of synchronous calls multiply latency and failure; slow calls held synchronously block resources and time out.
- alternatives: synchronous everywhere / asynchronous everywhere
- choose-when: T9 in ../guides/principle-tensions.md

## 04.8 Architecture fitness functions
- applies: stage=production OR horizon=splits
- rule: Enforce key boundaries with automated architecture tests (e.g. "domain must not import infrastructure").
- why: Boundaries that are not checked erode within months.

## 04.9 Extraction-ready modules
- applies: horizon=splits OR horizon=high-scale
- rule: Build each module so it could become a service later: one module per bounded context; modules talk only through a module's public interface; each module owns its tables (no cross-module joins or foreign keys, reference by ID); side effects between modules go through in-process events; no transaction spans modules unless documented; architecture tests (04.8) enforce these rules. Extract later with the strangler fig pattern, never a big-bang rewrite.
- why: The risk of "monolith first" is not the monolith but a big ball of mud; clean module boundaries make later extraction a routine change instead of a months-long untangling.

## 04.10 Quality attributes drive the design
- applies: stage>=mvp
- rule: Before choosing a style, name the top 3 quality attributes the system must deliver (e.g. availability, scalability, security, time to market, cost, modifiability, performance) with a measurable target where possible, and record them in ADR 0002. Use them to justify every major trade-off.
- why: Every architecture optimises some qualities at the expense of others; naming the priorities makes trade-offs explicit instead of accidental.

## 04.11 Architecture style chosen explicitly
- applies: always
- rule: Choose the style from ../guides/architecture-styles.md (modular monolith, service-based, microservices, event-driven, serverless, microkernel/plugin, pipeline) against the quality attributes (04.10) and the profile, and record the choice and the rejected options in an ADR.
- why: Styles have very different costs; choosing by fashion or habit is the most expensive architecture mistake.

## 04.12 Effort proportional to reversibility
- applies: always
- rule: Classify decisions as one-way doors (hard to reverse: data model, public API, database, cloud provider, tenancy model, licence) or two-way doors (easy to reverse: internal libraries, module structure). Spend analysis and an ADR on one-way doors; decide two-way doors quickly and move on.
- why: Over-analysing reversible choices wastes time; under-analysing irreversible ones creates years of cost.

## 04.13 API gateway and backend-for-frontend
- applies: architecture=services OR interfaces has public-api
- rule: Put a gateway at the edge for cross-cutting concerns (routing, authentication, rate limiting 05.7, TLS, request logging). Keep business logic out of the gateway. Add a backend-for-frontend (BFF) per client type only when clients need very different data shapes (e.g. web vs mobile vs partners).
- why: Centralises edge concerns once instead of in every service; BFFs keep clients simple without bloating a generic API.
- alternatives: direct client-to-service calls / one generic gateway / BFF per client type
- choose-when: T21 in ../guides/principle-tensions.md

## 04.14 Multi-tenancy model
- applies: tenancy=multi
- rule: Choose the isolation model per tier from ../guides/architecture-styles.md (shared schema with tenant ID and row-level security, schema per tenant, database per tenant, or a hybrid with premium tenants isolated) and record it in an ADR. Whatever the model: propagate the tenant context through every request, job and event; include the tenant in cache keys, queue routing, logs and metrics; enforce per-tenant limits against noisy neighbours; test for cross-tenant data leaks in CI; support per-tenant export, restore and deletion (09.3).
- why: The tenancy model is a one-way door that decides isolation, cost, compliance and how one customer's change or load can affect the others.
- alternatives: shared schema / schema per tenant / database per tenant / hybrid
- choose-when: T19 in ../guides/principle-tensions.md

## 04.15 Event-driven design
- applies: interfaces has events OR architecture=services
- rule: Model events as past-tense facts (`OrderPlaced`) and keep them distinct from commands (`PlaceOrder`). Treat event schemas as public contracts: version them, keep changes backward compatible, and validate them (05.1; a schema registry when there are many producers). Decide per event whether it only notifies or carries the state consumers need. Choose choreography or orchestration per business process.
- why: Events decouple producers and consumers in time and deployment, but only if their contracts are stable and their meaning is clear.
- alternatives: choreography / orchestration
- choose-when: T20 in ../guides/principle-tensions.md

## 04.16 Anti-corruption layer for external systems
- applies: stage>=mvp
- rule: Wherever an external model would otherwise leak into domain code, wrap the external or legacy system (third-party APIs, ERPs, partner systems, AI providers) behind an adapter that translates its model into your domain model; the rest of the code never uses the external model directly.
- why: External models change on someone else's schedule and leak awkward concepts into your domain; one adapter contains the damage and makes the provider replaceable.

## 04.17 Extension and plugin architecture
- applies: platform=yes
- rule: Expose a versioned extension contract (plugin API, events, extension points) and keep the core closed to direct modification. Plugins and apps built on the platform are isolated: their own data or schema, resource limits, capability-based permissions, and no rights to change shared resources (databases, extensions, global config). Every core change is tested against all registered extensions (contract tests); plugin install, upgrade and disable are reversible; publish a compatibility matrix.
- why: On a platform, one extension or one core change can break every other tenant or app; isolation and contract tests turn that into a failed check instead of an outage.

## 04.18 Availability and disaster recovery by design
- applies: stage=production
- rule: Derive the deployment topology from the SLO (10.4) and the RPO/RTO (06.4): single zone, multi-zone or multi-region. Remove single points of failure on the critical path, document the disaster-recovery procedure, and rehearse it at least yearly.
- why: Availability is designed, not added; a recovery plan that was never rehearsed usually fails when it is needed.

## 04.19 Boundaries aligned with teams (Conway's law)
- applies: team=multi-team OR horizon=splits
- rule: Give every module or service exactly one owning team, and align boundaries with team structure (or reshape teams to fit the target architecture). Record ownership in CODEOWNERS and the architecture docs.
- why: Systems mirror the communication structure of the organisations that build them; boundaries that cut across teams create constant coordination cost.

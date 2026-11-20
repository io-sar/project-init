---
group: Scalability and distributed systems
id: "07"
version: 0.4
reviewed: 2026-11-17
---

# 07 · Scalability and distributed systems

Once work crosses a network, everything can fail partially. Design for it from the start.

## 07.1 Horizontal scaling
- applies: scale=high
- rule: Scale by adding stateless instances behind a load balancer, not by growing one machine. Autoscale on load metrics.
- why: Vertical scaling has a ceiling and a single point of failure.

## 07.2 Timeouts and retries
- applies: stage>=mvp
- rule: Every remote call has a timeout. Retry only idempotent operations and only transient errors (timeouts, connection errors, 502/503/504, 429 respecting `Retry-After`), never 4xx validation or auth errors. Use exponential backoff with jitter and a retry limit, then fail gracefully or fall back. Retry in ONE layer only (client, gateway or service, not all of them).
- why: Calls without timeouts hang threads; retrying persistent errors wastes resources; retries at several layers multiply (3 layers × 3 retries = 27 calls) and turn small outages into retry storms.

## 07.3 Circuit breakers and bulkheads
- applies: architecture=services
- rule: Wrap calls to dependencies in circuit breakers and isolate resource pools per dependency.
- why: One slow dependency must not exhaust resources and take the whole system down.

## 07.4 Idempotent consumers
- applies: interfaces has events
- rule: Assume at-least-once delivery: every message handler is idempotent (deduplicate by message ID). Messages that keep failing after the retry limit go to a dead-letter queue, raise an alert, and can be replayed after a fix.
- why: Exactly-once delivery is rare in practice; duplicates will arrive, and poison messages must not loop forever or block the queue.

## 07.5 Transactional outbox
- applies: interfaces has events AND data>=stored
- rule: Publish events through an outbox table written in the same transaction as the state change.
- why: Avoids the "saved to DB but event lost" (or the reverse) inconsistency.

## 07.6 Sagas over distributed transactions
- applies: architecture=services
- rule: Coordinate multi-service business transactions with sagas (orchestrated or choreographed) and compensating actions. No two-phase commit across services.
- why: Distributed locks and 2PC hurt availability and scale.

## 07.7 Back-pressure and load levelling
- applies: scale=high
- rule: Put queues in front of spiky or slow work and apply back-pressure when consumers fall behind.
- why: Smooths peaks instead of failing under them.

## 07.8 CQRS and event sourcing only when needed
- applies: scale=high
- opt-in: yes (suggested in the summary, written only if the user accepts)
- rule: Do not introduce CQRS or event sourcing without an ADR naming the concrete need (read/write asymmetry, audit trail).
- why: Powerful patterns with a high complexity cost.

## 07.9 Design for partial failure
- applies: architecture=services
- rule: For each dependency, document what happens when it is down (degrade, queue, fail) and test it.
- why: In distributed systems the question is when a dependency fails, not if.

## 07.10 Consistency model chosen per operation
- applies: architecture=services OR interfaces has events OR scale=high
- rule: For each operation, decide and document whether it needs strong consistency (money, inventory, legal records) or can be eventually consistent (feeds, counters, analytics, search). Make eventual consistency visible in the UI where users could notice it.
- why: Strong consistency everywhere hurts availability and scale; eventual consistency in the wrong place causes real business errors.
- alternatives: strong consistency everywhere / eventual consistency everywhere
- choose-when: T6 in ../guides/principle-tensions.md

## 07.11 Replication and partitioning
- applies: scale=high
- rule: Scale reads with replicas (and accept replica lag where 07.10 allows). Introduce sharding/partitioning only after measuring a write or size limit, with an ADR naming the partition key.
- why: Replication is cheap and well understood; sharding is hard to undo and a bad partition key creates hot spots.

## 07.12 Service discovery and service mesh
- applies: architecture=services AND team=multi-team
- opt-in: yes (suggested in the summary, written only if the user accepts)
- rule: Use the platform's service discovery (e.g. Kubernetes DNS, Consul). Adopt a service mesh only with an ADR naming the need (mTLS everywhere, uniform retries/routing across many services).
- why: A mesh standardises routing, security and resilience across many services but is heavy to operate for few services.

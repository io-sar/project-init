---
group: Performance and cost
id: "12"
version: 0.4
reviewed: 2026-11-17
---

# 12 · Performance and cost

Fast enough and cheap enough are requirements; define them and measure them.

## 12.1 Measure before optimising
- applies: always
- rule: Profile before changing code for performance and record the before/after numbers in the PR.
- why: Intuition about bottlenecks is usually wrong.

## 12.2 Performance budgets
- applies: stage=production
- rule: Set budgets for key paths (p95/p99 latency, page weight, memory) and check them in CI or monitoring.
- why: Performance degrades slowly unless a number stops it.

## 12.3 Efficient data access
- applies: data>=stored
- rule: No N+1 queries and no unbounded queries; every query on a large table uses an index. Review query plans for new heavy queries.
- why: Database access is the most common performance bottleneck.

## 12.4 Cost visibility (FinOps basics)
- applies: deployment=cloud
- rule: Tag all cloud resources by project and environment, set budget alerts, and review cost monthly.
- why: Cloud cost surprises come from resources nobody knew were running.

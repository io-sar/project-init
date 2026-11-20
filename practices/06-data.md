---
group: Data
id: "06"
version: 0.4
reviewed: 2026-11-17
---

# 06 · Data

Data outlives code. Mistakes here are the hardest to undo.

## 06.1 Versioned migrations
- applies: data>=stored
- rule: Change the database only through versioned migrations in git (tables, indexes, roles, settings, and extensions with pinned versions), applied automatically in CI and deploys. Migrations are forward-only and backward-compatible with the running version (expand, then contract).
- why: Manual schema changes drift between environments and break zero-downtime deploys.

## 06.2 Choose the store by access pattern
- applies: data>=stored
- rule: Default to a relational database. Choose another store only for a documented access pattern, using ../guides/database-selection.md, and record it in an ADR.
- why: Relational databases cover most needs; every extra store adds backup, security and operations work.
- alternatives: document / NoSQL stores
- choose-when: see T11 in ../guides/principle-tensions.md

## 06.3 Explicit transactions and consistency
- applies: data>=stored
- rule: Define transaction boundaries explicitly in the application layer. Document where eventual consistency is accepted.
- why: Implicit transactions produce partial writes and race conditions.

## 06.4 Backups with tested restore
- applies: data>=stored AND stage=production
- rule: Automate backups, define RPO and RTO, and test a restore at least quarterly.
- why: An untested backup is a hope, not a backup.

## 06.5 Caching with explicit invalidation
- applies: scale>=moderate
- rule: Every cache has a TTL and a documented invalidation rule. Cache reads, never the source of truth.
- why: Stale caches cause bugs that are very hard to reproduce.

## 06.6 Data classification
- applies: data>=personal
- rule: Classify every stored field (public, internal, personal, special category) in a data inventory in `docs/data/`.
- why: You cannot protect, retain or delete what you have not identified.

## 06.7 Retention and deletion
- applies: data>=personal
- rule: Define a retention period per data type and implement automated deletion or anonymisation.
- why: Keeping data "just in case" is a GDPR violation and a growing breach risk.

## 06.8 Encryption
- applies: data>=personal OR deployment=cloud
- rule: Encrypt data in transit (TLS everywhere) and at rest. Keys live in a key management service, not in config.
- why: Limits the damage of stolen disks, snapshots or intercepted traffic.

## 06.9 Optimistic locking
- applies: data>=stored AND (team>=small OR interfaces has-any (web-ui, internal-api, public-api))
- rule: Protect records that can be edited concurrently with a version column (or timestamp) checked on update; reject stale updates with a conflict error instead of overwriting.
- why: Prevents "lost updates", where the last save silently wins over someone else's change.

## 06.10 Soft-delete policy
- applies: data>=stored
- rule: Decide per entity whether deletion is soft (flag) or hard, and document it. Soft-deleted personal data is NOT erased under GDPR: implement real deletion or anonymisation for erasure requests and retention (09.3, 06.7). Exclude soft-deleted rows by default in queries.
- why: Soft delete is convenient for undo and audit, but silently keeps data you may be obliged to remove.

## 06.11 Audit fields
- applies: data>=stored AND stage>=mvp
- note: in existing projects this is a planned item in the adoption plan, never a mass migration
- rule: Every entity table (not join or lookup tables) has `created_at` and `updated_at` (UTC); tables changed by users also record who made the change (`created_by` / `updated_by`). Use an audit log table for entities where the history matters.
- why: Answers "who changed this and when" during debugging, support and audits.

## 06.12 Migration safety checks
- applies: data>=stored AND stage>=mvp
- rule: Lint every migration in CI (e.g. Squawk or Atlas for Postgres) and require owner approval for destructive or locking changes and extension changes. Human accounts have no direct schema-change rights outside local development.
- why: An untracked change to a shared database (such as an extension upgrade) can break every consumer at once with no record of who or why.

## 06.13 Shared database governance
- applies: shared=yes AND data>=stored
- rule: A shared database or schema has a named owner and CODEOWNERS on its migrations. Before merge, CI runs the tests or contract tests of every consumer against the migrated schema (impact check). Treat the shared schema as a versioned contract: changelog, expand-then-contract for breaking changes, announced deprecations. Log DDL in the database itself (event triggers or pgAudit) so out-of-band changes are visible.
- why: Shared data is a hidden API; changes need the same discipline as a public API, or one consumer's change breaks the others.
- alternatives: separate schema or database per app/client (removes the coupling, see 04.6)
- choose-when: prefer separation when building new; apply governance when sharing already exists or is a deliberate platform choice

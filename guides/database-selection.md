# Database selection guide

Used by practice 06.2 and when writing the architecture ADR. Default: a relational database (PostgreSQL). Anything else needs a documented access pattern.

| Need | Recommended | Notes |
|---|---|---|
| General application data, relationships, transactions, reporting | **PostgreSQL** | Default. Most extensible, wide index types, JSONB covers many document needs. |
| Simple relational web app where the team or host already standardises on it | **MySQL / MariaDB** | Fine choice; widely supported. |
| Prototype, local tool, embedded, single-user app, tests | **SQLite** | Zero operations. Move to Postgres when concurrent writes or networked access are needed. |
| Cache, sessions, rate limiting, leaderboards, short-lived data | **Redis / Valkey** | Never the source of truth: assume data can be lost. |
| Documents whose shape varies a lot, very high write scale | **MongoDB** (or Postgres JSONB first) | Try JSONB before adding a second database. |
| Full-text search, faceting | **OpenSearch / Elasticsearch** (or Postgres full-text for small scale) | Secondary index fed from the primary store, never the source of truth. |
| Metrics, IoT, time-ordered events | **Time-series DB** (e.g. TimescaleDB, InfluxDB) | TimescaleDB keeps you on Postgres. |
| Vector similarity for AI features | **pgvector** first, dedicated vector DB at large scale | Avoid a new database until volume proves it. |
| Analytics over large volumes | **Columnar / warehouse** (e.g. DuckDB locally, BigQuery, Snowflake, ClickHouse) | Keep analytics off the transactional database. |

## Scaling notes
- Relational databases scale reads horizontally with read replicas; scaling writes (sharding) is hard for every engine. Decide on partitioning only with a measured need (07.11).
- Combining stores is normal (e.g. Postgres for transactions plus Redis for caching). Every extra store adds backup, security and operations work: justify each one in an ADR.

Source used: comparison of MySQL, PostgreSQL, Redis and MongoDB (https://3lys1an.com/posts/ec26f30f/), with corrections and additions.

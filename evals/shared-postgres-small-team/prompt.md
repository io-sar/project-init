---
tags: [skill-creator]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

/project-init dry run. Two internal apps in this repo share one Postgres database with other client apps of our platform. Answers: production, personal data, internal API, grows, GDPR, small team of 5, yes the database is shared, GitHub Issues. Input files: docker-compose.yml, apps/orders/pyproject.toml, apps/billing/pyproject.toml, migrations/001_init.sql

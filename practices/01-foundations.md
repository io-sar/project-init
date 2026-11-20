---
group: Engineering foundations
id: "01"
version: 0.4
reviewed: 2026-11-17
---

# 01 · Engineering foundations

The basics that make a repo understandable, runnable and safe to change. Without them every other practice is harder to apply.

## 01.1 Standard repo layout
- applies: always
- rule: Keep a predictable layout (`src/`, `tests/`, `docs/`, `scripts/`), with the README following 01.12.
- why: People and Claude find things without searching; onboarding takes hours, not days.

## 01.2 One-command setup and run
- applies: always
- rule: Provide single commands for setup, run, test and lint (Makefile, task runner or devcontainer). Document them in CLAUDE.md.
- why: Removes "works on my machine" and lets Claude verify its own changes.

## 01.3 Clean repository hygiene
- applies: always
- rule: Maintain `.gitignore` and `.editorconfig`. Never commit secrets, local env files, build output or generated files.
- why: Leaked secrets and noisy diffs are the most common avoidable incidents.

## 01.4 Branching model follows the release model
- applies: team>=small OR release!=continuous
- rule: Use trunk-based development with short-lived branches (merged within ~2 days) for continuous releases; use release branches or Gitflow only when releases are scheduled or several versions are supported. Always protect `main` with green CI; require PR review when team>=small. Record the choice in an ADR.
- why: Long-lived branches cause drift and painful merges; scheduled or multi-version releases genuinely need stabilisation branches.
- alternatives: Gitflow / release branches (see ../guides/branching.md)
- choose-when: release=continuous → trunk-based; release in (scheduled, multi-version) → release branches or Gitflow

## 01.5 Commit convention and versioning
- applies: stage>=mvp
- rule: Use Conventional Commits (`feat:`, `fix:`, `chore:` ...) and Semantic Versioning for releases.
- why: History becomes readable and changelogs and versions can be generated automatically.

## 01.6 Changelog
- applies: stage>=mvp
- rule: Keep a CHANGELOG generated from commits; every release has an entry.
- why: Users and operators know what changed without reading code.

## 01.7 Architecture Decision Records
- applies: always
- note: one-paragraph ADRs are enough for prototypes
- rule: Record significant decisions as ADRs in `docs/adr/NNNN-title.md` (context, decision, consequences). Never edit an accepted ADR; supersede it.
- why: Future people (and Claude) understand why things are the way they are and do not undo decisions blindly.

## 01.8 Configuration via environment
- applies: always
- rule: Read non-secret configuration from the environment (12-factor). Commit a `.env.example` with every variable and no real values. Secrets follow 08.1.
- why: The same build runs in every environment; config stays out of code.

## 01.9 Licensing
- applies: stage>=mvp
- rule: Check dependency licences for compatibility with how the product is distributed. Closed projects carry a proprietary notice (never add an open-source licence by default); public projects follow 17.1.
- why: Licence surprises can block a release or a sale late in the project.

## 01.10 Twelve-factor app
- applies: deployment in (cloud, paas) OR interfaces has public-api
- rule: Build the service as a twelve-factor app. Factors covered elsewhere: codebase (01.1), dependencies (08.5), config (01.8), build/release/run (11.2), processes (04.5), concurrency (07.1), disposability (10.7), dev/prod parity (11.4), logs (10.1), admin processes (06.1). Additionally: (a) the app is self-contained and exposes its service by binding to a port; (b) backing services (DB, queue, cache, mail) are attached resources swappable by changing config only; (c) admin and maintenance tasks run as one-off processes from the same release, never by hand on a server.
- why: A proven baseline for services that are easy to deploy, scale and replace. Source: https://12factor.net/

## 01.11 Containerised local environment
- applies: data>=stored OR interfaces has events OR deployment in (cloud, on-prem, regulated-env) OR team>=small
- note: embedded stores (SQLite, files) do not need a containerised backing service; see T16
- rule: Backing services (database, queue, cache) run locally with Docker Compose, using the same versions as production. The app has a Dockerfile (multi-stage, 08.9) when it is deployed as a container. Offer a devcontainer when team>=small so everyone shares the same toolchain. The app itself may run natively for a fast hot-reload loop; `docker compose up` must still start the full stack.
- why: Removes "works on my machine", makes integration tests realistic (03.5), and keeps dev close to production (11.4).
- alternatives: native-only local setup
- choose-when: T16 in ../guides/principle-tensions.md; native-only is fine for libraries, CLIs distributed via package managers, desktop/mobile apps, and prototypes with no backing services

## 01.12 README structure
- applies: always
- rule: The README answers, in this order: what it is and for whom (2–3 lines); status (build, coverage, version badges); quick start in three commands or fewer; prerequisites; configuration (link `.env.example`); usage examples; how to run tests; where to find architecture, ADRs and docs; how to contribute (link CONTRIBUTING.md); licence; owners/contact. Keep it short and link to `docs/` for depth. Organise `docs/` with the Diátaxis split (tutorials, how-to guides, reference, explanation) once it grows.
- why: The README is the front door for people and for Claude; a predictable structure makes it scannable, and pushing depth into docs keeps it current.

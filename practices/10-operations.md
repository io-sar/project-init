---
group: Reliability, observability and operations
id: "10"
version: 0.4
reviewed: 2026-11-17
---

# 10 · Reliability, observability and operations

You cannot run what you cannot see. Operations is part of the product, not an afterthought.

## 10.1 Structured logging
- applies: stage>=mvp
- rule: Log in structured format (JSON) with level, timestamp, and a correlation/request ID passed across calls. Write logs to stdout as an event stream and let the platform collect and route them; the app never manages log files. No personal data (see 09.5, 09.10).
- why: Structured logs can be searched and correlated across services; stdout logging works the same in every environment (12-factor).

## 10.2 Metrics and health endpoints
- applies: deployment in (cloud, on-prem, regulated-env)
- rule: Expose RED metrics (rate, errors, duration) for services and USE metrics (utilisation, saturation, errors) for resources, plus liveness and readiness endpoints.
- why: Orchestrators and on-call engineers need a fast health signal.

## 10.3 Distributed tracing
- applies: architecture=services
- rule: Instrument with OpenTelemetry and propagate trace context across all calls and messages.
- why: Without traces, finding where a slow request spent its time across services is guesswork.

## 10.4 SLOs and error budgets
- applies: stage=production
- rule: Define SLOs for key user journeys (e.g. 99.9% of checkouts succeed within 2 s) and use the error budget to balance features and reliability.
- why: Turns "is it reliable enough?" into a measurable, shared decision.

## 10.5 Actionable alerting
- applies: stage=production
- rule: Alert on user-facing symptoms (SLO burn), not on every cause. Every alert links to a runbook and needs a human action.
- why: Noisy alerts get ignored, and then the real one is missed.

## 10.6 Incident management
- applies: stage=production
- rule: Keep runbooks for known failures, a clear incident process (roles, communication), and blameless postmortems with tracked actions (ITIL incident and problem management).
- why: Incidents are inevitable; learning from them is optional unless it is a process.

## 10.7 Graceful shutdown and degradation
- applies: deployment in (cloud, on-prem, regulated-env)
- rule: Handle termination signals by finishing in-flight work; degrade non-critical features instead of failing completely.
- why: Deploys and scaling events should be invisible to users.

## 10.8 Security event logging
- applies: stage>=mvp AND (data>=personal OR interfaces has public-api)
- rule: Log security-relevant events (logins and failures, permission and role changes, admin actions, access to sensitive records, configuration changes) to an append-only audit log with who, what, when and from where, without personal data payloads (09.5). Alert on suspicious patterns.
- why: Without security events you cannot detect an attack or reconstruct one; logging and alerting failures are an OWASP Top 10:2025 category.

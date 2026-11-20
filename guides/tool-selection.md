# Tool selection guide (free vs paid, self-hosted vs managed)

Used by practice 16.8. "Free" is about licence cost only; the real comparison is total cost of ownership and risk.

## Criteria
| Criterion | Questions to answer |
|---|---|
| **Total cost of ownership** | Licence + hosting + operations + upgrades + people time. Who patches, backs up and is on call for it? |
| **Licence type** | Permissive open source (MIT, Apache-2.0, BSD), copyleft (GPL, AGPL: check obligations for SaaS), source-available (BSL, SSPL, Elastic: usage restrictions), proprietary. Does it fit how you distribute or host the product? |
| **Relicensing risk** | Is the project controlled by one company that could change the licence? Precedents: Terraform moved to BSL in 2023 (community fork: OpenTofu); Redis moved to source-available licences in 2024 (community fork: Valkey). Prefer foundation-governed projects or ones with credible forks. |
| **Lock-in and exit cost** | Proprietary APIs and data formats vs open standards (SQL, OpenTelemetry, OCI containers, OpenAPI, S3-compatible storage). How hard is it to leave? |
| **Free tier limits** | Where are the pricing cliffs (users, seats, build minutes, events, storage)? What happens at 10× usage? |
| **Support and SLA** | Does production need guaranteed response times? Is community support enough? |
| **Security and compliance** | Certifications (ISO 27001, SOC 2), EU data residency and a DPA for GDPR (09.6), SSO/audit logs, vulnerability response track record. |
| **Health and maturity** | Release activity, number of maintainers (bus factor), adoption, OpenSSF Scorecard result for open-source projects. |
| **Team fit** | Existing skills, learning curve, integration with the current stack and tracker. |

## Decision rules by profile
| Profile | Lean towards |
|---|---|
| stage=prototype | Free and open source, free tiers, zero-ops options (SQLite, local tools). Speed of learning matters most. |
| stage=mvp | Open source on open standards, managed free/low tiers; avoid choices that are expensive to leave. |
| stage=production | Pay where it buys reliability, support, compliance or saves more people-time than it costs; keep open standards at the boundaries to preserve an exit. |
| regulation!=none OR data>=special-category | Vendors with the needed certifications, EU hosting and a DPA; self-host only with the skills to run it securely. |
| deployment=cloud | Managed services for undifferentiated heavy lifting (databases, queues, identity) unless cost or lock-in says otherwise. |

## Build vs buy
Build only what differentiates the product. Buy or adopt open source for commodity capabilities (auth, payments, email, observability, CI), and wrap them behind your own interface (04.2) so they can be replaced.

## Record it
Write an ADR for any tool that is costly to reverse (database, cloud, identity provider, observability platform, framework): options considered, criteria scores, decision, exit plan.

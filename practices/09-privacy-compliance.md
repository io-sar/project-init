---
group: Privacy and compliance (EU-first)
id: "09"
version: 0.4
reviewed: 2026-11-17
---

# 09 · Privacy and compliance (EU-first)

Legal obligations shape design. These rules are engineering guidance, not legal advice: confirm with the organisation's DPO or legal team. Conflicts in this group are always flagged as high priority.

## 09.1 Privacy by design and default (GDPR)
- applies: data>=personal
- rule: Collect only the personal data needed for a stated purpose; the most private setting is the default.
- why: Data minimisation is a GDPR principle, and data you never collect cannot leak.

## 09.2 Purpose and lawful basis per field
- applies: data>=personal
- rule: Record a lawful basis per processing purpose, and map each purpose to the personal data fields it uses in the data inventory (see 06.6).
- why: Needed for the record of processing activities and for answering data subject requests.

## 09.3 Data subject rights built in
- applies: data>=personal AND stage>=mvp
- rule: Implement access/export, rectification and erasure for a user's data as product features, covering live stores and downstream systems; backups expire within the retention period, and deletions are re-applied after any restore.
- why: Requests have legal deadlines; retrofitting deletion across systems is very costly.

## 09.4 DPIA for high-risk processing
- applies: data>=personal AND (data=special-category OR ai!=none OR scale=high)
- rule: Run a Data Protection Impact Assessment before building high-risk processing (special categories, profiling, large scale, AI decisions about people).
- why: Required by GDPR for high-risk processing and surfaces design changes early.

## 09.5 No personal data in logs, tests or analytics
- applies: data>=personal
- rule: Mask or pseudonymise personal data in logs, error reports, analytics and non-production environments.
- why: Logs and test copies are frequent, unnoticed breach sources.

## 09.6 Data residency and processors
- applies: data>=personal AND deployment in (cloud, paas)
- rule: Know where personal data is stored and processed; prefer EU regions; have a data processing agreement with every processor; document any transfers outside the EEA.
- why: International transfers and unvetted processors are common compliance gaps.

## 09.7 Breach and incident readiness (GDPR, NIS2)
- applies: data>=personal OR regulation has nis2
- rule: Maintain an incident response procedure that can meet notification deadlines (GDPR: notify the authority within 72 hours where feasible, unless the breach is unlikely to result in a risk to people; NIS2, for in-scope entities: 24-hour early warning, 72-hour notification, final report within one month).
- why: The deadlines are short; the procedure must exist before the incident.

## 09.8 EU AI Act
- applies: regulation has ai-act
- rule: Classify the AI system (prohibited, high-risk, transparency obligations, minimal risk) and record the classification in an ADR. Transparency obligations (Art. 50: tell people they are interacting with AI; mark AI-generated content) apply since 2 August 2026. After the AI Omnibus (Regulation (EU) 2026/1744), high-risk obligations apply from 2 December 2027 for Annex III use cases and 2 August 2028 for AI in Annex I products. Providers and deployers also take measures for staff AI literacy.
- why: Obligations depend on the risk class and the dates; the classification decides what must be built (logging, human oversight, documentation).

## 09.9 Accessibility (European Accessibility Act)
- applies: regulation has accessibility-eaa
- rule: Meet WCAG 2.2 AA (the basis of the European harmonised standard EN 301 549) for in-scope products and services and publish an accessibility statement. Check the exemption for microenterprises providing services.
- why: Legally required for many consumer-facing digital services in the EU.

## 09.10 PII protection techniques
- applies: data>=personal
- rule: Choose the technique per use: masking for display (`j***@gmail.com`, last 4 digits); pseudonymisation or tokenisation for analytics and integrations; field-level encryption for special-category data; anonymisation only when re-identification is truly impossible. Log with an allow-list of safe fields rather than a block-list of PII fields, and redact centrally in the log formatter and the error tracker.
- why: Masked, pseudonymised and tokenised data is still personal data under GDPR; only true anonymisation is not. Allow-lists fail safe when a new PII field appears; block-lists do not.

## 09.11 Cyber Resilience Act readiness
- applies: regulation has cra
- rule: For products with digital elements sold or distributed in the EU: be able to report actively exploited vulnerabilities and severe incidents through ENISA's Single Reporting Platform (24-hour early warning, then follow-up notifications), keep an SBOM per release (08.6) and a coordinated vulnerability disclosure policy (08.10, 17.4). Plan for the full product requirements that apply from 11 December 2027.
- why: CRA reporting obligations have applied since 11 September 2026, also to products already on the market; the clock is short and the process must exist before the incident.

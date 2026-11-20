---
group: Open-source maintainer practices
id: "17"
version: 0.4
reviewed: 2026-11-17
---

# 17 · Open-source maintainer practices

For projects whose source is public. `published` covers what every public repo needs; `community` adds what it takes to accept outside contributions safely and sustainably. A project becomes open source by publishing the code under an open-source licence: there is no registration, but the licence is the declaration, and without one the code is "all rights reserved" even if it is public.

## 17.1 Choose a licence deliberately
- applies: openness>=published
- rule: Pick an OSI-approved licence before the first public commit and put it in `LICENSE`, stated as an SPDX identifier in the package metadata. Permissive (MIT, Apache-2.0) maximises adoption; Apache-2.0 adds an explicit patent grant; weak copyleft (MPL-2.0, LGPL) keeps changes to your files open; strong copyleft (GPL, AGPL) keeps derivatives open (AGPL also covers software offered over a network). Check that every dependency's licence is compatible (01.9). Record the choice in an ADR.
- why: The licence defines who can use the code and how; changing it later needs every contributor's agreement or a CLA.
- alternatives: permissive / weak copyleft / strong copyleft
- choose-when: T17 in ../guides/principle-tensions.md

## 17.2 Audit before going public
- applies: openness>=published AND mode=existing
- rule: Before making an existing repo public, scan the full git history for secrets, credentials, internal hostnames, customer data and personal data; rotate anything found and rewrite or squash history if needed. Remove internal-only docs and links. Confirm the organisation allows the release (ownership, employment contracts).
- why: Making a repo public publishes its entire history, not just the current files.

## 17.3 Community health files
- applies: openness>=published
- rule: Provide README (01.12), LICENSE, `SECURITY.md`, and for community projects `CONTRIBUTING.md` (how to set up, test, propose changes, what gets accepted), `CODE_OF_CONDUCT.md` (e.g. Contributor Covenant) with a real enforcement contact, and issue and PR templates.
- why: These files answer the questions every visitor and contributor has, and platforms surface them automatically.

## 17.4 Private vulnerability reporting
- applies: openness>=published
- rule: `SECURITY.md` states supported versions and how to report a vulnerability privately (enable the platform's private vulnerability reporting, e.g. GitHub security advisories). Acknowledge reports within an agreed time, fix, publish an advisory and credit the reporter.
- why: Without a private channel, vulnerabilities get reported in public issues, before a fix exists.

## 17.5 Contribution provenance: DCO or CLA
- applies: openness=community
- rule: Decide how contributors confirm they have the right to contribute: Developer Certificate of Origin (DCO, a `Signed-off-by` line checked in CI) or a Contributor Licence Agreement (CLA, signed once). Document it in CONTRIBUTING.md and enforce it in CI.
- why: Protects the project and its users from code contributed without the right to do so.
- alternatives: DCO / CLA
- choose-when: T18 in ../guides/principle-tensions.md

## 17.6 Governance and maintainers
- applies: openness=community
- rule: Document how decisions are made and who maintains what (`GOVERNANCE.md`, `MAINTAINERS` or CODEOWNERS): how to become a maintainer, how disagreements are resolved, and what happens if a maintainer leaves. Aim for at least two active maintainers.
- why: Contributors need to know how their work will be judged; a single maintainer is a single point of failure (bus factor 1).

## 17.7 Welcoming contribution workflow
- applies: openness=community
- rule: Label issues for newcomers (`good first issue`, `help wanted`), triage new issues and PRs within an agreed time, give actionable review feedback, and run full CI on forks without exposing secrets (11.12).
- why: Fast, clear responses turn first-time contributors into regular ones; silence drives them away.

## 17.8 Public, predictable releases
- applies: openness>=published
- rule: Use Semantic Versioning strictly (01.5): any breaking change of the public API is a major version. Publish release notes from the changelog (01.6), tag releases, sign artefacts where the ecosystem supports it, and publish through CI with trusted publishing (OIDC) instead of personal tokens.
- why: Users depend on your version numbers to upgrade safely; compromised publishing tokens are a common supply-chain attack.

## 17.9 Public API and deprecation policy
- applies: openness>=published
- rule: Define what the public API is (everything else is internal and may change). Deprecate before removing: warn at runtime or in docs for at least one minor release, document the migration path, and remove only in the next major version.
- why: Users cannot follow your internal discussions; a written policy lets them plan.

## 17.10 Licence and supply-chain transparency
- applies: openness>=published AND stage>=mvp
- rule: Add SPDX licence identifiers to source files (REUSE specification), generate an SBOM per release (08.6), and run the OpenSSF Scorecard; consider the OpenSSF Best Practices badge.
- why: Downstream users and companies need to verify licences and security posture before adopting a project.

## 17.11 Roadmap and support expectations
- applies: openness=community
- rule: Publish a short roadmap or project board and state support expectations plainly (e.g. "best effort, no SLA", supported versions, response times).
- why: Clear expectations prevent frustration on both sides and attract contributors to the work that matters.

## 17.12 Sustainability and regulation
- applies: openness>=published AND stage>=mvp
- rule: Decide how the project is sustained (sponsorship, foundation, company backing) and document it. If a company commercialises the software in the EU, check obligations under the Cyber Resilience Act (vulnerability handling and reporting; a lighter regime applies to open-source stewards).
- why: Unfunded projects burn out their maintainers; regulation treats commercial distribution differently from hobby publication.

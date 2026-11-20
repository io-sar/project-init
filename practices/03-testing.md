---
group: Testing
id: "03"
version: 0.4
reviewed: 2026-11-17
---

# 03 · Testing

Tests are the safety net that lets a team (and Claude) change code with confidence.

## 03.1 Test shape chosen by architecture
- applies: always
- rule: Choose the test shape from ../guides/testing-strategy.md and state it in the testing rules: pyramid (many unit, fewer integration, few E2E) for logic-heavy backends and monoliths; trophy (mostly integration) for UI-heavy frontends; honeycomb (mostly integration and contract) for microservices. Always keep E2E tests few and limited to critical journeys.
- why: Tests should sit where the bugs are: inside the logic for backends, in component behaviour for UIs, in the interactions for services.
- alternatives: pyramid / trophy / honeycomb
- choose-when: T14 in ../guides/principle-tensions.md

## 03.2 Tests with the code
- applies: always
- rule: Every behaviour change ships with tests and every bug fix starts with a failing regression test (the never-skip rule is non-negotiable 15.6). Use TDD (failing test first) for domain logic.
- why: Untested changes are guesses; disabled tests hide real regressions.
- alternatives: test-after
- choose-when: T10 in ../guides/principle-tensions.md; test-after is acceptable for spikes and exploratory UI, but tests still ship before merge

## 03.3 Tests gate merges
- applies: stage>=mvp
- rule: Run the full test suite in CI on every PR; failures block merging.
- why: A test that does not block anything is eventually ignored.

## 03.4 Coverage as a signal
- applies: stage>=mvp
- rule: Track coverage and keep a floor (e.g. 80% on domain logic). Do not write tests only to raise the number.
- why: Low coverage shows risk; chasing 100% produces low-value tests.

## 03.5 Real dependencies in integration tests
- applies: data>=stored
- rule: Run integration tests against real dependencies in containers (database, queue), not mocks of them.
- why: Mocks of a database agree with your assumptions, not with the database.

## 03.6 Contract tests
- applies: architecture=services OR interfaces has public-api
- rule: Verify API contracts with contract tests (consumer-driven or schema-based) in CI.
- why: Catches breaking changes between services before deployment.

## 03.7 Safe test data
- applies: data>=personal
- rule: Use factories or synthetic fixtures. Never use copies of production personal data in tests or local environments.
- why: Test environments are a common source of GDPR breaches.

## 03.8 Performance tests
- applies: scale>=moderate
- rule: Load-test critical paths against agreed latency targets before major releases.
- why: Performance problems found in production are the most expensive kind.

## 03.9 Security tests in the pipeline
- applies: stage>=mvp
- rule: Run static analysis (SAST) and dependency scanning on every PR; add dynamic scanning (DAST) for web apps before production.
- why: Finds known vulnerability patterns automatically and early.

## 03.10 Acceptance tests in Given/When/Then (BDD)
- applies: team>=small
- rule: Write acceptance tests for business rules as Given/When/Then scenarios in the domain's language (see 04.3). Start with plain tests named and structured this way; add a Gherkin toolchain (Cucumber, Behave, Reqnroll...) only if non-technical stakeholders read or write the scenarios.
- why: Shared examples catch misunderstood requirements before code is written; an unread Gherkin layer is pure maintenance cost.
- alternatives: plain developer tests only
- choose-when: T13 in ../guides/principle-tensions.md

## 03.11 Smoke tests after deploy
- applies: stage>=mvp AND deployment!=local
- rule: After every deploy, run a small automated smoke suite on the critical path (app is up, login works, main journey completes) and roll back automatically or alert on failure.
- why: Catches broken deploys in minutes, before users report them.

## 03.12 Positive, negative and boundary cases
- applies: always
- rule: For every behaviour you test, cover the normal case, the invalid inputs (one per equivalence class: empty, wrong type or format, too long, out of range, special characters) and the boundaries (at each limit and just past it). A negative test asserts the specific, clear rejection or error, not just "it didn't crash".
- why: Happy-path tests only prove a feature works when everything goes right; most escaped bugs live in invalid input and edge values.

## 03.13 Failure-path tests for dependencies
- applies: stage>=mvp AND (ai!=none OR interfaces has-any (internal-api, public-api) OR data>=stored)
- rule: For each external dependency (LLM provider, third-party API, database, queue), simulate its failures with fakes or recorded responses: timeout, connection error, rate limit, error response, malformed or schema-invalid output. Assert that the app degrades or fails clearly, retries only where intended (07.2), and never shows keys, stack traces or raw provider errors.
- why: Dependencies fail in production regularly; untested failure paths turn a provider hiccup into a crash or a leak.

## 03.14 Exploratory test sessions
- applies: stage>=mvp AND interfaces has-any (web-ui, public-api)
- rule: Before each release and after large changes, run chartered, time-boxed exploratory sessions ("Explore <area> with <resources or techniques> to discover <risks>", about 60 to 90 minutes, one charter each) and write a short debrief (covered, found, open). Every finding becomes an issue and then an automated regression test (03.2). Include at least one human session for user-experience judgement.
- why: Scripted tests only check the risks someone anticipated; exploration finds the unknown ones, and the debrief and regression tests keep the findings from coming back.

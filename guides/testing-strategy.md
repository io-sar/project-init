# Testing strategy guide

Used by group 03. Decide two things per project: the **shape** (how much of each level) and the **extra test types** the profile needs.

## Test types
| Type | What it checks | Speed | Typical tools (examples) |
|---|---|---|---|
| **Unit** | One function or class, no I/O | ms | the language's test framework |
| **Integration** | A module with its real dependencies (DB, queue) | seconds | test framework + containers |
| **Contract** | Two parties agree on an API or message format | seconds | Pact, schema validation against OpenAPI/AsyncAPI |
| **Component / API** | One service in isolation through its public interface, dependencies stubbed | seconds | HTTP test clients |
| **System / end-to-end (E2E)** | The whole system through the real UI or API, as a user would | minutes | Playwright, Cypress, API scripts |
| **Acceptance (BDD)** | Business rules in Given/When/Then, readable by stakeholders | varies | Cucumber, Behave, Reqnroll; or plain tests named Given/When/Then |
| **Smoke** | The deployed system is alive and its critical path works | seconds | a few E2E or API checks after each deploy |
| **Regression** | A fixed bug stays fixed | any level | a test added with every bug fix |
| **Performance / load** | Latency and throughput under expected and peak load | minutes | k6, Gatling, Locust, JMeter |
| **Security** | Known vulnerability patterns | minutes | SAST, dependency scan, DAST |
| **Accessibility** | WCAG rules in the UI | seconds | axe and similar |
| **Property-based** | Invariants over many generated inputs | seconds | Hypothesis, fast-check, jqwik |
| **Mutation** | Whether tests actually catch bugs (test quality) | slow | Stryker, mutmut, PIT |
| **Evals** | LLM output quality on a fixed set of cases | minutes | see 14.2 |
| **Exploratory / manual** | What scripts miss: usability, odd flows | human | time-boxed sessions |

## Shape: chosen by architecture and interfaces
| Shape | Distribution | Choose when |
|---|---|---|
| **Pyramid** | Many unit, fewer integration, few E2E | Logic-heavy backend, monolith, libraries |
| **Trophy** | Static checks + some unit + **mostly integration** + few E2E | UI-heavy frontends: test components the way users use them |
| **Honeycomb** | Few unit, **mostly integration and contract**, few E2E | Microservices: most bugs live in the interactions between services |

## Extra types switched on by the profile
| Profile signal | Add |
|---|---|
| stage>=mvp | smoke tests after every deploy, regression test per bug |
| architecture=services OR interfaces has public-api | contract tests |
| scale>=moderate | performance / load tests on critical paths |
| interfaces has web-ui | E2E on critical journeys, accessibility checks |
| business rules agreed with non-technical stakeholders, or regulation!=none | acceptance tests in Given/When/Then (BDD) |
| every project | positive, negative and boundary cases (03.12) |
| stage>=mvp with external dependencies | failure-path tests with fakes (03.13) |
| stage>=mvp with a UI or public API | exploratory sessions, human and agent-run (03.14, 15.9) |
| algorithmic or parsing code | property-based tests |
| stage=production, critical domain logic | mutation testing (periodically, not on every PR) |
| ai!=none | evals (14.2) |

## TDD, BDD and DDD: how they relate
- **TDD** (test-driven development) is a developer workflow: write a failing test, make it pass, refactor. Mostly at unit level.
- **BDD** (behaviour-driven development) is about agreeing behaviour with the business in examples (Given/When/Then) and turning them into acceptance tests. It works outside-in: an acceptance test first, then TDD inside.
- **DDD** (domain-driven design) is a design approach, not a testing method. It pairs naturally with BDD: the scenarios use the ubiquitous language of the bounded context.
- Lightweight BDD: name and structure plain tests as Given/When/Then without a Gherkin toolchain. Add Cucumber-style tooling only when stakeholders actually read or write the scenarios; otherwise the extra layer is maintenance with no reader.

## Test design techniques (which cases to write)
| Technique | How | Example |
|---|---|---|
| **Equivalence partitioning** | Group inputs that should behave the same; test one value per group, including every invalid group | Age field: one valid adult, one negative number, one non-number |
| **Boundary value analysis** | Test at each limit and just past it | Valid 1 to 10: test 0, 1, 10, 11 |
| **Negative testing** | Feed what the system must reject: empty, too long, wrong type or format, special characters, wrong state | Empty scenario text, 100 KB text, HTML tags in text |
| **Error guessing** | Use experience of typical bugs | Unicode, time zones, double submit, back button |
| **State transitions** | Test valid and invalid moves between states | Edit after export; regenerate while a call is running |
| **Decision tables** | List combinations of conditions and the expected outcome | Health score thresholds vs escalation level |
| **Failure injection** | Make dependencies fail through fakes | Provider timeout, rate limit, invalid JSON |

Write negative tests that assert the specific, user-safe rejection or error, not just "no crash".

## Exploratory sessions (03.14, 15.9)
Exploratory testing is simultaneous learning, test design and execution. Run it as Session-Based Test Management (Jonathan and James Bach):

1. **Charter:** "Explore <area> with <resources or techniques> to discover <risks>". One mission per session, not a list of test cases.
2. **Time box:** about 60 to 90 minutes, uninterrupted, one charter.
3. **Notes during the session:** what was tried, what looked wrong, questions.
4. **Debrief:** covered, found (each finding with steps to reproduce), open questions, follow-up charters.
5. **Close the loop:** each finding becomes an issue, then an automated regression test.

Useful "tours" (themes for a session): **saboteur** (try to break it on purpose), **all inputs** (every field with odd values), **back-and-forth** (undo, back, refresh, repeat), **first-time user** (no prior knowledge), **long run** (many steps in one session).

Agent-run sessions: safe mode only (demo data or fake clients, no paid calls, no real keys), report without fixing, and keep at least one human session for user-experience judgement.

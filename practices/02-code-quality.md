---
group: Code quality and design
id: "02"
version: 0.4
reviewed: 2026-11-17
---

# 02 · Code quality and design

Code is read far more often than written. These practices keep it cheap to change.

## 02.1 Automated formatting and linting
- applies: always
- rule: Enforce a formatter and linter automatically (pre-commit hook and CI). Do not argue style in reviews; the tool decides.
- why: Removes noise from reviews and keeps diffs focused on behaviour.

## 02.2 Static typing
- applies: always
- note: only where the language has a type system or type checker
- rule: Use type annotations on public functions and run the type checker in CI.
- why: Catches a whole class of bugs before runtime and documents intent.

## 02.3 Small, well-named units
- applies: always
- rule: In code you are writing or already changing: keep functions short and single-purpose, name things for what they mean in the domain, and delete dead code instead of commenting it out. Do not sweep unrelated files.
- why: Small named units are easy to test, review and reuse.

## 02.4 SOLID at the boundaries that matter
- applies: always
- rule: Apply SOLID where code is expected to change or be extended: Single responsibility (one reason to change per class/module); Open/closed (extend by adding code, not editing stable code); Liskov substitution (a subtype works wherever its parent works); Interface segregation (small, focused interfaces); Dependency inversion (depend on abstractions; see 02.6 and 04.2). Prefer composition over inheritance. Do not create an interface that has only one implementation and no test seam.
- why: Keeps long-lived code changeable; applied mechanically it produces over-engineering.
- alternatives: YAGNI / KISS (02.10)
- choose-when: horizon in (grows, splits, high-scale) OR team>=small → full SOLID; stage=prototype OR (horizon=stays-small AND team<=small) → KISS, SOLID only at module boundaries (T1 in ../guides/principle-tensions.md)

## 02.5 Explicit error handling
- applies: always
- rule: Never swallow exceptions. Use domain-specific errors, handle them at boundaries, and log with context.
- why: Silent failures are the hardest bugs to find in production.

## 02.6 Dependency injection at boundaries
- applies: stage>=mvp
- rule: Pass external dependencies (DB, HTTP clients, clock, config) into components instead of creating them inside. Keep domain logic pure.
- why: Makes code testable without real infrastructure and swappable later.

## 02.7 Code review standard
- applies: team>=small
- rule: Every change goes through a PR with a review checklist (correctness, tests, security, readability). Aim for PRs under ~400 changed lines.
- why: Review quality drops sharply on large PRs.

## 02.8 Quality gates
- applies: stage=production
- rule: Fail CI on new complexity or duplication above agreed thresholds.
- why: Prevents slow decay that nobody notices day to day.

## 02.9 Technical debt register
- applies: stage>=mvp
- rule: Track known debt as issues labelled `tech-debt` with impact; schedule a share of every iteration to reduce it.
- why: Visible debt gets managed; invisible debt grows.

## 02.10 YAGNI, KISS and the rule of three
- applies: always
- rule: Build only what current requirements need (YAGNI); choose the simplest design that works (KISS). Tolerate duplication until the third occurrence, then extract an abstraction only if the copies change for the same reason (rule of three / AHA: avoid hasty abstractions).
- why: Wrong abstractions are more expensive than duplication; requirements you guessed rarely arrive as guessed.
- alternatives: SOLID / deliberate abstraction (02.4), strict DRY
- choose-when: always active as a counterweight; dominant when stage=prototype OR horizon=stays-small (T1, T2)

## 02.11 Comments and docstrings
- applies: always
- rule: In code you are writing or already changing, comments explain why, not what: intent, constraints, trade-offs, links to the ADR or issue behind a non-obvious decision. Prefer clearer names over a comment that restates the code. Exported and public APIs have a docstring (purpose, parameters, return, errors) in the language's standard format, so API docs can be generated. `TODO` and `FIXME` include an issue key (`TODO(ABC-123): ...`) when a tracker is used. No commented-out code. Update or delete comments in the same change that makes them wrong.
- why: Code shows what happens; only comments can say why. Outdated comments are worse than none.

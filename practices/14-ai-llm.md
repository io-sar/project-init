---
group: AI / LLM features
id: "14"
version: 0.4
reviewed: 2026-11-17
---

# 14 · AI / LLM features

For projects that call language models or run agents. LLM output is probabilistic and its input can be adversarial.

## 14.1 Treat model input and output as untrusted
- applies: ai!=none
- rule: Defend against prompt injection (OWASP Top 10 for LLM Applications): separate instructions from user and retrieved content, validate and sanitise model output before using it, never execute it blindly.
- why: Any text the model reads can try to give it instructions.

## 14.2 Evals in CI
- applies: ai!=none AND stage>=mvp
- rule: Maintain an evaluation set of representative inputs with expected qualities (golden set, grown from real failures, plus edge and adversarial cases) and run it on every prompt or model change; the PR shows the score difference against main. Choose grading per check from ../guides/llm-evaluation.md: code-based assertions first, model-graded with a rubric where judgement is needed, human review for a sample.
- why: Without evals, a prompt "improvement" can silently break other cases; a score diff turns prompt changes into reviewable changes.

## 14.3 Personal data and models
- applies: ai!=none AND data>=personal
- rule: Send personal data to a model only with a lawful basis, a processor agreement, and verified provider terms on retention and training (use zero-retention options where needed); minimise or pseudonymise first.
- why: Prompts are data processing under GDPR.

## 14.4 Least privilege for agents
- applies: ai=agentic
- rule: Give agents only the tools and permissions they need; require human approval for irreversible or high-impact actions; log every tool call.
- why: An agent that can be manipulated must not be able to do serious damage.

## 14.5 Cost, latency and token budgets
- applies: ai!=none
- rule: Set and monitor budgets for tokens, cost and latency per feature; add caching and limits.
- why: LLM costs scale with usage in ways traditional compute does not.

## 14.6 Pinned models and traceable outputs
- applies: ai!=none
- rule: Pin model versions explicitly and record, for every output where it matters, which prompt version and model produced it. Upgrade models only through the eval gate (14.2).
- why: Makes behaviour changes traceable and reproducible.

## 14.7 Asynchronous patterns for model calls
- applies: ai!=none
- rule: Do not hold a user request open on a long model call. Pick the pattern by duration: interactive answers stream tokens (SSE or WebSocket); tasks over ~30 seconds (agent runs, document processing) run as background jobs with a job ID and status polling, webhook or push; non-urgent bulk work uses the provider's batch API (usually cheaper). Short, bounded calls (e.g. a small classification) may be synchronous with a tight timeout. Every call has a timeout, idempotent retries (07.2) and a concurrency limit that respects the provider's rate limits.
- why: Model latency is long and unpredictable; synchronous waits exhaust workers, hit gateway timeouts and give users a frozen screen.
- alternatives: synchronous request/response
- choose-when: T9 in ../guides/principle-tensions.md

## 14.8 Prompts as code
- applies: ai!=none
- rule: Keep prompts in their own files (templates with named variables), not inline strings scattered in code. Each prompt has an ID and version, an owner, the model it was tuned for, and its eval set. Prompt changes go through PRs like code, with the eval diff attached (14.2).
- why: Prompts are product logic; scattered inline strings cannot be reviewed, tested or rolled back.

## 14.9 Structured outputs
- applies: ai!=none
- rule: When code consumes model output, request structured output (JSON schema / tool use) and validate it against the schema; on failure, retry once with the validation error, then fall back. Never parse free text with regexes.
- why: Schema validation turns vague failures into detectable, testable ones.

## 14.10 Production feedback loop
- applies: ai!=none AND stage>=mvp
- rule: In production, log prompt ID/version, model, latency, tokens and cost per call (without personal data, 09.5); collect user feedback (thumbs, corrections) and run sampled online evals. Every confirmed failure becomes a case in the eval set. Re-run the full eval set before any model upgrade.
- why: Real users find failures the eval set does not have; the loop makes the eval set and the prompts improve continuously.

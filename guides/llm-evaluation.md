# LLM prompt testing and improvement guide

Used by group 14 when ai!=none. Goal: prompt and model changes are measured, reviewed and reversible.

## The improvement loop
1. **Define success** per prompt: what a good output must contain, must not contain, format, tone, latency and cost budget.
2. **Build the eval set**: 20–50 representative cases to start; add edge cases, adversarial cases (prompt injection, off-topic, empty input) and every real failure from production (14.10).
3. **Baseline**: run the eval set on the current prompt and model; store the scores.
4. **Change one thing** (wording, examples, structure, model, temperature) on a branch.
5. **Compare**: run the eval set; the PR shows the score difference per check and per case, plus cost and latency changes.
6. **Ship or revert** based on the diff, never on a few manual tries.
7. **Monitor** in production and feed failures back into step 2.

## Grading methods (cheapest and most reliable first)
| Method | Use for | Notes |
|---|---|---|
| **Code-based assertions** | Format, valid JSON/schema, required fields, contains/not-contains, length, exact match for classification | Fast, free, deterministic. Use wherever possible. |
| **Similarity** | Answers with a known reference | Embedding or text similarity with a threshold; brittle for open-ended text. |
| **Model-graded (LLM-as-judge)** | Tone, helpfulness, faithfulness to sources, rubric-based quality | Give the judge a specific rubric and ask for reasoning before the score; calibrate it against human labels on a sample; use a strong model as judge. |
| **Pairwise comparison** | Choosing between two prompt versions | Ask which output is better against the rubric; swap the order to avoid position bias. |
| **Human review** | Calibration, high-stakes domains, final sign-off | Review a sample each release; disagreements improve the rubric. |

## Prompt improvement techniques to try (one at a time)
- Clear role and task, explicit constraints and output format
- A few well-chosen examples (including a tricky one)
- Separate instructions from data with clear delimiters (also helps against injection, 14.1)
- Ask for reasoning before the answer where quality matters
- Split one large prompt into a chain of smaller steps
- Structured output with a schema (14.9)
- Provider prompt-improvement and evaluation tooling, where available

## Tools (examples, choose with tool-selection.md)
- Open source, runs in CI: promptfoo, DeepEval, Ragas (for retrieval-augmented generation)
- Platforms with tracing, datasets and online evals: LangSmith, Braintrust, Langfuse (open source, self-hostable)
- Plain test framework + a small eval harness is enough to start.

## Metrics to track per prompt version
Pass rate per check · cost per call · latency p50/p95 · failure categories · user feedback rate.

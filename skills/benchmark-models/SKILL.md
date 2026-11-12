---
name: benchmark-models
description: Select or compare AI models for a specific prompt using current official model guidance and, when the user explicitly approves paid calls, a same-input benchmark. Use for questions about which model, provider, or reasoning effort best fits a prompt; do not use for generic prompt rewriting.
license: MIT
metadata:
  adapted-from: https://github.com/garrytan/gstack/tree/main/benchmark-models
---

# Benchmark Models

Recommend the lightest model that meets the user's quality bar. Treat model selection as task-specific: never claim that one model is universally best.

## Choose a mode

- **Recommendation mode** is the default. Analyze the prompt and current official model documentation without sending the prompt to additional models.
- **Empirical mode** runs the same prompt through two or more models. Use it only when the user explicitly requests a benchmark and approves the selected providers, credentials, expected cost, and external data sharing.

## Recommendation mode

1. Preserve the user's prompt. Identify its modality, task type, ambiguity, tool needs, context size, failure cost, latency target, and cost priority. Ask only for a missing choice that would materially change the result.
2. Check current first-party documentation for the models actually available in the user's product or API account. Do not rely on a bundled model list for a current recommendation.
3. Shortlist no more than three candidates. Match reasoning effort separately from model capability.
4. Read [the evaluation rubric](references/evaluation-rubric.md) and define acceptance criteria that reflect the prompt's real use.
5. Recommend one model and reasoning effort, name the runner-up, and explain the quality/cost/latency trade-off. State any unverified availability, pricing, or limit.

## Empirical mode

Before any model call, show the candidates and execution method. Obtain explicit approval when calls can incur cost, disclose the prompt or workspace data to another provider, or require credentials.

After approval:

1. Verify each provider or CLI is available using a help, version, authentication-status, or dry-run command that does not submit the prompt. Never print tokens or secrets.
2. Send the same prompt, attachments, system instructions, tool access, and reasoning effort to every candidate where the interfaces allow it. Record unavoidable differences.
3. Capture the model identifier, completion status, latency, token usage, and reported cost. Do not estimate cost when the provider does not expose enough information.
4. Score outputs using [the evaluation rubric](references/evaluation-rubric.md). Prefer deterministic checks, then human review, then an optional model judge calibrated against human labels.
5. Report fastest, lowest reported cost, highest quality, and best overall for the stated priority. Call out errors, unavailable providers, and incomparable settings.

Do not install provider software, change account settings, create API keys, enable billing, or save benchmark results unless the user asks. Keep prompt contents and outputs out of the repository unless the user explicitly chooses a project path.

## Output

Include:

- **Recommendation:** model/provider and reasoning effort.
- **Why:** task characteristics and acceptance criteria that drove the choice.
- **Trade-off:** the strongest alternative and what it improves or sacrifices.
- **Evidence:** official documentation or benchmark observations, clearly distinguished.
- **Uncertainty:** availability, pricing, limits, missing providers, or non-equivalent settings.

This workflow is adapted from gstack's MIT-licensed `benchmark-models` concept. See [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES).

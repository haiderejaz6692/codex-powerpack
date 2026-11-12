---
name: token-saver
description: Reduce context use when working with large spreadsheets, documents, logs, JSON, search results, or long-running analyses while preserving instructions, errors, formulas, evidence, and decisions. Use when the user asks to save tokens or the task would otherwise load substantial irrelevant content; not for ordinary short requests.
---

# Token Saver

Minimize the information loaded into the active context without weakening correctness, traceability, or user control. This skill is an instruction workflow, not a compressor or background service.

## Build the smallest useful working set

1. Inspect filenames, sizes, schemas, worksheet names, headings, and other cheap structure before reading full contents.
2. Identify the decision, output, time range, entities, measures, and evidence needed for the request.
3. Read only the relevant files, sheets, columns, rows, sections, references, or date ranges.
4. Prefer deterministic local filtering, aggregation, search, and calculation over pasting raw source material into the conversation.
5. Reuse validated intermediate results instead of reopening or retransmitting the same source.

For large tables, preserve the source file and create a compact derived table at the required grain. Record source paths, filters, row counts, join keys, units, periods, and formulas so the result remains auditable.

## Preserve high-value information

Never remove or paraphrase away:

- the user's current instructions, constraints, approvals, and corrections;
- errors, warnings, failed checks, stack traces, and anomalous values relevant to the task;
- exact formulas, commands, paths, identifiers, dates, currencies, units, and comparison bases when their precision matters;
- assumptions, unresolved questions, decisions, evidence locations, and verification results.

Use representative samples only for discovery. Compute final conclusions from the complete relevant dataset, not from a sample, unless the user explicitly requests sampling.

## Keep outputs proportionate

Lead with the requested result and the few facts needed to act on it. Put extensive supporting tables in an artifact when the user requests a durable deliverable; do not duplicate the same material in chat. Expand detail when it affects a decision, exposes uncertainty, or is requested.

Do not claim a token or cost saving unless the environment exposes measured before-and-after counts. Otherwise describe the method as context reduction, not a quantified saving.

## Boundaries

- Do not modify source files merely to shorten them.
- Do not send source content to another model, compression service, telemetry endpoint, or external provider.
- Do not install packages, wrappers, proxies, hooks, or background processes.
- Do not omit evidence, tests, privacy safeguards, or verification to reduce context.
- Do not treat a compact summary as authoritative after the source changes; refresh the affected derivation.

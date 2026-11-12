# Model comparison rubric

Use this rubric only after reading the actual prompt. Replace irrelevant dimensions and define concrete pass conditions before comparing outputs.

## 1. Must-pass constraints

Mark an output ineligible for “best overall” when it fails a non-negotiable requirement such as:

- incorrect or fabricated facts;
- missing requested files, fields, citations, or actions;
- unsafe or unauthorized behavior;
- invalid syntax, schema, build, or tests;
- failure to preserve supplied data or unrelated project content.

Verify with deterministic checks whenever possible. For code, run the relevant tests. For computer-use tasks, inspect the saved external state. For structured output, parse it.

## 2. Quality dimensions

Score each relevant dimension from 0 to 5 and record one sentence of evidence.

| Dimension | Question |
|---|---|
| Correctness | Are claims, calculations, code, and actions accurate? |
| Instruction following | Did the result satisfy every explicit requirement and boundary? |
| Completeness | Is anything necessary for the requested outcome missing? |
| Judgment | Did the model make sound trade-offs under ambiguity? |
| Usability | Is the output clear, maintainable, and ready for its intended audience? |
| Tool reliability | Were tool choices, arguments, and completion claims accurate? |

Do not reward verbosity by itself. A shorter answer can be better when it meets the same acceptance criteria.

## 3. Operational measurements

Record these separately from quality:

- end-to-end latency;
- input, output, reasoning, and cached tokens when reported;
- provider-reported cost when available;
- retries, timeouts, rate limits, or failed tool calls;
- time required for a human to review or repair the result.

## 4. Comparison method

Prefer pairwise comparison or pass/fail decisions over an unconstrained numeric impression. When using a model judge, randomize or swap response order and check agreement against at least one human-reviewed example. Never let the judge see provider names when they are not relevant.

## 5. Result table

```text
Candidate | Must-pass | Quality evidence | Latency | Reported cost | Repair needed
```

Choose “best overall” according to the user's stated priority. If candidates are not comparable because tools, context, or reasoning settings differed, report that limitation instead of forcing a winner.

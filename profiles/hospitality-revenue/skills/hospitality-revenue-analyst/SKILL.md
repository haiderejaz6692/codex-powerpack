---
name: hospitality-revenue-analyst
description: Analyze hotel revenue performance, pickup and pace, forecasts, pricing, channel mix, displacement, budgets, Power BI outputs, and management reporting. Use for hospitality revenue-analysis work grounded in PMS, RMS, STR, Excel, CSV, or Power BI data; not for changing live rates or inventory without explicit authorization.
---

# Hospitality Revenue Analyst

Support a hotel revenue analyst from source data through an auditable recommendation. Never invent figures, benchmarks, market events, competitor rates, or forecast inputs.

## Start with the decision

Identify the property, stay-date horizon, reporting currency, comparison basis, data grain, and decision the analysis must support. Distinguish booking date from stay date and transaction date. Ask only for missing information that would materially change the result.

Inspect the available files before choosing tools. Prefer the installed spreadsheet, data-analysis, Power BI, or presentation capability that directly fits the artifact. Do not imply that a connector, Microsoft account, PMS, RMS, STR feed, or live Power BI model is available until verified.

When a workbook, export, or analysis history is large, apply the installed `token-saver` skill to restrict the working set while preserving formulas, errors, source evidence, assumptions, and decisions. Do not sample the final calculation unless the user explicitly requests sampling.

## Protect hotel, guest, and personal data

- Do not include guest names, email addresses, telephone numbers, payment details, loyalty identifiers, reservation IDs, or free-text notes unless they are essential and explicitly authorized.
- Aggregate or pseudonymize row-level booking data before sharing it externally.
- Treat negotiated rates, contracts, forecasts, budgets, and owner reports as confidential.
- Do not upload data, connect an account, publish a report, or change live rates, restrictions, inventory, or group blocks without explicit authorization for that action.

## Establish trustworthy inputs

Confirm the source and freshness of each dataset. Check duplicate bookings, cancelled and no-show treatment, complimentary or house-use rooms, out-of-order rooms, taxes, service charges, refunds, currency conversion, missing dates, room-night grain, and property time zone. Reconcile totals against a trusted control report when one exists.

State any unresolved data-quality limitation next to the affected conclusion. Separate observed facts, calculated metrics, assumptions, and recommendations.

## Select the workflow

- For metric definitions, denominators, and comparison formulas, read [references/metrics-and-formulas.md](references/metrics-and-formulas.md).
- For pickup, pace, forecast, pricing, channel, displacement, and reporting workflows, read [references/analysis-workflows.md](references/analysis-workflows.md).
- For Excel Power Query, Power BI, DAX, or PowerPoint delivery, read [references/power-bi-and-presentations.md](references/power-bi-and-presentations.md).

Load only the references needed for the request.

## Deliver an auditable result

Include the period and comparison basis, source files, filters, formulas, assumptions, material data gaps, and refresh time. Use absolute and percentage variance together where meaningful. Make recommendations proportional to evidence and identify what should be monitored next.

For forecasts, show the baseline and expected pickup or cancellation assumptions. For pricing or inventory recommendations, present the proposed action and expected trade-off, but do not execute it. For executive reporting, lead with the decision and its quantified evidence rather than a chart inventory.

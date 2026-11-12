# Power Query, Power BI, and presentations

## Tool routing

- Use an installed spreadsheet capability for Excel or CSV inspection, formulas, pivot tables, charts, and workbook delivery.
- Use the installed data-analysis capabilities for data quality, KPI design, diagnostics, forecasting, and durable reports.
- Use an installed presentation capability for PowerPoint creation and visual verification.
- Use Microsoft Fabric or Power BI skills only when they are actually installed and their required authentication or MCP connection is available.

Installation of this skill does not grant access to Microsoft Fabric, Power BI Service, a PMS, an RMS, STR, or any other hotel system.

## Power Query

Distinguish Excel or Power BI Desktop Power Query from Fabric Dataflows Gen2. Preserve a reproducible query chain: source, type normalization, filtering, joins, calculated fields, and final schema. Avoid embedding credentials, personal paths, or secrets in M. Parameterize file locations and environment-specific identifiers when practical.

Validate join keys and row counts before and after merges. Detect many-to-many expansion, locale-dependent dates or decimals, silent type coercion, missing values, and schema drift. Keep raw input queries separate from business-rule transformations.

## Power BI

Prefer a star schema with explicit measures, a conformed date dimension, documented relationships, and stable business definitions. Recompute hospitality ratios from their component measures rather than averaging percentages.

Treat `.pbix` as a binary delivery format. For source-controlled editing, prefer supported PBIP/PBIR/TMDL artifacts or a verified modelling connection. Do not claim a report was changed merely because DAX or M text was drafted.

Before publishing or refreshing, verify credentials, gateway or cloud connection, privacy levels, workspace and item identity, row-level security, refresh behavior, and stakeholder authorization. Publishing, rebinding, deleting, or changing a live model is a separate state-changing action requiring explicit approval.

Useful report pages for a hotel revenue audience often include:

1. Executive performance: revenue, occupancy, ADR, RevPAR, budget and prior-year variance.
2. Pace and forecast: OTB, pickup, forecast by stay date, lead time, and segment.
3. Segment and channel: mix, net ADR, cancellation behavior, and contribution.
4. Calendar or exceptions: dates requiring pricing, inventory, group, or operational review.

Choose pages from the decision need; do not add all pages by default.

## PowerPoint and management communication

Use an evidence-first narrative:

1. What changed and over which period.
2. Why the evidence indicates it changed.
3. What happens if no action is taken.
4. Recommended action, quantified trade-off, owner, and review date.

Keep definitions, source notes, refresh time, and important assumptions visible. Use charts for trends and comparisons, tables for exact operational decisions, and annotations for exceptional dates. Avoid decorative visuals that obscure scale or variance.

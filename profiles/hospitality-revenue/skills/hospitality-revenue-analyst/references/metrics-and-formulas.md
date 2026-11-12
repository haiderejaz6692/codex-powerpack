# Metrics and formulas

Use the property's documented accounting and STR conventions when they differ from these baseline definitions. Always label the numerator, denominator, period, currency, and inclusion rules.

## Core room metrics

| Metric | Baseline formula | Important checks |
|---|---|---|
| Available room nights | sellable rooms × nights | Explain treatment of out-of-order and house-use rooms. |
| Occupancy | rooms sold ÷ available room nights | Keep percentage and room-night variance together. |
| ADR | room revenue ÷ rooms sold | State treatment of packages, taxes, comps, no-shows, and day use. |
| RevPAR | room revenue ÷ available room nights | Cross-check against ADR × occupancy. |
| TRevPAR | total operating revenue ÷ available room nights | State included departments and gross/net treatment. |
| GOPPAR | gross operating profit ÷ available room nights | Use the property's approved GOP definition and accounting period. |
| Net ADR | (room revenue − defined distribution costs) ÷ rooms sold | Name which commissions, transaction fees, loyalty costs, and media costs are included. |
| Average length of stay | room nights ÷ bookings | Exclude cancellations consistently. |
| Cancellation rate | cancelled bookings ÷ eligible bookings | Define booking cohort and observation window to avoid incomplete recent cohorts. |
| No-show rate | no-show bookings ÷ confirmed arrivals due | Use arrival date, not booking creation date. |

Do not average property-level ADR, occupancy, or RevPAR percentages without appropriate weighting. Recompute ratios from summed numerators and denominators.

## Variance and index measures

- Absolute variance = actual − comparison.
- Percentage variance = (actual − comparison) ÷ comparison. Mark zero or missing comparison values as not meaningful rather than forcing a percentage.
- Revenue Generation Index = property RevPAR ÷ comp-set RevPAR × 100.
- Average Rate Index = property ADR ÷ comp-set ADR × 100.
- Market Penetration Index = property occupancy ÷ comp-set occupancy × 100.

Use STLY only when the compared dates are genuinely aligned. Call out weekday, holiday, event, leap-year, renovation, inventory, or reporting-rule differences.

## Pickup, pace, and forecast

- Pickup for a stay period is the change in on-the-books rooms or revenue between two snapshot dates, after consistently accounting for cancellations and modifications.
- Pace compares on-the-books position at equal lead time, such as 14 days before arrival this year versus 14 days before the aligned comparison stay date.
- A transparent rooms forecast can start with `current OTB + expected net pickup`, where net pickup incorporates expected new bookings, cancellations, no-shows, and wash.

Build pickup curves by stay date, lead-time bucket, segment, room type, and channel only when sample size supports that detail. Avoid applying a high-demand-event curve to normal dates.

## Forecast accuracy

Use at least one scale-aware error measure and retain the forecast vintage:

- Error = actual − forecast.
- Absolute error = |actual − forecast|.
- WAPE = sum absolute errors ÷ sum actuals, when aggregate actual is non-zero.
- Bias = sum errors ÷ number of observations, with sign convention stated.

MAPE is unstable when actual values are zero or very small. Do not use it blindly for low-volume segments.

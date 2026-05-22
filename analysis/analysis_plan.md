# Analysis Plan

## Business Question

Which customer-category opportunities should the account team bring into the next customer business review, and which data issues must be resolved before the recommendation is trusted?

## Inputs

- Syndicated-style weekly POS and share metrics.
- Retailer direct scan units and panel repeat rate.
- Distributor shipment, fill-rate, inventory, PO, and service-level metrics.
- Promotion calendar lift and compliance signals.
- Stakeholder request backlog.
- Power BI refresh, data quality, adoption, certification, and RLS signals.
- Semantic measure definitions and test coverage.

## Method

1. Aggregate POS, syndicated share, competitor share, ACV distribution, and category growth at the customer-category grain.
2. Join shipment and service-level data to identify opportunities blocked by fill rate or inventory constraints.
3. Join promotion lift and compliance to distinguish a demand problem from an execution problem.
4. Score each customer-category row using ACV gap, competitive share gap, fill-rate gap, promotion lift gap, category growth, confidence, and margin-weighted upside.
5. Build a data trust queue from freshness, failed record volume, status, and severity.
6. Convert top opportunities into a customer reporting package with meeting date, slide readiness, business-review theme, and open stakeholder asks.

## Output

- `analysis/outputs/opportunity_queue.csv`
- `analysis/outputs/data_trust_queue.csv`
- `analysis/outputs/reporting_package.csv`
- `analysis/outputs/summary.json`

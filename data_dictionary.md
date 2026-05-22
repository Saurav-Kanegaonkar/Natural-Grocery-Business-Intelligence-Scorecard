# Data Dictionary

| Table | Grain | Purpose |
|---|---|---|
| `customers.csv` | customer account | Account, channel, banner count, store count, region, and planning owner. |
| `categories.csv` | category | Natural grocery category, department, margin rate, and ACV benchmark. |
| `skus.csv` | SKU | Item attributes, category, case pack, base price, and margin rate. |
| `weekly_pos.csv` | customer x SKU x week | POS dollars, units, price, promotion flag, ACV distribution, velocity, syndicated share, competitor share, growth, retailer scans, and panel repeat rate. |
| `distributor_shipments.csv` | customer x SKU x week | Ordered cases, shipped cases, fill rate, on-hand cases, PO count, service level, and spoilage risk. |
| `promotion_calendar.csv` | promotion event | Planned lift, actual lift, merchandising support, compliance, and funding rate. |
| `data_quality_checks.csv` | source check | Source system, table, check type, severity, status, freshness, failed records, owner, and recommended fix. |
| `stakeholder_requests.csv` | request | Ad hoc analysis, dashboard, slide, data issue, metric definition, and planning requests. |
| `power_bi_assets.csv` | BI asset | Workspace, audience, cadence, refresh success, quality, adoption, certification, and RLS need. |
| `semantic_measures.csv` | metric definition | DAX-style pattern, grain, definition, certification, and test coverage. |
| `analysis/outputs/opportunity_queue.csv` | customer x category | Ranked category opportunities with ACV, share, fill-rate, promotion, confidence, and upside metrics. |
| `analysis/outputs/data_trust_queue.csv` | source check | Lowest-trust data checks for remediation before publishing reports. |
| `analysis/outputs/reporting_package.csv` | customer account | Business review theme, top categories, open asks, slide readiness, and next meeting date. |

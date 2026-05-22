# DAX Measure Catalog

These examples document the semantic layer expected behind the interactive console.

## Net Sales

```DAX
Net Sales = SUM(weekly_pos[sales_dollars])
```

Business definition: retail POS dollars after promoted price effects.

## ACV Distribution Gap

```DAX
ACV Distribution Gap =
MAX(categories[target_acv_pct]) - AVERAGE(weekly_pos[acv_distribution_pct])
```

Business definition: points of distribution still needed versus the category benchmark.

## Fill Rate Risk

```DAX
Fill Rate Risk =
1 - DIVIDE(SUM(distributor_shipments[shipped_cases]), SUM(distributor_shipments[ordered_cases]))
```

Business definition: unfilled ordered cases as a share of ordered cases.

## Promotion Lift Attainment

```DAX
Promotion Lift Attainment =
DIVIDE(AVERAGE(promotion_calendar[actual_lift_pct]), AVERAGE(promotion_calendar[planned_lift_pct]))
```

Business definition: actual promotion lift versus planned lift.

## Source Trust Score

```DAX
Source Trust Score =
100 - [Freshness Penalty] - [Failed Record Penalty] - [SLA Penalty]
```

Business definition: composite confidence score used before publishing a customer business review.

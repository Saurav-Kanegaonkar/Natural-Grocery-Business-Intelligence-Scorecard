import csv
import json
import math
import random
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "analysis" / "outputs"
SRC = ROOT / "src"

random.seed(29256)


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def money(value):
    return round(value, 2)


customers = [
    {
        "customer_id": "CUST01",
        "customer_name": "Central Market Group",
        "channel": "Conventional grocery",
        "banners": 7,
        "stores": 1285,
        "region": "Central",
        "planning_owner": "Customer planning",
    },
    {
        "customer_id": "CUST02",
        "customer_name": "Sproutline Natural Markets",
        "channel": "Natural grocery",
        "banners": 1,
        "stores": 424,
        "region": "West",
        "planning_owner": "Natural channel",
    },
    {
        "customer_id": "CUST03",
        "customer_name": "Northstar Independent Co-op",
        "channel": "Independent grocery",
        "banners": 18,
        "stores": 612,
        "region": "North",
        "planning_owner": "Independent accounts",
    },
    {
        "customer_id": "CUST04",
        "customer_name": "Fresh Table Supermarkets",
        "channel": "Regional grocery",
        "banners": 3,
        "stores": 286,
        "region": "Southeast",
        "planning_owner": "Regional accounts",
    },
    {
        "customer_id": "CUST05",
        "customer_name": "Urban Pantry Express",
        "channel": "Small format",
        "banners": 2,
        "stores": 338,
        "region": "Midwest",
        "planning_owner": "Emerging formats",
    },
]

categories = [
    {
        "category_id": "CAT01",
        "category": "Functional Beverages",
        "department": "Refrigerated",
        "gross_margin_pct": 0.34,
        "target_acv_pct": 88,
    },
    {
        "category_id": "CAT02",
        "category": "Better-for-You Snacks",
        "department": "Grocery",
        "gross_margin_pct": 0.31,
        "target_acv_pct": 90,
    },
    {
        "category_id": "CAT03",
        "category": "Plant-Based Meals",
        "department": "Frozen",
        "gross_margin_pct": 0.29,
        "target_acv_pct": 84,
    },
    {
        "category_id": "CAT04",
        "category": "Natural Personal Care",
        "department": "Wellness",
        "gross_margin_pct": 0.37,
        "target_acv_pct": 80,
    },
    {
        "category_id": "CAT05",
        "category": "Organic Pantry Staples",
        "department": "Grocery",
        "gross_margin_pct": 0.25,
        "target_acv_pct": 92,
    },
    {
        "category_id": "CAT06",
        "category": "Fresh Specialty Cheese",
        "department": "Fresh",
        "gross_margin_pct": 0.33,
        "target_acv_pct": 76,
    },
]

attributes = [
    "organic",
    "plant based",
    "low sugar",
    "high protein",
    "regenerative",
    "gluten free",
    "upcycled",
    "local origin",
]

skus = []
for category in categories:
    for i in range(1, 7):
        sku_id = f"{category['category_id']}-SKU{i:02d}"
        skus.append(
            {
                "sku_id": sku_id,
                "sku_name": f"{category['category'].split()[0]} Item {i}",
                "category_id": category["category_id"],
                "category": category["category"],
                "department": category["department"],
                "attribute": random.choice(attributes),
                "base_price": round(random.uniform(3.99, 12.49), 2),
                "case_pack": random.choice([6, 8, 12, 24]),
                "gross_margin_pct": category["gross_margin_pct"],
            }
        )

write_csv(DATA / "customers.csv", customers, list(customers[0].keys()))
write_csv(DATA / "categories.csv", categories, list(categories[0].keys()))
write_csv(DATA / "skus.csv", skus, list(skus[0].keys()))

weeks = [date(2025, 10, 6) + timedelta(days=7 * i) for i in range(26)]
weekly_pos = []
shipments = []
promotions = []

customer_bias = {
    "CUST01": 1.25,
    "CUST02": 1.06,
    "CUST03": 0.82,
    "CUST04": 0.93,
    "CUST05": 0.62,
}
category_growth = {
    "CAT01": 0.14,
    "CAT02": 0.08,
    "CAT03": 0.06,
    "CAT04": 0.04,
    "CAT05": 0.02,
    "CAT06": 0.09,
}

for week_index, week in enumerate(weeks):
    seasonality = 1 + 0.08 * math.sin(week_index / 26 * math.pi * 2)
    for customer in customers:
        for sku in skus:
            category = next(c for c in categories if c["category_id"] == sku["category_id"])
            promo_flag = 1 if random.random() < 0.18 else 0
            promo_lift = random.uniform(1.08, 1.42) if promo_flag else 1
            base_units = random.uniform(40, 165) * customer_bias[customer["customer_id"]] * seasonality
            trend = 1 + category_growth[sku["category_id"]] * week_index / 26
            units = max(1, int(base_units * trend * promo_lift * random.uniform(0.78, 1.18)))
            avg_price = sku["base_price"] * (random.uniform(0.82, 0.93) if promo_flag else random.uniform(0.96, 1.04))
            sales = units * avg_price
            acv = max(42, min(98, random.gauss(category["target_acv_pct"] - random.uniform(0, 9), 6)))
            comp_share = max(12, min(48, random.gauss(28, 7)))
            syndicated_share = max(8, min(52, comp_share + random.gauss(2.2, 4)))
            category_growth_pct = round(category_growth[sku["category_id"]] * 100 + random.gauss(0, 2.8), 1)
            retailer_scan_units = max(1, int(units * random.uniform(0.92, 1.08)))
            panel_repeat_rate = max(8, min(64, random.gauss(31, 8)))
            weekly_pos.append(
                {
                    "week_start": week.isoformat(),
                    "customer_id": customer["customer_id"],
                    "customer_name": customer["customer_name"],
                    "sku_id": sku["sku_id"],
                    "category_id": sku["category_id"],
                    "category": sku["category"],
                    "sales_dollars": money(sales),
                    "units": units,
                    "avg_price": round(avg_price, 2),
                    "promo_flag": promo_flag,
                    "acv_distribution_pct": round(acv, 1),
                    "velocity_units_per_store": round(units / max(1, customer["stores"]) * 100, 2),
                    "syndicated_share_pct": round(syndicated_share, 1),
                    "competitor_share_pct": round(comp_share, 1),
                    "category_growth_pct": category_growth_pct,
                    "retailer_scan_units": retailer_scan_units,
                    "panel_repeat_rate_pct": round(panel_repeat_rate, 1),
                }
            )
            ordered_cases = max(1, int(units / sku["case_pack"] * random.uniform(0.9, 1.18)))
            service_hit = random.random()
            fill_rate = random.uniform(0.91, 0.99)
            if service_hit < 0.12:
                fill_rate = random.uniform(0.72, 0.89)
            shipped_cases = int(ordered_cases * fill_rate)
            on_hand = max(0, int(random.gauss(ordered_cases * 0.45, max(2, ordered_cases * 0.18))))
            shipments.append(
                {
                    "week_start": week.isoformat(),
                    "customer_id": customer["customer_id"],
                    "customer_name": customer["customer_name"],
                    "sku_id": sku["sku_id"],
                    "category": sku["category"],
                    "ordered_cases": ordered_cases,
                    "shipped_cases": shipped_cases,
                    "fill_rate_pct": round(fill_rate * 100, 1),
                    "on_hand_cases": on_hand,
                    "inbound_po_count": random.randint(0, 4),
                    "dc_service_level_pct": round(max(74, min(99.8, random.gauss(94, 4.8))), 1),
                    "spoilage_risk_pct": round(max(0.5, min(12, random.gauss(3.2, 1.8))), 1),
                }
            )
            if promo_flag and random.random() < 0.72:
                promotions.append(
                    {
                        "promo_id": f"PROMO-{len(promotions)+1:04d}",
                        "customer_id": customer["customer_id"],
                        "customer_name": customer["customer_name"],
                        "sku_id": sku["sku_id"],
                        "category": sku["category"],
                        "week_start": week.isoformat(),
                        "planned_lift_pct": round(random.uniform(10, 38), 1),
                        "actual_lift_pct": round(random.uniform(4, 34), 1),
                        "feature_display": random.choice(["Feature", "Display", "Feature and display", "Digital only"]),
                        "compliance_pct": round(max(42, min(99, random.gauss(78, 13))), 1),
                        "funding_rate_pct": round(random.uniform(6, 18), 1),
                    }
                )

write_csv(DATA / "weekly_pos.csv", weekly_pos, list(weekly_pos[0].keys()))
write_csv(DATA / "distributor_shipments.csv", shipments, list(shipments[0].keys()))
write_csv(DATA / "promotion_calendar.csv", promotions, list(promotions[0].keys()))

quality_checks = []
sources = [
    ("Syndicated POS", "weekly_pos", "Freshness"),
    ("Retailer direct POS", "weekly_pos", "Scan reconciliation"),
    ("Distributor shipment ERP", "distributor_shipments", "Order to shipment match"),
    ("Promotion calendar", "promotion_calendar", "Promotion join coverage"),
    ("Item master", "skus", "Hierarchy completeness"),
    ("Planning request tracker", "stakeholder_requests", "Requirement clarity"),
    ("Power BI service", "power_bi_assets", "Refresh SLA"),
]
for i in range(1, 85):
    source, table, check_type = random.choice(sources)
    severity = random.choices(["Low", "Medium", "High", "Critical"], weights=[34, 35, 23, 8])[0]
    status = random.choices(["Pass", "Watch", "Fail"], weights=[58, 27, 15])[0]
    failed_records = 0 if status == "Pass" else random.randint(12, 920)
    freshness = random.randint(4, 72)
    quality_checks.append(
        {
            "check_id": f"DQ{i:03d}",
            "source_system": source,
            "table_name": table,
            "check_type": check_type,
            "severity": severity,
            "status": status,
            "freshness_hours": freshness,
            "failed_records": failed_records,
            "owner": random.choice(["BI analyst", "Data engineering", "Customer planning", "Category manager"]),
            "recommended_fix": random.choice(
                [
                    "Backfill missing week and republish dataset",
                    "Align item hierarchy mapping before business review",
                    "Reconcile retailer scans to distributor shipments",
                    "Clarify stakeholder metric definition",
                    "Patch promotion calendar join key",
                    "Certify measure after peer review",
                ]
            ),
        }
    )

stakeholder_requests = []
request_types = ["Ad hoc analysis", "Dashboard change", "Business review slide", "Data issue", "Metric definition", "Customer planning question"]
for i in range(1, 121):
    impact = random.randint(2, 10)
    urgency = random.randint(1, 10)
    clarity = random.randint(45, 98)
    stakeholder_requests.append(
        {
            "request_id": f"REQ{i:03d}",
            "request_type": random.choice(request_types),
            "customer_id": random.choice(customers)["customer_id"],
            "category": random.choice(categories)["category"],
            "business_question": random.choice(
                [
                    "Where are distribution voids suppressing growth?",
                    "Which promotion is missing expected lift?",
                    "Why do syndicated sales and retailer scans disagree?",
                    "What should go into next customer business review?",
                    "Which SKU needs assortment or supply follow-up?",
                ]
            ),
            "impact_score": impact,
            "urgency_score": urgency,
            "requirement_clarity_pct": clarity,
            "age_days": random.randint(0, 39),
            "status": random.choice(["New", "In progress", "Waiting on data", "Ready for review", "Published"]),
        }
    )

power_bi_assets = []
asset_names = [
    "Customer Business Review",
    "Gap and Void Dashboard",
    "Promotion Performance",
    "Fill Rate and Inventory",
    "Category Share Tracker",
    "Ad Hoc Insights Pack",
    "Supplier Scorecard",
    "Forecasted Sales Potential",
]
for i, asset in enumerate(asset_names, start=1):
    refresh_success = round(random.uniform(84, 99.7), 1)
    data_quality = round(random.uniform(72, 98), 1)
    adoption = random.randint(24, 144)
    power_bi_assets.append(
        {
            "asset_id": f"PBI{i:02d}",
            "asset_name": asset,
            "workspace": random.choice(["Customer analytics", "Category management", "Executive reporting"]),
            "primary_audience": random.choice(["Account team", "Customer planning", "Leadership", "Supplier managers"]),
            "refresh_cadence": random.choice(["Daily", "Weekly", "Twice weekly"]),
            "refresh_success_pct": refresh_success,
            "data_quality_pct": data_quality,
            "monthly_active_users": adoption,
            "certification_status": random.choice(["Certified", "Promoted", "Draft", "Needs review"]),
            "rls_required": random.choice(["Yes", "No"]),
        }
    )

semantic_measures = [
    {
        "measure_name": "Net Sales",
        "grain": "Customer x SKU x week",
        "dax_pattern": "SUM(weekly_pos[sales_dollars])",
        "business_definition": "Retail POS dollars after promoted price effects.",
        "certification_status": "Certified",
        "test_coverage_pct": 94,
    },
    {
        "measure_name": "ACV Distribution Gap",
        "grain": "Customer x category x week",
        "dax_pattern": "MAX(categories[target_acv_pct]) - AVERAGE(weekly_pos[acv_distribution_pct])",
        "business_definition": "Points of distribution still needed versus category benchmark.",
        "certification_status": "Certified",
        "test_coverage_pct": 91,
    },
    {
        "measure_name": "Fill Rate Risk",
        "grain": "Customer x SKU x week",
        "dax_pattern": "1 - DIVIDE(SUM(shipments[shipped_cases]), SUM(shipments[ordered_cases]))",
        "business_definition": "Unfilled ordered cases as a share of ordered cases.",
        "certification_status": "Promoted",
        "test_coverage_pct": 86,
    },
    {
        "measure_name": "Promotion Lift Attainment",
        "grain": "Promotion",
        "dax_pattern": "DIVIDE(AVERAGE(promotions[actual_lift_pct]), AVERAGE(promotions[planned_lift_pct]))",
        "business_definition": "Actual promotion lift versus planned lift.",
        "certification_status": "Needs review",
        "test_coverage_pct": 71,
    },
    {
        "measure_name": "Source Trust Score",
        "grain": "Dataset x refresh",
        "dax_pattern": "100 - [Freshness Penalty] - [Failed Record Penalty] - [SLA Penalty]",
        "business_definition": "Composite confidence score used before publishing a business review.",
        "certification_status": "Draft",
        "test_coverage_pct": 68,
    },
]

write_csv(DATA / "data_quality_checks.csv", quality_checks, list(quality_checks[0].keys()))
write_csv(DATA / "stakeholder_requests.csv", stakeholder_requests, list(stakeholder_requests[0].keys()))
write_csv(DATA / "power_bi_assets.csv", power_bi_assets, list(power_bi_assets[0].keys()))
write_csv(DATA / "semantic_measures.csv", semantic_measures, list(semantic_measures[0].keys()))

pos_summary = defaultdict(lambda: defaultdict(float))
ship_summary = defaultdict(lambda: defaultdict(float))
promo_summary = defaultdict(lambda: defaultdict(float))

for row in weekly_pos:
    key = (row["customer_id"], row["customer_name"], row["category_id"], row["category"])
    s = pos_summary[key]
    s["sales"] += float(row["sales_dollars"])
    s["units"] += int(row["units"])
    s["acv"] += float(row["acv_distribution_pct"])
    s["share"] += float(row["syndicated_share_pct"])
    s["comp_share"] += float(row["competitor_share_pct"])
    s["growth"] += float(row["category_growth_pct"])
    s["repeat"] += float(row["panel_repeat_rate_pct"])
    s["rows"] += 1

for row in shipments:
    key = (row["customer_id"], row["customer_name"], next(s["category_id"] for s in skus if s["sku_id"] == row["sku_id"]), row["category"])
    s = ship_summary[key]
    s["ordered"] += int(row["ordered_cases"])
    s["shipped"] += int(row["shipped_cases"])
    s["service"] += float(row["dc_service_level_pct"])
    s["rows"] += 1

for row in promotions:
    key = (row["customer_id"], row["customer_name"], next(s["category_id"] for s in skus if s["sku_id"] == row["sku_id"]), row["category"])
    s = promo_summary[key]
    s["planned"] += float(row["planned_lift_pct"])
    s["actual"] += float(row["actual_lift_pct"])
    s["compliance"] += float(row["compliance_pct"])
    s["rows"] += 1

opportunities = []
for key, pos in pos_summary.items():
    customer_id, customer_name, category_id, category_name = key
    category = next(c for c in categories if c["category_id"] == category_id)
    ship = ship_summary[key]
    promo = promo_summary[key]
    avg_acv = pos["acv"] / pos["rows"]
    avg_share = pos["share"] / pos["rows"]
    avg_comp_share = pos["comp_share"] / pos["rows"]
    avg_growth = pos["growth"] / pos["rows"]
    avg_repeat = pos["repeat"] / pos["rows"]
    fill_rate = ship["shipped"] / max(1, ship["ordered"]) * 100
    service = ship["service"] / max(1, ship["rows"])
    promo_attainment = 100
    promo_compliance = 100
    if promo["rows"]:
        promo_attainment = promo["actual"] / max(1, promo["planned"]) * 100
        promo_compliance = promo["compliance"] / promo["rows"]
    acv_gap = max(0, category["target_acv_pct"] - avg_acv)
    share_gap = max(0, avg_comp_share - avg_share)
    fill_gap = max(0, 96 - fill_rate)
    promo_gap = max(0, 90 - promo_attainment) + max(0, 82 - promo_compliance) * 0.35
    growth_score = max(0, avg_growth)
    confidence = max(48, min(98, 100 - fill_gap * 1.6 - (0 if promo["rows"] else 7) - random.uniform(0, 9)))
    margin = category["gross_margin_pct"]
    estimated_margin_upside = pos["sales"] * margin * (acv_gap * 0.006 + share_gap * 0.007 + fill_gap * 0.01 + promo_gap * 0.003)
    score = acv_gap * 1.9 + share_gap * 1.4 + fill_gap * 2.2 + promo_gap * 0.8 + growth_score * 1.1 + estimated_margin_upside / 7500
    if fill_gap > 7:
        action = "Resolve fill-rate and inventory constraint before customer review"
    elif acv_gap > 11:
        action = "Bring gap and void expansion story to customer planning"
    elif promo_gap > 15:
        action = "Rebuild promotion story with compliance and lift readout"
    elif share_gap > 5:
        action = "Prepare competitive share defense and assortment ask"
    else:
        action = "Monitor in recurring business review"
    opportunities.append(
        {
            "customer_id": customer_id,
            "customer_name": customer_name,
            "category_id": category_id,
            "category": category_name,
            "net_sales": money(pos["sales"]),
            "avg_acv_distribution_pct": round(avg_acv, 1),
            "acv_gap_pct": round(acv_gap, 1),
            "syndicated_share_pct": round(avg_share, 1),
            "competitor_share_pct": round(avg_comp_share, 1),
            "fill_rate_pct": round(fill_rate, 1),
            "promotion_lift_attainment_pct": round(promo_attainment, 1),
            "category_growth_pct": round(avg_growth, 1),
            "panel_repeat_rate_pct": round(avg_repeat, 1),
            "estimated_margin_upside": money(estimated_margin_upside),
            "confidence_score": round(confidence, 1),
            "opportunity_score": round(score, 1),
            "recommended_action": action,
        }
    )

opportunities = sorted(opportunities, key=lambda row: row["opportunity_score"], reverse=True)
write_csv(OUTPUTS / "opportunity_queue.csv", opportunities, list(opportunities[0].keys()))

trust_rows = []
for row in quality_checks:
    penalty = {"Low": 4, "Medium": 8, "High": 14, "Critical": 22}[row["severity"]]
    status_penalty = {"Pass": 0, "Watch": 8, "Fail": 19}[row["status"]]
    freshness_penalty = max(0, (int(row["freshness_hours"]) - 24) * 0.25)
    trust = max(0, 100 - penalty - status_penalty - freshness_penalty - int(row["failed_records"]) / 120)
    trust_rows.append({**row, "trust_score": round(trust, 1)})

trust_rows = sorted(trust_rows, key=lambda row: row["trust_score"])[:30]
write_csv(OUTPUTS / "data_trust_queue.csv", trust_rows, list(trust_rows[0].keys()))

package_rows = []
for customer in customers:
    customer_opps = [o for o in opportunities if o["customer_id"] == customer["customer_id"]]
    top = customer_opps[:3]
    sales = sum(float(o["net_sales"]) for o in customer_opps)
    upside = sum(float(o["estimated_margin_upside"]) for o in top)
    open_reqs = [r for r in stakeholder_requests if r["customer_id"] == customer["customer_id"] and r["status"] not in ("Published",)]
    package_rows.append(
        {
            "customer_id": customer["customer_id"],
            "customer_name": customer["customer_name"],
            "business_review_theme": random.choice(
                [
                    "Distribution whitespace and supply readiness",
                    "Promotion productivity and category share",
                    "Assortment growth story with data quality guardrails",
                    "Fill-rate stabilization before expansion ask",
                ]
            ),
            "net_sales": money(sales),
            "top_categories": "; ".join(o["category"] for o in top),
            "estimated_margin_upside": money(upside),
            "open_stakeholder_requests": len(open_reqs),
            "slides_ready": random.choice(["Yes", "Needs source validation", "Needs account signoff"]),
            "next_meeting": (date(2026, 6, 1) + timedelta(days=random.randint(0, 24))).isoformat(),
        }
    )

write_csv(OUTPUTS / "reporting_package.csv", package_rows, list(package_rows[0].keys()))

summary = {
    "total_sales": round(sum(float(r["sales_dollars"]) for r in weekly_pos), 0),
    "estimated_margin_upside": round(sum(float(r["estimated_margin_upside"]) for r in opportunities[:10]), 0),
    "critical_opportunities": sum(1 for r in opportunities if float(r["opportunity_score"]) >= 48),
    "avg_fill_rate": round(sum(float(r["fill_rate_pct"]) for r in shipments) / len(shipments), 1),
    "data_trust_fails": sum(1 for r in quality_checks if r["status"] == "Fail"),
    "published_assets": sum(1 for r in power_bi_assets if r["certification_status"] in ("Certified", "Promoted")),
}

app_payload = {
    "summary": summary,
    "customers": customers,
    "categories": categories,
    "opportunities": opportunities[:18],
    "trustQueue": trust_rows[:16],
    "packages": package_rows,
    "assets": power_bi_assets,
    "measures": semantic_measures,
}

(SRC / "data.js").write_text(
    "window.BI_DATA = " + json.dumps(app_payload, indent=2) + ";\n",
    encoding="utf-8",
)

(OUTPUTS / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

print(json.dumps(summary, indent=2))

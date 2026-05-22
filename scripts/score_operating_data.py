import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


summary = json.loads((ROOT / "analysis" / "outputs" / "summary.json").read_text())
queue = read_csv(ROOT / "analysis" / "outputs" / "opportunity_queue.csv")
trust = read_csv(ROOT / "analysis" / "outputs" / "data_trust_queue.csv")
packages = read_csv(ROOT / "analysis" / "outputs" / "reporting_package.csv")

print("Customer BI planning summary")
print(f"Modeled POS dollars: ${summary['total_sales']:,.0f}")
print(f"Top 10 margin upside: ${summary['estimated_margin_upside']:,.0f}")
print(f"Critical opportunities: {summary['critical_opportunities']}")
print(f"Average fill rate: {summary['avg_fill_rate']}%")
print()

print("Top opportunity queue")
for row in queue[:8]:
    print(
        f"{row['customer_name']} | {row['category']}: "
        f"score={row['opportunity_score']}, "
        f"ACV gap={row['acv_gap_pct']}%, "
        f"fill rate={row['fill_rate_pct']}%, "
        f"upside=${float(row['estimated_margin_upside']):,.0f}"
    )

print()
print("Lowest trust checks")
for row in trust[:5]:
    print(
        f"{row['source_system']} | {row['check_type']}: "
        f"trust={row['trust_score']}, status={row['status']}, fix={row['recommended_fix']}"
    )

print()
print("Reporting package readiness")
for row in packages:
    print(f"{row['customer_name']}: {row['slides_ready']} for {row['next_meeting']}")

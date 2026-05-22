-- Natural grocery customer BI planning checks
-- Written in warehouse-style SQL to document the logic behind the portfolio artifact.

-- 1. Customer-category opportunity foundation
with pos as (
  select
    customer_id,
    customer_name,
    category,
    sum(sales_dollars) as net_sales,
    avg(acv_distribution_pct) as avg_acv_distribution_pct,
    avg(syndicated_share_pct) as syndicated_share_pct,
    avg(competitor_share_pct) as competitor_share_pct,
    avg(category_growth_pct) as category_growth_pct
  from weekly_pos
  group by 1, 2, 3
),
shipments as (
  select
    customer_id,
    category,
    sum(shipped_cases) / nullif(sum(ordered_cases), 0) * 100 as fill_rate_pct
  from distributor_shipments
  group by 1, 2
)
select
  pos.customer_name,
  pos.category,
  pos.net_sales,
  pos.avg_acv_distribution_pct,
  pos.syndicated_share_pct,
  pos.competitor_share_pct,
  shipments.fill_rate_pct
from pos
left join shipments
  on pos.customer_id = shipments.customer_id
 and pos.category = shipments.category
order by pos.net_sales desc;

-- 2. Source trust checks that should block a customer business review
select
  source_system,
  table_name,
  check_type,
  severity,
  status,
  freshness_hours,
  failed_records,
  recommended_fix
from data_quality_checks
where status <> 'Pass'
   or severity in ('High', 'Critical')
order by
  case severity
    when 'Critical' then 1
    when 'High' then 2
    when 'Medium' then 3
    else 4
  end,
  failed_records desc;

-- 3. Power BI portfolio readiness
select
  workspace,
  count(*) as asset_count,
  avg(refresh_success_pct) as avg_refresh_success_pct,
  avg(data_quality_pct) as avg_data_quality_pct,
  sum(monthly_active_users) as monthly_active_users,
  sum(case when certification_status in ('Certified', 'Promoted') then 1 else 0 end) as published_assets
from power_bi_assets
group by 1
order by monthly_active_users desc;

-- 4. Stakeholder request prioritization
select
  request_type,
  customer_id,
  category,
  business_question,
  impact_score,
  urgency_score,
  requirement_clarity_pct,
  age_days,
  impact_score * 0.45
    + urgency_score * 0.35
    + age_days / 10.0
    + case when requirement_clarity_pct < 70 then 1.5 else 0 end as request_priority_score
from stakeholder_requests
where status not in ('Published')
order by request_priority_score desc;

-- 5. Semantic measure certification gaps
select
  measure_name,
  grain,
  certification_status,
  test_coverage_pct,
  business_definition
from semantic_measures
where certification_status <> 'Certified'
   or test_coverage_pct < 85
order by test_coverage_pct asc;

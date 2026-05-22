const data = window.BI_DATA;

const formatCurrency = (value) =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(value);

const formatNumber = (value) =>
  new Intl.NumberFormat("en-US", { maximumFractionDigits: 0 }).format(value);

const kpis = [
  ["Modeled POS", formatCurrency(data.summary.total_sales), "26 weeks"],
  ["Margin Upside", formatCurrency(data.summary.estimated_margin_upside), "top 10 actions"],
  ["Critical Gaps", data.summary.critical_opportunities, "ranked queue"],
  ["Fill Rate", `${data.summary.avg_fill_rate}%`, "case shipped"],
  ["Trust Fails", data.summary.data_trust_fails, "source checks"],
  ["Certified Assets", data.summary.published_assets, "BI portfolio"],
];

document.getElementById("kpis").innerHTML = kpis
  .map(
    ([label, value, note]) => `
      <article class="kpi-card">
        <span>${label}</span>
        <strong>${value}</strong>
        <em>${note}</em>
      </article>
    `
  )
  .join("");

const customerSales = data.customers
  .map((customer) => {
    const sales = data.opportunities
      .filter((row) => row.customer_id === customer.customer_id)
      .reduce((sum, row) => sum + Number(row.net_sales), 0);
    const upside = data.opportunities
      .filter((row) => row.customer_id === customer.customer_id)
      .reduce((sum, row) => sum + Number(row.estimated_margin_upside), 0);
    return { ...customer, sales, upside };
  })
  .sort((a, b) => b.sales - a.sales);

const maxSales = Math.max(...customerSales.map((row) => row.sales));
document.getElementById("customer-bars").innerHTML = customerSales
  .map(
    (row) => `
      <div class="bar-row">
        <div>
          <b>${row.customer_name}</b>
          <span>${row.channel} | ${formatNumber(row.stores)} stores | ${row.region}</span>
        </div>
        <strong>${formatCurrency(row.sales)}</strong>
        <i style="width:${Math.max(8, (row.sales / maxSales) * 100)}%"></i>
        <small>${formatCurrency(row.upside)} modeled margin upside</small>
      </div>
    `
  )
  .join("");

document.getElementById("asset-list").innerHTML = data.assets
  .map(
    (asset) => `
      <div class="asset-card">
        <div>
          <b>${asset.asset_name}</b>
          <span>${asset.workspace} | ${asset.primary_audience}</span>
        </div>
        <dl>
          <dt>Refresh</dt><dd>${asset.refresh_success_pct}%</dd>
          <dt>Quality</dt><dd>${asset.data_quality_pct}%</dd>
          <dt>Users</dt><dd>${asset.monthly_active_users}</dd>
        </dl>
        <em class="${asset.certification_status.toLowerCase().replaceAll(" ", "-")}">${asset.certification_status}</em>
      </div>
    `
  )
  .join("");

document.getElementById("opportunity-table").innerHTML = data.opportunities
  .map(
    (row) => `
      <tr>
        <td><b>${row.customer_name}</b></td>
        <td>${row.category}</td>
        <td><span class="score">${row.opportunity_score}</span></td>
        <td>${row.acv_gap_pct}%</td>
        <td>${row.fill_rate_pct}%</td>
        <td>${formatCurrency(row.estimated_margin_upside)}</td>
        <td>${row.recommended_action}</td>
      </tr>
    `
  )
  .join("");

document.getElementById("trust-table").innerHTML = data.trustQueue
  .map(
    (row) => `
      <tr>
        <td><b>${row.source_system}</b><span>${row.table_name}</span></td>
        <td>${row.check_type}</td>
        <td><span class="status ${row.status.toLowerCase()}">${row.status}</span></td>
        <td><span class="score">${row.trust_score}</span></td>
        <td>${row.recommended_fix}</td>
      </tr>
    `
  )
  .join("");

document.getElementById("measure-list").innerHTML = data.measures
  .map(
    (measure) => `
      <div class="measure-card">
        <div>
          <b>${measure.measure_name}</b>
          <span>${measure.grain}</span>
        </div>
        <code>${measure.dax_pattern}</code>
        <p>${measure.business_definition}</p>
        <small>${measure.certification_status} | ${measure.test_coverage_pct}% tests</small>
      </div>
    `
  )
  .join("");

document.getElementById("package-grid").innerHTML = data.packages
  .map(
    (row) => `
      <article class="package-card">
        <span>${row.next_meeting}</span>
        <h3>${row.customer_name}</h3>
        <p>${row.business_review_theme}</p>
        <dl>
          <dt>Net sales</dt><dd>${formatCurrency(row.net_sales)}</dd>
          <dt>Upside</dt><dd>${formatCurrency(row.estimated_margin_upside)}</dd>
          <dt>Open asks</dt><dd>${row.open_stakeholder_requests}</dd>
          <dt>Slides</dt><dd>${row.slides_ready}</dd>
        </dl>
        <b>${row.top_categories}</b>
      </article>
    `
  )
  .join("");

const showView = (button, updateHash = true) => {
  document.querySelectorAll(".tab").forEach((tab) => tab.classList.remove("active"));
  document.querySelectorAll(".view").forEach((view) => view.classList.remove("active"));
  button.classList.add("active");
  document.getElementById(button.dataset.tab).classList.add("active");
  if (updateHash) {
    window.history.replaceState(null, "", `#${button.dataset.tab}`);
  }
  window.scrollTo(0, 0);
};

document.querySelectorAll(".tab").forEach((button) => {
  button.addEventListener("click", () => {
    showView(button);
  });
});

const showHashView = () => {
  const requestedView = window.location.hash.replace("#", "");
  const requestedButton = document.querySelector(`.tab[data-tab="${requestedView}"]`);
  if (requestedButton) {
    showView(requestedButton, false);
  }
};

showHashView();
window.addEventListener("hashchange", showHashView);

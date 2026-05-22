let
    Source = Csv.Document(File.Contents("data/distributor_shipments.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    TypedColumns = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"week_start", type date},
            {"customer_id", type text},
            {"customer_name", type text},
            {"sku_id", type text},
            {"category", type text},
            {"ordered_cases", Int64.Type},
            {"shipped_cases", Int64.Type},
            {"fill_rate_pct", type number},
            {"on_hand_cases", Int64.Type},
            {"inbound_po_count", Int64.Type},
            {"dc_service_level_pct", type number},
            {"spoilage_risk_pct", type number}
        }
    ),
    AddedFillRateBand = Table.AddColumn(
        TypedColumns,
        "fill_rate_band",
        each if [fill_rate_pct] < 90 then "At risk" else if [fill_rate_pct] < 96 then "Watch" else "Stable",
        type text
    ),
    AddedInventorySignal = Table.AddColumn(
        AddedFillRateBand,
        "inventory_signal",
        each if [on_hand_cases] = 0 then "No on-hand" else if [on_hand_cases] < [ordered_cases] * 0.2 then "Low cover" else "Covered",
        type text
    )
in
    AddedInventorySignal

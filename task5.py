    plt.tight_layout()
    plt.savefig(OUTPUT / "monthly_revenue_trend.png", dpi=160)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.barplot(data=regional, x="region", y="revenue")
    plt.title("Revenue by Region")
    plt.xlabel("Region")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.savefig(OUTPUT / "regional_revenue.png", dpi=160)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x="marketing_spend", y="revenue", hue="region")
    plt.title("Marketing Spend vs Revenue")
    plt.xlabel("Marketing Spend")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.savefig(OUTPUT / "marketing_vs_revenue.png", dpi=160)
    plt.close()


def write_report(monthly, regional, summary):
    best_region = regional.iloc[0]
    best_month = monthly.loc[monthly["revenue"].idxmax()]
    weakest_region = regional.iloc[-1]

    # Insights are calculated from this sample dataset.
    executive_summary = (
        f"Across the 12-month sample, total revenue was {summary['total_revenue']:,.2f} "
        f"from {summary['total_orders']:,} orders. Average customer satisfaction was "
        f"{summary['average_satisfaction']:.2f}/5. The leading region by revenue was "
        f"{best_region['region']}, while {weakest_region['region']} had the lowest revenue. "
        f"The highest-revenue month was {best_month['month'].strftime('%B %Y')}."
    )

    recommendations = [
        f"Review the practices and customer mix in {best_region['region']} to identify "
        "approaches that could be replicated in other regions.",
        f"Investigate {weakest_region['region']} for opportunities in demand generation, "
        "conversion, product mix, or customer experience.",
        "Evaluate marketing spend alongside revenue and campaign-level attribution before "
        "changing budgets; correlation alone does not establish causation.",
        "Monitor customer satisfaction with revenue and order metrics to avoid focusing on "
        "sales growth at the expense of customer experience.",
    ]

    report = [
        "# Analytics Report & Insights",
        "",
        "## Executive Summary",
        executive_summary,
        "",
        "## Key Findings",
        f"- Total revenue: **{summary['total_revenue']:,.2f}**",
        f"- Total orders: **{summary['total_orders']:,}**",
        f"- Average revenue per order: **{summary['overall_revenue_per_order']:,.2f}**",
        f"- Average customer satisfaction: **{summary['average_satisfaction']:.2f}/5**",
        f"- Total marketing spend: **{summary['total_marketing_spend']:,.2f}**",
        f"- Highest-revenue month: **{best_month['month'].strftime('%B %Y')}**",
        f"- Highest-revenue region: **{best_region['region']}**",
        "",
        "## Regional Summary",
        regional.to_string(index=False, float_format=lambda x: f"{x:,.2f}"),
        "",
        "## Monthly Summary",
        monthly.to_string(index=False, float_format=lambda x: f"{x:,.2f}"),
        "",
        "## Insights",
        f"- {best_region['region']} leads regions by total revenue in this generated dataset.",
        f"- {weakest_region['region']} has the lowest regional revenue and merits further investigation.",
        "- Monthly trends can help identify seasonal patterns, but this sample is simulated.",
        "- Marketing spend and revenue should be assessed with more detailed campaign data before causal conclusions.",
        "",
        "## Actionable Recommendations",
    ]
    report.extend([f"- {rec}" for rec in recommendations])
    report.extend([
        "",
        "## Visualizations",
        "- monthly_revenue_trend.png: monthly revenue trend",
        "- regional_revenue.png: revenue comparison by region",
        "- marketing_vs_revenue.png: marketing spend versus revenue",
        "",
        "## Data and Limitations",
        "This report uses synthetic demonstration data, not actual company records. "
        "Patterns and recommendations are illustrative only. Validate insights using real data, "
        "business context, and appropriate statistical methods before making decisions.",
    ])

    (OUTPUT / "analytics_report.md").write_text("\n".join(report), encoding="utf-8")


def main():
    data = create_business_dataset()
    clean, monthly, regional, summary = analyze_data(data)

    print("=== Executive Summary Metrics ===")
    for key, value in summary.items():
        print(f"{key.replace('_', ' ').title()}: {value:,.2f}")

    print("\n=== Regional Summary ===")
    print(regional.round(2).to_string(index=False))
    print("\n=== Monthly Summary ===")
    print(monthly.round(2).to_string(index=False))

    create_visualizations(clean, monthly, regional)
    write_report(monthly, regional, summary)

    clean.to_csv(OUTPUT / "cleaned_business_dataset.csv", index=False)
    monthly.to_csv(OUTPUT / "monthly_summary.csv", index=False)
    regional.to_csv(OUTPUT / "regional_summary.csv", index=False)

    print(f"\nOutputs created in: {OUTPUT.resolve()}")
    print("Includes Markdown analytics report, summary CSVs, and visualizations.")


if __name__ == "__main__":
    main()

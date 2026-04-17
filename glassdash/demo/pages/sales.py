"""Sales Statistics Dashboard page."""

import polars as pl

from glassdash import GlassDashboard, GlassTheme, Section
from glassdash.components import (
    AreaChart,
    BarChart,
    DualAreaChart,
    MultiLinesChart,
    RadialGauge,
    StackedBarChart,
)


def get_sales_data():
    return pl.DataFrame(
        {
            "month": [
                "2024-07",
                "2024-08",
                "2024-09",
                "2024-10",
                "2024-11",
                "2024-12",
                "2025-01",
                "2025-02",
                "2025-03",
                "2025-04",
                "2025-05",
                "2025-06",
            ],
            "leads": [320, 345, 368, 392, 415, 438, 462, 489, 515, 542, 571, 602],
            "conversions": [85, 92, 98, 105, 112, 118, 125, 133, 141, 149, 158, 168],
            "revenue": [
                425000,
                458000,
                492000,
                528000,
                565000,
                602000,
                642000,
                685000,
                732000,
                782000,
                836000,
                894000,
            ],
            "enterprise": [
                180000,
                195000,
                212000,
                230000,
                250000,
                272000,
                295000,
                320000,
                348000,
                378000,
                410000,
                445000,
            ],
            "mid_market": [
                145000,
                158000,
                172000,
                187000,
                203000,
                220000,
                238000,
                258000,
                280000,
                304000,
                330000,
                358000,
            ],
            "smb": [
                100000,
                105000,
                108000,
                111000,
                112000,
                110000,
                109000,
                107000,
                104000,
                100000,
                96000,
                91000,
            ],
            "avg_deal_size": [
                8500,
                9200,
                9800,
                10500,
                11200,
                11800,
                12500,
                13200,
                14000,
                14800,
                15700,
                16700,
            ],
            "sales_cycle_days": [45, 43, 42, 40, 39, 38, 37, 36, 35, 34, 33, 32],
            "win_rate": [26.5, 26.7, 26.6, 26.8, 27.0, 26.9, 27.2, 27.4, 27.5, 27.5, 27.7, 27.9],
            "pipeline_value": [
                2100000,
                2280000,
                2480000,
                2690000,
                2920000,
                3160000,
                3420000,
                3700000,
                4000000,
                4320000,
                4660000,
                5020000,
            ],
        }
    )


def SalesPage(theme=None):
    if theme is None:
        theme = GlassTheme()
    df = get_sales_data()
    return GlassDashboard(
        title="Sales Statistics Dashboard",
        date_range=("2024-07-01", "2025-06-13"),
        theme=theme,
        children=[
            Section(
                "Pipeline & Revenue",
                "Sales funnel overview",
                height=600,
                children=[
                    AreaChart(df, x="month", y="pipeline_value", theme=theme),
                    MultiLinesChart(
                        df,
                        x="month",
                        lines={"Leads": "leads", "Conversions": "conversions"},
                        theme=theme,
                    ),
                ],
            ),
            Section(
                "Revenue by Segment",
                "Market segmentation",
                height=600,
                children=[
                    StackedBarChart(
                        df,
                        x="month",
                        segments={
                            "Enterprise": "enterprise",
                            "Mid-Market": "mid_market",
                            "SMB": "smb",
                        },
                        theme=theme,
                    ),
                    BarChart(df, x="month", y="avg_deal_size", theme=theme),
                ],
            ),
            Section(
                "Performance Metrics",
                "Key sales indicators",
                height=400,
                children=[
                    DualAreaChart(df, x="month", y1="win_rate", y2="sales_cycle_days", theme=theme),
                ],
            ),
            Section(
                "Conversion Rate",
                "Current win rate",
                height=400,
                children=[
                    RadialGauge(value=27.9, max_value=100, label="Win Rate %", theme=theme),
                ],
            ),
        ],
    )

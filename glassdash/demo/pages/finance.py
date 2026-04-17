"""Finance Statistics Dashboard page."""

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


def get_finance_data():
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
            "revenue": [
                420000,
                445000,
                468000,
                492000,
                515000,
                538000,
                562000,
                589000,
                615000,
                642000,
                671000,
                702000,
            ],
            "expenses": [
                280000,
                285000,
                292000,
                298000,
                305000,
                312000,
                318000,
                325000,
                332000,
                340000,
                348000,
                356000,
            ],
            "profit": [
                140000,
                160000,
                176000,
                194000,
                210000,
                226000,
                244000,
                264000,
                283000,
                302000,
                323000,
                346000,
            ],
            "marketing": [
                25000,
                28000,
                32000,
                35000,
                38000,
                42000,
                45000,
                48000,
                52000,
                55000,
                59000,
                63000,
            ],
            "operations": [
                85000,
                88000,
                92000,
                95000,
                98000,
                101000,
                104000,
                108000,
                111000,
                115000,
                119000,
                123000,
            ],
            "salaries": [
                120000,
                122000,
                125000,
                128000,
                131000,
                134000,
                137000,
                140000,
                143000,
                147000,
                150000,
                154000,
            ],
            "infrastructure": [
                50000,
                48000,
                52000,
                55000,
                51000,
                54000,
                57000,
                59000,
                62000,
                65000,
                68000,
                71000,
            ],
            "cash_flow": [
                95000,
                110000,
                125000,
                142000,
                158000,
                175000,
                192000,
                212000,
                230000,
                250000,
                272000,
                295000,
            ],
            "burn_rate": [
                65000,
                62000,
                58000,
                55000,
                52000,
                48000,
                45000,
                42000,
                38000,
                35000,
                31000,
                28000,
            ],
            "runway_months": [18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40],
        }
    )


def FinancePage(theme=None):
    if theme is None:
        theme = GlassTheme()
    df = get_finance_data()
    return GlassDashboard(
        title="Finance Statistics Dashboard",
        date_range=("2024-07-01", "2025-06-13"),
        theme=theme,
        children=[
            Section(
                "Revenue & Profit",
                "Financial overview",
                height=600,
                children=[
                    AreaChart(df, x="month", y="revenue", theme=theme),
                    MultiLinesChart(
                        df,
                        x="month",
                        lines={"Revenue": "revenue", "Expenses": "expenses", "Profit": "profit"},
                        theme=theme,
                    ),
                ],
            ),
            Section(
                "Expense Breakdown",
                "Cost distribution by category",
                height=600,
                children=[
                    StackedBarChart(
                        df,
                        x="month",
                        segments={
                            "Marketing": "marketing",
                            "Operations": "operations",
                            "Salaries": "salaries",
                            "Infrastructure": "infrastructure",
                        },
                        theme=theme,
                    ),
                    BarChart(df, x="month", y="burn_rate", theme=theme),
                ],
            ),
            Section(
                "Cash Flow",
                "Cash management metrics",
                height=400,
                children=[
                    DualAreaChart(df, x="month", y1="cash_flow", y2="burn_rate", theme=theme),
                ],
            ),
            Section(
                "Runway",
                "Financial runway",
                height=400,
                children=[
                    RadialGauge(value=40, max_value=48, label="Runway (months)", theme=theme),
                ],
            ),
        ],
    )

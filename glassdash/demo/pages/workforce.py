"""Workforce Statistics Dashboard page."""

import polars as pl

from glassdash import GlassDashboard, GlassTheme, Section
from glassdash.components import (
    AreaChart,
    BarChart,
    DualAreaChart,
    MultiBarsChart,
    MultiLinesChart,
    RadialGauge,
    StackedBarChart,
    StackedBarWithBreakdown,
    StackedBarWithLine,
)


def get_workforce_data():
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
            "fte": [18.2, 19.1, 19.5, 20.3, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5],
            "fte_ft": [12, 13, 13, 14, 14, 15, 15, 16, 16, 16, 17, 17],
            "fte_pt": [4, 4, 4, 4, 5, 4, 5, 4, 5, 5, 5, 5],
            "fte_cont": [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            "fte_other": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            "total_fte": [19, 20, 20, 21, 22, 22, 23, 23, 24, 24, 25, 25],
            "efficiency": [82, 83, 84, 85, 86, 85, 87, 87, 88, 87, 87, 87],
            "efficacy": [88, 89, 90, 91, 92, 91, 93, 93, 94, 93, 93, 93],
            "yield_pct": [3.2, 3.3, 3.4, 3.5, 3.6, 3.5, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2],
            "code_integration": [65, 70, 75, 78, 80, 82, 85, 87, 88, 90, 92, 95],
            "squads": [4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8],
            "ai_usage": [10, 12, 15, 18, 22, 28, 35, 42, 50, 58, 68, 78],
            "squad_a": [4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8],
            "squad_b": [3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7],
            "squad_c": [3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7],
            "fte_avg": [85, 86, 87, 87, 88, 87, 88, 89, 89, 90, 90, 91],
            "fte_target": [90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90],
        }
    )


def WorkforcePage(theme=None):
    if theme is None:
        theme = GlassTheme()
    df = get_workforce_data()
    return GlassDashboard(
        title="Workforce Statistics Dashboard",
        date_range=("2024-07-01", "2025-06-13"),
        theme=theme,
        children=[
            Section(
                "FTE Trends",
                "Full-time equivalent over time",
                height=600,
                children=[
                    AreaChart(df, x="month", y="fte", theme=theme),
                    MultiLinesChart(
                        df, x="month", lines={"FTE": "fte", "Target": "total_fte"}, theme=theme
                    ),
                ],
            ),
            Section(
                "Squad Performance",
                "Team composition by squad",
                height=600,
                children=[
                    MultiBarsChart(
                        df,
                        x="month",
                        bars={"Squad A": "squad_a", "Squad B": "squad_b", "Squad C": "squad_c"},
                        theme=theme,
                        highlight_current=False,
                    ),
                    BarChart(df, x="month", y="squads", theme=theme),
                ],
            ),
            Section(
                "Labor Mix",
                "Breakdown by employment type",
                height=900,
                children=[
                    StackedBarChart(
                        df,
                        x="month",
                        segments={
                            "Full-time": "fte_ft",
                            "Part-time": "fte_pt",
                            "Contingent": "fte_cont",
                            "Others": "fte_other",
                        },
                        theme=theme,
                    ),
                    StackedBarWithLine(
                        df,
                        x="month",
                        bar_segments={
                            "Full-time": "fte_ft",
                            "Part-time": "fte_pt",
                            "Contingent": "fte_cont",
                        },
                        line_y="total_fte",
                        theme=theme,
                    ),
                    StackedBarWithBreakdown(
                        df,
                        x="month",
                        bar_segments={
                            "Full-time": "fte_ft",
                            "Part-time": "fte_pt",
                            "Contingent": "fte_cont",
                            "Others": "fte_other",
                        },
                        breakdown={
                            "Full-time": {
                                "Analyst": 0.3,
                                "Engineer": 0.4,
                                "Sales": 0.2,
                                "Others": 0.1,
                            },
                            "Part-time": {"Morning": 0.5, "Afternoon": 0.5},
                            "Contingent": {"Contractor": 0.6, "Temp": 0.4},
                            "Others": {"External": 0.7, "Internal": 0.3},
                        },
                        theme=theme,
                    ),
                ],
            ),
            Section(
                "Efficiency Metrics",
                "Efficiency and efficacy over time",
                height=400,
                children=[
                    DualAreaChart(df, x="month", y1="efficiency", y2="efficacy", theme=theme),
                ],
            ),
            Section(
                "Yield Gauge",
                "Current yield performance",
                height=400,
                children=[
                    RadialGauge(value=61, max_value=100, label="Yield", theme=theme),
                ],
            ),
        ],
    )

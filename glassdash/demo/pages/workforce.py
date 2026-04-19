"""Workforce Statistics Dashboard page."""

import polars as pl

from glassdash import GlassDashboard, GlassTheme, Section
from glassdash.components import (
    ChartsGroup,
    MultiAreaChart,
    MultiBarsChart,
    MultiLinesChart,
    RadialGauge,
    StackedBarChart,
    StackedBarHorizontalChart,
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


def get_headcount_data():
    data = [
        {"category": "Q1 2025", "subcategory": "Engineering", "value": 45},
        {"category": "Q1 2025", "subcategory": "Sales", "value": 20},
        {"category": "Q1 2025", "subcategory": "Marketing", "value": 8},
        {"category": "Q1 2025", "subcategory": "Operations", "value": 15},
        {"category": "Q2 2025", "subcategory": "Engineering", "value": 52},
        {"category": "Q2 2025", "subcategory": "Sales", "value": 22},
        {"category": "Q2 2025", "subcategory": "Marketing", "value": 9},
        {"category": "Q2 2025", "subcategory": "Operations", "value": 16},
        {"category": "Q3 2025", "subcategory": "Engineering", "value": 58},
        {"category": "Q3 2025", "subcategory": "Sales", "value": 25},
        {"category": "Q3 2025", "subcategory": "Marketing", "value": 10},
        {"category": "Q3 2025", "subcategory": "Operations", "value": 17},
        {"category": "Q4 2025", "subcategory": "Engineering", "value": 65},
        {"category": "Q4 2025", "subcategory": "Sales", "value": 28},
        {"category": "Q4 2025", "subcategory": "Marketing", "value": 12},
        {"category": "Q4 2025", "subcategory": "Operations", "value": 18},
    ]
    return pl.DataFrame(data)


def WorkforcePage(theme=None):
    if theme is None:
        theme = GlassTheme()
    df = get_workforce_data()
    headcount_df = get_headcount_data()
    return GlassDashboard(
        title="Workforce Statistics Dashboard",
        date_range=("2024-07-01", "2025-06-13"),
        theme=theme,
        children=[
            Section(
                "FTE Overview",
                "Full-time equivalent trends and composition",
                height=1200,
                children=[
                    MultiLinesChart(
                        df, x="month", lines={"FTE": "fte"}, title="FTE Trend", theme=theme
                    ),
                    MultiAreaChart(
                        df,
                        x="month",
                        areas={"FT": "fte_ft", "PT": "fte_pt", "Contingent": "fte_cont"},
                        title="Headcount Mix",
                        theme=theme,
                    ),
                    StackedBarChart(
                        df,
                        x="month",
                        segments={
                            "Full-time": "fte_ft",
                            "Part-time": "fte_pt",
                            "Contingent": "fte_cont",
                        },
                        title="FTE Composition",
                        theme=theme,
                    ),
                    MultiBarsChart(
                        df,
                        x="month",
                        bars={"Squad A": "squad_a", "Squad B": "squad_b", "Squad C": "squad_c"},
                        title="Team Distribution",
                        theme=theme,
                        highlight_current=False,
                    ),
                ],
            ),
            Section(
                "Performance Metrics",
                "Team efficiency and effectiveness",
                height=1200,
                children=[
                    MultiLinesChart(
                        df,
                        x="month",
                        lines={"Efficiency": "efficiency", "Efficacy": "efficacy"},
                        title="Efficiency Metrics",
                        theme=theme,
                    ),
                    MultiLinesChart(
                        df,
                        x="month",
                        lines={"Code Integration": "code_integration"},
                        title="Code Integration",
                        theme=theme,
                    ),
                    ChartsGroup(
                        df,
                        x="month",
                        title="AI Analytics",
                        charts=[
                            lambda df, x, theme, id, **kwargs: MultiLinesChart(
                                df,
                                x=x,
                                lines={"AI Usage": "ai_usage"},
                                theme=theme,
                                id=id,
                                **kwargs,
                            ),
                            lambda df, x, theme, id, **kwargs: MultiBarsChart(
                                df, x=x, bars={"AI Usage": "ai_usage"}, theme=theme, id=id, **kwargs
                            ),
                        ],
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
                        title="FTE with Total",
                        theme=theme,
                    ),
                ],
            ),
            Section(
                "KPIs & Targets",
                "Key performance indicators",
                height=1200,
                children=[
                    RadialGauge(value=61, max_value=100, label="Yield %", theme=theme),
                    RadialGauge(value=90, max_value=100, label="FTE Target %", theme=theme),
                    RadialGauge(value=87, max_value=100, label="Efficiency %", theme=theme),
                    StackedBarHorizontalChart(
                        headcount_df,
                        category="category",
                        subcategory="subcategory",
                        value="value",
                        title="Headcount by Department",
                        theme=theme,
                    ),
                ],
            ),
        ],
    )

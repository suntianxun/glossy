import uuid

from dash import html

from glassdash.components._chart_helpers import parse_month_strings
from glassdash.theme import GlassTheme


def ChartsGroup(
    dataframe,
    x="month",
    charts=None,
    title=None,
    theme=None,
    id=None,
    **kwargs,
):
    if theme is None:
        theme = GlassTheme()

    if charts is None:
        charts = []

    chart_id = id or f"charts-group-{uuid.uuid4().hex[:8]}"

    parse_month_strings(dataframe[x].to_list())

    chart_children = []
    for i, chart_func in enumerate(charts):
        chart_component = chart_func(
            dataframe,
            x=x,
            theme=theme,
            id=f"{chart_id}-chart-{i}",
            internal_wrap=False,
        )

        wrapper = html.Div(
            children=[chart_component],
            style={
                "flex": "1",
                "minWidth": "0",
                "minHeight": "0",
                "height": "100%",
                "overflow": "hidden",
            },
        )
        chart_children.append(wrapper)

        if i < len(charts) - 1:
            divider = html.Div(
                style={
                    "width": "1px",
                    "background": theme.colors["glass_border"],
                    "margin": "0 10px",
                    "boxShadow": "0 0 10px rgba(255,255,255,0.1)",
                    "flexShrink": "0",
                }
            )
            chart_children.append(divider)

    charts_row = html.Div(
        children=chart_children,
        style={
            "display": "flex",
            "alignItems": "stretch",
            "flex": "1",
            "minHeight": "0",
            "height": "100%",
        },
    )

    if title:
        return html.Div(
            [
                html.Div(
                    title,
                    className="glass-chart-title",
                    style={"flex": "0 0 auto", "paddingBottom": "4px"},
                ),
                html.Div(
                    charts_row,
                    style={"flex": "1", "minHeight": "0", "height": "100%"},
                ),
            ],
            className="glass-card",
            style={
                "padding": "15px",
                "display": "flex",
                "flexDirection": "column",
                "flex": "1",
                "minHeight": "0",
                "height": "100%",
            },
            **kwargs,
        )

    return html.Div(
        children=charts_row,
        className="glass-card",
        style={
            "padding": "15px",
            "display": "flex",
            "flexDirection": "column",
            "flex": "1",
            "minHeight": "0",
            "height": "100%",
        },
        **kwargs,
    )

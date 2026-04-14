"""KPICard - key metric display with trend."""

from dash import html
from glassdash.theme import GlassTheme


def KPICard(
    title, value, trend=None, trend_label="% vs last month", theme=None, **kwargs
):
    if theme is None:
        theme = GlassTheme()

    trend_class = (
        "glass-kpi-trend-up"
        if (trend and trend > 0)
        else "glass-kpi-trend-down"
        if trend
        else ""
    )
    trend_symbol = "↑" if (trend and trend > 0) else "↓" if trend else ""

    return html.Div(
        [
            html.Div(title.upper(), className="glass-kpi-label"),
            html.Div(f"{value}", className="glass-kpi-value"),
            html.Div(
                f"{trend_symbol} {abs(trend)} {trend_label}" if trend else "",
                className=f"glass-kpi-label {trend_class}" if trend else "",
            ),
        ],
        className="glass-card glass-kpi",
        style={"textAlign": "center"},
        **kwargs,
    )

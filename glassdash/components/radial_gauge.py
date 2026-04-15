"""RadialGauge - arc/gauge visualization."""

from dash import dcc, html
from plotly import graph_objects as go

from glassdash.theme import GlassTheme


def RadialGauge(value, max_value=100, label="Value", color="success", theme=None, **kwargs):
    if theme is None:
        theme = GlassTheme()

    gauge_color = theme.colors.get(color, theme.colors["success"])

    percentage = min(value / max_value, 1.0)

    fig = go.Figure(
        go.Pie(
            values=[percentage, 1 - percentage],
            hole=0.7,
            marker_colors=[gauge_color, "rgba(255,255,255,0.1)"],
            showlegend=False,
            textinfo="none",
            sort=False,
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"l": 10, "r": 10, "t": 10, "b": 10},
        annotations=[
            {
                "text": f"{value:.1f}%",
                "x": 0.5,
                "y": 0.5,
                "font": {"size": 22, "color": "white", "family": theme.fonts["family"]},
                "showarrow": False,
            },
            {
                "text": label.upper(),
                "x": 0.5,
                "y": 0.4,
                "font": {
                    "size": 10,
                    "color": theme.colors["text_muted"],
                    "family": theme.fonts["family"],
                },
                "showarrow": False,
            },
        ],
    )

    return html.Div(
        html.Div(
            className="glass-card",
            style={
                "padding": "15px",
                "height": "100%",
                "min-height": "0",
                "box-sizing": "border-box",
            },
            children=[dcc.Graph(figure=fig, style={"height": "100%"})],
        ),
        **kwargs,
    )

import uuid

from dash import Input, Output, callback, dcc, html
from plotly import graph_objects as go

from glassdash.components._base import _with_validation
from glassdash.components._chart_helpers import (
    apply_date_filter,
    create_popup_filter_panel,
    parse_month_strings,
)
from glassdash.theme import GlassTheme


def hex_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return f"rgb({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)})"


@_with_validation
def MultiAreaChart(
    dataframe,
    x="month",
    areas=None,
    colors=None,
    highlight_current=True,
    title=None,
    theme=None,
    id=None,
    internal_wrap=True,
    show_filter=True,
    **kwargs,
):
    if theme is None:
        theme = GlassTheme()

    if areas is None:
        areas = {"Area 1": "value1", "Area 2": "value2"}
    if colors is None:
        colors = ["accent", "purple", "cyan", "success", "warning"]

    chart_id = id or f"multi-area-{uuid.uuid4().hex[:8]}"
    area_keys = list(areas.keys())

    x_dates_all = parse_month_strings(dataframe[x].to_list())

    toggle_btn, overlay, hidden_filter_state = create_popup_filter_panel(
        chart_id, x_dates_all, categories=area_keys
    )

    graph = dcc.Graph(
        id=chart_id,
        style={"height": "100%", "minHeight": "0"},
        config={"responsive": True},
    )

    chart_container = html.Div(
        [
            html.Div(
                title,
                className="glass-chart-title",
                style={"display": "none" if not title else "block", "flex": "0 0 auto"},
            )
            if title
            else None,
            html.Div(
                toggle_btn,
                style={
                    "textAlign": "right",
                    "marginBottom": "5px",
                    "position": "relative",
                    "zIndex": 100,
                    "display": "none" if not show_filter else "block",
                },
            ),
            html.Div(
                graph,
                className="glass-chart-container",
                style={"flex": "1", "minHeight": "0", "height": "100%", "overflow": "hidden"},
            ),
            overlay,
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            "flex": "1",
            "minHeight": "0",
            "height": "100%",
            "overflow": "hidden",
        },
    )

    @callback(
        Output(overlay, "style"),
        Input(f"{chart_id}-toggle-filter", "n_clicks"),
    )
    def toggle_filter(n_clicks):
        if n_clicks % 2 == 1:
            return {
                "display": "block",
                "position": "fixed",
                "top": "50%",
                "left": "50%",
                "transform": "translate(-50%, -50%)",
                "zIndex": 1000,
            }
        return {"display": "none"}

    @callback(
        Output(chart_id, "figure"),
        Input(f"{chart_id}-categories", "value"),
        Input(f"{chart_id}-start-date", "value"),
        Input(f"{chart_id}-end-date", "value"),
    )
    def update_chart(selected_areas, start_date, end_date):
        if not selected_areas:
            selected_areas = area_keys

        selected_set = set(selected_areas)
        filtered_dates = apply_date_filter(x_dates_all, start_date, end_date)

        fig = go.Figure()

        area_colors = [
            theme.colors.get(colors[i % len(colors)], theme.colors["accent"])
            for i in range(len(areas))
        ]

        for i, (label, col) in enumerate(areas.items()):
            if label not in selected_set:
                continue

            color = area_colors[i]
            rgb = hex_to_rgb(color)

            y_all = dataframe[col].to_list()
            date_to_y = dict(zip(x_dates_all, y_all, strict=False))
            filtered_y = [date_to_y.get(d, 0) for d in filtered_dates]

            fig.add_trace(
                go.Scatter(
                    x=filtered_dates + filtered_dates[::-1],
                    y=filtered_y + [0] * len(filtered_y),
                    fill="toself",
                    fillcolor=f"rgba({rgb[4:-1]},0.35)",
                    line={"color": color, "width": 2},
                    name=label,
                    hovertemplate=f"{label}: %{{y:.1f}}<extra></extra>",
                )
            )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={
                "family": theme.fonts["family"],
                "size": theme.fonts["axis_label"],
                "color": theme.colors["text_muted"],
            },
            margin={"l": 20, "r": 20, "t": 20, "b": 40},
            xaxis={
                "showgrid": False,
                "zeroline": True,
                "zerolinecolor": "rgba(255,255,255,0.3)",
                "zerolinewidth": 1.5,
                "tickangle": 0,
                "tickformat": "%b%y",
                "dtick": "M3",
                "linecolor": "rgba(255,255,255,0.2)",
                "linewidth": 1.5,
            },
            yaxis={
                "showgrid": False,
                "zeroline": True,
                "zerolinecolor": "rgba(255,255,255,0.3)",
                "zerolinewidth": 1.5,
                "linecolor": "rgba(255,255,255,0.2)",
                "linewidth": 1.5,
            },
            legend={
                "orientation": "h",
                "yanchor": "bottom",
                "y": 1.02,
                "xanchor": "center",
                "x": 0.5,
                "font": {"size": 10},
            },
            hovermode="x unified",
            hoverlabel={
                "bgcolor": "rgba(20,20,40,0.85)",
                "bordercolor": "rgba(255,255,255,0.3)",
                "font": {"color": "white", "size": 12, "family": theme.fonts["family"]},
                "align": "left",
            },
        )

        return fig

    if internal_wrap:
        return html.Div(
            html.Div(
                className="glass-card",
                style={"padding": "15px"},
                children=[chart_container],
            ),
            **kwargs,
        )
    return chart_container

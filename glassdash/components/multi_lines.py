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


@_with_validation
def MultiLinesChart(
    dataframe,
    x="month",
    lines=None,
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

    if lines is None:
        lines = {"Line 1": "value1", "Line 2": "value2"}
    if colors is None:
        color_cycle = ["accent", "purple", "cyan", "success", "warning"]
        colors = {k: color_cycle[i % len(color_cycle)] for i, k in enumerate(lines)}

    chart_id = id or f"multi-lines-{uuid.uuid4().hex[:8]}"

    x_dates_all = parse_month_strings(dataframe[x].to_list())
    segment_keys = list(lines.keys())

    toggle_btn, overlay, hidden_filter_state = create_popup_filter_panel(
        chart_id, x_dates_all, categories=segment_keys
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
    def update_chart(selected_categories, start_date, end_date):
        if not selected_categories:
            selected_categories = segment_keys

        selected_set = set(selected_categories)
        filtered_dates = apply_date_filter(x_dates_all, start_date, end_date)

        fig = go.Figure()

        for label, col in lines.items():
            if label not in selected_set:
                continue

            color_key = colors.get(label, "accent")
            line_color = theme.colors.get(color_key, theme.colors["accent"])
            y_all = dataframe[col].to_list()
            date_to_y = dict(zip(x_dates_all, y_all, strict=False))
            filtered_y = [date_to_y.get(d, 0) for d in filtered_dates]

            fig.add_trace(
                go.Scatter(
                    x=filtered_dates,
                    y=filtered_y,
                    mode="lines",
                    name=label,
                    line={"color": line_color, "width": 2},
                    hovertemplate=f"{label}: %{{y:.1f}}<extra></extra>",
                )
            )

            if highlight_current and len(filtered_dates) > 0:
                fig.add_trace(
                    go.Scatter(
                        x=[filtered_dates[-1]],
                        y=[filtered_y[-1]],
                        mode="markers",
                        marker={"color": line_color, "size": 8},
                        showlegend=False,
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

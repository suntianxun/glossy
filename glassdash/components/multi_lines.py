import datetime
import uuid

from dash import Input, Output, callback, dcc, html
from plotly import graph_objects as go

from glassdash.components._base import _with_validation
from glassdash.theme import GlassTheme


@_with_validation
def MultiLinesChart(
    dataframe,
    x="month",
    lines=None,
    colors=None,
    highlight_current=True,
    theme=None,
    id=None,
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
    filter_id = f"{chart_id}-filter"

    x_str_all = dataframe[x].to_list()
    x_dates_all = []
    for s in x_str_all:
        try:
            parts = s.split("-")
            d = datetime.date(int(parts[0]), int(parts[1]), 1)
            x_dates_all.append(d)
        except (ValueError, IndexError):
            x_dates_all.append(datetime.date.today())

    segment_keys = list(lines.keys())

    filter_panel = html.Div(
        [
            html.Div(
                [
                    html.Span(
                        "Categories:",
                        style={
                            "color": "white",
                            "fontSize": "11px",
                            "marginRight": "8px",
                        },
                    ),
                    dcc.Checklist(
                        id=f"{chart_id}-categories",
                        options=[{"label": seg, "value": seg} for seg in segment_keys],
                        value=segment_keys,
                        inline=True,
                        inputStyle={"marginRight": "4px", "cursor": "pointer"},
                        labelStyle={
                            "color": "white",
                            "fontSize": "11px",
                            "marginRight": "12px",
                            "cursor": "pointer",
                        },
                    ),
                ],
                style={"marginBottom": "8px"},
            ),
            html.Div(
                [
                    html.Span(
                        "From:",
                        style={
                            "color": "white",
                            "fontSize": "11px",
                            "marginRight": "8px",
                        },
                    ),
                    dcc.Input(
                        id=f"{chart_id}-start-date",
                        type="text",
                        value=x_dates_all[0].strftime("%Y-%m-%d") if x_dates_all else "",
                        placeholder="YYYY-MM-DD",
                        style={
                            "background": "rgba(255,255,255,0.1)",
                            "border": "1px solid rgba(255,255,255,0.2)",
                            "borderRadius": "8px",
                            "color": "white",
                            "fontSize": "11px",
                            "padding": "4px 8px",
                            "width": "100px",
                            "marginRight": "16px",
                        },
                    ),
                    html.Span(
                        "To:",
                        style={
                            "color": "white",
                            "fontSize": "11px",
                            "marginRight": "8px",
                        },
                    ),
                    dcc.Input(
                        id=f"{chart_id}-end-date",
                        type="text",
                        value=x_dates_all[-1].strftime("%Y-%m-%d") if x_dates_all else "",
                        placeholder="YYYY-MM-DD",
                        style={
                            "background": "rgba(255,255,255,0.1)",
                            "border": "1px solid rgba(255,255,255,0.2)",
                            "borderRadius": "8px",
                            "color": "white",
                            "fontSize": "11px",
                            "padding": "4px 8px",
                            "width": "100px",
                        },
                    ),
                ],
                style={"display": "flex", "alignItems": "center"},
            ),
        ],
        id=filter_id,
        className="glass-filter-panel",
        style={"display": "none"},
    )

    toggle_btn = html.Div(
        html.Button(
            "⚙ Filter",
            id=f"{chart_id}-toggle-filter",
            n_clicks=0,
            style={
                "background": "rgba(255,255,255,0.1)",
                "border": "1px solid rgba(255,255,255,0.2)",
                "borderRadius": "8px",
                "color": "white",
                "fontSize": "11px",
                "padding": "4px 12px",
                "cursor": "pointer",
            },
        )
    )

    graph = dcc.Graph(id=chart_id, style={"height": "200px"})

    chart_container = html.Div(
        [
            html.Div(
                toggle_btn,
                style={
                    "textAlign": "right",
                    "marginBottom": "5px",
                    "position": "relative",
                    "zIndex": 100,
                },
            ),
            filter_panel,
            html.Div(graph, className="glass-chart-container"),
        ]
    )

    @callback(
        Output(filter_id, "style"),
        Input(f"{chart_id}-toggle-filter", "n_clicks"),
    )
    def toggle_filter(n_clicks):
        if n_clicks % 2 == 1:
            return {"display": "block"}
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

        filtered_dates = x_dates_all
        if start_date:
            try:
                if isinstance(start_date, str):
                    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
                filtered_dates = [d for d in filtered_dates if d >= start_date]
            except (ValueError, TypeError):
                pass
        if end_date:
            try:
                if isinstance(end_date, str):
                    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
                filtered_dates = [d for d in filtered_dates if d <= end_date]
            except (ValueError, TypeError):
                pass

        if not filtered_dates:
            filtered_dates = x_dates_all

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
                "tickangle": -45,
                "tickformat": "%b%y",
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

    return html.Div(
        html.Div(
            className="glass-card",
            style={"padding": "15px"},
            children=[chart_container],
        ),
        **kwargs,
    )

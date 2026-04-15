import datetime
import uuid

from dash import Input, Output, callback, dcc, html
from plotly import graph_objects as go

from glassdash.components._base import _with_validation
from glassdash.theme import GlassTheme


def hex_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return f"rgb({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)})"


@_with_validation
def DualAreaChart(
    dataframe,
    x="month",
    y1="value1",
    y2="value2",
    color1="accent",
    color2="purple",
    labels=None,
    highlight_current=True,
    theme=None,
    id=None,
    **kwargs,
):
    if theme is None:
        theme = GlassTheme()

    if labels is None:
        labels = [y1, y2]

    chart_id = id or f"dual-area-{uuid.uuid4().hex[:8]}"
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

    filter_panel = html.Div(
        [
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

    graph = dcc.Graph(id=chart_id, style={"height": "100%", "min-height": "200px"})

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
        Input(f"{chart_id}-start-date", "value"),
        Input(f"{chart_id}-end-date", "value"),
    )
    def update_chart(start_date, end_date):
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

        c1 = theme.colors.get(color1, theme.colors["accent"])
        c2 = theme.colors.get(color2, theme.colors["purple"])

        rgb1 = hex_to_rgb(c1)
        rgb2 = hex_to_rgb(c2)

        y1_all = dataframe[y1].to_list()
        y2_all = dataframe[y2].to_list()
        date_to_y1 = dict(zip(x_dates_all, y1_all, strict=False))
        date_to_y2 = dict(zip(x_dates_all, y2_all, strict=False))

        filtered_y1 = [date_to_y1.get(d, 0) for d in filtered_dates]
        filtered_y2 = [date_to_y2.get(d, 0) for d in filtered_dates]

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=filtered_dates + filtered_dates[::-1],
                y=filtered_y1 + [0] * len(filtered_y1),
                fill="toself",
                fillcolor=f"rgba({rgb1[4:-1]},0.4)",
                line={"color": c1, "width": 2},
                name=labels[0],
                hovertemplate=f"{labels[0]}: %{{y:.1f}}<extra></extra>",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=filtered_dates + filtered_dates[::-1],
                y=filtered_y2 + [0] * len(filtered_y2),
                fill="toself",
                fillcolor=f"rgba({rgb2[4:-1]},0.4)",
                line={"color": c2, "width": 2},
                name=labels[1],
                hovertemplate=f"{labels[1]}: %{{y:.1f}}<extra></extra>",
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
            style={"padding": "15px", "height": "100%", "box-sizing": "border-box"},
            children=[chart_container],
        ),
        **kwargs,
    )

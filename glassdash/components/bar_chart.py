import datetime
import uuid
import polars as pl
from dash import html, dcc, callback, Input, Output
from plotly import graph_objects as go
from glassdash.theme import GlassTheme


def BarChart(
    dataframe,
    x="month",
    y="value",
    color="purple",
    highlight_current=True,
    theme=None,
    id=None,
    **kwargs,
):
    if theme is None:
        theme = GlassTheme()

    chart_id = id or f"bar-chart-{uuid.uuid4().hex[:8]}"
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
                        value=x_dates_all[0].strftime("%Y-%m-%d")
                        if x_dates_all
                        else "",
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
                        value=x_dates_all[-1].strftime("%Y-%m-%d")
                        if x_dates_all
                        else "",
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
        Input(f"{chart_id}-start-date", "value"),
        Input(f"{chart_id}-end-date", "value"),
    )
    def update_chart(start_date, end_date):
        filtered_dates = x_dates_all
        if start_date:
            try:
                if isinstance(start_date, str):
                    start_date = datetime.datetime.strptime(
                        start_date, "%Y-%m-%d"
                    ).date()
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

        bar_color = theme.colors.get(color, theme.colors["purple"])
        y_all = dataframe[y].to_list()
        date_to_y = dict(zip(x_dates_all, y_all))

        filtered_y = [date_to_y.get(d, 0) for d in filtered_dates]

        fig = go.Figure()

        h = bar_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

        if len(filtered_dates) > 1:
            fig.add_trace(
                go.Bar(
                    x=filtered_dates[:-1],
                    y=filtered_y[:-1],
                    marker=dict(
                        color=bar_color,
                        line=dict(width=0),
                        cornerradius=4,
                    ),
                    hovertemplate=f"<b>{y}</b><br>Value: %{{y:.1f}}<extra></extra>",
                    hoverlabel=dict(
                        bgcolor=bar_color,
                        font=dict(color="white", size=12, family=theme.fonts["family"]),
                    ),
                )
            )

        accent_color = theme.colors["accent"]

        fig.add_trace(
            go.Bar(
                x=[filtered_dates[-1]],
                y=[filtered_y[-1]],
                marker=dict(
                    color=accent_color,
                    line=dict(width=0),
                    cornerradius=4,
                ),
                hovertemplate=f"<b>{y}</b><br>Value: %{{y:.1f}}<extra></extra>",
                hoverlabel=dict(
                    bgcolor=accent_color,
                    font=dict(color="white", size=12, family=theme.fonts["family"]),
                ),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=filtered_dates,
                y=[max(filtered_y) * 1.1] * len(filtered_dates),
                mode="lines",
                line=dict(color="rgba(255,255,255,0.08)", width=1),
                hoverinfo="skip",
            )
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                family=theme.fonts["family"],
                size=theme.fonts["axis_label"],
                color=theme.colors["text_muted"],
            ),
            margin=dict(l=20, r=20, t=30, b=40),
            xaxis=dict(
                showgrid=False,
                zeroline=True,
                zerolinecolor="rgba(255,255,255,0.3)",
                zerolinewidth=1.5,
                tickangle=-45,
                tickformat="%b%y",
                linecolor="rgba(255,255,255,0.2)",
                linewidth=1.5,
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=True,
                zerolinecolor="rgba(255,255,255,0.3)",
                zerolinewidth=1.5,
                linecolor="rgba(255,255,255,0.2)",
                linewidth=1.5,
            ),
            hovermode="closest",
            hoverdistance=-1,
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

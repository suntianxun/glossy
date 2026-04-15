"""StackedBarChart - stacked proportional bar chart."""

import datetime
import uuid

from dash import Input, Output, callback, dcc, html
from plotly import graph_objects as go

from glassdash.components._base import _with_validation
from glassdash.theme import GlassTheme


@_with_validation
def StackedBarChart(
    dataframe,
    x="month",
    segments=None,
    colors=None,
    highlight_current=True,
    theme=None,
    id=None,
    **kwargs,
):
    if theme is None:
        theme = GlassTheme()

    if segments is None:
        segments = {
            "Full-time": "fte_ft",
            "Part-time": "fte_pt",
            "Contingent": "fte_cont",
            "Others": "fte_other",
        }
    if colors is None:
        colors = {
            "Full-time": "dark_yellow",
            "Part-time": "accent",
            "Contingent": "purple",
            "Others": "cyan",
        }

    chart_id = id or f"stacked-bar-{uuid.uuid4().hex[:8]}"
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

    segment_keys = list(segments.keys())

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
                        style={"display": "inline-block"},
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

    segment_keys = list(segments.keys())

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
                        style={"display": "inline-block"},
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

    graph = dcc.Graph(
        id=chart_id,
        style={"height": "250px"},
    )

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

        last_idx = len(filtered_dates) - 1

        for label, col in segments.items():
            if label not in selected_set:
                continue

            color_key = colors.get(label, "primary")
            bar_color = theme.colors.get(color_key, theme.colors["primary"])
            h = bar_color.lstrip("#")
            r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

            y_values = dataframe[col].to_list()

            date_to_y = dict(zip(x_dates_all, y_values))

            for date_idx, xd in enumerate(filtered_dates):
                is_current = date_idx == last_idx
                opacity = 1.0 if is_current else 0.85
                yv = date_to_y.get(xd, 0)

                fig.add_trace(
                    go.Bar(
                        x=[xd],
                        y=[yv],
                        name=label if date_idx == 0 else None,
                        marker=dict(
                            color=bar_color,
                            line=dict(width=0),
                            cornerradius=4,
                        ),
                        hovertemplate=f"<b>{label}</b><br>Value: {yv}<extra></extra>",
                        showlegend=(date_idx == 0),
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
            margin=dict(l=20, r=20, t=20, b=40),
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
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.08,
                xanchor="center",
                x=0.5,
                font=dict(size=10),
            ),
            barmode="stack",
            hovermode="x unified",
            showlegend=True,
            hoverlabel=dict(
                bgcolor="rgba(20,20,40,0.85)",
                bordercolor="rgba(255,255,255,0.3)",
                font=dict(color="white", size=12, family=theme.fonts["family"]),
                align="left",
            ),
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

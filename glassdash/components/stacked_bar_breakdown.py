"""StackedBarWithBreakdown - stacked bar + horizontal breakdown bars."""

import datetime
import uuid

from dash import Input, Output, callback, dcc, html
from plotly import graph_objects as go

from glassdash.components._base import _with_validation
from glassdash.theme import GlassTheme


@_with_validation
def StackedBarWithBreakdown(
    dataframe,
    x="month",
    bar_segments=None,
    colors=None,
    breakdown=None,
    highlight_current=True,
    theme=None,
    id=None,
    **kwargs,
):
    if theme is None:
        theme = GlassTheme()

    if bar_segments is None:
        bar_segments = {
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
    if breakdown is None:
        breakdown = {
            "Full-time": {"Analyst": 0.3, "Engineer": 0.4, "Sales": 0.2, "Others": 0.1},
            "Part-time": {"Morning": 0.5, "Afternoon": 0.5},
            "Contingent": {"Contractor": 0.6, "Temp": 0.4},
            "Others": {"External": 0.7, "Internal": 0.3},
        }

    chart_id = id or f"stacked-bar-breakdown-{uuid.uuid4().hex[:8]}"
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

    segment_keys = list(bar_segments.keys())

    filter_panel = html.Div(
        [
            html.Div(
                [
                    html.Span(
                        "Breakdown:",
                        style={
                            "color": "white",
                            "fontSize": "11px",
                            "marginRight": "8px",
                        },
                    ),
                    dcc.Dropdown(
                        id=f"{chart_id}-category",
                        options=[{"label": seg, "value": seg} for seg in segment_keys],
                        value=segment_keys[0],
                        clearable=False,
                        style={
                            "background": "rgba(255,255,255,0.1)",
                            "border": "1px solid rgba(255,255,255,0.2)",
                            "borderRadius": "8px",
                            "color": "black",
                            "fontSize": "11px",
                            "width": "150px",
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "marginBottom": "8px",
                },
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

    stacked_graph = dcc.Graph(id=f"{chart_id}-stacked", style={"height": "100%"})
    breakdown_graph = dcc.Graph(id=f"{chart_id}-breakdown", style={"height": "100%"})

    divider = html.Div(
        style={
            "width": "1px",
            "background": theme.colors["glass_border"],
            "margin": "0 10px",
            "boxShadow": "0 0 10px rgba(255,255,255,0.1)",
        }
    )

    charts_row = html.Div(
        [
            html.Div(stacked_graph, style={"flex": "1"}),
            divider,
            html.Div(breakdown_graph, style={"flex": "1"}),
        ],
        style={"display": "flex", "alignItems": "stretch"},
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
            charts_row,
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
        Output(f"{chart_id}-stacked", "figure"),
        Output(f"{chart_id}-breakdown", "figure"),
        Input(f"{chart_id}-category", "value"),
        Input(f"{chart_id}-start-date", "value"),
        Input(f"{chart_id}-end-date", "value"),
    )
    def update_charts(selected_category, start_date, end_date):
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

        len(filtered_dates) - 1

        stacked_fig = go.Figure()
        for label, col in bar_segments.items():
            color_key = colors.get(label, "primary")
            bar_color = theme.colors.get(color_key, theme.colors["primary"])
            h = bar_color.lstrip("#")
            _r, _g, _b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

            y_values = dataframe[col].to_list()
            date_to_y = dict(zip(x_dates_all, y_values, strict=False))

            for date_idx, xd in enumerate(filtered_dates):
                yv = date_to_y.get(xd, 0)

                stacked_fig.add_trace(
                    go.Bar(
                        x=[xd],
                        y=[yv],
                        name=label if date_idx == 0 else None,
                        marker={
                            "color": bar_color,
                            "line": {"width": 0},
                            "cornerradius": 4,
                        },
                        hovertemplate=f"<b>{label}</b><br>Value: {yv}<extra></extra>",
                        showlegend=(date_idx == 0),
                    )
                )

        stacked_fig.update_layout(
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
                "y": 1.08,
                "xanchor": "center",
                "x": 0.5,
                "font": {"size": 10},
            },
            barmode="stack",
            hovermode="x unified",
            showlegend=True,
            hoverlabel={
                "bgcolor": "rgba(20,20,40,0.85)",
                "bordercolor": "rgba(255,255,255,0.3)",
                "font": {"color": "white", "size": 12, "family": theme.fonts["family"]},
                "align": "left",
            },
        )

        breakdown_data = breakdown.get(selected_category, {})
        breakdown_labels = list(breakdown_data.keys())
        breakdown_fractions = list(breakdown_data.values())

        segment_col = bar_segments.get(selected_category, "")
        category_values = dataframe[segment_col].to_list() if segment_col else []
        date_to_cat_value = dict(zip(x_dates_all, category_values, strict=False))

        segment_color_key = colors.get(selected_category, "primary")
        base_color = theme.colors.get(segment_color_key, theme.colors["primary"])
        h = base_color.lstrip("#")
        _r, _g, _b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

        breakdown_fig = go.Figure()

        for date_idx, xd in enumerate(filtered_dates):
            cat_value = date_to_cat_value.get(xd, 0)

            for blabel, bfrac in zip(breakdown_labels, breakdown_fractions, strict=False):
                actual_value = cat_value * bfrac
                breakdown_fig.add_trace(
                    go.Bar(
                        x=[actual_value],
                        y=[xd],
                        orientation="h",
                        name=f"{blabel}" if date_idx == 0 else None,
                        marker={
                            "color": base_color,
                            "line": {"width": 0},
                            "cornerradius": 3,
                        },
                        hovertemplate=f"<b>{blabel}</b><br>{xd.strftime('%Y-%m')}: {actual_value:.1f}<extra></extra>",
                        showlegend=(date_idx == 0),
                    )
                )

        breakdown_fig.update_layout(
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
                "linecolor": "rgba(255,255,255,0.2)",
                "linewidth": 1.5,
            },
            yaxis={
                "showgrid": False,
                "zeroline": True,
                "zerolinecolor": "rgba(255,255,255,0.3)",
                "zerolinewidth": 1.5,
                "tickformat": "%Y-%m",
                "autorange": "reversed",
                "linecolor": "rgba(255,255,255,0.2)",
                "linewidth": 1.5,
            },
            barmode="stack",
            hovermode="y unified",
            showlegend=True,
            legend={
                "orientation": "h",
                "yanchor": "bottom",
                "y": 1.08,
                "xanchor": "center",
                "x": 0.5,
                "font": {"size": 10},
            },
            hoverlabel={
                "bgcolor": "rgba(20,20,40,0.85)",
                "bordercolor": "rgba(255,255,255,0.3)",
                "font": {"color": "white", "size": 12, "family": theme.fonts["family"]},
                "align": "left",
            },
        )

        return stacked_fig, breakdown_fig

    return html.Div(
        html.Div(
            className="glass-card",
            style={"padding": "15px"},
            children=[chart_container],
        ),
        **kwargs,
    )

import uuid

import polars as pl
from dash import Input, Output, callback, dcc, html
from plotly import graph_objects as go

from glassdash.components._base import _with_validation
from glassdash.theme import GlassTheme


@_with_validation
def StackedBarHorizontalChart(
    dataframe,
    category="category",
    subcategory="subcategory",
    value="value",
    title=None,
    colors=None,
    theme=None,
    id=None,
    internal_wrap=True,
    show_filter=True,
    **kwargs,
):
    if theme is None:
        theme = GlassTheme()

    if colors is None:
        colors = ["primary", "accent", "purple", "cyan", "dark_yellow", "success"]

    chart_id = id or f"stacked-bar-h-{uuid.uuid4().hex[:8]}"

    all_categories = dataframe[category].unique().to_list()
    all_subcategories = dataframe[subcategory].unique().to_list()

    toggle_btn = html.Button(
        "⚙ Filter",
        id=f"{chart_id}-toggle-filter",
        n_clicks=0,
        style={
            "background": "rgba(255,255,255,0.1)",
            "border": "1px solid rgba(255,255,255,0.2)",
            "borderRadius": "4px",
            "color": "white",
            "cursor": "pointer",
            "padding": "4px 12px",
            "fontSize": "12px",
        },
    )

    popup_content = html.Div(
        [
            html.Div(
                "Filter",
                style={
                    "color": "white",
                    "fontSize": "14px",
                    "fontWeight": "bold",
                    "marginBottom": "12px",
                },
            ),
            html.Div(
                [
                    html.Span(
                        "Categories:",
                        style={"color": "white", "fontSize": "11px", "marginRight": "8px"},
                    ),
                    dcc.Checklist(
                        id=f"{chart_id}-categories",
                        options=[{"label": cat, "value": cat} for cat in all_categories],
                        value=all_categories,
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
        ],
        style={
            "background": "rgba(30,30,50,0.95)",
            "border": "1px solid rgba(255,255,255,0.2)",
            "borderRadius": "12px",
            "padding": "16px",
            "minWidth": "280px",
        },
    )

    overlay = html.Div(
        popup_content,
        id=f"{chart_id}-filter-overlay",
        style={
            "display": "none",
            "position": "fixed",
            "top": "50%",
            "left": "50%",
            "transform": "translate(-50%, -50%)",
            "zIndex": 1000,
        },
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
    )
    def update_chart(selected_categories):
        if not selected_categories:
            selected_categories = all_categories

        selected_set = set(selected_categories)

        filtered_df = dataframe.filter(pl.col(category).is_in(selected_set))

        fig = go.Figure()

        for i, subcat in enumerate(all_subcategories):
            subcat_color = theme.colors.get(colors[i % len(colors)], theme.colors["primary"])

            for cat in selected_categories:
                cat_data = filtered_df.filter(
                    (pl.col(category) == cat) & (pl.col(subcategory) == subcat)
                )

                if cat_data.is_empty():
                    continue

                val = cat_data[value].to_list()[0]

                fig.add_trace(
                    go.Bar(
                        x=[val],
                        y=[cat],
                        orientation="h",
                        name=subcat,
                        marker={
                            "color": subcat_color,
                            "line": {"width": 0},
                            "cornerradius": 4,
                        },
                        hovertemplate=f"<b>{subcat}</b><br>Value: {val}<extra></extra>",
                        showlegend=(cat == selected_categories[0]),
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
                "linecolor": "rgba(255,255,255,0.2)",
                "linewidth": 1.5,
            },
            yaxis={
                "showgrid": False,
                "zeroline": False,
                "linecolor": "rgba(255,255,255,0.2)",
                "linewidth": 1.5,
                "categoryorder": "array",
                "categoryarray": selected_categories,
            },
            legend={
                "orientation": "h",
                "yanchor": "bottom",
                "y": 1.02,
                "xanchor": "center",
                "x": 0.5,
                "font": {"size": 10},
            },
            barmode="stack",
            hovermode="y unified",
            showlegend=True,
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

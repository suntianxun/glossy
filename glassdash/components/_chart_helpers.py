"""Shared chart helpers for GlassDash components."""

import datetime

from dash import dcc, html


def parse_month_strings(month_strings):
    """Convert YYYY-MM strings to datetime.date objects."""
    dates = []
    for s in month_strings:
        try:
            parts = s.split("-")
            d = datetime.date(int(parts[0]), int(parts[1]), 1)
            dates.append(d)
        except (ValueError, IndexError):
            dates.append(datetime.date.today())
    return dates


def apply_date_filter(all_dates, start_date=None, end_date=None):
    """Filter dates by start/end bounds."""
    filtered = list(all_dates)
    if start_date:
        try:
            if isinstance(start_date, str):
                start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            filtered = [d for d in filtered if d >= start_date]
        except (ValueError, TypeError):
            pass
    if end_date:
        try:
            if isinstance(end_date, str):
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            filtered = [d for d in filtered if d <= end_date]
        except (ValueError, TypeError):
            pass
    return filtered or all_dates


STANDARD_BUTTON_STYLE = {
    "background": "rgba(255,255,255,0.1)",
    "border": "1px solid rgba(255,255,255,0.2)",
    "borderRadius": "8px",
    "color": "white",
    "fontSize": "11px",
    "padding": "4px 12px",
    "cursor": "pointer",
}

STANDARD_INPUT_STYLE = {
    "background": "rgba(255,255,255,0.1)",
    "border": "1px solid rgba(255,255,255,0.2)",
    "borderRadius": "8px",
    "color": "white",
    "fontSize": "11px",
    "padding": "4px 8px",
    "width": "100px",
}


def create_popup_filter_panel(chart_id, x_dates_all, categories=None):
    """Create a popup filter panel with overlay.

    Returns toggle button and popup div that can be used in a chart.
    The popup appears centered on screen when filter button is clicked.
    """
    filter_id = f"{chart_id}-filter"
    popup_id = f"{chart_id}-filter-popup"

    toggle_btn = html.Div(
        html.Button(
            "⚙ Filter",
            id=f"{chart_id}-toggle-filter",
            n_clicks=0,
            style=STANDARD_BUTTON_STYLE,
        )
    )

    category_controls = []
    if categories:
        category_controls.append(
            html.Div(
                [
                    html.Span(
                        "Categories:",
                        style={"color": "white", "fontSize": "11px", "marginRight": "8px"},
                    ),
                    dcc.Checklist(
                        id=f"{chart_id}-categories",
                        options=[{"label": cat, "value": cat} for cat in categories],
                        value=categories,
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
            )
        )

    date_controls = html.Div(
        [
            html.Span(
                "From:",
                style={"color": "white", "fontSize": "11px", "marginRight": "8px"},
            ),
            dcc.Input(
                id=f"{chart_id}-start-date",
                type="text",
                value=x_dates_all[0].strftime("%Y-%m-%d") if x_dates_all else "",
                placeholder="YYYY-MM-DD",
                style=STANDARD_INPUT_STYLE,
            ),
            html.Span(
                "To:",
                style={
                    "color": "white",
                    "fontSize": "11px",
                    "marginRight": "8px",
                    "marginLeft": "16px",
                },
            ),
            dcc.Input(
                id=f"{chart_id}-end-date",
                type="text",
                value=x_dates_all[-1].strftime("%Y-%m-%d") if x_dates_all else "",
                placeholder="YYYY-MM-DD",
                style=STANDARD_INPUT_STYLE,
            ),
        ],
        style={"display": "flex", "alignItems": "center"},
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
            *category_controls,
            date_controls,
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
        id=popup_id,
        style={
            "display": "none",
            "position": "fixed",
            "top": "50%",
            "left": "50%",
            "transform": "translate(-50%, -50%)",
            "zIndex": 1000,
        },
    )

    hidden_filter_state = html.Div(id=filter_id, style={"display": "none"})

    return toggle_btn, overlay, hidden_filter_state


def build_standard_layout(theme, hovermode="x unified"):
    """Build standard Plotly layout with glass theme."""
    return {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {
            "family": theme.fonts["family"],
            "size": theme.fonts["axis_label"],
            "color": theme.colors["text_muted"],
        },
        "margin": {"l": 20, "r": 20, "t": 20, "b": 60},
        "xaxis": {
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
        "yaxis": {
            "showgrid": False,
            "zeroline": True,
            "zerolinecolor": "rgba(255,255,255,0.3)",
            "zerolinewidth": 1.5,
            "linecolor": "rgba(255,255,255,0.2)",
            "linewidth": 1.5,
        },
        "hovermode": hovermode,
        "hoverlabel": {
            "bgcolor": "rgba(20,20,40,0.85)",
            "bordercolor": "rgba(255,255,255,0.3)",
            "font": {"color": "white", "size": 12, "family": theme.fonts["family"]},
            "align": "left",
        },
    }

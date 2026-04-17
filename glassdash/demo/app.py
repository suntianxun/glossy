"""Demo dashboard with multi-page navigation."""

import os

from dash import Dash, Input, Output, State, dcc, html


def create_demo_app():
    app = Dash(
        __name__,
        assets_folder=os.path.join(os.path.dirname(__file__), "..", "assets"),
    )

    from glassdash import GlassTheme
    from glassdash.demo.pages.finance import FinancePage
    from glassdash.demo.pages.sales import SalesPage
    from glassdash.demo.pages.workforce import WorkforcePage

    theme = GlassTheme()

    nav_items = [
        {"id": "workforce", "label": "Workforce", "icon": "👥"},
        {"id": "finance", "label": "Finance", "icon": "💰"},
        {"id": "sales", "label": "Sales", "icon": "📊"},
    ]

    sidebar = html.Div(
        [
            html.Div(
                [
                    html.Div(className="glass-sidebar-logo"),
                    html.Span("GlassDash", className="glass-sidebar-title"),
                ],
                className="glass-sidebar-header",
            ),
        ]
        + [
            html.Div(
                [
                    html.Div(item["icon"], className="glass-sidebar-icon"),
                    html.Span(item["label"], className="glass-sidebar-label"),
                ],
                className=f"glass-sidebar-item {'active' if item['id'] == 'workforce' else ''}",
                id=f"nav-{item['id']}",
            )
            for item in nav_items
        ],
        id="sidebar",
        className="glass-sidebar",
    )

    content = html.Div(id="page-content", className="glass-main-content")

    url = dcc.Location(id="url", refresh=False)

    app.layout = html.Div([url, sidebar, content])

    @app.callback(
        Output("page-content", "children"),
        Output("sidebar", "children"),
        Input("url", "pathname"),
        [State("sidebar", "children")],
    )
    def render_page(pathname, sidebar_children):
        page_id = pathname.lstrip("/") if pathname else "workforce"

        if page_id not in ["workforce", "finance", "sales"]:
            page_id = "workforce"

        page_funcs = {
            "workforce": WorkforcePage,
            "finance": FinancePage,
            "sales": SalesPage,
        }

        page_func = page_funcs.get(page_id, WorkforcePage)

        header = sidebar_children[0]

        new_nav = [
            html.Div(
                [
                    html.Div(item["icon"], className="glass-sidebar-icon"),
                    html.Span(item["label"], className="glass-sidebar-label"),
                ],
                className=f"glass-sidebar-item {'active' if item['id'] == page_id else ''}",
                id=f"nav-{item['id']}",
            )
            for item in nav_items
        ]

        return page_func(theme=theme), [header] + new_nav

    @app.callback(
        Output("url", "pathname"),
        Input("nav-workforce", "n_clicks"),
        Input("nav-finance", "n_clicks"),
        Input("nav-sales", "n_clicks"),
    )
    def update_url(n_workforce, n_finance, n_sales):
        import dash

        ctx = dash.callback_context
        if not ctx.triggered:
            return "/workforce"
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
        page_id = triggered_id.replace("nav-", "")
        return f"/{page_id}"

    return app


if __name__ == "__main__":
    app = create_demo_app()
    app.run(debug=True, port=8050)

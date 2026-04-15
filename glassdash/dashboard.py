from dash import html

from glassdash.theme import GlassTheme


def GlassDashboard(title="Dashboard", date_range=None, theme=None, children=None, **kwargs):
    if theme is None:
        theme = GlassTheme()

    header = html.Div(
        [
            html.H1(
                title,
                style={
                    "fontSize": "24px",
                    "fontWeight": "700",
                    "background": "linear-gradient(135deg, #4facfe, #06b6d4)",
                    "-webkit-background-clip": "text",
                    "-webkit-text-fill-color": "transparent",
                    "marginBottom": "8px",
                },
            ),
        ],
        style={"textAlign": "center", "marginBottom": "24px"},
    )

    if date_range:
        header.children.append(
            html.Div(
                f"{date_range[0]} → {date_range[1]}",
                style={"color": theme.colors["text_muted"], "fontSize": "12px"},
            )
        )

    content = html.Div(children, style={"maxWidth": "1400px", "margin": "0 auto"})

    return html.Div(
        [
            html.Link(
                href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
                rel="stylesheet",
            ),
            html.Link(href="/assets/glass.css", rel="stylesheet"),
            header,
            content,
        ],
        **kwargs,
    )


def Section(title: str, description: str = None, children=None, theme=None, **kwargs) -> html.Div:
    theme = theme or GlassTheme()

    header = html.Div(
        [
            html.H2(title, className="glass-section-title"),
            html.P(description, className="glass-section-description") if description else None,
        ],
        className="glass-section-header",
    )

    return html.Div(
        [header, html.Div(children, className="glass-section-children")],
        className="glass-section",
        **kwargs,
    )

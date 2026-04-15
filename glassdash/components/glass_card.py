"""GlassCard - frosted glass container component."""

from dash import html

from glassdash.theme import GlassTheme


def GlassCard(children=None, title=None, theme=None, **kwargs):
    if theme is None:
        theme = GlassTheme()

    content = []
    if title:
        content.append(html.H3(title, className="glass-chart-title"))
    content.append(html.Div(children))

    return html.Div(
        content, className="glass-card", style={"marginBottom": "20px"}, **kwargs
    )

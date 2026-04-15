from dash import html

from glassdash.theme import GlassTheme


def GlassDashboard(
    title="Dashboard",
    date_range=None,
    theme=None,
    columns=3,
    children=None,
    **kwargs,
):
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

    grid_style = {
        "display": "grid",
        "gridTemplateColumns": f"repeat({columns}, 1fr)",
        "gap": "24px",
        "maxWidth": "1400px",
        "margin": "0 auto",
    }

    content = html.Div(children, style=grid_style)

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


def Section(
    title: str,
    description: str = None,
    children=None,
    theme=None,
    height=None,
    width=None,
    **kwargs,
) -> html.Div:
    theme = theme or GlassTheme()

    existing_class = kwargs.pop("className", "")
    section_class = "glass-section"
    if existing_class:
        section_class = f"{section_class} {existing_class}"

    style = {}
    if height is not None:
        style["height"] = f"{height}px"
    if width is not None:
        style["width"] = f"{width}px"
    if style:
        kwargs["style"] = {**(kwargs.get("style") or {}), **style}

    child_list = children if isinstance(children, list) else [children]
    n_children = len(child_list) if child_list else 0

    if height is not None and n_children > 0:
        children_style = {
            "display": "grid",
            "gap": "20px",
            "gridTemplateRows": f"repeat({n_children}, 1fr)",
            "height": "100%",
        }
    else:
        children_style = {"display": "grid", "gap": "20px"}

    return html.Div(
        [
            html.Div(
                [
                    html.H2(title, className="glass-section-title"),
                    html.P(description, className="glass-section-description")
                    if description
                    else None,
                ],
                className="glass-section-header",
            ),
            html.Div(children, className="glass-section-children", style=children_style),
            html.Div(className="glass-section-divider"),
        ],
        className=section_class,
        **kwargs,
    )

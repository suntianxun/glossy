# GlassDash Sidebar Navigation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a collapsible glassmorphic left sidebar to the GlassDash demo with three pages: Workforce, Finance, and Sales Statistics.

**Architecture:** Dash multi-page app using `dcc.Location` for URL routing and callbacks to swap page content. Sidebar state (expanded/collapsed) managed via a Dash `Store` component. Each page is a separate function returning a `html.Div`.

**Tech Stack:** Dash, Plotly, Polars, glassmorphism CSS

---

## File Inventory

| File | Action | Purpose |
|------|--------|---------|
| `glassdash/assets/glass.css` | Modify | Add sidebar CSS classes |
| `glassdash/demo/app.py` | Modify | Restructure as multi-page app with sidebar |
| `glassdash/demo/pages/workforce.py` | Create | Workforce Statistics page (extract from current app.py) |
| `glassdash/demo/pages/finance.py` | Create | Finance Statistics page (placeholder) |
| `glassdash/demo/pages/sales.py` | Create | Sales Statistics page (placeholder) |

---

## Task 1: Add Sidebar CSS Styles

**Files:**
- Modify: `glassdash/assets/glass.css`

- [ ] **Step 1: Add sidebar CSS to glass.css**

Append these styles to the end of `glassdash/assets/glass.css`:

```css
/* Sidebar styles */
.glass-sidebar {
    position: fixed;
    left: 0;
    top: 0;
    height: 100vh;
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-right: 1px solid rgba(255,255,255,0.2);
    display: flex;
    flex-direction: column;
    transition: width 0.3s ease;
    z-index: 1000;
    overflow: hidden;
}
.glass-sidebar.expanded {
    width: 220px;
    padding: 20px 16px;
}
.glass-sidebar.collapsed {
    width: 60px;
    padding: 20px 12px;
}
.glass-sidebar-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 32px;
    padding-bottom: 16px;
    border-bottom: 1px solid rgba(255,255,255,0.2);
    overflow: hidden;
}
.glass-sidebar-logo {
    width: 32px;
    height: 32px;
    min-width: 32px;
    background: linear-gradient(135deg, #4facfe, #06b6d4);
    border-radius: 8px;
}
.glass-sidebar-title {
    font-size: 16px;
    font-weight: 600;
    color: #ffffff;
    white-space: nowrap;
    opacity: 1;
    transition: opacity 0.2s;
}
.glass-sidebar.collapsed .glass-sidebar-title {
    opacity: 0;
    width: 0;
}
.glass-sidebar-nav {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.glass-sidebar-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    border-radius: 12px;
    cursor: pointer;
    transition: background 0.2s;
    text-decoration: none;
    color: rgba(255,255,255,0.7);
    overflow: hidden;
}
.glass-sidebar-item:hover {
    background: rgba(255,255,255,0.1);
    color: #ffffff;
}
.glass-sidebar-item.active {
    background: rgba(79,172,254,0.2);
    color: #4facfe;
    border: 1px solid rgba(79,172,254,0.3);
}
.glass-sidebar-icon {
    font-size: 20px;
    min-width: 24px;
    text-align: center;
}
.glass-sidebar-label {
    font-size: 14px;
    font-weight: 500;
    white-space: nowrap;
    opacity: 1;
    transition: opacity 0.2s;
}
.glass-sidebar.collapsed .glass-sidebar-label {
    opacity: 0;
    width: 0;
}
.glass-sidebar-toggle {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 12px;
    border-radius: 12px;
    cursor: pointer;
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    color: rgba(255,255,255,0.7);
    transition: all 0.2s;
    margin-top: auto;
}
.glass-sidebar-toggle:hover {
    background: rgba(255,255,255,0.15);
    color: #ffffff;
}
.glass-main-content {
    margin-left: 220px;
    padding: 20px;
    transition: margin-left 0.3s ease;
    min-height: 100vh;
    box-sizing: border-box;
}
.glass-main-content.sidebar-collapsed {
    margin-left: 60px;
}
```

- [ ] **Step 2: Verify CSS syntax**

Run: `ruff check glassdash/assets/glass.css`
Expected: No errors (CSS is not Python but ruff won't choke on it)

- [ ] **Step 3: Commit**

```bash
git add glassdash/assets/glass.css
git commit -m "feat: add glassmorphic sidebar styles"
```

---

## Task 2: Create Page Module Structure

**Files:**
- Create: `glassdash/demo/pages/__init__.py`
- Create: `glassdash/demo/pages/workforce.py`
- Create: `glassdash/demo/pages/finance.py`
- Create: `glassdash/demo/pages/sales.py`

- [ ] **Step 1: Create pages directory and __init__.py**

Create `glassdash/demo/pages/__init__.py`:
```python
"""Dashboard page modules."""
```

- [ ] **Step 2: Create workforce.py with current demo content**

Extract the DataFrame and sections from current `app.py` into `glassdash/demo/pages/workforce.py`:

```python
"""Workforce Statistics Dashboard page."""
import polars as pl
from glassdash import GlassDashboard, GlassTheme, Section
from glassdash.components import (
    AreaChart,
    BarChart,
    DualAreaChart,
    MultiBarsChart,
    MultiLinesChart,
    RadialGauge,
    StackedBarChart,
    StackedBarWithBreakdown,
    StackedBarWithLine,
)


def get_workforce_data():
    return pl.DataFrame(
        {
            "month": ["2024-07","2024-08","2024-09","2024-10","2024-11","2024-12","2025-01","2025-02","2025-03","2025-04","2025-05","2025-06"],
            "fte": [18.2,19.1,19.5,20.3,21.0,21.5,22.0,22.5,23.0,23.5,24.0,24.5],
            "fte_ft": [12,13,13,14,14,15,15,16,16,16,17,17],
            "fte_pt": [4,4,4,4,5,4,5,4,5,5,5,5],
            "fte_cont": [2,2,2,2,2,2,2,2,2,2,2,2],
            "fte_other": [1,1,1,1,1,1,1,1,1,1,1,1],
            "total_fte": [19,20,20,21,22,22,23,23,24,24,25,25],
            "efficiency": [82,83,84,85,86,85,87,87,88,87,87,87],
            "efficacy": [88,89,90,91,92,91,93,93,94,93,93,93],
            "yield_pct": [3.2,3.3,3.4,3.5,3.6,3.5,3.7,3.8,3.9,4.0,4.1,4.2],
            "code_integration": [65,70,75,78,80,82,85,87,88,90,92,95],
            "squads": [4,4,5,5,5,6,6,6,7,7,7,8],
            "ai_usage": [10,12,15,18,22,28,35,42,50,58,68,78],
            "squad_a": [4,4,5,5,5,6,6,6,7,7,7,8],
            "squad_b": [3,4,4,4,5,5,5,6,6,6,7,7],
            "squad_c": [3,3,4,4,4,5,5,5,6,6,6,7],
            "fte_avg": [85,86,87,87,88,87,88,89,89,90,90,91],
            "fte_target": [90,90,90,90,90,90,90,90,90,90,90,90],
        }
    )


def WorkforcePage(theme=None):
    if theme is None:
        theme = GlassTheme()
    df = get_workforce_data()
    return GlassDashboard(
        title="Workforce Statistics Dashboard",
        date_range=("2024-07-01", "2025-06-13"),
        theme=theme,
        children=[
            Section("FTE Trends", "Full-time equivalent over time", height=600, children=[
                AreaChart(df, x="month", y="fte", theme=theme),
                MultiLinesChart(df, x="month", lines={"FTE": "fte", "Target": "total_fte"}, theme=theme),
            ]),
            Section("Squad Performance", "Team composition by squad", height=600, children=[
                MultiBarsChart(df, x="month", bars={"Squad A": "squad_a", "Squad B": "squad_b", "Squad C": "squad_c"}, theme=theme, highlight_current=False),
                BarChart(df, x="month", y="squads", theme=theme),
            ]),
            Section("Labor Mix", "Breakdown by employment type", height=900, children=[
                StackedBarChart(df, x="month", segments={"Full-time": "fte_ft", "Part-time": "fte_pt", "Contingent": "fte_cont", "Others": "fte_other"}, theme=theme),
                StackedBarWithLine(df, x="month", bar_segments={"Full-time": "fte_ft", "Part-time": "fte_pt", "Contingent": "fte_cont"}, line_y="total_fte", theme=theme),
                StackedBarWithBreakdown(df, x="month", bar_segments={"Full-time": "fte_ft", "Part-time": "fte_pt", "Contingent": "fte_cont", "Others": "fte_other"}, breakdown={"Full-time": {"Analyst": 0.3, "Engineer": 0.4, "Sales": 0.2, "Others": 0.1}, "Part-time": {"Morning": 0.5, "Afternoon": 0.5}, "Contingent": {"Contractor": 0.6, "Temp": 0.4}, "Others": {"External": 0.7, "Internal": 0.3}}, theme=theme),
            ]),
            Section("Efficiency Metrics", "Efficiency and efficacy over time", height=400, children=[
                DualAreaChart(df, x="month", y1="efficiency", y2="efficacy", theme=theme),
            ]),
            Section("Yield Gauge", "Current yield performance", height=400, children=[
                RadialGauge(value=61, max_value=100, label="Yield", theme=theme),
            ]),
        ],
    )
```

- [ ] **Step 3: Create finance.py with placeholder data**

```python
"""Finance Statistics Dashboard page."""
import polars as pl
from glassdash import GlassDashboard, GlassTheme, Section
from glassdash.components import (
    AreaChart,
    BarChart,
    DualAreaChart,
    MultiBarsChart,
    MultiLinesChart,
    RadialGauge,
    StackedBarChart,
    StackedBarWithBreakdown,
    StackedBarWithLine,
)


def get_finance_data():
    return pl.DataFrame(
        {
            "month": ["2024-07","2024-08","2024-09","2024-10","2024-11","2024-12","2025-01","2025-02","2025-03","2025-04","2025-05","2025-06"],
            "revenue": [420000,445000,468000,492000,515000,538000,562000,589000,615000,642000,671000,702000],
            "expenses": [280000,285000,292000,298000,305000,312000,318000,325000,332000,340000,348000,356000],
            "profit": [140000,160000,176000,194000,210000,226000,244000,264000,283000,302000,323000,346000],
            "marketing": [25000,28000,32000,35000,38000,42000,45000,48000,52000,55000,59000,63000],
            "operations": [85000,88000,92000,95000,98000,101000,104000,108000,111000,115000,119000,123000],
            "salaries": [120000,122000,125000,128000,131000,134000,137000,140000,143000,147000,150000,154000],
            "infrastructure": [50000,48000,52000,55000,51000,54000,57000,59000,62000,65000,68000,71000],
            "cash_flow": [95000,110000,125000,142000,158000,175000,192000,212000,230000,250000,272000,295000],
            "burn_rate": [65000,62000,58000,55000,52000,48000,45000,42000,38000,35000,31000,28000],
            "runway_months": [18,20,22,24,26,28,30,32,34,36,38,40],
        }
    )


def FinancePage(theme=None):
    if theme is None:
        theme = GlassTheme()
    df = get_finance_data()
    return GlassDashboard(
        title="Finance Statistics Dashboard",
        date_range=("2024-07-01", "2025-06-13"),
        theme=theme,
        children=[
            Section("Revenue & Profit", "Financial overview", height=600, children=[
                AreaChart(df, x="month", y="revenue", theme=theme),
                MultiLinesChart(df, x="month", lines={"Revenue": "revenue", "Expenses": "expenses", "Profit": "profit"}, theme=theme),
            ]),
            Section("Expense Breakdown", "Cost distribution by category", height=600, children=[
                StackedBarChart(df, x="month", segments={"Marketing": "marketing", "Operations": "operations", "Salaries": "salaries", "Infrastructure": "infrastructure"}, theme=theme),
                BarChart(df, x="month", y="burn_rate", theme=theme),
            ]),
            Section("Cash Flow", "Cash management metrics", height=400, children=[
                DualAreaChart(df, x="month", y1="cash_flow", y2="burn_rate", theme=theme),
            ]),
            Section("Runway", "Financial runway", height=400, children=[
                RadialGauge(value=40, max_value=48, label="Runway (months)", theme=theme),
            ]),
        ],
    )
```

- [ ] **Step 4: Create sales.py with placeholder data**

```python
"""Sales Statistics Dashboard page."""
import polars as pl
from glassdash import GlassDashboard, GlassTheme, Section
from glassdash.components import (
    AreaChart,
    BarChart,
    DualAreaChart,
    MultiBarsChart,
    MultiLinesChart,
    RadialGauge,
    StackedBarChart,
    StackedBarWithBreakdown,
    StackedBarWithLine,
)


def get_sales_data():
    return pl.DataFrame(
        {
            "month": ["2024-07","2024-08","2024-09","2024-10","2024-11","2024-12","2025-01","2025-02","2025-03","2025-04","2025-05","2025-06"],
            "leads": [320,345,368,392,415,438,462,489,515,542,571,602],
            "conversions": [85,92,98,105,112,118,125,133,141,149,158,168],
            "revenue": [425000,458000,492000,528000,565000,602000,642000,685000,732000,782000,836000,894000],
            "enterprise": [180000,195000,212000,230000,250000,272000,295000,320000,348000,378000,410000,445000],
            "mid_market": [145000,158000,172000,187000,203000,220000,238000,258000,280000,304000,330000,358000],
            "smb": [100000,105000,108000,111000,112000,110000,109000,107000,104000,100000,96000,91000],
            "avg_deal_size": [8500,9200,9800,10500,11200,11800,12500,13200,14000,14800,15700,16700],
            "sales_cycle_days": [45,43,42,40,39,38,37,36,35,34,33,32],
            "win_rate": [26.5,26.7,26.6,26.8,27.0,26.9,27.2,27.4,27.5,27.5,27.7,27.9],
            "pipeline_value": [2100000,2280000,2480000,2690000,2920000,3160000,3420000,3700000,4000000,4320000,4660000,5020000],
        }
    )


def SalesPage(theme=None):
    if theme is None:
        theme = GlassTheme()
    df = get_sales_data()
    return GlassDashboard(
        title="Sales Statistics Dashboard",
        date_range=("2024-07-01", "2025-06-13"),
        theme=theme,
        children=[
            Section("Pipeline & Revenue", "Sales funnel overview", height=600, children=[
                AreaChart(df, x="month", y="pipeline_value", theme=theme),
                MultiLinesChart(df, x="month", lines={"Leads": "leads", "Conversions": "conversions"}, theme=theme),
            ]),
            Section("Revenue by Segment", "Market segmentation", height=600, children=[
                StackedBarChart(df, x="month", segments={"Enterprise": "enterprise", "Mid-Market": "mid_market", "SMB": "smb"}, theme=theme),
                BarChart(df, x="month", y="avg_deal_size", theme=theme),
            ]),
            Section("Performance Metrics", "Key sales indicators", height=400, children=[
                DualAreaChart(df, x="month", y1="win_rate", y2="sales_cycle_days", theme=theme),
            ]),
            Section("Conversion Rate", "Current win rate", height=400, children=[
                RadialGauge(value=27.9, max_value=100, label="Win Rate %", theme=theme),
            ]),
        ],
    )
```

- [ ] **Step 5: Commit**

```bash
git add glassdash/demo/pages/
git commit -m "feat: add page modules for Workforce, Finance, Sales dashboards"
```

---

## Task 3: Restructure app.py with Sidebar and Multi-Page Routing

**Files:**
- Modify: `glassdash/demo/app.py`

- [ ] **Step 1: Rewrite app.py with sidebar and multi-page support**

Replace the entire content of `glassdash/demo/app.py` with:

```python
"""Demo dashboard with multi-page navigation."""
import os
from dash import Dash, dcc, html, Input, Output, State


def create_demo_app():
    app = Dash(
        __name__,
        assets_folder=os.path.join(os.path.dirname(__file__), "..", "assets"),
    )
    
    from glassdash import GlassTheme
    from glassdash.demo.pages.workforce import WorkforcePage
    from glassdash.demo.pages.finance import FinancePage
    from glassdash.demo.pages.sales import SalesPage
    
    theme = GlassTheme()
    
    # Sidebar navigation items
    nav_items = [
        {"id": "workforce", "label": "Workforce", "icon": "👥", "page": WorkforcePage(theme)},
        {"id": "finance", "label": "Finance", "icon": "💰", "page": FinancePage(theme)},
        {"id": "sales", "label": "Sales", "icon": "📊", "page": SalesPage(theme)},
    ]
    
    # Sidebar component
    sidebar = html.Div(
        [
            html.Div(
                [
                    html.Div(className="glass-sidebar-logo"),
                    html.Span("GlassDash", className="glass-sidebar-title"),
                ],
                className="glass-sidebar-header",
            ),
            html.Div(
                [
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
                className="glass-sidebar-nav",
            ),
            html.Div(
                [
                    html.Button("◀", id="sidebar-toggle", n_clicks=0),
                ],
                className="glass-sidebar-toggle",
            ),
        ],
        id="sidebar",
        className="glass-sidebar expanded",
    )
    
    # Main content area
    content = html.Div(id="page-content", className="glass-main-content")
    
    # Store for sidebar state
    store = dcc.Store(id="sidebar-state", data={"collapsed": False})
    
    # URL for routing
    url = dcc.Location(id="url", refresh=False)
    
    app.layout = html.Div([url, store, sidebar, content])
    
    @app.callback(
        Output("sidebar", "className"),
        Output("page-content", "className"),
        Input("sidebar-toggle", "n_clicks"),
        State("sidebar-state", "data"),
    )
    def toggle_sidebar(n_clicks, state):
        if n_clicks and n_clicks > 0:
            collapsed = not state.get("collapsed", False)
            state["collapsed"] = collapsed
        else:
            collapsed = state.get("collapsed", False)
        
        sidebar_class = f"glass-sidebar {'collapsed' if collapsed else 'expanded'}"
        content_class = f"glass-main-content {'sidebar-collapsed' if collapsed else ''}"
        return sidebar_class, content_class
    
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
        
        # Update active state on nav items
        nav_ids = ["workforce", "finance", "sales"]
        updated_nav = []
        for child in sidebar_children:
            if hasattr(child, "props") and "nav-" in str(child.props.get("id", "")):
                nav_id = child.props["id"].replace("nav-", "")
                is_active = nav_id == page_id
                new_class = f"glass-sidebar-item {'active' if is_active else ''}"
                child.props["className"] = new_class
                updated_nav.append(child)
            else:
                updated_nav.append(child)
        
        return page_func(theme=theme), updated_nav
    
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
```

- [ ] **Step 2: Run demo to verify**

Run: `cd /Users/stephen/dev/glossy && python -m glassdash.demo.app`
Expected: App starts on port 8050, sidebar visible, page navigation works

- [ ] **Step 3: Commit**

```bash
git add glassdash/demo/app.py glassdash/demo/pages/
git commit -m "feat: add collapsible sidebar with multi-page navigation"
```

---

## Task 4: Fix any Issues and Verify

- [ ] **Step 1: Run linter**

Run: `ruff check glassdash/`
Expected: No errors

- [ ] **Step 2: Test navigation manually**

Verify:
1. Sidebar appears on left with Workforce active
2. Clicking Finance navigates to Finance page
3. Clicking Sales navigates to Sales page
4. Toggle button collapses/expands sidebar
5. All three pages render their charts correctly

- [ ] **Step 3: Final commit if needed**

```bash
git add -A
git commit -m "fix: resolve any issues from testing"
```

---

## Verification Checklist

- [ ] Sidebar is glassmorphic (blur, transparency, border)
- [ ] Expanded width: 220px with labels
- [ ] Collapsed width: 60px with icons only
- [ ] Toggle button works at bottom of sidebar
- [ ] Three pages: Workforce, Finance, Sales
- [ ] Active page highlighted in sidebar
- [ ] URL updates when navigating
- [ ] All charts render on each page
- [ ] Theme colors consistent throughout

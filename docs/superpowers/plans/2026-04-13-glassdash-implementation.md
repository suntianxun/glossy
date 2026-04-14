# GlassDash Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python library providing beautiful glassmorphism-themed dashboard components for Plotly Dash + Polars

**Architecture:** Single library `glassdash/` with modular components. Theme system provides CSS/colors to all chart components. Each chart type is a reusable Dash component accepting Polars DataFrames. GlassDashboard wrapper provides layout + global theme.

**Tech Stack:** Python, Plotly Dash, Polars, HTML/CSS

---

## File Structure

```
glassdash/
├── __init__.py              # Main exports
├── theme.py                 # GlassTheme class, colors, CSS
├── components/
│   ├── __init__.py
│   ├── glass_card.py        # GlassCard component
│   ├── kpi_card.py          # KPICard component
│   ├── line_chart.py        # LineChart
│   ├── area_chart.py        # AreaChart
│   ├── multi_lines.py       # MultiLinesChart
│   ├── multi_bars.py        # MultiBarsChart
│   ├── stacked_bar.py        # StackedBarChart
│   ├── stacked_bar_line.py   # StackedBarWithLine
│   ├── stacked_bar_breakdown.py  # StackedBarWithBreakdown
│   ├── bar_chart.py         # BarChart
│   ├── dual_area.py         # DualAreaChart
│   └── radial_gauge.py      # RadialGauge
├── dashboard.py             # GlassDashboard wrapper
├── utils.py                 # Polars helpers
└── demo/
    ├── __init__.py
    └── app.py               # Demo dashboard
```

---

## Tasks

### Task 1: Project Setup & GlassTheme

**Files:**
- Create: `glassdash/__init__.py`
- Create: `glassdash/theme.py`
- Create: `glassdash/utils.py`
- Create: `glassdash/components/__init__.py`
- Create: `glassdash/demo/__init__.py`

- [ ] **Step 1: Create glassdash/theme.py with GlassTheme class**

```python
"""Theme system for GlassDash."""

from dataclasses import dataclass, field
from typing import Optional

@dataclass
class GlassTheme:
    """Customizable theme for GlassDash components.
    
    All color values accept hex strings (#RRGGBB), rgb/rgba strings,
    or any CSS color value.
    """
    colors: dict = field(default_factory=lambda: {
        "primary": "#e94560",
        "accent": "#4facfe",
        "success": "#10b981",
        "warning": "#f59e0b",
        "purple": "#8b5cf6",
        "cyan": "#06b6d4",
        "bg_start": "#1a1a2e",
        "bg_end": "#0f3460",
        "glass_bg": "rgba(255,255,255,0.15)",
        "glass_border": "rgba(255,255,255,0.2)",
        "text": "#ffffff",
        "text_muted": "rgba(255,255,255,0.6)",
    })
    fonts: dict = field(default_factory=lambda: {
        "family": "Inter, -apple-system, BlinkMacSystemFont, sans-serif",
        "kpi_value": 28,
        "kpi_label": 11,
        "chart_title": 14,
        "axis_label": 10,
    })
    effects: dict = field(default_factory=lambda: {
        "blur": 12,
        "glow": True,
        "animation": True,
    })
    
    def get_css(self) -> str:
        """Generate CSS for this theme."""
        return f"""
        body {{
            font-family: {self.fonts['family']};
            background: linear-gradient(135deg, {self.colors['bg_start']}, {self.colors['bg_end']});
            margin: 0;
            padding: 20px;
        }}
        .glass-card {{
            background: {self.colors['glass_bg']};
            backdrop-filter: blur({self.effects['blur']}px);
            -webkit-backdrop-filter: blur({self.effects['blur']}px);
            border: 1px solid {self.colors['glass_border']};
            border-radius: 16px;
            padding: 20px;
        }}
        .glass-kpi {{
            text-align: center;
        }}
        .glass-kpi-label {{
            font-size: {self.fonts['kpi_label']}px;
            text-transform: uppercase;
            color: {self.colors['text_muted']};
            margin-bottom: 8px;
        }}
        .glass-kpi-value {{
            font-size: {self.fonts['kpi_value']}px;
            font-weight: 700;
            color: {self.colors['text']};
        }}
        .glass-kpi-trend-up {{ color: {self.colors['success']}; }}
        .glass-kpi-trend-down {{ color: {self.colors['primary']}; }}
        .glass-chart-title {{
            font-size: {self.fonts['chart_title']}px;
            font-weight: 500;
            color: {self.colors['text']};
            margin-bottom: 16px;
        }}
        .glass-axis-label {{
            font-size: {self.fonts['axis_label']}px;
            color: {self.colors['text_muted']};
        }}
        """
```

- [ ] **Step 2: Create glassdash/utils.py with Polars helpers**

```python
"""Utility functions for working with Polars DataFrames."""

import polars as pl
from datetime import datetime
from typing import Optional

def get_last_n_months(n: int = 12) -> pl.DataFrame:
    """Generate last N months in yyyy-mm format."""
    today = datetime.now()
    months = []
    for i in range(n - 1, -1, -1):
        d = datetime(today.year, today.month, 1)
        if i > 0:
            import calendar
            d = d.replace(day=1) - calendar.monthdelta(today.year, today.month - i - 1)
        months.append(d.strftime("%Y-%m"))
    return pl.DataFrame({"month": months})

def ensure_month_column(df: pl.DataFrame, col: str = "month") -> pl.DataFrame:
    """Ensure DataFrame has properly formatted month column."""
    if col not in df.columns:
        raise ValueError(f"DataFrame must contain '{col}' column")
    return df.with_columns(pl.col(col).cast(pl.Utf8))

def filter_to_current_month(df: pl.DataFrame, month_col: str = "month") -> tuple[pl.DataFrame, int]:
    """Filter DataFrame to current month, return (rest, current_idx)."""
    today = datetime.now()
    current = today.strftime("%Y-%m")
    mask = df[month_col] == current
    current_idx = df.filter(mask).height - 1 if mask.any() else -1
    return df, current_idx
```

- [ ] **Step 3: Create glassdash/__init__.py with exports**

```python
"""GlassDash - Beautiful glassmorphism dashboards for Plotly Dash + Polars."""

from glassdash.theme import GlassTheme
from glassdash.dashboard import GlassDashboard

__all__ = ["GlassTheme", "GlassDashboard"]
```

- [ ] **Step 4: Create glassdash/components/__init__.py**

```python
"""GlassDash chart components."""

from glassdash.components.glass_card import GlassCard
from glassdash.components.kpi_card import KPICard
from glassdash.components.line_chart import LineChart
from glassdash.components.area_chart import AreaChart
from glassdash.components.multi_lines import MultiLinesChart
from glassdash.components.multi_bars import MultiBarsChart
from glassdash.components.stacked_bar import StackedBarChart
from glassdash.components.stacked_bar_line import StackedBarWithLine
from glassdash.components.stacked_bar_breakdown import StackedBarWithBreakdown
from glassdash.components.bar_chart import BarChart
from glassdash.components.dual_area import DualAreaChart
from glassdash.components.radial_gauge import RadialGauge

__all__ = [
    "GlassCard",
    "KPICard",
    "LineChart",
    "AreaChart",
    "MultiLinesChart",
    "MultiBarsChart",
    "StackedBarChart",
    "StackedBarWithLine",
    "StackedBarWithBreakdown",
    "BarChart",
    "DualAreaChart",
    "RadialGauge",
]
```

- [ ] **Step 5: Create glassdash/demo/__init__.py**

```python
"""GlassDash demo."""
```

- [ ] **Step 6: Run tests**

```bash
cd /Users/stephen/dev/glossy
python -c "from glassdash import GlassTheme; t = GlassTheme(); print(t.get_css()[:200])"
```

- [ ] **Step 7: Commit**

```bash
git add -A && git commit -m "feat: add GlassTheme, utils, and project structure"
```

---

### Task 2: GlassCard & KPICard Components

**Files:**
- Create: `glassdash/components/glass_card.py`
- Create: `glassdash/components/kpi_card.py`
- Modify: `glassdash/__init__.py` (add exports)

- [ ] **Step 1: Create glassdash/components/glass_card.py**

```python
"""GlassCard - frosted glass container component."""

from dash import html
from glassdash.theme import GlassTheme

def GlassCard(
    children=None,
    title: str = None,
    theme: GlassTheme = None,
    **kwargs
):
    """Frosted glass container.
    
    Args:
        children: Content to put inside the card
        title: Optional title for the card
        theme: GlassTheme instance (uses default if None)
        **kwargs: Additional html.Div properties
    """
    if theme is None:
        from glassdash.theme import GlassTheme
        theme = GlassTheme()
    
    content = []
    if title:
        content.append(html.H3(title, className="glass-chart-title"))
    content.append(html.Div(children))
    
    return html.Div(
        content,
        className="glass-card",
        style={"marginBottom": "20px"},
        **kwargs
    )
```

- [ ] **Step 2: Create glassdash/components/kpi_card.py**

```python
"""KPICard - key metric display with trend."""

from dash import html
from glassdash.theme import GlassTheme

def KPICard(
    title: str,
    value: float,
    trend: float = None,
    trend_label: str = "% vs last month",
    theme: GlassTheme = None,
    **kwargs
):
    """Key metric card with trend indicator.
    
    Args:
        title: Metric label (e.g., "FTE", "Efficiency")
        value: Current value to display
        trend: Percentage change (positive = up, negative = down)
        trend_label: Description of trend
        theme: GlassTheme instance
        **kwargs: Additional html.Div properties
    """
    if theme is None:
        from glassdash.theme import GlassTheme
        theme = GlassTheme()
    
    trend_class = "glass-kpi-trend-up" if (trend and trend > 0) else "glass-kpi-trend-down" if trend else ""
    trend_symbol = "↑" if (trend and trend > 0) else "↓" if trend else ""
    
    return html.Div(
        [
            html.Div(title.upper(), className="glass-kpi-label"),
            html.Div(f"{value}", className="glass-kpi-value"),
            html.Div(
                f"{trend_symbol} {abs(trend)} {trend_label}" if trend else "",
                className=f"glass-kpi-label {trend_class}" if trend else ""
            ),
        ],
        className="glass-card glass-kpi",
        style={"textAlign": "center"},
        **kwargs
    )
```

- [ ] **Step 3: Update glassdash/__init__.py**

Add `GlassCard` and `KPICard` to exports.

- [ ] **Step 4: Run tests**

```bash
cd /Users/stephen/dev/glossy
python -c "
from glassdash.components import GlassCard, KPICard
from glassdash.theme import GlassTheme
t = GlassTheme()
card = GlassCard(title='Test', children='Content', theme=t)
kpi = KPICard(title='FTE', value=24.5, trend=2.3, theme=t)
print('GlassCard:', card.className)
print('KPICard:', kpi.className)
"
```

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: add GlassCard and KPICard components"
```

---

### Task 3: LineChart & AreaChart Components

**Files:**
- Create: `glassdash/components/line_chart.py`
- Create: `glassdash/components/area_chart.py`

- [ ] **Step 1: Create glassdash/components/line_chart.py**

```python
"""LineChart - simple time series line chart."""

import polars as pl
from dash import html
from plotly import graph_objects as go
from glassdash.theme import GlassTheme

def LineChart(
    dataframe: pl.DataFrame,
    x: str = "month",
    y: str = "value",
    color: str = "accent",
    highlight_current: bool = True,
    theme: GlassTheme = None,
    **kwargs
):
    """Line chart with glassmorphism styling.
    
    Args:
        dataframe: Polars DataFrame with x and y columns
        x: Column name for x-axis (default "month")
        y: Column name for y-axis
        color: Theme color key (default "accent")
        highlight_current: Highlight last point with glow
        theme: GlassTheme instance
    """
    if theme is None:
        from glassdash.theme import GlassTheme
        theme = GlassTheme()
    
    df = dataframe.select([x, y])
    x_data = df[x].to_list()
    y_data = df[y].to_list()
    
    line_color = theme.colors.get(color, theme.colors["accent"])
    highlight_color = theme.colors["accent"]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode="lines",
        line=dict(color=line_color, width=2.5),
        hovertemplate=f"{y}: %{{y:.1f}}<extra></extra>",
    ))
    
    if highlight_current and len(x_data) > 0:
        fig.add_trace(go.Scatter(
            x=[x_data[-1]],
            y=[y_data[-1]],
            mode="markers",
            marker=dict(
                color=highlight_color,
                size=10,
                line=dict(width=2, color=theme.colors["bg_start"]),
            ),
            hovertemplate=f"{y}: {y_data[-1]:.1f}<extra>Current</extra>",
        ))
    
    fig.update_layout(
        paper_bgcolor="transparent",
        plot_bgcolor="transparent",
        font=dict(
            family=theme.fonts["family"],
            size=theme.fonts["axis_label"],
            color=theme.colors["text_muted"],
        ),
        margin=dict(l=20, r=20, t=20, b=40),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickangle=-45,
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
        ),
        hovermode="x unified",
    )
    
    return html.Div(
        [
            html.Div(className="glass-card", style={"padding": "15px"}, children=[
                html.Div(go.Figure(fig), style={"height": "120px"})
            ])
        ],
        **kwargs
    )
```

- [ ] **Step 2: Create glassdash/components/area_chart.py**

```python
"""AreaChart - line chart with gradient fill."""

import polars as pl
from dash import html
from plotly import graph_objects as go
from glassdash.theme import GlassTheme

def AreaChart(
    dataframe: pl.DataFrame,
    x: str = "month",
    y: str = "value",
    color: str = "purple",
    highlight_current: bool = True,
    theme: GlassTheme = None,
    **kwargs
):
    """Area chart with gradient fill.
    
    Args:
        dataframe: Polars DataFrame with x and y columns
        x: Column name for x-axis
        y: Column name for y-axis
        color: Theme color key for fill
        highlight_current: Highlight last point with glow
        theme: GlassTheme instance
    """
    if theme is None:
        from glassdash.theme import GlassTheme
        theme = GlassTheme()
    
    df = dataframe.select([x, y])
    x_data = df[x].to_list()
    y_data = df[y].to_list()
    
    base_color = theme.colors.get(color, theme.colors["purple"])
    highlight_color = theme.colors["accent"]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode="lines",
        line=dict(color=base_color, width=2),
        fill="tonexty",
        fillcolor=f"rgba({int(base_color[1:3],16)},{int(base_color[3:5],16)},{int(base_color[5:7],16)},0.3)",
        hovertemplate=f"{y}: %{{y:.1f}}<extra></extra>",
    ))
    
    if highlight_current and len(x_data) > 0:
        fig.add_trace(go.Scatter(
            x=[x_data[-1]],
            y=[y_data[-1]],
            mode="markers",
            marker=dict(
                color=highlight_color,
                size=10,
            ),
            hovertemplate=f"Current: {y_data[-1]:.1f}<extra></extra>",
        ))
    
    fig.update_layout(
        paper_bgcolor="transparent",
        plot_bgcolor="transparent",
        font=dict(
            family=theme.fonts["family"],
            size=theme.fonts["axis_label"],
            color=theme.colors["text_muted"],
        ),
        margin=dict(l=20, r=20, t=20, b=40),
        xaxis=dict(showgrid=False, zeroline=False, tickangle=-45),
        yaxis=dict(showgrid=False, zeroline=False),
        hovermode="x unified",
    )
    
    return html.Div(
        html.Div(className="glass-card", style={"padding": "15px"}, children=[
            html.Div(go.Figure(fig), style={"height": "120px"})
        ]),
        **kwargs
    )
```

- [ ] **Step 3: Run tests**

```bash
cd /Users/stephen/dev/glossy
python -c "
import polars as pl
from glassdash.components import LineChart, AreaChart
df = pl.DataFrame({'month': ['2025-01', '2025-02', '2025-03'], 'value': [10, 15, 20]})
lc = LineChart(df, x='month', y='value')
ac = AreaChart(df, x='month', y='value')
print('LineChart created:', lc.children[0].style is not None)
print('AreaChart created:', ac.children[0].style is not None)
"
```

- [ ] **Step 4: Commit**

```bash
git add -A && git commit -m "feat: add LineChart and AreaChart components"
```

---

### Task 4: MultiLinesChart & MultiBarsChart

**Files:**
- Create: `glassdash/components/multi_lines.py`
- Create: `glassdash/components/multi_bars.py`

- [ ] **Step 1: Create multi_lines.py** (similar pattern to LineChart but with dict of lines)

```python
"""MultiLinesChart - multiple overlaid lines."""

import polars as pl
from dash import html
from plotly import graph_objects as go
from glassdash.theme import GlassTheme

def MultiLinesChart(
    dataframe: pl.DataFrame,
    x: str = "month",
    lines: dict = None,
    colors: dict = None,
    highlight_current: bool = True,
    theme: GlassTheme = None,
    **kwargs
):
    """Multi-line chart with multiple series.
    
    Args:
        dataframe: Polars DataFrame
        x: Column name for x-axis
        lines: Dict of {label: column_name}
        colors: Dict of {label: color_key} (uses theme colors if not provided)
        highlight_current: Highlight last point of each line
        theme: GlassTheme instance
    """
    if theme is None:
        from glassdash.theme import GlassTheme
        theme = GlassTheme()
    
    if lines is None:
        lines = {"Line 1": "value1", "Line 2": "value2"}
    if colors is None:
        color_cycle = ["accent", "purple", "cyan", "success", "warning"]
        colors = {k: color_cycle[i % len(color_cycle)] for i, k in enumerate(lines)}
    
    x_data = dataframe[x].to_list()
    
    fig = go.Figure()
    
    for label, col in lines.items():
        color_key = colors.get(label, "accent")
        line_color = theme.colors.get(color_key, theme.colors["accent"])
        y_data = dataframe[col].to_list()
        
        fig.add_trace(go.Scatter(
            x=x_data,
            y=y_data,
            mode="lines",
            name=label,
            line=dict(color=line_color, width=2),
            hovertemplate=f"{label}: %{{y:.1f}}<extra></extra>",
        ))
        
        if highlight_current and len(x_data) > 0:
            fig.add_trace(go.Scatter(
                x=[x_data[-1]],
                y=[y_data[-1]],
                mode="markers",
                marker=dict(color=line_color, size=8),
                showlegend=False,
            ))
    
    fig.update_layout(
        paper_bgcolor="transparent",
        plot_bgcolor="transparent",
        font=dict(
            family=theme.fonts["family"],
            size=theme.fonts["axis_label"],
            color=theme.colors["text_muted"],
        ),
        margin=dict(l=20, r=20, t=20, b=40),
        xaxis=dict(showgrid=False, zeroline=False, tickangle=-45),
        yaxis=dict(showgrid=False, zeroline=False),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=10),
        ),
        hovermode="x unified",
    )
    
    return html.Div(
        html.Div(className="glass-card", style={"padding": "15px"}, children=[
            html.Div(go.Figure(fig), style={"height": "120px"})
        ]),
        **kwargs
    )
```

- [ ] **Step 2: Create multi_bars.py** (grouped bars)

```python
"""MultiBarsChart - grouped bar chart."""

import polars as pl
from dash import html
from plotly import graph_objects as go
from glassdash.theme import GlassTheme

def MultiBarsChart(
    dataframe: pl.DataFrame,
    x: str = "month",
    bars: dict = None,
    colors: list = None,
    highlight_current: bool = True,
    theme: GlassTheme = None,
    **kwargs
):
    """Grouped bar chart.
    
    Args:
        dataframe: Polars DataFrame
        x: Column name for x-axis
        bars: Dict of {label: column_name}
        colors: List of theme color keys
        highlight_current: Highlight last bar group
        theme: GlassTheme instance
    """
    if theme is None:
        from glassdash.theme import GlassTheme
        theme = GlassTheme()
    
    if bars is None:
        bars = {"Bar 1": "value1", "Bar 2": "value2", "Bar 3": "value3"}
    if colors is None:
        colors = ["accent", "purple", "cyan"]
    
    x_data = dataframe[x].to_list()
    
    fig = go.Figure()
    
    bar_colors = [theme.colors.get(colors[i % len(colors)], theme.colors["accent"]) for i in range(len(bars))]
    
    for i, (label, col) in enumerate(bars.items()):
        y_data = dataframe[col].to_list()
        color = bar_colors[i]
        
        if highlight_current and i == len(bars) - 1:
            color = theme.colors["accent"]
        
        fig.add_trace(go.Bar(
            x=x_data,
            y=y_data,
            name=label,
            marker=dict(
                color=color,
                line=dict(width=0),
            ),
            hovertemplate=f"{label}: %{{y:.1f}}<extra></extra>",
        ))
    
    fig.update_layout(
        paper_bgcolor="transparent",
        plot_bgcolor="transparent",
        font=dict(
            family=theme.fonts["family"],
            size=theme.fonts["axis_label"],
            color=theme.colors["text_muted"],
        ),
        margin=dict(l=20, r=20, t=20, b=40),
        xaxis=dict(showgrid=False, zeroline=False, tickangle=-45),
        yaxis=dict(showgrid=False, zeroline=False),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=10),
        ),
        barmode="group",
        hovermode="x unified",
    )
    
    return html.Div(
        html.Div(className="glass-card", style={"padding": "15px"}, children=[
            html.Div(go.Figure(fig), style={"height": "120px"})
        ]),
        **kwargs
    )
```

- [ ] **Step 3: Run tests**

```bash
cd /Users/stephen/dev/glossy
python -c "
import polars as pl
from glassdash.components import MultiLinesChart, MultiBarsChart
df = pl.DataFrame({
    'month': ['2025-01', '2025-02', '2025-03'],
    'value1': [10, 15, 20],
    'value2': [8, 12, 16],
    'value3': [5, 8, 12],
})
ml = MultiLinesChart(df, x='month', lines={'FTE': 'value1', 'Target': 'value2'})
mb = MultiBarsChart(df, x='month', bars={'A': 'value1', 'B': 'value2', 'C': 'value3'})
print('MultiLinesChart created:', ml is not None)
print('MultiBarsChart created:', mb is not None)
"
```

- [ ] **Step 4: Commit**

```bash
git add -A && git commit -m "feat: add MultiLinesChart and MultiBarsChart components"
```

---

### Task 5: StackedBarChart

**Files:**
- Create: `glassdash/components/stacked_bar.py`

- [ ] **Step 1: Create stacked_bar.py**

```python
"""StackedBarChart - stacked proportional bar chart."""

import polars as pl
from dash import html
from plotly import graph_objects as go
from glassdash.theme import GlassTheme

def StackedBarChart(
    dataframe: pl.DataFrame,
    x: str = "month",
    segments: dict = None,
    colors: dict = None,
    highlight_current: bool = True,
    theme: GlassTheme = None,
    **kwargs
):
    """Stacked bar chart for labor mix etc.
    
    Args:
        dataframe: Polars DataFrame
        x: Column name for x-axis
        segments: Dict of {label: column_name}
        colors: Dict of {label: color_key}
        highlight_current: Highlight last bar
        theme: GlassTheme instance
    """
    if theme is None:
        from glassdash.theme import GlassTheme
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
            "Full-time": "primary",
            "Part-time": "warning",
            "Contingent": "purple",
            "Others": "cyan",
        }
    
    x_data = dataframe[x].to_list()
    
    fig = go.Figure()
    
    for label, col in segments.items():
        color_key = colors.get(label, "primary")
        bar_color = theme.colors.get(color_key, theme.colors["primary"])
        
        if highlight_current:
            bar_color = theme.colors["accent"]
        
        fig.add_trace(go.Bar(
            x=x_data,
            y=dataframe[col].to_list(),
            name=label,
            marker=dict(
                color=bar_color,
                line=dict(width=0),
            ),
            hovertemplate=f"{label}: %{{y:.1f}}<extra></extra>",
        ))
    
    fig.update_layout(
        paper_bgcolor="transparent",
        plot_bgcolor="transparent",
        font=dict(
            family=theme.fonts["family"],
            size=theme.fonts["axis_label"],
            color=theme.colors["text_muted"],
        ),
        margin=dict(l=20, r=20, t=20, b=40),
        xaxis=dict(showgrid=False, zeroline=False, tickangle=-45),
        yaxis=dict(showgrid=False, zeroline=False),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=10),
        ),
        barmode="stack",
        hovermode="x unified",
    )
    
    return html.Div(
        html.Div(className="glass-card", style={"padding": "15px"}, children=[
            html.Div(go.Figure(fig), style={"height": "120px"})
        ]),
        **kwargs
    )
```

- [ ] **Step 2: Run tests**

```bash
cd /Users/stephen/dev/glossy
python -c "
import polars as pl
from glassdash.components import StackedBarChart
df = pl.DataFrame({
    'month': ['2025-01', '2025-02', '2025-03'],
    'fte_ft': [15, 16, 17],
    'fte_pt': [5, 4, 4],
    'fte_cont': [3, 3, 4],
    'fte_other': [2, 2, 2],
})
sbc = StackedBarChart(df, x='month')
print('StackedBarChart created:', sbc is not None)
"
```

- [ ] **Step 3: Commit**

```bash
git add -A && git commit -m "feat: add StackedBarChart component"
```

---

### Task 6: StackedBarWithLine

**Files:**
- Create: `glassdash/components/stacked_bar_line.py`

- [ ] **Step 1: Create stacked_bar_line.py**

```python
"""StackedBarWithLine - stacked bar + dashed line on secondary y-axis."""

import polars as pl
from dash import html
from plotly import graph_objects as go
from glassdash.theme import GlassTheme

def StackedBarWithLine(
    dataframe: pl.DataFrame,
    x: str = "month",
    bar_segments: dict = None,
    line_y: str = "total",
    line_color: str = "accent",
    line_dash: str = "dash",
    highlight_current: bool = True,
    theme: GlassTheme = None,
    **kwargs
):
    """Stacked bar chart with line on secondary y-axis.
    
    Args:
        dataframe: Polars DataFrame
        x: Column name for x-axis
        bar_segments: Dict of {label: column_name} for stacked bars
        line_y: Column name for line data (on secondary y-axis)
        line_color: Theme color key for line
        line_dash: Line dash style ('dash', 'dot', etc.)
        highlight_current: Highlight last bar + line point
        theme: GlassTheme instance
    """
    if theme is None:
        from glassdash.theme import GlassTheme
        theme = GlassTheme()
    
    if bar_segments is None:
        bar_segments = {
            "Full-time": "fte_ft",
            "Part-time": "fte_pt",
            "Contingent": "fte_cont",
        }
    
    x_data = dataframe[x].to_list()
    y_line = dataframe[line_y].to_list()
    line_color_value = theme.colors.get(line_color, theme.colors["accent"])
    
    fig = go.Figure()
    
    for label, col in bar_segments.items():
        fig.add_trace(go.Bar(
            x=x_data,
            y=dataframe[col].to_list(),
            name=label,
            marker=dict(color=theme.colors["purple"], line=dict(width=0)),
            hovertemplate=f"{label}: %{{y:.1f}}<extra></extra>",
        ))
    
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_line,
        mode="lines+markers",
        name=line_y,
        line=dict(color=line_color_value, width=2, dash=line_dash),
        marker=dict(size=8, color=line_color_value),
        yaxis="y2",
        hovertemplate=f"{line_y}: %{{y:.1f}}<extra></extra>",
    ))
    
    fig.update_layout(
        paper_bgcolor="transparent",
        plot_bgcolor="transparent",
        font=dict(
            family=theme.fonts["family"],
            size=theme.fonts["axis_label"],
            color=theme.colors["text_muted"],
        ),
        margin=dict(l=20, r=50, t=20, b=40),
        xaxis=dict(showgrid=False, zeroline=False, tickangle=-45),
        yaxis=dict(showgrid=False, zeroline=False, side="left"),
        yaxis2=dict(
            showgrid=False,
            zeroline=False,
            side="right",
            overlaying="y",
            tickfont=dict(color=line_color_value),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=10),
        ),
        barmode="stack",
        hovermode="x unified",
    )
    
    return html.Div(
        html.Div(className="glass-card", style={"padding": "15px"}, children=[
            html.Div(go.Figure(fig), style={"height": "120px"})
        ]),
        **kwargs
    )
```

- [ ] **Step 2: Run tests**

```bash
cd /Users/stephen/dev/glossy
python -c "
import polars as pl
from glassdash.components import StackedBarWithLine
df = pl.DataFrame({
    'month': ['2025-01', '2025-02', '2025-03'],
    'fte_ft': [15, 16, 17],
    'fte_pt': [5, 4, 4],
    'fte_cont': [3, 3, 4],
    'total': [23, 23, 25],
})
sbwl = StackedBarWithLine(df, x='month', line_y='total')
print('StackedBarWithLine created:', sbwl is not None)
"
```

- [ ] **Step 3: Commit**

```bash
git add -A && git commit -m "feat: add StackedBarWithLine component"
```

---

### Task 7: StackedBarWithBreakdown

**Files:**
- Create: `glassdash/components/stacked_bar_breakdown.py`

- [ ] **Step 1: Create stacked_bar_breakdown.py**

```python
"""StackedBarWithBreakdown - stacked bar + horizontal breakdown bars."""

import polars as pl
from dash import html, div
from plotly import graph_objects as go
from glassdash.theme import GlassTheme

def StackedBarWithBreakdown(
    dataframe: pl.DataFrame,
    x: str = "month",
    bar_segments: dict = None,
    breakdown_bars: dict = None,
    breakdown_orientation: str = "horizontal",
    highlight_current: bool = True,
    theme: GlassTheme = None,
    **kwargs
):
    """Stacked bar chart with breakdown bars.
    
    Args:
        dataframe: Polars DataFrame
        x: Column name for x-axis
        bar_segments: Dict of {label: column_name} for main stacked bars
        breakdown_bars: Dict of {label: column_name} for breakdown bars
        breakdown_orientation: 'horizontal' (bars to the right)
        highlight_current: Highlight last bar group
        theme: GlassTheme instance
    """
    if theme is None:
        from glassdash.theme import GlassTheme
        theme = GlassTheme()
    
    if bar_segments is None:
        bar_segments = {
            "Full-time": "fte_ft",
            "Part-time": "fte_pt",
            "Contingent": "fte_cont",
            "Others": "fte_other",
        }
    if breakdown_bars is None:
        breakdown_bars = {"Avg": "fte_avg", "Target": "fte_target"}
    
    x_data = dataframe[x].to_list()
    
    fig_main = go.Figure()
    
    for label, col in bar_segments.items():
        fig_main.add_trace(go.Bar(
            x=x_data,
            y=dataframe[col].to_list(),
            name=label,
            marker=dict(color=theme.colors["purple"], line=dict(width=0)),
            hovertemplate=f"{label}: %{{y:.1f}}<extra></extra>",
        ))
    
    fig_main.update_layout(
        paper_bgcolor="transparent",
        plot_bgcolor="transparent",
        font=dict(
            family=theme.fonts["family"],
            size=theme.fonts["axis_label"],
            color=theme.colors["text_muted"],
        ),
        margin=dict(l=20, r=20, t=20, b=40),
        xaxis=dict(showgrid=False, zeroline=False, tickangle=-45),
        yaxis=dict(showgrid=False, zeroline=False),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=10),
        ),
        barmode="stack",
        hovermode="x unified",
    )
    
    breakdown_content = []
    for label, col in breakdown_bars.items():
        bar_color = theme.colors.get(label.lower(), theme.colors["success"])
        value = dataframe[col].to_list()[-1] if len(dataframe) > 0 else 0
        breakdown_content.append(
            div([
                html.Div(label, style={"color": theme.colors["text_muted"], "fontSize": "10px", "marginBottom": "4px"}),
                html.Div(
                    style={
                        "width": f"{value}%",
                        "maxWidth": "100px",
                        "height": "10px",
                        "background": bar_color,
                        "borderRadius": "5px",
                        "position": "relative",
                    }
                ),
                html.Div(f"{value}", style={"color": "white", "fontSize": "12px", "marginTop": "4px"}),
            ],
            style={"marginBottom": "12px"})
        )
    
    return html.Div(
        [
            html.Div(className="glass-card", style={"padding": "15px", "flex": "2"}, children=[
                html.Div(go.Figure(fig_main), style={"height": "120px"})
            ]),
            html.Div(
                breakdown_content,
                style={
                    "flex": "1",
                    "borderLeft": f"1px solid {theme.colors['glass_border']}",
                    "paddingLeft": "20px",
                    "marginLeft": "20px",
                    "display": "flex",
                    "flexDirection": "column",
                    "justifyContent": "center",
                }
            ),
        ],
        style={"display": "flex", "alignItems": "stretch"},
        **kwargs
    )
```

- [ ] **Step 2: Run tests**

```bash
cd /Users/stephen/dev/glossy
python -c "
import polars as pl
from glassdash.components import StackedBarWithBreakdown
df = pl.DataFrame({
    'month': ['2025-01', '2025-02', '2025-03'],
    'fte_ft': [15, 16, 17],
    'fte_pt': [5, 4, 4],
    'fte_cont': [3, 3, 4],
    'fte_other': [2, 2, 2],
    'fte_avg': [85, 87, 89],
    'fte_target': [100, 100, 100],
})
sbwb = StackedBarWithBreakdown(df, x='month')
print('StackedBarWithBreakdown created:', sbwb is not None)
"
```

- [ ] **Step 3: Commit**

```bash
git add -A && git commit -m "feat: add StackedBarWithBreakdown component"
```

---

### Task 8: BarChart, DualAreaChart, RadialGauge

**Files:**
- Create: `glassdash/components/bar_chart.py`
- Create: `glassdash/components/dual_area.py`
- Create: `glassdash/components/radial_gauge.py`

- [ ] **Step 1: Create bar_chart.py**

```python
"""BarChart - simple bar chart."""

import polars as pl
from dash import html
from plotly import graph_objects as go
from glassdash.theme import GlassTheme

def BarChart(
    dataframe: pl.DataFrame,
    x: str = "month",
    y: str = "value",
    color: str = "purple",
    highlight_current: bool = True,
    theme: GlassTheme = None,
    **kwargs
):
    """Simple bar chart."""
    if theme is None:
        from glassdash.theme import GlassTheme
        theme = GlassTheme()
    
    x_data = dataframe[x].to_list()
    y_data = dataframe[y].to_list()
    bar_color = theme.colors.get(color, theme.colors["purple"])
    
    colors = [bar_color] * (len(y_data) - 1) + [theme.colors["accent"]] if highlight_current else [bar_color] * len(y_data)
    
    fig = go.Figure(go.Bar(
        x=x_data,
        y=y_data,
        marker=dict(color=colors, line=dict(width=0)),
        hovertemplate=f"{y}: %{{y:.1f}}<extra></extra>",
    ))
    
    fig.update_layout(
        paper_bgcolor="transparent",
        plot_bgcolor="transparent",
        font=dict(
            family=theme.fonts["family"],
            size=theme.fonts["axis_label"],
            color=theme.colors["text_muted"],
        ),
        margin=dict(l=20, r=20, t=20, b=40),
        xaxis=dict(showgrid=False, zeroline=False, tickangle=-45),
        yaxis=dict(showgrid=False, zeroline=False),
        hovermode="x unified",
    )
    
    return html.Div(
        html.Div(className="glass-card", style={"padding": "15px"}, children=[
            html.Div(go.Figure(fig), style={"height": "120px"})
        ]),
        **kwargs
    )
```

- [ ] **Step 2: Create dual_area.py**

```python
"""DualAreaChart - two overlaid area charts."""

import polars as pl
from dash import html
from plotly import graph_objects as go
from glassdash.theme import GlassTheme

def DualAreaChart(
    dataframe: pl.DataFrame,
    x: str = "month",
    y1: str = "value1",
    y2: str = "value2",
    color1: str = "accent",
    color2: str = "purple",
    labels: list = None,
    highlight_current: bool = True,
    theme: GlassTheme = None,
    **kwargs
):
    """Dual area chart with two overlaid areas."""
    if theme is None:
        from glassdash.theme import GlassTheme
        theme = GlassTheme()
    
    if labels is None:
        labels = [y1, y2]
    
    x_data = dataframe[x].to_list()
    y1_data = dataframe[y1].to_list()
    y2_data = dataframe[y2].to_list()
    
    c1 = theme.colors.get(color1, theme.colors["accent"])
    c2 = theme.colors.get(color2, theme.colors["purple"])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x_data + x_data[::-1],
        y=y1_data + [0] * len(y1_data),
        fill="toself",
        fillcolor=f"rgba({int(c1[1:3],16)},{int(c1[3:5],16)},{int(c1[5:7],16)},0.4)",
        line=dict(color=c1, width=2),
        name=labels[0],
        hovertemplate=f"{labels[0]}: %{{y:.1f}}<extra></extra>",
    ))
    
    fig.add_trace(go.Scatter(
        x=x_data + x_data[::-1],
        y=y2_data + [0] * len(y2_data),
        fill="toself",
        fillcolor=f"rgba({int(c2[1:3],16)},{int(c2[3:5],16)},{int(c2[5:7],16)},0.4)",
        line=dict(color=c2, width=2),
        name=labels[1],
        hovertemplate=f"{labels[1]}: %{{y:.1f}}<extra></extra>",
    ))
    
    fig.update_layout(
        paper_bgcolor="transparent",
        plot_bgcolor="transparent",
        font=dict(
            family=theme.fonts["family"],
            size=theme.fonts["axis_label"],
            color=theme.colors["text_muted"],
        ),
        margin=dict(l=20, r=20, t=20, b=40),
        xaxis=dict(showgrid=False, zeroline=False, tickangle=-45),
        yaxis=dict(showgrid=False, zeroline=False),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=10),
        ),
        hovermode="x unified",
    )
    
    return html.Div(
        html.Div(className="glass-card", style={"padding": "15px"}, children=[
            html.Div(go.Figure(fig), style={"height": "120px"})
        ]),
        **kwargs
    )
```

- [ ] **Step 3: Create radial_gauge.py**

```python
"""RadialGauge - arc/gauge visualization."""

from dash import html
from plotly import graph_objects as go
from glassdash.theme import GlassTheme

def RadialGauge(
    value: float,
    max_value: float = 100,
    label: str = "Value",
    color: str = "success",
    theme: GlassTheme = None,
    **kwargs
):
    """Radial gauge chart.
    
    Args:
        value: Current value
        max_value: Maximum value for 100%
        label: Label to display
        color: Theme color key
        theme: GlassTheme instance
    """
    if theme is None:
        from glassdash.theme import GlassTheme
        theme = GlassTheme()
    
    gauge_color = theme.colors.get(color, theme.colors["success"])
    
    percentage = min(value / max_value, 1.0)
    degrees = percentage * 270
    color_rgb = f"rgb({int(gauge_color[1:3],16)},{int(gauge_color[3:5],16)},{int(gauge_color[5:7],16)})"
    
    fig = go.Figure(go.Pie(
        values=[percentage, 1 - percentage],
        Hole=0.7,
        marker_colors=[gauge_color, "rgba(255,255,255,0.1)"],
        showlegend=False,
        textinfo="none",
        sort=False,
    ))
    
    fig.update_layout(
        paper_bgcolor="transparent",
        plot_bgcolor="transparent",
        margin=dict(l=10, r=10, t=10, b=10),
        annotations=[
            dict(
                text=f"{value:.1f}%",
                x=0.5,
                y=0.5,
                font=dict(
                    size=22,
                    color="white",
                    family=theme.fonts["family"],
                ),
                showarrow=False,
            ),
            dict(
                text=label.upper(),
                x=0.5,
                y=0.4,
                font=dict(
                    size=10,
                    color=theme.colors["text_muted"],
                    family=theme.fonts["family"],
                ),
                showarrow=False,
            ),
        ],
    )
    
    return html.Div(
        html.Div(className="glass-card", style={"padding": "15px"}, children=[
            html.Div(go.Figure(fig), style={"height": "120px"})
        ]),
        **kwargs
    )
```

- [ ] **Step 4: Run tests**

```bash
cd /Users/stephen/dev/glossy
python -c "
import polars as pl
from glassdash.components import BarChart, DualAreaChart, RadialGauge
df = pl.DataFrame({
    'month': ['2025-01', '2025-02', '2025-03'],
    'value': [10, 15, 20],
    'value1': [80, 85, 87],
    'value2': [90, 92, 93],
})
bc = BarChart(df, x='month', y='value')
da = DualAreaChart(df, x='month', y1='value1', y2='value2')
rg = RadialGauge(value=61, max_value=100, label='Yield')
print('BarChart:', bc is not None)
print('DualAreaChart:', da is not None)
print('RadialGauge:', rg is not None)
"
```

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: add BarChart, DualAreaChart, RadialGauge components"
```

---

### Task 9: GlassDashboard Wrapper

**Files:**
- Create: `glassdash/dashboard.py`
- Modify: `glassdash/__init__.py` (add GlassDashboard export)

- [ ] **Step 1: Create dashboard.py**

```python
"""GlassDashboard - main dashboard wrapper."""

from dash import html, dcc
from glassdash.theme import GlassTheme

def GlassDashboard(
    title: str = "Dashboard",
    date_range: tuple = None,
    theme: GlassTheme = None,
    children=None,
    **kwargs
):
    """Main dashboard wrapper with glassmorphism theme.
    
    Args:
        title: Dashboard title
        date_range: Tuple of (start_date, end_date) in yyyy-mm format
        theme: GlassTheme instance
        children: Dashboard content (KPICards, charts, etc.)
    """
    if theme is None:
        theme = GlassTheme()
    
    header = html.Div(
        [
            html.H1(
                title,
                style={
                    "fontSize": "24px",
                    "fontWeight": "700",
                    "background": f"linear-gradient(135deg, {theme.colors['accent']}, {theme.colors['cyan']})",
                    "-webkit-background-clip": "text",
                    "-webkit-text-fill-color": "transparent",
                    "marginBottom": "8px",
                }
            ),
        ],
        style={"textAlign": "center", "marginBottom": "24px"}
    )
    
    if date_range:
        header.children.append(
            html.Div(
                f"{date_range[0]} → {date_range[1]}",
                style={
                    "color": theme.colors["text_muted"],
                    "fontSize": "12px",
                }
            )
        )
    
    content = html.Div(
        children,
        style={
            "maxWidth": "1400px",
            "margin": "0 auto",
        }
    )
    
    return html.Div(
        [
            html.Link(
                href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
                rel="stylesheet"
            ),
            html.Style(children=theme.get_css()),
            header,
            content,
        ],
        **kwargs
    )
```

- [ ] **Step 2: Update glassdash/__init__.py**

```python
"""GlassDash - Beautiful glassmorphism dashboards for Plotly Dash + Polars."""

from glassdash.theme import GlassTheme
from glassdash.dashboard import GlassDashboard
from glassdash.components import (
    GlassCard,
    KPICard,
    LineChart,
    AreaChart,
    MultiLinesChart,
    MultiBarsChart,
    StackedBarChart,
    StackedBarWithLine,
    StackedBarWithBreakdown,
    BarChart,
    DualAreaChart,
    RadialGauge,
)

__all__ = [
    "GlassTheme",
    "GlassDashboard",
    "GlassCard",
    "KPICard",
    "LineChart",
    "AreaChart",
    "MultiLinesChart",
    "MultiBarsChart",
    "StackedBarChart",
    "StackedBarWithLine",
    "StackedBarWithBreakdown",
    "BarChart",
    "DualAreaChart",
    "RadialGauge",
]
```

- [ ] **Step 3: Run tests**

```bash
cd /Users/stephen/dev/glossy
python -c "
from glassdash import GlassDashboard, GlassTheme, KPICard
from glassdash.components import AreaChart, StackedBarChart
import polars as pl

theme = GlassTheme()
df = pl.DataFrame({'month': ['2025-01', '2025-02'], 'value': [10, 15]})

dashboard = GlassDashboard(
    title='My Dashboard',
    date_range=('2025-01', '2025-03'),
    theme=theme,
    children=[
        KPICard(title='FTE', value=24.5, trend=2.3, theme=theme),
        AreaChart(df, x='month', y='value', theme=theme),
    ]
)
print('Dashboard created:', dashboard is not None)
"
```

- [ ] **Step 4: Commit**

```bash
git add -A && git commit -m "feat: add GlassDashboard wrapper"
```

---

### Task 10: Demo App

**Files:**
- Create: `glassdash/demo/app.py`

- [ ] **Step 1: Create demo/app.py with full demo**

```python
"""Demo dashboard showcasing all GlassDash components."""

from dash import Dash
from glassdash import GlassDashboard, GlassTheme, KPICard
from glassdash.components import (
    LineChart, AreaChart, MultiLinesChart, MultiBarsChart,
    StackedBarChart, StackedBarWithLine, StackedBarWithBreakdown,
    BarChart, DualAreaChart, RadialGauge
)
import polars as pl

def create_demo_app():
    """Create demo app with sample data."""
    app = Dash(__name__)
    
    theme = GlassTheme()
    
    df = pl.DataFrame({
        "month": ["2024-07", "2024-08", "2024-09", "2024-10", "2024-11", "2024-12",
                  "2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06"],
        "fte": [18.2, 19.1, 19.5, 20.3, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5],
        "fte_ft": [12, 13, 13, 14, 14, 15, 15, 16, 16, 16, 17, 17],
        "fte_pt": [4, 4, 4, 4, 5, 4, 5, 4, 5, 5, 5, 5],
        "fte_cont": [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        "fte_other": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "total_fte": [19, 20, 20, 21, 22, 22, 23, 23, 24, 24, 25, 25],
        "efficiency": [82, 83, 84, 85, 86, 85, 87, 87, 88, 87, 87, 87],
        "efficacy": [88, 89, 90, 91, 92, 91, 93, 93, 94, 93, 93, 93],
        "yield_pct": [3.2, 3.3, 3.4, 3.5, 3.6, 3.5, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2],
        "code_integration": [65, 70, 75, 78, 80, 82, 85, 87, 88, 90, 92, 95],
        "squads": [4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8],
        "ai_usage": [10, 12, 15, 18, 22, 28, 35, 42, 50, 58, 68, 78],
        "squad_a": [4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8],
        "squad_b": [3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7],
        "squad_c": [3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7],
        "fte_avg": [85, 86, 87, 87, 88, 87, 88, 89, 89, 90, 90, 91],
        "fte_target": [90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90],
    })
    
    app.layout = GlassDashboard(
        title="Workforce Statistics Dashboard",
        date_range=("2024-07-01", "2025-06-13"),
        theme=theme,
        children=[
            html.Div(
                [
                    KPICard(title="FTE", value=24.5, trend=2.3, theme=theme),
                    KPICard(title="Efficiency", value="87.2%", trend=1.8, theme=theme),
                    KPICard(title="Efficacy", value="92.8%", trend=-0.5, theme=theme),
                    KPICard(title="Yield", value="4.2%", trend=0.3, theme=theme),
                ],
                style={"display": "grid", "gridTemplateColumns": "repeat(4, 1fr)", "gap": "16px", "marginBottom": "20px"}
            ),
            AreaChart(df, x="month", y="fte", theme=theme),
            MultiLinesChart(df, x="month", lines={"FTE": "fte", "Target": "total_fte"}, theme=theme),
            MultiBarsChart(df, x="month", bars={"Squad A": "squad_a", "Squad B": "squad_b", "Squad C": "squad_c"}, theme=theme),
            StackedBarChart(df, x="month", segments={
                "Full-time": "fte_ft", "Part-time": "fte_pt", "Contingent": "fte_cont", "Others": "fte_other"
            }, theme=theme),
            StackedBarWithLine(df, x="month", bar_segments={
                "Full-time": "fte_ft", "Part-time": "fte_pt", "Contingent": "fte_cont"
            }, line_y="total_fte", theme=theme),
            StackedBarWithBreakdown(df, x="month", breakdown_bars={"Avg": "fte_avg", "Target": "fte_target"}, theme=theme),
            BarChart(df, x="month", y="squads", theme=theme),
            DualAreaChart(df, x="month", y1="efficiency", y2="efficacy", theme=theme),
            RadialGauge(value=61, max_value=100, label="Yield", theme=theme),
        ],
    )
    
    return app

if __name__ == "__main__":
    app = create_demo_app()
    app.run(debug=True, port=8050)
```

- [ ] **Step 2: Run demo**

```bash
cd /Users/stephen/dev/glossy
pip install dash polars plotly 2>/dev/null
python glassdash/demo/app.py
```

- [ ] **Step 3: Commit**

```bash
git add -A && git commit -m "feat: add demo app"
```

---

## Self-Review Checklist

- [ ] All 12 components implemented (GlassCard, KPICard, LineChart, AreaChart, MultiLinesChart, MultiBarsChart, StackedBarChart, StackedBarWithLine, StackedBarWithBreakdown, BarChart, DualAreaChart, RadialGauge)
- [ ] GlassTheme with customizable colors, fonts, effects
- [ ] GlassDashboard wrapper
- [ ] Demo app with sample data
- [ ] All components accept Polars DataFrames
- [ ] highlight_current works on all time-series charts
- [ ] Theme customization fully documented

---

## Spec Coverage

| Spec Section | Tasks |
|--------------|-------|
| Theme System | Task 1 |
| GlassCard | Task 2 |
| KPICard | Task 2 |
| LineChart | Task 3 |
| AreaChart | Task 3 |
| MultiLinesChart | Task 4 |
| MultiBarsChart | Task 4 |
| StackedBarChart | Task 5 |
| StackedBarWithLine | Task 6 |
| StackedBarWithBreakdown | Task 7 |
| BarChart | Task 8 |
| DualAreaChart | Task 8 |
| RadialGauge | Task 8 |
| GlassDashboard | Task 9 |
| Demo | Task 10 |

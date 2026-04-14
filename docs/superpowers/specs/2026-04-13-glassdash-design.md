# GlassDash - Plotly Dash Glassmorphism Dashboard Library

**Date:** 2026-04-13
**Status:** Approved

## Overview

A Python library providing beautiful glassmorphism-themed dashboard components for Plotly Dash, designed to work seamlessly with Polars DataFrames.

## Design System

### Theme: Glassmorphism
- Frosted glass panels with `backdrop-filter: blur(12px)`
- Semi-transparent backgrounds: `rgba(255,255,255,0.15)`
- Subtle white borders: `rgba(255,255,255,0.2)`
- Vibrant gradient accents (cyan, purple, pink)
- Soft shadows with colored glows on active/highlighted elements

### Color Palette (Defaults - All Customizable)

| Role | Hex | Usage |
|------|-----|-------|
| Background Gradient Start | `#1a1a2e` | Dark base |
| Background Gradient Mid | `#16213e` | Card backgrounds |
| Background Gradient End | `#0f3460` | Deep accent |
| Accent Cyan | `#4facfe` | Highlights, current period |
| Accent Teal | `#00f2fe` | Glow effects |
| Accent Purple | `#667eea` | Primary charts |
| Accent Magenta | `#764ba2` | Secondary charts |
| Success Green | `#10b981` | Positive trends |
| Warning Amber | `#f59e0b` | Caution trends |
| Danger Red | `#e94560` | Negative trends |
| Labor Full-time | `#e94560` | Stacked bar segment |
| Labor Part-time | `#f59e0b` | Stacked bar segment |
| Labor Contingent | `#8b5cf6` | Stacked bar segment |
| Labor Others | `#06b6d4` | Stacked bar segment |

### Typography (Defaults - All Customizable)
- KPI Values: 26px bold
- KPI Labels: 11px uppercase, muted
- Chart Titles: 13-14px medium
- Axis Labels: 9-10px muted

### Customizable Theme

Users can override any value via `GlassTheme`:

```python
from glassdash import GlassTheme

custom = GlassTheme(
    colors={
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
    },
    fonts={
        "family": "Inter, -apple-system, sans-serif",
        "kpi_value": 28,
        "kpi_label": 11,
        "chart_title": 14,
        "axis_label": 10,
    },
    effects={
        "blur": 12,
        "glow": True,
        "animation": True,
    }
)

app.layout = GlassDashboard(theme=custom, children=[...])
```

## Components

### 1. GlassCard
Reusable frosted glass container.
```python
GlassCard(children=[...], title="Optional Title")
```

### 2. KPICard
Key metric display with trend indicator.
```python
KPICard(
    title="FTE",
    value=24.5,
    trend=2.3,  # positive = up, negative = down
    trend_label="% vs last month"
)
```

### 3. LineChart
Simple time series line chart.
```python
LineChart(
    dataframe=polars_df,
    x="month",  # yyyy-mm-dd format
    y="fte",
    color="primary",  # uses theme colors
    highlight_current=True  # glow on last point
)
```

### 4. AreaChart
Time series with gradient fill.
```python
AreaChart(
    dataframe=polars_df,
    x="month",
    y="fte",
    color="primary",
    highlight_current=True
)
```

### 5. MultiLinesChart
Multiple time series lines on same axes.
```python
MultiLinesChart(
    dataframe=polars_df,
    x="month",
    lines={
        "FTE": "fte",
        "Target": "fte_target"
    },
    colors={"FTE": "cyan", "Target": "amber"},
    highlight_current=True
)
```

### 6. MultiBarsChart
Grouped bar chart (multiple bars per x-value).
```python
MultiBarsChart(
    dataframe=polars_df,
    x="month",
    bars={
        "Squad A": "squad_a",
        "Squad B": "squad_b",
        "Squad C": "squad_c"
    },
    colors=["cyan", "purple", "pink"],
    highlight_current=True
)
```

### 7. StackedBarChart
Labor mix or similar proportional data.
```python
StackedBarChart(
    dataframe=polars_df,
    x="month",
    segments={
        "Full-time": "fte_fulltime",
        "Part-time": "fte_parttime",
        "Contingent": "fte_contingent",
        "Others": "fte_others"
    },
    colors={...},  # or use theme defaults
    highlight_current=True
)
```

### 8. StackedBarWithLine
Stacked bar chart with dashed line on secondary y-axis.
Useful for showing total value + composition.
```python
StackedBarWithLine(
    dataframe=polars_df,
    x="month",
    bar_segments={
        "Full-time": "fte_ft",
        "Part-time": "fte_pt",
        "Contingent": "fte_cont",
        "Others": "fte_other"
    },
    line_y="total_fte",  # goes to secondary y-axis
    line_color="cyan",
    line_dash="dash",
    highlight_current=True
)
```

### 9. StackedBarWithBreakdown
Stacked bar chart with horizontal breakdown bar on the right.
Shows main stacked bar + detailed breakdown bars to the side.
```python
StackedBarWithBreakdown(
    dataframe=polars_df,
    x="month",
    bar_segments={
        "Full-time": "fte_ft",
        "Part-time": "fte_pt",
        "Contingent": "fte_cont",
        "Others": "fte_other"
    },
    breakdown_bars={
        "Avg": "fte_avg",
        "Target": "fte_target"
    },
    breakdown_orientation="horizontal",  # bars go to the right
    highlight_current=True
)
```

### 10. BarChart
Simple bar chart for discrete metrics.
```python
BarChart(
    dataframe=polars_df,
    x="month",
    y="squads",
    color="purple",
    highlight_current=True
)
```

### 11. DualAreaChart
Overlay two metrics (e.g., Efficiency + Efficacy).
```python
DualAreaChart(
    dataframe=polars_df,
    x="month",
    y1="efficiency",
    y2="efficacy",
    color1="cyan",
    color2="pink",
    labels=["Efficiency", "Efficacy"]
)
```

### 12. RadialGauge
Single metric with arc visualization.
```python
RadialGauge(
    value=4.2,
    max_value=10,
    label="Yield",
    color="success"
)
```

## Dashboard Layout

### Theme Wrapper
```python
GlassDashboard(
    title="Workforce Statistics",
    date_range=("2024-07-01", "2025-06-13"),
    children=[
        KPICard(...),  # row of 4 KPIs
        AreaChart(...),  # FTE trend
        StackedBarChart(...),  # Labor mix
        LineChart(...),  # Simple trend line
        MultiLinesChart(...),  # Multiple metrics
        MultiBarsChart(...),  # Grouped comparison
        StackedBarWithLine(...),  # Stacked + secondary line
        StackedBarWithBreakdown(...),  # Stacked + breakdown
        BarChart(...),  # Discrete values
        DualAreaChart(...),  # Two overlaid areas
        RadialGauge(...)  # Single metric gauge
    ]
)
```

## Data Format

All charts accept Polars DataFrames with:
- `month` column: string in `yyyy-mm` format (displayed as `yyyy-mm`)
- All metrics as numeric columns
- 12 rows max (last 12 months including current)

## Animations

- Page load: staggered fade-in (opacity 0→1, 300ms, 50ms stagger)
- Hover: subtle scale (1.02x) + enhanced glow
- Current period: pulsing glow animation (2s infinite)
- Chart updates: smooth transitions (400ms ease-out)

## File Structure

```
glassdash/
├── __init__.py
├── theme.py          # Color constants, CSS
├── components.py     # All chart components
├── dashboard.py      # Dashboard wrapper
└── utils.py          # Polars helpers
```

## Dependencies

- `plotly`
- `dash`
- `polars`

## Usage Example

```python
from glassdash import GlassDashboard, KPICard, AreaChart, StackedBarChart
import polars as pl

df = pl.read_csv("workforce.csv")

app = Dash(__name__)

app.layout = GlassDashboard(
    title="Workforce Statistics",
    children=[
        KPICard(title="FTE", value=24.5, trend=2.3),
        KPICard(title="Efficiency", value=87.2, trend=1.8),
        KPICard(title="Efficacy", value=92.8, trend=-0.5),
        KPICard(title="Yield", value=4.2, trend=0.3),
        AreaChart(df, x="month", y="fte"),
        StackedBarChart(df, x="month", segments={...}),
    ]
)
```

## Scope

1. Core theme system (colors, glass effect CSS)
2. KPICard component
3. LineChart - simple time series line
4. AreaChart - line with gradient fill
5. MultiLinesChart - multiple overlaid lines
6. MultiBarsChart - grouped bars
7. StackedBarChart - stacked proportional bars
8. StackedBarWithLine - stacked bar + dashed line on secondary axis
9. StackedBarWithBreakdown - stacked bar + horizontal breakdown bars
10. BarChart - simple discrete bars
11. DualAreaChart - two overlaid areas
12. RadialGauge - arc/gauge visualization
13. GlassDashboard layout wrapper
14. Polars DataFrame utilities
15. Demo dashboard with sample data

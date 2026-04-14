# GlassDash

Beautiful glassmorphism dashboards for Plotly Dash + Polars.

## Installation

```bash
pip install glassdash
```

Or install from source:

```bash
pip install -e .
```

## Quick Start

```python
from dash import Dash
from glassdash import GlassDashboard, GlassTheme, KPICard
from glassdash.components import AreaChart, StackedBarChart
import polars as pl

app = Dash(__name__)
theme = GlassTheme()

df = pl.DataFrame({
    "month": ["2024-07", "2024-08", "2024-09"],
    "fte": [18.2, 19.1, 19.5],
})

app.layout = GlassDashboard(
    title="My Dashboard",
    theme=theme,
    children=[
        KPICard(title="FTE", value=19.5, trend=2.3, theme=theme),
        AreaChart(df, x="month", y="fte", theme=theme),
        StackedBarChart(df, x="month", segments={...}, theme=theme),
    ],
)

if __name__ == "__main__":
    app.run(debug=True, port=8050)
```

## Components

| Component | Description |
|-----------|-------------|
| `GlassCard` | Frosted glass container |
| `KPICard` | Key metric with trend indicator |
| `LineChart` | Time series line chart |
| `AreaChart` | Line chart with gradient fill |
| `MultiLinesChart` | Multiple overlaid lines |
| `MultiBarsChart` | Grouped bar chart |
| `StackedBarChart` | Stacked proportional bars |
| `StackedBarWithLine` | Stacked bars + dashed line |
| `StackedBarWithBreakdown` | Stacked bars + breakdown |
| `BarChart` | Simple bar chart |
| `DualAreaChart` | Two overlaid areas |
| `RadialGauge` | Arc/gauge visualization |

## Theme

Customize colors, fonts, and effects:

```python
custom = GlassTheme(
    colors={
        "primary": "#e94560",
        "accent": "#4facfe",
        "glass_bg": "rgba(255,255,255,0.15)",
    },
    fonts={"family": "Inter, sans-serif", "kpi_value": 28},
    effects={"blur": 12, "glow": True},
)
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run linter
ruff check glassdash/

# Run demo
python -m glassdash.demo.app
```

## Requirements

- Python >= 3.10
- dash >= 2.0
- polars >= 0.19
- plotly >= 5.0

---
name: glassdash-component-development
description: Use when creating new chart components for GlassDash or modifying existing ones
---

# GlassDash Component Development

## Overview

GlassDash provides 12 chart components (AreaChart, BarChart, LineChart, etc.) built on Plotly Dash + Polars with a glassmorphism theme. All components follow a consistent validation and rendering pattern.

## Component Pattern

Every chart component follows this structure:

```python
from glassdash.components._base import _with_validation
from glassdash.theme import GlassTheme

@_with_validation
def SomeChart(dataframe, x="month", y="value", theme=None, **kwargs):
    if theme is None:
        theme = GlassTheme()
    # ... return Dash html.Div with className="glass-card"
```

Key points:
- **Always use `@_with_validation` decorator** - validates DataFrame before rendering
- **Default x="month"** - expects YYYY-MM string format
- **Default y="value"** - numeric column
- **theme=None** - falls back to GlassTheme()
- **Return `html.Div` with `className="glass-card"`**

## Validation Schema System

Components are validated against schemas in `glassdash/components/_validation.py`:

```python
SCHEMAS = {
    "SomeChart": {"x": pl.Utf8, "y": NUMERIC},
    # ...
}
```

### Schema Types

| Schema Type | Accepts |
|-------------|---------|
| `pl.Utf8` | String columns (month names, categories) |
| `NUMERIC` | Int64, Int32, Float64, Float32 columns |

### Important: `line_y` is NUMERIC, not String

`StackedBarWithLine` has `line_y` in its schema as NUMERIC (since it's a column of numeric values), not Utf8.

## Creating a New Component

1. **Create file** in `glassdash/components/`
2. **Import decorator and theme**:
   ```python
   from glassdash.components._base import _with_validation
   from glassdash.theme import GlassTheme
   ```
3. **Define function with decorator**:
   ```python
   @_with_validation
   def NewChart(dataframe, x="month", y="value", theme=None, **kwargs):
   ```
4. **Add schema to `_validation.py`**:
   ```python
   SCHEMAS["NewChart"] = {"x": pl.Utf8, "y": NUMERIC}
   ```
5. **Export from `glassdash/components/__init__.py`**
6. **Add tests** in `tests/test_components.py`
7. **Run demo** to verify: `python -m glassdash.demo.app`

## Common Patterns

### Filter Panel (for LineChart/AreaChart)

Components with date filtering include a toggle filter panel:

```python
filter_panel = html.Div(
    [html.Div([...dcc.Input for date range...])],
    id=filter_id,
    className="glass-filter-panel",
    style={"display": "none"},
)
toggle_btn = html.Button("⚙ Filter", id=f"{chart_id}-toggle-filter", n_clicks=0)
```

### Plotly Graph

```python
from plotly import graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(x=data, y=data, mode="lines", fill="tonexty"))
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family=theme.fonts["family"], color=theme.colors["text_muted"]),
    xaxis=dict(showgrid=False, zerolinecolor="rgba(255,255,255,0.3)"),
    yaxis=dict(showgrid=False, zerolinecolor="rgba(255,255,255,0.3)"),
)
```

## Testing

Run all tests:
```bash
python -m pytest tests/ -v
```

Add component tests following `tests/test_components.py` pattern:
```python
def test_new_chart_renders(self, theme, sample_df):
    """NewChart should render without validation errors."""
    result = NewChart(sample_df, x="month", y="fte", theme=theme)
    assert result is not None
    assert "error" not in type(result).__name__.lower()
```

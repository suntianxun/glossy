# GlassDash Library Design

**Date:** 2026-04-14
**Status:** Draft

## Overview

Transform GlassDash from a demo app into a reusable library for creating glassmorphism dashboards. Users import chart functions, pass Polars DataFrames, and get validated Dash components.

## Goals

1. **Library as dependency** - `pip install glassdash`, import charts, use immediately
2. **Pandera validation** - DataFrame schemas validated at chart call time
3. **Graceful errors** - Validation failures display in UI, not as exceptions
4. **Beautiful glass theme** - Consistent glassmorphism aesthetic throughout

## Architecture

### Charts as Functions

Charts remain functions (not classes) for simplicity:

```python
from glassdash import LineChart, AreaChart, GlassTheme

theme = GlassTheme()

LineChart(df, x="month", y="fte", theme=theme)
AreaChart(df, x="month", y="value", theme=theme)
```

### Built-in Schemas

Each chart function has a built-in schema defining required columns and types:

```python
SCHEMAS = {
    "LineChart": {"month": pl.Utf8, "value": pl.Float64},
    "AreaChart": {"month": pl.Utf8, "value": pl.Float64},
    "MultiLinesChart": {"month": pl.Utf8, "lines": {"*": pl.Float64}},
    "MultiBarsChart": {"month": pl.Utf8, "bars": {"*": pl.Float64}},
    "StackedBarChart": {"month": pl.Utf8, "segments": {"*": pl.Float64}},
    "StackedBarWithLine": {"month": pl.Utf8, "bar_segments": {"*": pl.Float64}, "line_y": pl.Float64},
    "StackedBarWithBreakdown": {"month": pl.Utf8, "bar_segments": {"*": pl.Float64}, "breakdown": dict},
    "BarChart": {"month": pl.Utf8, "y": pl.Float64},
    "DualAreaChart": {"month": pl.Utf8, "y1": pl.Float64, "y2": pl.Float64},
    "RadialGauge": {},  # no dataframe
    "GlassCard": {},  # no dataframe
    "KPICard": {},  # no dataframe
}
```

### Validation Flow

```
Chart(dataframe, x="month", y="value")
    │
    ▼
_validate_schema(dataframe, schema)
    │
    ├── Pass → render chart
    │
    └── Fail → render error card
```

### Error Display

When validation fails, chart renders an error glass card:

```python
def _render_error_card(chart_name: str, errors: list[str], found_columns: list[str]) -> html.Div:
    return html.Div(
        [
            html.Div("⚠️ Validation Error", className="glass-error-title"),
            html.Div(f"{chart_name} requires:", className="glass-error-text"),
            html.Ul([html.Li(e) for e in errors], className="glass-error-list"),
            html.Div(f"Found: {found_columns}", className="glass-error-found"),
        ],
        className="glass-card glass-error-card"
    )
```

Error styling:
- Red accent border (`#e94560`)
- Warning icon (⚠️)
- Clear listing of missing/incorrect columns

## Components

### 1. Dashboard Structure

```
GlassDashboard
├── html.Link (Google Fonts)
├── html.Link (glass.css)
├── Header (title, date_range)
└── Content
    └── Sections
        └── Section
            ├── Section Header (glass effect, title + description)
            └── Charts (no glass wrapper)
```

### 2. Section Component

```python
def Section(
    title: str,
    description: str = None,
    children=None,
    theme=None,
    **kwargs
) -> html.Div:
    """
    Groups charts with optional title and description.
    """
    header = html.Div([
        html.H2(title, className="glass-section-title"),
        html.P(description, className="glass-section-description") if description else None,
    ], className="glass-section-header")

    return html.Div([
        header,
        html.Div(children, className="glass-section-children")
    ], className="glass-section", **kwargs)
```

### 3. Section Styling (glass-section-header)

```css
.glass-section-header {
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 16px;
}
.glass-section-title {
    font-size: 18px;
    font-weight: 600;
    color: #ffffff;
    margin: 0 0 4px 0;
}
.glass-section-description {
    font-size: 12px;
    color: rgba(255,255,255,0.6);
    margin: 0;
}
.glass-section-children {
    display: grid;
    gap: 20px;
}
```

## Validation Implementation

### Custom Exception

```python
class GlassValidationError(Exception):
    """Raised when DataFrame doesn't match chart schema."""
    def __init__(self, chart_name: str, errors: list[str], found_columns: list[str]):
        self.chart_name = chart_name
        self.errors = errors
        self.found_columns = found_columns
        super().__init__(f"{chart_name} validation failed: {errors}")
```

### Schema Validator

```python
def validate_dataframe(
    df: pl.DataFrame,
    schema: dict[str, type]
) -> tuple[bool, list[str]]:
    """
    Validate DataFrame against schema.
    Returns (is_valid, list_of_errors).
    """
    errors = []
    found_columns = df.columns

    for col, expected_type in schema.items():
        if col not in df.columns:
            errors.append(f"'{col}' - missing")
        elif not _is_compatible_type(df[col].dtype, expected_type):
            errors.append(f"'{col}' - expected {expected_type.__name__}, got {df[col].dtype}")

    return len(errors) == 0, errors
```

### Chart Wrapper

```python
def _with_validation(chart_func):
    def wrapper(dataframe, **kwargs):
        schema = SCHEMAS[chart_func.__name__]
        is_valid, errors = validate_dataframe(dataframe, schema)
        if not is_valid:
            return _render_error_card(chart_func.__name__, errors, dataframe.columns)
        return chart_func(dataframe, **kwargs)
    return wrapper

@_with_validation
def LineChart(dataframe, x="month", y="value", theme=None, **kwargs):
    ...
```

## File Structure

```
glassdash/
├── __init__.py              # Public API: all charts, GlassTheme, GlassDashboard, Section
├── theme.py                 # GlassTheme dataclass
├── dashboard.py             # GlassDashboard, Section
├── components/
│   ├── __init__.py          # Re-exports all charts
│   ├── _validation.py       # SCHEMAS, validate_dataframe, GlassValidationError, _render_error_card
│   ├── _base.py              # _with_validation decorator
│   ├── line_chart.py
│   ├── area_chart.py
│   └── ...
└── assets/
    └── glass.css
```

## Dependencies

```toml
[project]
dependencies = [
    "dash>=2.0",
    "polars>=0.19",
    "plotly>=5.0",
    "pandera>=0.19",
]
```

## Usage Example

```python
from dash import Dash
from glassdash import (
    GlassDashboard, GlassTheme, Section,
    LineChart, AreaChart, StackedBarChart
)
import polars as pl

app = Dash(__name__)
theme = GlassTheme()

df = pl.read_csv("workforce.csv")

app.layout = GlassDashboard(
    title="Workforce Dashboard",
    theme=theme,
    children=[
        Section(
            "FTE Trends",
            "Full-time equivalent over time",
            children=[
                LineChart(df, x="month", y="fte", theme=theme),
                AreaChart(df, x="month", y="fte", theme=theme),
            ]
        ),
        Section(
            "Labor Mix",
            "Breakdown by employment type",
            children=[
                StackedBarChart(df, x="month", segments={
                    "Full-time": "fte_ft",
                    "Part-time": "fte_pt",
                }, theme=theme),
            ]
        ),
    ]
)

if __name__ == "__main__":
    app.run(debug=True, port=8050)
```

## Validation Error Examples

### Missing Column
```
┌─────────────────────────────────┐
│  ⚠️  Validation Error          │
│                                 │
│  LineChart requires:            │
│  • 'value' - missing           │
│                                 │
│  Found: ['month', 'amount']    │
└─────────────────────────────────┘
```

### Wrong Type
```
┌─────────────────────────────────┐
│  ⚠️  Validation Error          │
│                                 │
│  LineChart requires:            │
│  • 'value' - expected float64, │
│    got str                     │
│                                 │
│  Found: ['month', 'value']     │
└─────────────────────────────────┘
```

## Open Questions

- [ ] How to handle optional columns?
- [ ] Should validation run in production or only in debug mode?
- [ ] Support for Polars LazyFrame?

## TODO

- [ ] Create `glassdash/components/_validation.py`
- [ ] Create `glassdash/components/_base.py`
- [ ] Update all chart functions with `@_with_validation`
- [ ] Add Section component to dashboard.py
- [ ] Add glass-section-* styles to glass.css
- [ ] Add pandera to dependencies
- [ ] Update demo app to use Section
- [ ] Test validation with various error cases

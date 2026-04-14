# GlassDash Library Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform GlassDash into a reusable library with pandera.polars validation and Section grouping.

**Architecture:** 
- Create `_validation.py` for schema definitions and validation logic
- Create `_base.py` for the `@_with_validation` decorator
- Wrap each chart function with the decorator
- Add Section component to dashboard.py
- Update CSS for section styling

**Tech Stack:** Python, Polars, Pandera, Dash, Plotly

---

## File Structure

```
glassdash/
├── __init__.py
├── theme.py
├── dashboard.py              # Add Section component
├── components/
│   ├── __init__.py
│   ├── _validation.py        # CREATE: schemas, GlassValidationError, validate_dataframe, _render_error_card
│   ├── _base.py              # CREATE: @_with_validation decorator
│   ├── glass_card.py         # No dataframe - skip
│   ├── kpi_card.py          # No dataframe - skip
│   ├── line_chart.py         # UPDATE: add decorator
│   ├── area_chart.py         # UPDATE: add decorator
│   ├── multi_lines.py        # UPDATE: add decorator
│   ├── multi_bars.py         # UPDATE: add decorator
│   ├── stacked_bar.py        # UPDATE: add decorator
│   ├── stacked_bar_line.py   # UPDATE: add decorator
│   ├── stacked_bar_breakdown.py  # UPDATE: add decorator
│   ├── bar_chart.py          # UPDATE: add decorator
│   ├── dual_area.py          # UPDATE: add decorator
│   └── radial_gauge.py      # No dataframe - skip
├── assets/
│   └── glass.css             # UPDATE: add section styles
└── demo/
    └── app.py                # UPDATE: use Section
```

---

## Task 1: Create validation module

**Files:**
- Create: `glassdash/components/_validation.py`

- [ ] **Step 1: Create _validation.py with SCHEMAS, GlassValidationError, validate_dataframe, _render_error_card**

```python
"""Validation for GlassDash chart components."""

import polars as pl
from dash import html


class GlassValidationError(Exception):
    """Raised when DataFrame doesn't match chart schema."""

    def __init__(self, chart_name: str, errors: list[str], found_columns: list[str]):
        self.chart_name = chart_name
        self.errors = errors
        self.found_columns = found_columns
        super().__init__(f"{chart_name} validation failed: {errors}")


SCHEMAS = {
    "LineChart": {"x": pl.Utf8, "y": pl.Float64},
    "AreaChart": {"x": pl.Utf8, "y": pl.Float64},
    "MultiLinesChart": {"x": pl.Utf8},
    "MultiBarsChart": {"x": pl.Utf8},
    "StackedBarChart": {"x": pl.Utf8},
    "StackedBarWithLine": {"x": pl.Utf8, "line_y": pl.Utf8},
    "StackedBarWithBreakdown": {"x": pl.Utf8},
    "BarChart": {"x": pl.Utf8, "y": pl.Float64},
    "DualAreaChart": {"x": pl.Utf8, "y1": pl.Float64, "y2": pl.Float64},
    "GlassCard": {},
    "KPICard": {},
    "RadialGauge": {},
}


def validate_dataframe(
    df: pl.DataFrame,
    schema: dict[str, type],
) -> tuple[bool, list[str]]:
    """Validate DataFrame against schema. Returns (is_valid, errors)."""
    errors = []
    found_columns = df.columns

    for col, expected_type in schema.items():
        if col not in df.columns:
            errors.append(f"'{col}' - missing")
        elif not _is_compatible_type(df[col].dtype, expected_type):
            errors.append(f"'{col}' - expected {expected_type.__name__}, got {df[col].dtype}")

    return len(errors) == 0, errors


def _is_compatible_type(polars_dtype, expected) -> bool:
    """Check if Polars dtype is compatible with expected Python type."""
    dtype_map = {
        pl.Utf8: str,
        pl.Float64: float,
        pl.Int64: int,
        pl.Int32: int,
        pl.Boolean: bool,
    }
    return dtype_map.get(polars_dtype) == expected


def _render_error_card(chart_name: str, errors: list[str], found_columns: list[str]) -> html.Div:
    """Render an error card when validation fails."""
    return html.Div(
        [
            html.Div("⚠️  Validation Error", className="glass-error-title"),
            html.Div(f"{chart_name} requires:", className="glass-error-text"),
            html.Ul([html.Li(e) for e in errors], className="glass-error-list"),
            html.Div(f"Found: {found_columns}", className="glass-error-found"),
        ],
        className="glass-card glass-error-card",
        style={"minHeight": "150px"}
    )
```

- [ ] **Step 2: Commit**

```bash
git add glassdash/components/_validation.py
git commit -m "feat: add validation module with schemas and error rendering"
```

---

## Task 2: Create base decorator module

**Files:**
- Create: `glassdash/components/_base.py`

- [ ] **Step 1: Create _base.py with @_with_validation decorator**

```python
"""Base decorator for GlassDash chart components."""

from functools import wraps
from glassdash.components._validation import SCHEMAS, validate_dataframe, _render_error_card


def _with_validation(chart_func):
    """Decorator that validates DataFrame before calling chart function."""

    @wraps(chart_func)
    def wrapper(dataframe=None, **kwargs):
        schema = SCHEMAS.get(chart_func.__name__, {})

        if schema and dataframe is not None:
            is_valid, errors = validate_dataframe(dataframe, schema)
            if not is_valid:
                return _render_error_card(chart_func.__name__, errors, dataframe.columns)

        return chart_func(dataframe=dataframe, **kwargs)

    return wrapper
```

- [ ] **Step 2: Commit**

```bash
git add glassdash/components/_base.py
git commit -m "feat: add validation decorator base module"
```

---

## Task 3: Update LineChart with validation

**Files:**
- Modify: `glassdash/components/line_chart.py:1-10`

- [ ] **Step 1: Add import for decorator**

Add after existing imports:
```python
from glassdash.components._base import _with_validation
```

- [ ] **Step 2: Add decorator to LineChart function**

Change:
```python
def LineChart(
```

To:
```python
@_with_validation
def LineChart(
```

- [ ] **Step 3: Run lint check**

```bash
ruff check glassdash/components/line_chart.py
```

- [ ] **Step 4: Commit**

```bash
git add glassdash/components/line_chart.py
git commit -m "feat: add validation to LineChart"
```

---

## Task 4: Update AreaChart with validation

**Files:**
- Modify: `glassdash/components/area_chart.py`

- [ ] **Step 1: Add import and decorator**

```python
from glassdash.components._base import _with_validation
```

Add `@_with_validation` before function definition.

- [ ] **Step 2: Run lint check and commit**

```bash
ruff check glassdash/components/area_chart.py && git add glassdash/components/area_chart.py && git commit -m "feat: add validation to AreaChart"
```

---

## Task 5: Update MultiLinesChart with validation

**Files:**
- Modify: `glassdash/components/multi_lines.py`

- [ ] **Step 1: Add import and decorator**

- [ ] **Step 2: Run lint check and commit**

```bash
ruff check glassdash/components/multi_lines.py && git add glassdash/components/multi_lines.py && git commit -m "feat: add validation to MultiLinesChart"
```

---

## Task 6: Update MultiBarsChart with validation

**Files:**
- Modify: `glassdash/components/multi_bars.py`

- [ ] **Step 1: Add import and decorator**

- [ ] **Step 2: Run lint check and commit**

```bash
ruff check glassdash/components/multi_bars.py && git add glassdash/components/multi_bars.py && git commit -m "feat: add validation to MultiBarsChart"
```

---

## Task 7: Update StackedBarChart with validation

**Files:**
- Modify: `glassdash/components/stacked_bar.py`

- [ ] **Step 1: Add import and decorator**

- [ ] **Step 2: Run lint check and commit**

```bash
ruff check glassdash/components/stacked_bar.py && git add glassdash/components/stacked_bar.py && git commit -m "feat: add validation to StackedBarChart"
```

---

## Task 8: Update StackedBarWithLine with validation

**Files:**
- Modify: `glassdash/components/stacked_bar_line.py`

- [ ] **Step 1: Add import and decorator**

- [ ] **Step 2: Run lint check and commit**

```bash
ruff check glassdash/components/stacked_bar_line.py && git add glassdash/components/stacked_bar_line.py && git commit -m "feat: add validation to StackedBarWithLine"
```

---

## Task 9: Update StackedBarWithBreakdown with validation

**Files:**
- Modify: `glassdash/components/stacked_bar_breakdown.py`

- [ ] **Step 1: Add import and decorator**

- [ ] **Step 2: Run lint check and commit**

```bash
ruff check glassdash/components/stacked_bar_breakdown.py && git add glassdash/components/stacked_bar_breakdown.py && git commit -m "feat: add validation to StackedBarWithBreakdown"
```

---

## Task 10: Update BarChart with validation

**Files:**
- Modify: `glassdash/components/bar_chart.py`

- [ ] **Step 1: Add import and decorator**

- [ ] **Step 2: Run lint check and commit**

```bash
ruff check glassdash/components/bar_chart.py && git add glassdash/components/bar_chart.py && git commit -m "feat: add validation to BarChart"
```

---

## Task 11: Update DualAreaChart with validation

**Files:**
- Modify: `glassdash/components/dual_area.py`

- [ ] **Step 1: Add import and decorator**

- [ ] **Step 2: Run lint check and commit**

```bash
ruff check glassdash/components/dual_area.py && git add glassdash/components/dual_area.py && git commit -m "feat: add validation to DualAreaChart"
```

---

## Task 12: Add Section component to dashboard.py

**Files:**
- Modify: `glassdash/dashboard.py`

- [ ] **Step 1: Add Section function after GlassDashboard**

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
    theme = theme or GlassTheme()

    header = html.Div([
        html.H2(title, className="glass-section-title"),
        html.P(description, className="glass-section-description") if description else None,
    ], className="glass-section-header")

    return html.Div([
        header,
        html.Div(children, className="glass-section-children")
    ], className="glass-section", **kwargs)
```

- [ ] **Step 2: Add Section to imports in __init__.py if needed**

- [ ] **Step 3: Commit**

```bash
git add glassdash/dashboard.py && git commit -m "feat: add Section component for chart grouping"
```

---

## Task 13: Update glass.css with section and error styles

**Files:**
- Modify: `glassdash/assets/glass.css`

- [ ] **Step 1: Append section and error styles to glass.css**

```css
/* Section styles */
.glass-section {
    margin-bottom: 32px;
}
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

/* Error card styles */
.glass-error-card {
    border-left: 4px solid #e94560;
    min-height: 150px;
}
.glass-error-title {
    font-size: 14px;
    font-weight: 600;
    color: #e94560;
    margin-bottom: 8px;
}
.glass-error-text {
    font-size: 12px;
    color: rgba(255,255,255,0.8);
    margin-bottom: 4px;
}
.glass-error-list {
    font-size: 11px;
    color: rgba(255,255,255,0.7);
    margin: 0;
    padding-left: 20px;
}
.glass-error-found {
    font-size: 11px;
    color: rgba(255,255,255,0.5);
    margin-top: 8px;
}
```

- [ ] **Step 2: Commit**

```bash
git add glassdash/assets/glass.css && git commit -m "feat: add section and error card styles to glass.css"
```

---

## Task 14: Update pyproject.toml with pandera dependency

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Add pandera to dependencies**

Change:
```toml
dependencies = [
    "dash>=2.0",
    "polars>=0.19",
    "plotly>=5.0",
]
```

To:
```toml
dependencies = [
    "dash>=2.0",
    "polars>=0.19",
    "plotly>=5.0",
    "pandera>=0.19",
]
```

- [ ] **Step 2: Run uv lock**

```bash
uv lock
```

- [ ] **Step 3: Commit**

```bash
git add pyproject.toml uv.lock && git commit -m "chore: add pandera dependency"
```

---

## Task 15: Update demo app to use Section

**Files:**
- Modify: `glassdash/demo/app.py`

- [ ] **Step 1: Import Section**

Add to imports:
```python
from glassdash import GlassDashboard, GlassTheme, KPICard, Section
```

- [ ] **Step 2: Wrap chart groups with Section components**

Organize charts into logical sections with titles and descriptions.

- [ ] **Step 3: Commit**

```bash
git add glassdash/demo/app.py && git commit -m "feat: update demo to use Section grouping"
```

---

## Task 16: Test validation

- [ ] **Step 1: Create a test DataFrame with wrong columns and verify error card renders**

```bash
.venv/bin/python -c "
from glassdash import LineChart, GlassTheme
import polars as pl
theme = GlassTheme()

# Wrong columns
df = pl.DataFrame({'date': ['2024-01'], 'amount': [1.0]})
result = LineChart(dataframe=df, x='month', y='value', theme=theme)
print('Type:', type(result).__name__)
print('Has error:', 'error' in str(result.children[0].className).lower())
"
```

- [ ] **Step 2: Test with correct columns**

```bash
.venv/bin/python -c "
from glassdash import LineChart, GlassTheme
import polars as pl
theme = GlassTheme()

# Correct columns
df = pl.DataFrame({'month': ['2024-01'], 'value': [1.0]})
result = LineChart(dataframe=df, x='month', y='value', theme=theme)
print('Type:', type(result).__name__)
"
```

---

## Spec Coverage Check

- [x] Validation module created (Task 1)
- [x] Base decorator created (Task 2)
- [x] All 8 dataframe charts wrapped with validation (Tasks 3-11)
- [x] Section component added (Task 12)
- [x] CSS styles for section and error cards (Task 13)
- [x] pandera dependency added (Task 14)
- [x] Demo app updated (Task 15)
- [x] Validation tested (Task 16)

---

**Plan complete.** Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?

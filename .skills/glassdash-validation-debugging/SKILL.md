---
name: glassdash-validation-debugging
description: Use when charts show "requires: x - missing" or type validation errors in GlassDash
---

# GlassDash Validation Debugging

## Symptoms

Charts display error cards with messages like:
- `'y' - missing`
- `'x' - expected Float64, got Int64`
- `'y1' - expected Float64, got Int64`
- `'line_y' - expected String, got Int64`

## Root Causes

### 1. Column Name Mapping Bug

The `_with_validation` decorator must resolve actual column names from parameters. If it checks for columns literally named `"x"` and `"y"` instead of using the parameter values (`x="month"`, y="fte"`), validation fails.

**Fix location**: `glassdash/components/_base.py`

The decorator should inspect function signature and bind arguments:
```python
sig = inspect.signature(chart_func)
bound = sig.bind_partial(**kwargs)
for param_name, param in sig.parameters.items():
    if param_name not in bound.arguments and param.default is not inspect.Parameter.empty:
        bound.arguments[param_name] = param.default
# Map schema keys to actual column names
column_mapping = {}
for key in schema.keys():
    if key in bound.arguments:
        val = bound.arguments[key]
        if isinstance(val, str):
            column_mapping[key] = val
```

### 2. Type Comparison Bug

`_is_compatible_type` must compare Polars dtypes directly, not convert to Python types. The schema stores Polars types (`pl.Float64`), not Python types (`float`).

**Fix location**: `glassdash/components/_validation.py`

Correct comparison:
```python
def _is_compatible_type(polars_dtype, expected) -> bool:
    if polars_dtype == expected:
        return True
    if isinstance(expected, _Numeric):
        return polars_dtype in {pl.Float64, pl.Float32, pl.Int64, pl.Int32}
    # ... handle aliases
```

### 3. Schema Type Too Strict

If schema says `y: pl.Float64` but DataFrame has Int64 column, validation fails. Use `NUMERIC` marker for any numeric column.

**Fix location**: `glassdash/components/_validation.py`

Define and use NUMERIC marker:
```python
class _Numeric:
    """Marker type for numeric columns (Int/Float)."""
    pass

NUMERIC = _Numeric()

SCHEMAS = {
    "AreaChart": {"x": pl.Utf8, "y": NUMERIC},  # Accepts Int AND Float
}
```

## Validation Flow

```
Component called: AreaChart(df, x="month", y="fte")
        ↓
Decorator intercepts: _with_validation
        ↓
Get schema: SCHEMAS["AreaChart"] → {"x": pl.Utf8, "y": NUMERIC}
        ↓
Bind args to get actual column names: {"x": "month", "y": "fte"}
        ↓
validate_dataframe(df, schema, {"x": "month", "y": "fte"})
        ↓
For each schema key:
  - Get actual column from mapping
  - Check column exists in df
  - Check dtype is compatible
        ↓
Return component or error card
```

## Debugging Steps

1. **Check error message** - tells which column is missing/wrong type
2. **Verify DataFrame columns** - `df.columns` and `df[col].dtype`
3. **Check schema definition** - `SCHEMAS["ComponentName"]`
4. **Verify column mapping** - print `column_mapping` in decorator
5. **Check dtype compatibility** - `_is_compatible_type(df[col].dtype, schema[col])`

## Quick Test

```python
from glassdash.components._validation import validate_dataframe, SCHEMAS
import polars as pl

df = pl.DataFrame({"month": ["2024-07"], "fte": [18.2]})
schema = SCHEMAS["AreaChart"]
column_mapping = {"x": "month", "y": "fte"}

is_valid, errors = validate_dataframe(df, schema, column_mapping)
print(f"Valid: {is_valid}, Errors: {errors}")
```

## Common Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `'y' - missing` | Column mapping not resolving | Fix `_with_validation` decorator |
| `'y' - expected Float64, got Int64` | Schema too strict | Use `NUMERIC` instead of `pl.Float64` |
| `'line_y' - expected String, got Int64` | Schema wrong type | `line_y` is a column, should be `NUMERIC` |
| Type errors after fix | `pl.Utf8 != str` | Compare Polars dtypes directly |

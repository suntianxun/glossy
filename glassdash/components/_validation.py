"""Validation for GlassDash chart components."""

from typing import Any

import polars as pl
from dash import html


class GlassValidationError(Exception):
    """Raised when DataFrame doesn't match chart schema."""

    def __init__(self, chart_name: str, errors: list[str], found_columns: list[str]):
        self.chart_name = chart_name
        self.errors = errors
        self.found_columns = found_columns
        super().__init__(f"{chart_name} validation failed: {errors}")


class _Numeric:
    """Marker type for numeric columns (Int/Float)."""

    pass


class _DictNumeric:
    """Marker: parameter is a dict mapping labels → numeric column names."""

    pass


NUMERIC = _Numeric()
DICT_NUMERIC = _DictNumeric()

SCHEMAS = {
    "LineChart": {"x": pl.Utf8, "y": NUMERIC},
    "MultiLinesChart": {"x": pl.Utf8, "lines": DICT_NUMERIC},
    "MultiBarsChart": {"x": pl.Utf8, "bars": DICT_NUMERIC},
    "MultiAreaChart": {"x": pl.Utf8, "areas": DICT_NUMERIC},
    "StackedBarChart": {"x": pl.Utf8},
    "StackedBarWithLine": {"x": pl.Utf8, "line_y": NUMERIC},
    "StackedBarHorizontalChart": {"category": pl.Utf8, "subcategory": pl.Utf8, "value": NUMERIC},
    "GlassCard": {},
    "KPICard": {},
    "RadialGauge": {},
}


def validate_dataframe(
    df: pl.DataFrame,
    schema: dict[str, type],
    column_mapping: dict[str, str] | None = None,
    arg_values: dict[str, Any] | None = None,
) -> tuple[bool, list[str]]:
    """Validate DataFrame against schema. Returns (is_valid, errors)."""
    errors = []
    column_mapping = column_mapping or {}
    arg_values = arg_values or {}

    for key, expected_type in schema.items():
        if isinstance(expected_type, _DictNumeric):
            val = arg_values.get(key)
            if val is None:
                continue
            if not isinstance(val, dict):
                errors.append(f"'{key}' - expected dict, got {type(val).__name__}")
                continue
            for label, col in val.items():
                if col not in df.columns:
                    errors.append(f"'{key}[\"{label}\"]' column '{col}' - missing")
                elif not _is_compatible_type(df[col].dtype, NUMERIC):
                    errors.append(
                        f"'{key}[\"{label}\"]' column '{col}' - not numeric (got {df[col].dtype})"
                    )
            continue

        actual_col = column_mapping.get(key, key)
        if actual_col not in df.columns:
            errors.append(f"'{key}' - missing")
        elif not _is_compatible_type(df[actual_col].dtype, expected_type):
            errors.append(
                f"'{key}' - expected {expected_type.__name__}, got {df[actual_col].dtype}"
            )

    return len(errors) == 0, errors


def _is_compatible_type(polars_dtype, expected) -> bool:
    """Check if Polars dtype is compatible with expected type."""
    if polars_dtype == expected:
        return True
    if isinstance(expected, _Numeric):
        return polars_dtype in {pl.Float64, pl.Float32, pl.Int64, pl.Int32}
    dtype_aliases = {
        pl.Utf8: {pl.Utf8, pl.String},
        pl.String: {pl.Utf8, pl.String},
        pl.Float64: {pl.Float64, pl.Float32},
        pl.Float32: {pl.Float64, pl.Float32},
        pl.Int64: {pl.Int64, pl.Int32},
        pl.Int32: {pl.Int64, pl.Int32},
    }
    compatible_types = dtype_aliases.get(expected, {expected})
    return polars_dtype in compatible_types


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
        style={"minHeight": "150px"},
    )

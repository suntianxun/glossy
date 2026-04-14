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
        style={"minHeight": "150px"},
    )

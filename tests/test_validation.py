"""Tests for GlassDash validation logic."""

import polars as pl
import pytest

from glassdash.components._validation import (
    NUMERIC,
    SCHEMAS,
    _is_compatible_type,
    validate_dataframe,
)


class TestIsCompatibleType:
    """Test _is_compatible_type function."""

    def test_string_column_with_utf8_schema(self):
        """String column should match Utf8 schema."""
        assert _is_compatible_type(pl.Utf8, pl.Utf8) is True

    def test_string_column_with_string_schema(self):
        """String column should match String schema (alias)."""
        assert _is_compatible_type(pl.String, pl.Utf8) is True

    def test_float_column_with_float64_schema(self):
        """Float64 column should match Float64 schema."""
        assert _is_compatible_type(pl.Float64, pl.Float64) is True

    def test_int_column_with_float64_schema(self):
        """Int64 column should NOT directly match Float64 schema (needs NUMERIC)."""
        assert _is_compatible_type(pl.Int64, pl.Float64) is False

    def test_int_column_with_numeric_schema(self):
        """Int64 column should match NUMERIC schema."""
        assert _is_compatible_type(pl.Int64, NUMERIC) is True

    def test_float_column_with_numeric_schema(self):
        """Float64 column should match NUMERIC schema."""
        assert _is_compatible_type(pl.Float64, NUMERIC) is True

    def test_int32_column_with_numeric_schema(self):
        """Int32 column should match NUMERIC schema."""
        assert _is_compatible_type(pl.Int32, NUMERIC) is True

    def test_float32_column_with_numeric_schema(self):
        """Float32 column should match NUMERIC schema."""
        assert _is_compatible_type(pl.Float32, NUMERIC) is True

    def test_string_column_with_numeric_schema_fails(self):
        """String column should NOT match NUMERIC schema."""
        assert _is_compatible_type(pl.String, NUMERIC) is False


class TestValidateDataframe:
    """Test validate_dataframe function."""

    def test_valid_dataframe_with_default_column_names(self):
        """DataFrame with columns matching schema keys passes validation."""
        df = pl.DataFrame({"month": ["2024-07"], "value": [18.2]})
        schema = SCHEMAS["AreaChart"]
        column_mapping = {"x": "month", "y": "value"}
        is_valid, errors = validate_dataframe(df, schema, column_mapping)
        assert is_valid is True
        assert errors == []

    def test_valid_dataframe_with_custom_column_names(self):
        """DataFrame with custom column names passes when mapped correctly."""
        df = pl.DataFrame({"month": ["2024-07"], "fte": [18.2]})
        schema = SCHEMAS["AreaChart"]
        column_mapping = {"x": "month", "y": "fte"}
        is_valid, errors = validate_dataframe(df, schema, column_mapping)
        assert is_valid is True
        assert errors == []

    def test_missing_column_reports_error(self):
        """Missing column should be reported in errors."""
        df = pl.DataFrame({"month": ["2024-07"]})
        schema = SCHEMAS["AreaChart"]
        column_mapping = {"x": "month", "y": "fte"}
        is_valid, errors = validate_dataframe(df, schema, column_mapping)
        assert is_valid is False
        assert "'y' - missing" in errors

    def test_int_column_passes_numeric_validation(self):
        """Int64 column should pass NUMERIC validation."""
        df = pl.DataFrame({"month": ["2024-07"], "squads": [4]})
        schema = SCHEMAS["BarChart"]
        column_mapping = {"x": "month", "y": "squads"}
        is_valid, errors = validate_dataframe(df, schema, column_mapping)
        assert is_valid is True
        assert errors == []

    def test_float_column_passes_numeric_validation(self):
        """Float64 column should pass NUMERIC validation."""
        df = pl.DataFrame({"month": ["2024-07"], "fte": [18.2]})
        schema = SCHEMAS["AreaChart"]
        column_mapping = {"x": "month", "y": "fte"}
        is_valid, errors = validate_dataframe(df, schema, column_mapping)
        assert is_valid is True
        assert errors == []


class TestSCHEMAS:
    """Test that SCHEMAS are correctly defined."""

    def test_area_chart_schema(self):
        """AreaChart requires x (Utf8) and y (NUMERIC)."""
        schema = SCHEMAS["AreaChart"]
        assert schema["x"] == pl.Utf8
        assert schema["y"] == NUMERIC

    def test_bar_chart_schema(self):
        """BarChart requires x (Utf8) and y (NUMERIC)."""
        schema = SCHEMAS["BarChart"]
        assert schema["x"] == pl.Utf8
        assert schema["y"] == NUMERIC

    def test_dual_area_chart_schema(self):
        """DualAreaChart requires x (Utf8), y1 (NUMERIC), y2 (NUMERIC)."""
        schema = SCHEMAS["DualAreaChart"]
        assert schema["x"] == pl.Utf8
        assert schema["y1"] == NUMERIC
        assert schema["y2"] == NUMERIC

    def test_stacked_bar_with_line_schema(self):
        """StackedBarWithLine requires x (Utf8) and line_y (NUMERIC)."""
        schema = SCHEMAS["StackedBarWithLine"]
        assert schema["x"] == pl.Utf8
        assert schema["line_y"] == NUMERIC

    def test_line_chart_schema(self):
        """LineChart requires x (Utf8) and y (NUMERIC)."""
        schema = SCHEMAS["LineChart"]
        assert schema["x"] == pl.Utf8
        assert schema["y"] == NUMERIC

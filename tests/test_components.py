"""Tests for GlassDash chart components."""

import polars as pl
import pytest

from glassdash import GlassTheme
from glassdash.components import (
    ChartsGroup,
    GlassCard,
    KPICard,
    LineChart,
    MultiAreaChart,
    MultiBarsChart,
    MultiLinesChart,
    RadialGauge,
    StackedBarChart,
    StackedBarHorizontalChart,
    StackedBarWithLine,
)


@pytest.fixture
def theme():
    """Create a GlassTheme for tests."""
    return GlassTheme()


@pytest.fixture
def sample_df():
    """Create sample DataFrame for tests."""
    return pl.DataFrame(
        {
            "month": ["2024-07", "2024-08", "2024-09"],
            "fte": [18.2, 19.1, 19.5],
            "fte_ft": [12, 13, 13],
            "fte_pt": [4, 4, 4],
            "fte_cont": [2, 2, 2],
            "fte_other": [1, 1, 1],
            "total_fte": [19, 20, 20],
            "efficiency": [82, 83, 84],
            "efficacy": [88, 89, 90],
            "yield_pct": [3.2, 3.3, 3.4],
            "squads": [4, 4, 5],
            "squad_a": [4, 4, 5],
            "squad_b": [3, 4, 4],
            "squad_c": [3, 3, 4],
        }
    )


@pytest.fixture
def sample_headcount_df():
    """Create sample headcount DataFrame for horizontal bar tests."""
    return pl.DataFrame(
        {
            "category": ["Q1 2025", "Q1 2025", "Q2 2025", "Q2 2025"],
            "subcategory": ["Engineering", "Sales", "Engineering", "Sales"],
            "value": [45, 20, 52, 22],
        }
    )


class TestGlassCard:
    """Test GlassCard component."""

    def test_glass_card_renders(self, theme):
        """GlassCard should render without errors."""
        result = GlassCard(children="Test content", theme=theme)
        assert result is not None
        assert "glass-card" in result.className

    def test_glass_card_with_title(self, theme):
        """GlassCard should accept title prop."""
        result = GlassCard(children="Test", title="My Card", theme=theme)
        assert result is not None


class TestKPICard:
    """Test KPICard component."""

    def test_kpi_card_renders(self, theme):
        """KPICard should render without errors."""
        result = KPICard(title="FTE", value=24.5, trend=2.3, theme=theme)
        assert result is not None
        assert "glass-card" in result.className

    def test_kpi_card_with_string_value(self, theme):
        """KPICard should accept string value."""
        result = KPICard(title="Efficiency", value="87.2%", trend=1.8, theme=theme)
        assert result is not None


class TestMultiAreaChart:
    """Test MultiAreaChart component."""

    def test_multi_area_chart_renders(self, theme, sample_df):
        """MultiAreaChart should render without validation errors."""
        result = MultiAreaChart(
            sample_df, x="month", areas={"FTE": "fte", "Total": "total_fte"}, theme=theme
        )
        assert result is not None
        assert "error" not in type(result).__name__.lower()

    def test_multi_area_chart_with_int_column(self, theme, sample_df):
        """MultiAreaChart should accept integer columns."""
        result = MultiAreaChart(sample_df, x="month", areas={"Squads": "squads"}, theme=theme)
        assert result is not None
        assert "error" not in type(result).__name__.lower()


class TestLineChart:
    """Test LineChart component."""

    def test_line_chart_renders(self, theme, sample_df):
        """LineChart should render without validation errors."""
        result = LineChart(sample_df, x="month", y="fte", theme=theme)
        assert result is not None
        assert "error" not in type(result).__name__.lower()

    def test_line_chart_with_title(self, theme, sample_df):
        """LineChart should accept title parameter."""
        result = LineChart(sample_df, x="month", y="fte", title="FTE Trend", theme=theme)
        assert result is not None


class TestMultiLinesChart:
    """Test MultiLinesChart component."""

    def test_multi_lines_chart_renders(self, theme, sample_df):
        """MultiLinesChart should render without validation errors."""
        result = MultiLinesChart(
            sample_df,
            x="month",
            lines={"FTE": "fte", "Total": "total_fte"},
            theme=theme,
        )
        assert result is not None
        assert "error" not in type(result).__name__.lower()


class TestMultiBarsChart:
    """Test MultiBarsChart component."""

    def test_multi_bars_chart_renders(self, theme, sample_df):
        """MultiBarsChart should render without validation errors."""
        result = MultiBarsChart(
            sample_df,
            x="month",
            bars={"Squad A": "squad_a", "Squad B": "squad_b"},
            theme=theme,
        )
        assert result is not None
        assert "error" not in type(result).__name__.lower()


class TestStackedBarChart:
    """Test StackedBarChart component."""

    def test_stacked_bar_chart_renders(self, theme, sample_df):
        """StackedBarChart should render without validation errors."""
        result = StackedBarChart(
            sample_df,
            x="month",
            segments={
                "Full-time": "fte_ft",
                "Part-time": "fte_pt",
                "Contingent": "fte_cont",
            },
            theme=theme,
        )
        assert result is not None
        assert "error" not in type(result).__name__.lower()


class TestStackedBarWithLine:
    """Test StackedBarWithLine component."""

    def test_stacked_bar_with_line_renders(self, theme, sample_df):
        """StackedBarWithLine should render without validation errors."""
        result = StackedBarWithLine(
            sample_df,
            x="month",
            bar_segments={
                "Full-time": "fte_ft",
                "Part-time": "fte_pt",
            },
            line_y="total_fte",
            theme=theme,
        )
        assert result is not None
        assert "error" not in type(result).__name__.lower()


class TestStackedBarHorizontalChart:
    """Test StackedBarHorizontalChart component."""

    def test_stacked_bar_horizontal_renders(self, theme, sample_headcount_df):
        """StackedBarHorizontalChart should render without errors."""
        result = StackedBarHorizontalChart(
            sample_headcount_df,
            category="category",
            subcategory="subcategory",
            value="value",
            theme=theme,
        )
        assert result is not None

    def test_stacked_bar_horizontal_with_title(self, theme, sample_headcount_df):
        """StackedBarHorizontalChart should accept title parameter."""
        result = StackedBarHorizontalChart(
            sample_headcount_df,
            category="category",
            subcategory="subcategory",
            value="value",
            title="Headcount by Department",
            theme=theme,
        )
        assert result is not None


class TestChartsGroup:
    """Test ChartsGroup component."""

    def test_charts_group_renders(self, theme, sample_df):
        """ChartsGroup should render without errors."""
        result = ChartsGroup(
            sample_df,
            x="month",
            charts=[
                lambda df, x, theme, id, **kwargs: LineChart(
                    df, x=x, y="fte", theme=theme, id=id, **kwargs
                ),
                lambda df, x, theme, id, **kwargs: MultiBarsChart(
                    df, x=x, bars={"Squad A": "squad_a"}, theme=theme, id=id, **kwargs
                ),
            ],
            theme=theme,
        )
        assert result is not None

    def test_charts_group_with_title(self, theme, sample_df):
        """ChartsGroup should accept title parameter."""
        result = ChartsGroup(
            sample_df,
            x="month",
            title="Team Metrics",
            charts=[
                lambda df, x, theme, id, **kwargs: LineChart(
                    df, x=x, y="fte", theme=theme, id=id, **kwargs
                ),
            ],
            theme=theme,
        )
        assert result is not None


class TestRadialGauge:
    """Test RadialGauge component."""

    def test_radial_gauge_renders(self, theme):
        """RadialGauge should render without errors."""
        result = RadialGauge(value=61, max_value=100, label="Yield", theme=theme)
        assert result is not None
        assert hasattr(result, "className") or hasattr(result, "children")

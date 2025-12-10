"""
Test module for visualizations.py

Tests cover:
- Chart data preparation
- Bar chart generation
- Line chart generation
- Pie chart generation
- Table formatting
"""

import pytest
import pandas as pd
import matplotlib

matplotlib.use("Agg")  # Non-interactive backend for testing
import matplotlib.pyplot as plt

from src.visualizations import (
    prepare_chart_data,
    create_bar_chart,
    create_line_chart,
    create_pie_chart,
    display_table,
    save_chart,
)


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def vaccination_df():
    """Sample vaccination data for chart testing."""
    return pd.DataFrame(
        {
            "location": ["United Kingdom", "United States", "Germany", "France"],
            "total_vaccinations": [50000000, 200000000, 60000000, 45000000],
            "people_vaccinated": [40000000, 160000000, 48000000, 36000000],
        }
    )


@pytest.fixture
def time_series_df():
    """Time series data for line chart testing."""
    dates = pd.date_range("2021-01-01", periods=7, freq="D")
    return pd.DataFrame(
        {
            "date": dates,
            "daily_vaccinations": [10000, 15000, 20000, 18000, 25000, 30000, 28000],
        }
    )


# ============================================================================
# Tests for prepare_chart_data()
# ============================================================================


class TestPrepareChartData:
    """Tests for chart data preparation."""

    def test_prepare_returns_dict(self, vaccination_df):
        """Test that prepare_chart_data returns a dictionary."""
        result = prepare_chart_data(
            vaccination_df, x="location", y="total_vaccinations"
        )
        assert isinstance(result, dict)

    def test_prepare_contains_x_values(self, vaccination_df):
        """Test that result contains x values."""
        result = prepare_chart_data(
            vaccination_df, x="location", y="total_vaccinations"
        )
        assert "x" in result
        assert len(result["x"]) == 4

    def test_prepare_contains_y_values(self, vaccination_df):
        """Test that result contains y values."""
        result = prepare_chart_data(
            vaccination_df, x="location", y="total_vaccinations"
        )
        assert "y" in result
        assert len(result["y"]) == 4


# ============================================================================
# Tests for create_bar_chart()
# ============================================================================


class TestCreateBarChart:
    """Tests for bar chart creation."""

    def test_bar_chart_returns_figure(self, vaccination_df):
        """Test that create_bar_chart returns a matplotlib Figure."""
        fig = create_bar_chart(
            vaccination_df,
            x="location",
            y="total_vaccinations",
            title="Vaccinations by Country",
        )
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_bar_chart_has_title(self, vaccination_df):
        """Test that bar chart has correct title."""
        fig = create_bar_chart(
            vaccination_df, x="location", y="total_vaccinations", title="Test Title"
        )
        # Get the axes and check title
        ax = fig.axes[0]
        assert ax.get_title() == "Test Title"
        plt.close(fig)


# ============================================================================
# Tests for create_line_chart()
# ============================================================================


class TestCreateLineChart:
    """Tests for line chart creation."""

    def test_line_chart_returns_figure(self, time_series_df):
        """Test that create_line_chart returns a matplotlib Figure."""
        fig = create_line_chart(
            time_series_df,
            x="date",
            y="daily_vaccinations",
            title="Daily Vaccinations Trend",
        )
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_line_chart_has_labels(self, time_series_df):
        """Test that line chart has axis labels."""
        fig = create_line_chart(
            time_series_df,
            x="date",
            y="daily_vaccinations",
            title="Trend",
            xlabel="Date",
            ylabel="Vaccinations",
        )
        ax = fig.axes[0]
        assert ax.get_xlabel() == "Date"
        assert ax.get_ylabel() == "Vaccinations"
        plt.close(fig)


# ============================================================================
# Tests for create_pie_chart()
# ============================================================================


class TestCreatePieChart:
    """Tests for pie chart creation."""

    def test_pie_chart_returns_figure(self, vaccination_df):
        """Test that create_pie_chart returns a matplotlib Figure."""
        fig = create_pie_chart(
            labels=vaccination_df["location"].tolist(),
            values=vaccination_df["total_vaccinations"].tolist(),
            title="Vaccination Distribution",
        )
        assert isinstance(fig, plt.Figure)
        plt.close(fig)


# ============================================================================
# Tests for display_table()
# ============================================================================


class TestDisplayTable:
    """Tests for table formatting."""

    def test_display_table_returns_string(self, vaccination_df):
        """Test that display_table returns a string."""
        result = display_table(vaccination_df)
        assert isinstance(result, str)

    def test_display_table_contains_data(self, vaccination_df):
        """Test that table output contains data values."""
        result = display_table(vaccination_df)
        assert "United Kingdom" in result
        assert "United States" in result

    def test_display_table_with_max_rows(self, vaccination_df):
        """Test limiting table rows."""
        result = display_table(vaccination_df, max_rows=2)
        # Should contain fewer rows
        assert isinstance(result, str)


# ============================================================================
# Tests for save_chart()
# ============================================================================


class TestSaveChart:
    """Tests for chart saving."""

    def test_save_chart_creates_file(self, vaccination_df, tmp_path):
        """Test that save_chart creates a file."""
        fig = create_bar_chart(
            vaccination_df, x="location", y="total_vaccinations", title="Test"
        )
        filepath = tmp_path / "test_chart.png"
        result = save_chart(fig, str(filepath))
        assert result is True
        assert filepath.exists()
        plt.close(fig)


# ============================================================================
# Integration Tests
# ============================================================================


class TestVisualizationsIntegration:
    """Integration tests for visualization module."""

    def test_prepare_and_create_chart(self, vaccination_df):
        """Test preparing data and creating chart."""
        data = prepare_chart_data(vaccination_df, "location", "total_vaccinations")
        assert len(data["x"]) == 4

        fig = create_bar_chart(
            vaccination_df, x="location", y="total_vaccinations", title="Vaccinations"
        )
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

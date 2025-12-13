"""
Tests for DataFilter Class (OOP with Method Chaining)

Tests for the DataFilter class that provides fluent filtering
of vaccination data with proper encapsulation and chaining.
"""

import pytest
import pandas as pd
from datetime import datetime


@pytest.fixture
def sample_data():
    """Sample vaccination data for testing."""
    return pd.DataFrame(
        {
            "location": ["Spain", "Spain", "Germany", "Germany", "France", "France"],
            "date": pd.to_datetime(
                [
                    "2021-01-01",
                    "2021-06-01",
                    "2021-01-01",
                    "2021-06-01",
                    "2021-01-01",
                    "2021-06-01",
                ]
            ),
            "total_vaccinations": [100, 200, 150, 250, 120, 220],
            "continent": ["Europe", "Europe", "Europe", "Europe", "Europe", "Europe"],
        }
    )


class TestDataFilterClass:
    """Tests for DataFilter class existence and initialization."""

    def test_data_filter_class_exists(self):
        """Test that DataFilter class is defined."""
        from src.filters import DataFilter

        assert DataFilter is not None

    def test_data_filter_initialization(self, sample_data):
        """Test that DataFilter can be instantiated with DataFrame."""
        from src.filters import DataFilter

        df = DataFilter(sample_data)
        assert df is not None

    def test_data_filter_stores_data(self, sample_data):
        """Test that DataFilter stores the data."""
        from src.filters import DataFilter

        df = DataFilter(sample_data)
        assert len(df.result()) == 6


class TestDataFilterByCountry:
    """Tests for by_country() method."""

    def test_by_country_method_exists(self, sample_data):
        """Test that by_country method is defined."""
        from src.filters import DataFilter

        df = DataFilter(sample_data)
        assert hasattr(df, "by_country")

    def test_by_country_returns_data_filter(self, sample_data):
        """Test that by_country returns DataFilter for chaining."""
        from src.filters import DataFilter

        df = DataFilter(sample_data)
        result = df.by_country("Spain")

        assert isinstance(result, DataFilter)

    def test_by_country_filters_correctly(self, sample_data):
        """Test that by_country filters to specified country."""
        from src.filters import DataFilter

        df = DataFilter(sample_data)
        result = df.by_country("Spain").result()

        assert len(result) == 2
        assert all(result["location"] == "Spain")

    def test_by_country_multiple_countries(self, sample_data):
        """Test filtering by multiple countries."""
        from src.filters import DataFilter

        df = DataFilter(sample_data)
        result = df.by_country(["Spain", "Germany"]).result()

        assert len(result) == 4


class TestDataFilterByDateRange:
    """Tests for by_date_range() method."""

    def test_by_date_range_method_exists(self, sample_data):
        """Test that by_date_range method is defined."""
        from src.filters import DataFilter

        df = DataFilter(sample_data)
        assert hasattr(df, "by_date_range")

    def test_by_date_range_returns_data_filter(self, sample_data):
        """Test that by_date_range returns DataFilter for chaining."""
        from src.filters import DataFilter

        df = DataFilter(sample_data)
        result = df.by_date_range(start=datetime(2021, 1, 1))

        assert isinstance(result, DataFilter)

    def test_by_date_range_filters_start(self, sample_data):
        """Test filtering with start date only."""
        from src.filters import DataFilter

        df = DataFilter(sample_data)
        result = df.by_date_range(start=datetime(2021, 3, 1)).result()

        assert len(result) == 3  # Only June dates

    def test_by_date_range_filters_end(self, sample_data):
        """Test filtering with end date only."""
        from src.filters import DataFilter

        df = DataFilter(sample_data)
        result = df.by_date_range(end=datetime(2021, 3, 1)).result()

        assert len(result) == 3  # Only January dates

    def test_by_date_range_filters_both(self, sample_data):
        """Test filtering with both start and end dates."""
        from src.filters import DataFilter

        df = DataFilter(sample_data)
        result = df.by_date_range(
            start=datetime(2021, 1, 1), end=datetime(2021, 3, 1)
        ).result()

        assert len(result) == 3


class TestDataFilterByContinent:
    """Tests for by_continent() method."""

    def test_by_continent_method_exists(self, sample_data):
        """Test that by_continent method is defined."""
        from src.filters import DataFilter

        df = DataFilter(sample_data)
        assert hasattr(df, "by_continent")

    def test_by_continent_returns_data_filter(self, sample_data):
        """Test that by_continent returns DataFilter for chaining."""
        from src.filters import DataFilter

        df = DataFilter(sample_data)
        result = df.by_continent("Europe")

        assert isinstance(result, DataFilter)


class TestDataFilterResult:
    """Tests for result() method."""

    def test_result_method_exists(self, sample_data):
        """Test that result method is defined."""
        from src.filters import DataFilter

        df = DataFilter(sample_data)
        assert hasattr(df, "result")

    def test_result_returns_dataframe(self, sample_data):
        """Test that result returns a DataFrame."""
        from src.filters import DataFilter

        df = DataFilter(sample_data)
        result = df.result()

        assert isinstance(result, pd.DataFrame)

    def test_result_returns_copy(self, sample_data):
        """Test that result returns copy (encapsulation)."""
        from src.filters import DataFilter

        df = DataFilter(sample_data)
        result1 = df.result()
        result1["new_col"] = 1
        result2 = df.result()

        assert "new_col" not in result2.columns


class TestDataFilterChaining:
    """Tests for method chaining."""

    def test_chain_country_then_date(self, sample_data):
        """Test chaining country and date filters."""
        from src.filters import DataFilter

        result = (
            DataFilter(sample_data)
            .by_country("Spain")
            .by_date_range(start=datetime(2021, 3, 1))
            .result()
        )

        assert len(result) == 1
        assert result.iloc[0]["location"] == "Spain"

    def test_chain_date_then_country(self, sample_data):
        """Test chaining date then country filters."""
        from src.filters import DataFilter

        result = (
            DataFilter(sample_data)
            .by_date_range(end=datetime(2021, 3, 1))
            .by_country("Germany")
            .result()
        )

        assert len(result) == 1
        assert result.iloc[0]["location"] == "Germany"

    def test_chain_preserves_immutability(self, sample_data):
        """Test that chaining doesn't modify original."""
        from src.filters import DataFilter

        original = DataFilter(sample_data)
        _ = original.by_country("Spain")

        # Original should still have all data
        assert len(original.result()) == 6


class TestDataFilterCount:
    """Tests for count property."""

    def test_count_property_exists(self, sample_data):
        """Test that count property is defined."""
        from src.filters import DataFilter

        df = DataFilter(sample_data)
        assert hasattr(df, "count")

    def test_count_returns_integer(self, sample_data):
        """Test that count returns integer."""
        from src.filters import DataFilter

        df = DataFilter(sample_data)
        assert isinstance(df.count, int)
        assert df.count == 6

    def test_count_after_filter(self, sample_data):
        """Test count after filtering."""
        from src.filters import DataFilter

        df = DataFilter(sample_data).by_country("Spain")
        assert df.count == 2

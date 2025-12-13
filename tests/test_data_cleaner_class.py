"""
Tests for DataCleaner Class (OOP with Method Chaining)

Tests for the DataCleaner class that provides fluent data cleaning
operations with method chaining support.
"""

import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def sample_data():
    """Sample data with various issues for testing."""
    return pd.DataFrame(
        {
            "location": ["Spain", "Germany", "France", "Spain", None],
            "date": [
                "2021-01-01",
                "2021-01-02",
                "2021-01-03",
                "2021-01-01",
                "2021-01-04",
            ],
            "total_vaccinations": [100, None, 150, 100, 200],
            "daily_vaccinations": [10.0, 20.0, None, 10.0, 25.0],
        }
    )


@pytest.fixture
def data_with_missing():
    """Data with missing values."""
    return pd.DataFrame(
        {"value": [1.0, None, 3.0, None, 5.0], "category": ["A", "B", None, "D", "E"]}
    )


class TestDataCleanerClass:
    """Tests for DataCleaner class existence and initialization."""

    def test_data_cleaner_class_exists(self):
        """Test that DataCleaner class is defined."""
        from src.data_cleaner import DataCleaner

        assert DataCleaner is not None

    def test_data_cleaner_initialization(self, sample_data):
        """Test that DataCleaner can be instantiated."""
        from src.data_cleaner import DataCleaner

        cleaner = DataCleaner(sample_data)
        assert cleaner is not None

    def test_data_cleaner_stores_data(self, sample_data):
        """Test that DataCleaner stores the data."""
        from src.data_cleaner import DataCleaner

        cleaner = DataCleaner(sample_data)
        assert len(cleaner.result()) == 5


class TestDataCleanerFillMissing:
    """Tests for fill_missing() method."""

    def test_fill_missing_method_exists(self, sample_data):
        """Test that fill_missing method is defined."""
        from src.data_cleaner import DataCleaner

        cleaner = DataCleaner(sample_data)
        assert hasattr(cleaner, "fill_missing")

    def test_fill_missing_returns_data_cleaner(self, sample_data):
        """Test that fill_missing returns DataCleaner for chaining."""
        from src.data_cleaner import DataCleaner

        cleaner = DataCleaner(sample_data)
        result = cleaner.fill_missing(value=0)

        assert isinstance(result, DataCleaner)

    def test_fill_missing_with_value(self, data_with_missing):
        """Test filling missing values with specific value."""
        from src.data_cleaner import DataCleaner

        result = DataCleaner(data_with_missing).fill_missing(value=0).result()

        assert result["value"].isna().sum() == 0
        assert 0 in result["value"].values

    def test_fill_missing_with_mean(self, data_with_missing):
        """Test filling missing values with mean."""
        from src.data_cleaner import DataCleaner

        result = DataCleaner(data_with_missing).fill_missing(strategy="mean").result()

        assert result["value"].isna().sum() == 0


class TestDataCleanerConvertDates:
    """Tests for convert_dates() method."""

    def test_convert_dates_method_exists(self, sample_data):
        """Test that convert_dates method is defined."""
        from src.data_cleaner import DataCleaner

        cleaner = DataCleaner(sample_data)
        assert hasattr(cleaner, "convert_dates")

    def test_convert_dates_returns_data_cleaner(self, sample_data):
        """Test that convert_dates returns DataCleaner for chaining."""
        from src.data_cleaner import DataCleaner

        cleaner = DataCleaner(sample_data)
        result = cleaner.convert_dates(["date"])

        assert isinstance(result, DataCleaner)

    def test_convert_dates_converts_to_datetime(self, sample_data):
        """Test that dates are converted to datetime."""
        from src.data_cleaner import DataCleaner

        result = DataCleaner(sample_data).convert_dates(["date"]).result()

        assert pd.api.types.is_datetime64_any_dtype(result["date"])


class TestDataCleanerRemoveDuplicates:
    """Tests for remove_duplicates() method."""

    def test_remove_duplicates_method_exists(self, sample_data):
        """Test that remove_duplicates method is defined."""
        from src.data_cleaner import DataCleaner

        cleaner = DataCleaner(sample_data)
        assert hasattr(cleaner, "remove_duplicates")

    def test_remove_duplicates_returns_data_cleaner(self, sample_data):
        """Test that remove_duplicates returns DataCleaner for chaining."""
        from src.data_cleaner import DataCleaner

        cleaner = DataCleaner(sample_data)
        result = cleaner.remove_duplicates()

        assert isinstance(result, DataCleaner)

    def test_remove_duplicates_removes_dupes(self, sample_data):
        """Test that duplicates are removed."""
        from src.data_cleaner import DataCleaner

        # sample_data has duplicate rows (Spain, 2021-01-01)
        result = DataCleaner(sample_data).remove_duplicates().result()

        assert len(result) < len(sample_data)


class TestDataCleanerResult:
    """Tests for result() method."""

    def test_result_method_exists(self, sample_data):
        """Test that result method is defined."""
        from src.data_cleaner import DataCleaner

        cleaner = DataCleaner(sample_data)
        assert hasattr(cleaner, "result")

    def test_result_returns_dataframe(self, sample_data):
        """Test that result returns a DataFrame."""
        from src.data_cleaner import DataCleaner

        cleaner = DataCleaner(sample_data)
        result = cleaner.result()

        assert isinstance(result, pd.DataFrame)

    def test_result_returns_copy(self, sample_data):
        """Test that result returns copy (encapsulation)."""
        from src.data_cleaner import DataCleaner

        cleaner = DataCleaner(sample_data)
        result1 = cleaner.result()
        result1["new_col"] = 1
        result2 = cleaner.result()

        assert "new_col" not in result2.columns


class TestDataCleanerChaining:
    """Tests for method chaining."""

    def test_chain_fill_then_convert(self, sample_data):
        """Test chaining fill_missing and convert_dates."""
        from src.data_cleaner import DataCleaner

        result = (
            DataCleaner(sample_data)
            .fill_missing(value=0)
            .convert_dates(["date"])
            .result()
        )

        assert result["total_vaccinations"].isna().sum() == 0
        assert pd.api.types.is_datetime64_any_dtype(result["date"])

    def test_chain_multiple_operations(self, sample_data):
        """Test chaining multiple cleaning operations."""
        from src.data_cleaner import DataCleaner

        result = (
            DataCleaner(sample_data)
            .remove_duplicates()
            .fill_missing(value=0)
            .convert_dates(["date"])
            .result()
        )

        assert len(result) < len(sample_data)  # Duplicates removed
        assert result["total_vaccinations"].isna().sum() == 0

    def test_chain_preserves_immutability(self, sample_data):
        """Test that chaining doesn't modify original."""
        from src.data_cleaner import DataCleaner

        original = DataCleaner(sample_data)
        _ = original.fill_missing(value=0)

        # Original should still have missing values
        assert original.result()["total_vaccinations"].isna().sum() > 0


class TestDataCleanerCount:
    """Tests for count property."""

    def test_count_property_exists(self, sample_data):
        """Test that count property is defined."""
        from src.data_cleaner import DataCleaner

        cleaner = DataCleaner(sample_data)
        assert hasattr(cleaner, "count")

    def test_count_returns_integer(self, sample_data):
        """Test that count returns integer."""
        from src.data_cleaner import DataCleaner

        cleaner = DataCleaner(sample_data)
        assert isinstance(cleaner.count, int)
        assert cleaner.count == 5

    def test_count_after_remove_duplicates(self, sample_data):
        """Test count after removing duplicates."""
        from src.data_cleaner import DataCleaner

        cleaner = DataCleaner(sample_data).remove_duplicates()
        assert cleaner.count < 5

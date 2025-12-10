"""
Test module for data_cleaner.py

Tests cover:
- Handling missing values (fill, drop strategies)
- Type conversions (dates, numbers)
- Text standardization
- Data validation
- Edge cases (all nulls, mixed types)
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime

from src.data_cleaner import (
    handle_missing_values,
    convert_dates,
    convert_numeric,
    standardize_text,
    remove_duplicates,
    validate_data_range,
    clean_dataframe,
)


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def df_with_missing():
    """DataFrame with missing values."""
    return pd.DataFrame(
        {
            "location": ["United Kingdom", "United States", None, "Germany"],
            "iso_code": ["GBR", "USA", "FRA", "DEU"],
            "total_vaccinations": [1000000, None, 500000, None],
            "people_vaccinated": [800000, 4000000, None, 400000],
        }
    )


@pytest.fixture
def df_with_dates():
    """DataFrame with date strings."""
    return pd.DataFrame(
        {
            "location": ["UK", "US", "DE"],
            "date": ["2021-01-15", "2021-02-20", "2021-03-25"],
            "total": [1000, 2000, 3000],
        }
    )


@pytest.fixture
def df_with_numeric_strings():
    """DataFrame with numbers stored as strings."""
    return pd.DataFrame(
        {
            "location": ["UK", "US", "DE"],
            "cases": ["1000", "2000", "3000"],
            "rate": ["10.5", "20.3", "30.1"],
        }
    )


@pytest.fixture
def df_with_inconsistent_text():
    """DataFrame with inconsistent text formatting."""
    return pd.DataFrame(
        {
            "location": ["  United Kingdom  ", "UNITED STATES", "germany", "FRANCE"],
            "iso_code": ["gbr", "USA", "deu", "FRA"],
        }
    )


@pytest.fixture
def df_with_duplicates():
    """DataFrame with duplicate rows."""
    return pd.DataFrame(
        {
            "location": ["UK", "US", "UK", "DE", "US"],
            "date": [
                "2021-01-01",
                "2021-01-01",
                "2021-01-01",
                "2021-01-02",
                "2021-01-01",
            ],
            "cases": [100, 200, 100, 150, 200],
        }
    )


@pytest.fixture
def sample_clean_df():
    """A clean sample DataFrame."""
    return pd.DataFrame(
        {
            "location": ["United Kingdom", "United States", "Germany"],
            "iso_code": ["GBR", "USA", "DEU"],
            "date": ["2021-01-01", "2021-01-01", "2021-01-02"],
            "total_vaccinations": [1000000, 5000000, 500000],
        }
    )


# ============================================================================
# Tests for handle_missing_values()
# ============================================================================


class TestHandleMissingValues:
    """Tests for handling missing values."""

    def test_fill_with_value(self, df_with_missing):
        """Test filling missing values with a specific value."""
        result = handle_missing_values(df_with_missing, strategy="fill", fill_value=0)
        assert result["total_vaccinations"].isna().sum() == 0
        assert result["total_vaccinations"].iloc[1] == 0

    def test_fill_with_mean(self, df_with_missing):
        """Test filling numeric columns with mean."""
        result = handle_missing_values(df_with_missing, strategy="mean")
        assert result["total_vaccinations"].isna().sum() == 0

    def test_fill_with_median(self, df_with_missing):
        """Test filling numeric columns with median."""
        result = handle_missing_values(df_with_missing, strategy="median")
        assert result["total_vaccinations"].isna().sum() == 0

    def test_drop_rows_with_any_missing(self, df_with_missing):
        """Test dropping rows with any missing values."""
        result = handle_missing_values(df_with_missing, strategy="drop")
        assert len(result) == 1  # Only one row has no missing values

    def test_fill_specific_column(self, df_with_missing):
        """Test filling only specific columns."""
        result = handle_missing_values(
            df_with_missing, strategy="fill", fill_value="Unknown", columns=["location"]
        )
        assert result["location"].isna().sum() == 0
        # Other columns should still have nulls
        assert result["total_vaccinations"].isna().sum() > 0

    def test_returns_dataframe(self, df_with_missing):
        """Test that function returns a DataFrame."""
        result = handle_missing_values(df_with_missing, strategy="fill", fill_value=0)
        assert isinstance(result, pd.DataFrame)

    def test_does_not_modify_original(self, df_with_missing):
        """Test that original DataFrame is not modified."""
        original_nulls = df_with_missing["total_vaccinations"].isna().sum()
        handle_missing_values(df_with_missing, strategy="fill", fill_value=0)
        assert df_with_missing["total_vaccinations"].isna().sum() == original_nulls


# ============================================================================
# Tests for convert_dates()
# ============================================================================


class TestConvertDates:
    """Tests for date conversion."""

    def test_convert_date_column(self, df_with_dates):
        """Test converting date string column to datetime."""
        result = convert_dates(df_with_dates, columns=["date"])
        assert pd.api.types.is_datetime64_any_dtype(result["date"])

    def test_date_values_preserved(self, df_with_dates):
        """Test that date values are correctly parsed."""
        result = convert_dates(df_with_dates, columns=["date"])
        assert result["date"].iloc[0].year == 2021
        assert result["date"].iloc[0].month == 1
        assert result["date"].iloc[0].day == 15

    def test_invalid_date_handling(self):
        """Test handling of invalid date strings."""
        df = pd.DataFrame({"date": ["2021-01-15", "invalid", "2021-03-25"]})
        result = convert_dates(df, columns=["date"], errors="coerce")
        assert pd.isna(result["date"].iloc[1])

    def test_returns_dataframe(self, df_with_dates):
        """Test that function returns a DataFrame."""
        result = convert_dates(df_with_dates, columns=["date"])
        assert isinstance(result, pd.DataFrame)


# ============================================================================
# Tests for convert_numeric()
# ============================================================================


class TestConvertNumeric:
    """Tests for numeric conversion."""

    def test_convert_integer_strings(self, df_with_numeric_strings):
        """Test converting integer strings to numeric."""
        result = convert_numeric(df_with_numeric_strings, columns=["cases"])
        assert pd.api.types.is_numeric_dtype(result["cases"])

    def test_convert_float_strings(self, df_with_numeric_strings):
        """Test converting float strings to numeric."""
        result = convert_numeric(df_with_numeric_strings, columns=["rate"])
        assert pd.api.types.is_numeric_dtype(result["rate"])
        assert result["rate"].iloc[0] == 10.5

    def test_invalid_numeric_handling(self):
        """Test handling of non-numeric strings."""
        df = pd.DataFrame({"value": ["100", "abc", "300"]})
        result = convert_numeric(df, columns=["value"], errors="coerce")
        assert pd.isna(result["value"].iloc[1])

    def test_returns_dataframe(self, df_with_numeric_strings):
        """Test that function returns a DataFrame."""
        result = convert_numeric(df_with_numeric_strings, columns=["cases"])
        assert isinstance(result, pd.DataFrame)


# ============================================================================
# Tests for standardize_text()
# ============================================================================


class TestStandardizeText:
    """Tests for text standardization."""

    def test_strip_whitespace(self, df_with_inconsistent_text):
        """Test stripping leading/trailing whitespace."""
        result = standardize_text(df_with_inconsistent_text, columns=["location"])
        assert result["location"].iloc[0] == "United Kingdom"

    def test_convert_to_lowercase(self, df_with_inconsistent_text):
        """Test converting text to lowercase."""
        result = standardize_text(
            df_with_inconsistent_text, columns=["location"], case="lower"
        )
        assert result["location"].iloc[1] == "united states"

    def test_convert_to_uppercase(self, df_with_inconsistent_text):
        """Test converting text to uppercase."""
        result = standardize_text(
            df_with_inconsistent_text, columns=["iso_code"], case="upper"
        )
        assert result["iso_code"].iloc[0] == "GBR"

    def test_convert_to_title_case(self, df_with_inconsistent_text):
        """Test converting text to title case."""
        result = standardize_text(
            df_with_inconsistent_text, columns=["location"], case="title"
        )
        assert result["location"].iloc[2] == "Germany"

    def test_returns_dataframe(self, df_with_inconsistent_text):
        """Test that function returns a DataFrame."""
        result = standardize_text(df_with_inconsistent_text, columns=["location"])
        assert isinstance(result, pd.DataFrame)


# ============================================================================
# Tests for remove_duplicates()
# ============================================================================


class TestRemoveDuplicates:
    """Tests for duplicate removal."""

    def test_remove_exact_duplicates(self, df_with_duplicates):
        """Test removing exact duplicate rows."""
        result = remove_duplicates(df_with_duplicates)
        assert len(result) == 3  # 5 rows -> 3 unique rows

    def test_remove_duplicates_by_column(self, df_with_duplicates):
        """Test removing duplicates based on specific columns."""
        result = remove_duplicates(df_with_duplicates, subset=["location"])
        assert len(result) == 3  # UK, US, DE unique locations

    def test_keep_first_duplicate(self, df_with_duplicates):
        """Test keeping first occurrence of duplicates."""
        result = remove_duplicates(df_with_duplicates, keep="first")
        assert len(result) == 3

    def test_keep_last_duplicate(self, df_with_duplicates):
        """Test keeping last occurrence of duplicates."""
        result = remove_duplicates(df_with_duplicates, keep="last")
        assert len(result) == 3


# ============================================================================
# Tests for validate_data_range()
# ============================================================================


class TestValidateDataRange:
    """Tests for data range validation."""

    def test_validate_within_range(self, sample_clean_df):
        """Test validation passes when values are within range."""
        result = validate_data_range(
            sample_clean_df, column="total_vaccinations", min_val=0, max_val=10000000
        )
        assert result["valid"] is True

    def test_validate_outside_range(self, sample_clean_df):
        """Test validation fails when values are outside range."""
        result = validate_data_range(
            sample_clean_df,
            column="total_vaccinations",
            min_val=0,
            max_val=100000,  # Too small
        )
        assert result["valid"] is False
        assert result["out_of_range_count"] > 0

    def test_returns_dict(self, sample_clean_df):
        """Test that function returns a dictionary."""
        result = validate_data_range(sample_clean_df, "total_vaccinations", 0, 10000000)
        assert isinstance(result, dict)


# ============================================================================
# Tests for clean_dataframe()
# ============================================================================


class TestCleanDataframe:
    """Tests for the comprehensive cleaning function."""

    def test_clean_removes_duplicates(self, df_with_duplicates):
        """Test that clean_dataframe removes duplicates."""
        result = clean_dataframe(df_with_duplicates)
        original_len = len(df_with_duplicates)
        assert len(result) < original_len

    def test_clean_handles_missing(self, df_with_missing):
        """Test that clean_dataframe handles missing values."""
        result = clean_dataframe(df_with_missing, fill_missing=True, fill_value=0)
        # Numeric columns should have no missing values
        numeric_cols = result.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            assert result[col].isna().sum() == 0

    def test_clean_returns_dataframe(self, sample_clean_df):
        """Test that clean_dataframe returns a DataFrame."""
        result = clean_dataframe(sample_clean_df)
        assert isinstance(result, pd.DataFrame)


# ============================================================================
# Integration Tests
# ============================================================================


class TestDataCleanerIntegration:
    """Integration tests for data cleaning pipeline."""

    def test_full_cleaning_pipeline(self):
        """Test a complete data cleaning workflow."""
        # Create messy data
        df = pd.DataFrame(
            {
                "location": ["  UK  ", "GERMANY", "uk", None],
                "date": ["2021-01-01", "2021-01-02", "2021-01-01", "2021-01-03"],
                "cases": ["1000", "2000", "1000", "3000"],
            }
        )

        # Apply cleaning steps
        df = handle_missing_values(
            df, strategy="fill", fill_value="Unknown", columns=["location"]
        )
        df = standardize_text(df, columns=["location"], case="title")
        df = convert_numeric(df, columns=["cases"])
        df = convert_dates(df, columns=["date"])
        df = remove_duplicates(df)

        # Verify results
        assert df["location"].isna().sum() == 0
        assert pd.api.types.is_numeric_dtype(df["cases"])
        assert pd.api.types.is_datetime64_any_dtype(df["date"])

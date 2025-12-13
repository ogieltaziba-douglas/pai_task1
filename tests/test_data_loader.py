"""
Test module for data_loader.py

Tests cover:
- Loading CSV files into pandas DataFrames
- Error handling for missing files
- Edge cases: empty files, corrupt data
- Data info extraction
"""

import pytest
import pandas as pd
import os
import tempfile

from src.data_loader import load_csv, get_data_info


# ============================================================================
# Fixtures - Test data setup
# ============================================================================


@pytest.fixture
def sample_csv_file():
    """Create a temporary CSV file with sample vaccination data."""
    content = """location,iso_code,date,total_vaccinations,people_vaccinated
United Kingdom,GBR,2021-01-01,1000000,800000
United States,USA,2021-01-01,5000000,4000000
Germany,DEU,2021-01-02,500000,400000
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(content)
        filepath = f.name
    yield filepath
    os.unlink(filepath)


@pytest.fixture
def empty_csv_file():
    """Create an empty CSV file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        filepath = f.name
    yield filepath
    os.unlink(filepath)


@pytest.fixture
def csv_with_only_headers():
    """Create a CSV file with only headers, no data rows."""
    content = "location,iso_code,date,total_vaccinations,people_vaccinated\n"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(content)
        filepath = f.name
    yield filepath
    os.unlink(filepath)


@pytest.fixture
def csv_with_missing_values():
    """Create a CSV file with missing values."""
    content = """location,iso_code,date,total_vaccinations,people_vaccinated
United Kingdom,GBR,2021-01-01,,800000
United States,USA,,5000000,
Germany,DEU,2021-01-02,500000,400000
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(content)
        filepath = f.name
    yield filepath
    os.unlink(filepath)


# ============================================================================
# Tests for load_csv()
# ============================================================================


class TestLoadCSV:
    """Test cases for the load_csv function."""

    def test_load_csv_returns_dataframe(self, sample_csv_file):
        """Test that load_csv returns a pandas DataFrame."""
        result = load_csv(sample_csv_file)
        assert isinstance(result, pd.DataFrame)

    def test_load_csv_correct_shape(self, sample_csv_file):
        """Test that loaded DataFrame has correct number of rows and columns."""
        result = load_csv(sample_csv_file)
        assert result.shape == (3, 5)  # 3 rows, 5 columns

    def test_load_csv_correct_columns(self, sample_csv_file):
        """Test that loaded DataFrame has expected column names."""
        result = load_csv(sample_csv_file)
        expected_columns = [
            "location",
            "iso_code",
            "date",
            "total_vaccinations",
            "people_vaccinated",
        ]
        assert list(result.columns) == expected_columns

    def test_load_csv_correct_data(self, sample_csv_file):
        """Test that loaded data contains expected values."""
        result = load_csv(sample_csv_file)
        assert result.iloc[0]["location"] == "United Kingdom"
        assert result.iloc[1]["iso_code"] == "USA"

    def test_load_csv_file_not_found_raises_error(self):
        """Test that FileNotFoundError is raised for non-existent file."""
        with pytest.raises(FileNotFoundError):
            load_csv("/nonexistent/path/to/file.csv")

    def test_load_csv_empty_file_returns_empty_dataframe(self, empty_csv_file):
        """Test that empty file returns an empty DataFrame."""
        result = load_csv(empty_csv_file)
        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_load_csv_headers_only_returns_empty_dataframe(self, csv_with_only_headers):
        """Test that CSV with only headers returns DataFrame with columns but no rows."""
        result = load_csv(csv_with_only_headers)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
        assert len(result.columns) == 5

    def test_load_csv_preserves_missing_values(self, csv_with_missing_values):
        """Test that missing values are preserved as NaN."""
        result = load_csv(csv_with_missing_values)
        assert pd.isna(result.iloc[0]["total_vaccinations"])
        assert pd.isna(result.iloc[1]["date"])


# ============================================================================
# Tests for get_data_info()
# ============================================================================


class TestGetDataInfo:
    """Test cases for the get_data_info function."""

    def test_get_data_info_returns_dict(self, sample_csv_file):
        """Test that get_data_info returns a dictionary."""
        df = load_csv(sample_csv_file)
        result = get_data_info(df)
        assert isinstance(result, dict)

    def test_get_data_info_contains_row_count(self, sample_csv_file):
        """Test that info contains row count."""
        df = load_csv(sample_csv_file)
        result = get_data_info(df)
        assert "row_count" in result
        assert result["row_count"] == 3

    def test_get_data_info_contains_column_count(self, sample_csv_file):
        """Test that info contains column count."""
        df = load_csv(sample_csv_file)
        result = get_data_info(df)
        assert "column_count" in result
        assert result["column_count"] == 5

    def test_get_data_info_contains_columns_list(self, sample_csv_file):
        """Test that info contains list of column names."""
        df = load_csv(sample_csv_file)
        result = get_data_info(df)
        assert "columns" in result
        assert "location" in result["columns"]

    def test_get_data_info_contains_missing_count(self, csv_with_missing_values):
        """Test that info contains count of missing values."""
        df = load_csv(csv_with_missing_values)
        result = get_data_info(df)
        assert "missing_values" in result
        assert result["missing_values"] > 0


# ============================================================================
# Integration Tests
# ============================================================================


class TestDataLoaderIntegration:
    """Integration tests for data loader module."""

    def test_load_and_get_info(self, sample_csv_file):
        """Test loading CSV and getting its info."""
        df = load_csv(sample_csv_file)
        info = get_data_info(df)
        assert info["row_count"] == 3
        assert info["column_count"] == 5

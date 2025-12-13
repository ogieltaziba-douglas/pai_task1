"""
Dashboard Module

This module contains all business logic and data operations
for the Public Health Data Insights Dashboard.

Classes:
    DashboardState: Holds application state (data, connection)
    Dashboard: OOP class with encapsulation

Functions:
    load_data: Load CSV data
    get_summary: Generate data summary
    get_statistics: Calculate column statistics
    get_trend_analysis: Calculate trend for a country
    filter_data_by_continent: Filter by continent
"""

import pandas as pd
from typing import Optional


from src.data_loader import load_csv, get_data_info
from src.data_cleaner import DataCleaner
from src.filters import DataFilter
from src.summaries import calculate_statistics, calculate_trend, get_summary_report


class DashboardState:
    """
    Holds the application state (legacy, kept for backwards compatibility).

    Attributes:
        current_data: Currently loaded DataFrame
        db_connection: Database connection if active
    """

    def __init__(self):
        """Initialize dashboard state with empty data."""
        self.current_data: Optional[pd.DataFrame] = None
        self.db_connection = None


class Dashboard:
    """
    Dashboard class with OOP encapsulation.
    """

    def __init__(self):
        """Initialize Dashboard with no data."""
        self._data: Optional[pd.DataFrame] = None
        self.db_connection = None  # SQLite connection for SQL filters

    def load(self, filepath: str) -> dict:
        """
        Load data from CSV file.

        Args:
            filepath: Path to CSV file

        Returns:
            Dict with success status and metadata
        """
        try:
            # Load directly using load_csv
            data = load_csv(filepath)
            # Use DataCleaner OOP class
            data = DataCleaner(data).convert_dates(["date"]).result()
            self._data = data

            return {
                "success": True,
                "row_count": len(data),
                "column_count": len(data.columns),
                "columns": list(data.columns),
            }
        except FileNotFoundError:
            return {"success": False, "error": f"File not found: {filepath}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @property
    def data(self) -> Optional[pd.DataFrame]:
        """Get current data (returns copy for encapsulation)."""
        if self._data is None:
            return None
        return self._data.copy()

    @property
    def current_data(self) -> Optional[pd.DataFrame]:
        """
        Get current data (backwards compatible with DashboardState).

        Note: Returns the actual data, not a copy, for compatibility
        with handlers that modify state.current_data directly.
        """
        return self._data

    @current_data.setter
    def current_data(self, value: Optional[pd.DataFrame]) -> None:
        """Set current data (backwards compatible with DashboardState)."""
        self._data = value

    @property
    def row_count(self) -> int:
        """Get number of rows in current data."""
        if self._data is None:
            return 0
        return len(self._data)

    @property
    def is_loaded(self) -> bool:
        """Check if data is loaded."""
        return self._data is not None

    def summary(self) -> dict:
        """
        Get summary of current data.

        Returns:
            Dict with summary statistics
        """
        if self._data is None:
            return {"row_count": 0, "columns": []}

        return {
            "row_count": len(self._data),
            "column_count": len(self._data.columns),
            "columns": list(self._data.columns),
        }

    def filter(self):
        """
        Get DataFilter for current data.

        Returns:
            DataFilter instance for method chaining
        """
        from src.filters import DataFilter

        if self.db_connection is None:
            raise ValueError("No database connection. Load data first.")
        return DataFilter(self.db_connection)

    def set_data(self, data: pd.DataFrame) -> None:
        """
        Set current data (makes a copy).

        Args:
            data: DataFrame to set as current data
        """
        self._data = data.copy()


def load_data(state: DashboardState, filepath: str = "data/vaccinations.csv") -> dict:
    """
    Load vaccination data from CSV file.

    Args:
        state: DashboardState to update
        filepath: Path to CSV file

    Returns:
        Dictionary with 'success' key, data info, and missing value stats
    """
    try:
        data = load_csv(filepath)
        data = DataCleaner(data).convert_dates(["date"]).result()

        # Count missing values before filling
        missing_before = data.isna().sum().sum()

        # Apply forward fill for numeric columns (per location)
        numeric_cols = data.select_dtypes(include=["number"]).columns
        data = data.sort_values(["location", "date"])
        data[numeric_cols] = data.groupby("location")[numeric_cols].ffill()

        # Count remaining missing values
        missing_after = data.isna().sum().sum()
        filled_count = missing_before - missing_after

        state.current_data = data

        info = get_data_info(data)
        return {
            "success": True,
            "row_count": info["row_count"],
            "column_count": info["column_count"],
            "columns": info["columns"],
            "missing_filled": int(filled_count),
            "missing_remaining": int(missing_after),
        }
    except FileNotFoundError:
        return {"success": False, "error": f"File not found: {filepath}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_summary(state: DashboardState) -> dict:
    """
    Generate data summary.

    Args:
        state: DashboardState with loaded data

    Returns:
        Dictionary with summary information
    """
    if state.current_data is None:
        return {"error": "No data loaded"}

    report = get_summary_report(
        state.current_data, date_column="date", location_column="location"
    )

    return {
        "total_records": report["total_records"],
        "date_range": report.get("date_range"),
        "unique_locations": report.get("unique_locations"),
    }


def get_statistics(state: DashboardState, column: str) -> dict:
    """
    Calculate statistics for a column.

    Args:
        state: DashboardState with loaded data
        column: Column name to analyze

    Returns:
        Dictionary with statistical measures
    """
    if state.current_data is None:
        return {"error": "No data loaded"}

    if column not in state.current_data.columns:
        return {"error": f"Column not found: {column}"}

    stats = calculate_statistics(state.current_data, column)
    return stats


def get_trend_analysis(state: DashboardState, country: str) -> dict:
    """
    Calculate trend analysis for a country.

    Args:
        state: DashboardState with loaded data
        country: Country name to analyze

    Returns:
        Dictionary with trend information
    """
    if state.db_connection is None:
        return {"error": "No data loaded"}

    # SQL-based filtering
    country_data = DataFilter(state.db_connection).by_country(country).result()

    if country_data.empty:
        return {"error": f"No data found for: {country}"}

    country_data = country_data.sort_values("date")

    # Calculate trend for daily_vaccinations
    if "daily_vaccinations" in country_data.columns:
        trend = calculate_trend(country_data, "date", "daily_vaccinations")
    else:
        trend = {"direction": "unknown", "start_value": 0, "end_value": 0}

    return {
        "country": country,
        "date_range": {
            "start": country_data["date"].min(),
            "end": country_data["date"].max(),
        },
        "total_records": len(country_data),
        "direction": trend["direction"],
        "start_value": trend["start_value"],
        "end_value": trend["end_value"],
        "total_change": trend.get("total_change", 0),
        "percent_change": trend.get("percent_change", 0),
    }


def filter_data_by_continent(state: DashboardState, continent: str) -> pd.DataFrame:
    """
    Filter data by continent.

    Args:
        state: DashboardState with loaded data
        continent: Continent name

    Returns:
        Filtered DataFrame
    """
    if state.db_connection is None:
        return pd.DataFrame()

    # SQL-based filtering
    return DataFilter(state.db_connection).by_country(continent).result()

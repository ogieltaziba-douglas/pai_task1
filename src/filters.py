"""
Filters Module

This module provides the DataFilter class for filtering public health
vaccination data using SQL queries.

Classes:
    DataFilter: OOP class with fluent interface for SQL-based filtering
"""

import sqlite3
import pandas as pd
from typing import Optional


class DataFilter:
    """
    SQL-based data filter with method chaining support.

    Example:
        >>> result = (DataFilter(conn)
        ...           .by_country('Spain')
        ...           .by_date_range(start='2021-01-01')
        ...           .result())
    """

    def __init__(
        self,
        connection: sqlite3.Connection,
        table: str = "vaccinations",
        where_clauses: list = None,
    ):
        """
        Initialize DataFilter with database connection.

        Args:
            connection: SQLite database connection
            table: Table name to query (default: 'vaccinations')
            where_clauses: List of WHERE clause conditions (internal use)
        """
        self._conn = connection
        self._table = table
        self._where_clauses = where_clauses if where_clauses else []

    def by_country(self, countries, column: str = "location") -> "DataFilter":
        """
        Filter by country using SQL WHERE clause.

        Args:
            countries: Country name (str) or list of countries
            column: Column name to filter on (default: 'location')

        Returns:
            New DataFilter with added WHERE clause
        """
        # Handle single country or list
        if isinstance(countries, str):
            countries = [countries]

        # Build SQL IN clause
        placeholders = ", ".join([f"'{c}'" for c in countries])
        clause = f"{column} IN ({placeholders})"

        # Return new instance with added clause (immutability)
        new_clauses = self._where_clauses + [clause]
        return DataFilter(self._conn, self._table, new_clauses)

    def by_date_range(
        self,
        start: Optional[str] = None,
        end: Optional[str] = None,
        date_column: str = "date",
    ) -> "DataFilter":
        """
        Filter by date range using SQL WHERE clause.

        Args:
            start: Start date string (inclusive)
            end: End date string (inclusive)
            date_column: Column name for dates (default: 'date')

        Returns:
            New DataFilter with added WHERE clause
        """
        new_clauses = self._where_clauses.copy()

        if start is not None:
            # Handle datetime objects
            if hasattr(start, "strftime"):
                start = start.strftime("%Y-%m-%d")
            new_clauses.append(f"{date_column} >= '{start}'")

        if end is not None:
            if hasattr(end, "strftime"):
                end = end.strftime("%Y-%m-%d")
            new_clauses.append(f"{date_column} <= '{end}'")

        return DataFilter(self._conn, self._table, new_clauses)

    def by_continent(self, continent: str) -> "DataFilter":
        """
        Filter by continent using SQL WHERE clause.

        Args:
            continent: Continent name

        Returns:
            New DataFilter with added WHERE clause
        """
        clause = f"location = '{continent}'"
        new_clauses = self._where_clauses + [clause]
        return DataFilter(self._conn, self._table, new_clauses)

    def result(self) -> pd.DataFrame:
        """
        Execute SQL query and return result as DataFrame.

        Returns:
            DataFrame with query results (dates converted to datetime)
        """
        result = pd.read_sql_query(self.query, self._conn)
        # Convert date column from string to datetime (SQLite returns text)
        if "date" in result.columns:
            result["date"] = pd.to_datetime(result["date"])
        return result

    @property
    def query(self) -> str:
        """
        Get the SQL query string.

        Returns:
            SQL query string (useful for LO3 demonstration)
        """
        base = f"SELECT * FROM {self._table}"

        if self._where_clauses:
            where = " AND ".join(self._where_clauses)
            return f"{base} WHERE {where}"

        return base

    @property
    def count(self) -> int:
        """
        Get count of rows matching current filters using SQL COUNT.

        Returns:
            Row count
        """
        count_query = f"SELECT COUNT(*) FROM {self._table}"

        if self._where_clauses:
            where = " AND ".join(self._where_clauses)
            count_query = f"{count_query} WHERE {where}"

        cursor = self._conn.cursor()
        cursor.execute(count_query)
        return cursor.fetchone()[0]

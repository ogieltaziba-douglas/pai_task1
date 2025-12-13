"""
Database Module

This module provides functions for SQLite database operations
for storing and managing public health vaccination data.

Functions:
    create_connection: Connect to SQLite database
    insert_dataframe: Insert DataFrame into table
"""

import sqlite3
import pandas as pd


def create_connection(db_path: str) -> sqlite3.Connection:
    """
    Create a connection to a SQLite database.

    Args:
        db_path: Path to the database file, or ':memory:' for in-memory database.

    Returns:
        sqlite3.Connection object.

    Example:
        >>> conn = create_connection('data/health.db')
    """
    conn = sqlite3.connect(db_path)
    # Enable foreign keys and return rows as Row objects for dict-like access
    conn.row_factory = sqlite3.Row
    return conn


def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    """
    Check if a table exists in the database.

    Args:
        conn: Database connection.
        table_name: Name of the table to check.

    Returns:
        True if table exists, False otherwise.
    """
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,)
    )
    result = cursor.fetchone()
    return result is not None


def insert_dataframe(
    conn: sqlite3.Connection, table_name: str, df: pd.DataFrame
) -> int:
    """
    Insert a DataFrame into a database table.

    Creates the table if it doesn't exist, using DataFrame columns.

    Args:
        conn: Database connection.
        table_name: Name of the table to insert into.
        df: DataFrame to insert.

    Returns:
        Number of rows inserted.

    Example:
        >>> df = pd.DataFrame({'location': ['UK', 'US'], 'cases': [100, 200]})
        >>> rows = insert_dataframe(conn, 'data', df)
        >>> print(f"Inserted {rows} rows")
    """
    if df.empty:
        return 0

    try:
        # Use pandas to_sql for easy insertion
        rows_before = 0
        if table_exists(conn, table_name):
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            rows_before = cursor.fetchone()[0]

        df.to_sql(table_name, conn, if_exists="append", index=False)

        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        rows_after = cursor.fetchone()[0]

        return rows_after - rows_before
    except Exception as e:
        print(f"Error inserting data: {e}")
        return 0

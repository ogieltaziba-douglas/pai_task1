"""
Database Module

This module provides functions for SQLite database operations
for storing and managing public health vaccination data.

Functions:
    create_connection: Connect to SQLite database
    close_connection: Close database connection
    create_table: Create a new table
    table_exists: Check if table exists
    insert_dataframe: Insert DataFrame into table
    fetch_all: Retrieve all records from table
    execute_query: Run custom SQL query
    create_record: Insert single record
    read_record: Read single record by ID
    update_record: Update record by ID
    delete_record: Delete record by ID
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
        >>> # Use connection...
        >>> close_connection(conn)
    """
    conn = sqlite3.connect(db_path)
    # Enable foreign keys and return rows as Row objects for dict-like access
    conn.row_factory = sqlite3.Row
    return conn


def close_connection(conn: sqlite3.Connection) -> bool:
    """
    Close a database connection.

    Args:
        conn: The database connection to close.

    Returns:
        True if connection was closed successfully.
    """
    try:
        conn.close()
        return True
    except Exception:
        return False


def create_table(conn: sqlite3.Connection, table_name: str, columns: dict) -> bool:
    """
    Create a table with the specified columns.

    Args:
        conn: Database connection.
        table_name: Name of the table to create.
        columns: Dictionary of column_name: column_type pairs.
                 Example: {'id': 'INTEGER PRIMARY KEY', 'name': 'TEXT'}

    Returns:
        True if table was created successfully.

    Example:
        >>> columns = {'id': 'INTEGER PRIMARY KEY', 'location': 'TEXT'}
        >>> create_table(conn, 'vaccinations', columns)
    """
    try:
        # Build column definitions
        column_defs = ", ".join([f"{name} {dtype}" for name, dtype in columns.items()])

        # Create the table
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_defs})"
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error creating table: {e}")
        return False


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
        # 'append' mode adds to existing table or creates if not exists
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


def fetch_all(conn: sqlite3.Connection, table_name: str) -> pd.DataFrame:
    """
    Fetch all records from a table.

    Args:
        conn: Database connection.
        table_name: Name of the table to fetch from.

    Returns:
        DataFrame containing all records.

    Example:
        >>> df = fetch_all(conn, 'vaccinations')
        >>> print(df.head())
    """
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql_query(query, conn)


def execute_query(conn: sqlite3.Connection, query: str) -> pd.DataFrame:
    """
    Execute a custom SQL query.

    Args:
        conn: Database connection.
        query: SQL query string.

    Returns:
        DataFrame containing query results.

    Example:
        >>> result = execute_query(conn, "SELECT * FROM data WHERE cases > 100")
    """
    return pd.read_sql_query(query, conn)


def create_record(conn: sqlite3.Connection, table_name: str, data: dict) -> int:
    """
    Create a single record in a table.

    Args:
        conn: Database connection.
        table_name: Name of the table.
        data: Dictionary of column: value pairs.

    Returns:
        ID (rowid) of the created record.

    Example:
        >>> record = {'location': 'France', 'cases': 150}
        >>> record_id = create_record(conn, 'data', record)
    """
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?" for _ in data])
    values = tuple(data.values())

    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()

    return cursor.lastrowid


def read_record(conn: sqlite3.Connection, table_name: str, record_id: int) -> dict:
    """
    Read a single record by ID (rowid).

    Args:
        conn: Database connection.
        table_name: Name of the table.
        record_id: ID (rowid) of the record to read.

    Returns:
        Dictionary containing the record, or None if not found.

    Example:
        >>> record = read_record(conn, 'vaccinations', 1)
        >>> if record:
        >>>     print(record['location'])
    """
    query = f"SELECT rowid, * FROM {table_name} WHERE rowid = ?"

    cursor = conn.cursor()
    cursor.execute(query, (record_id,))
    row = cursor.fetchone()

    if row is None:
        return None

    # Convert Row object to dictionary
    return dict(row)


def update_record(
    conn: sqlite3.Connection, table_name: str, record_id: int, data: dict
) -> bool:
    """
    Update a record by ID (rowid).

    Args:
        conn: Database connection.
        table_name: Name of the table.
        record_id: ID (rowid) of the record to update.
        data: Dictionary of column: value pairs to update.

    Returns:
        True if record was updated successfully.

    Example:
        >>> update_record(conn, 'data', 1, {'cases': 200})
    """
    set_clause = ", ".join([f"{col} = ?" for col in data.keys()])
    values = tuple(data.values()) + (record_id,)

    query = f"UPDATE {table_name} SET {set_clause} WHERE rowid = ?"

    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()

    return cursor.rowcount > 0


def delete_record(conn: sqlite3.Connection, table_name: str, record_id: int) -> bool:
    """
    Delete a record by ID (rowid).

    Args:
        conn: Database connection.
        table_name: Name of the table.
        record_id: ID (rowid) of the record to delete.

    Returns:
        True if record was deleted, False if not found.

    Example:
        >>> deleted = delete_record(conn, 'data', 1)
        >>> if deleted:
        >>>     print("Record deleted")
    """
    query = f"DELETE FROM {table_name} WHERE rowid = ?"

    cursor = conn.cursor()
    cursor.execute(query, (record_id,))
    conn.commit()

    return cursor.rowcount > 0


# ============================================================================
# OOP SQLDataFilter Class (SQL-based filtering with method chaining)
# ============================================================================


class SQLDataFilter:
    """
    SQL-based data filter with method chaining support.

    OOP Principles Demonstrated:
    - Method chaining (fluent interface)
    - Encapsulation (private attributes)
    - SQL query building

    LO3 Demonstration:
    - Uses actual SQL WHERE clauses
    - Executes SQL queries against SQLite database

    Example:
        >>> result = (SQLDataFilter(conn)
        ...           .by_country('Spain')
        ...           .by_date_range(start='2021-01-01')
        ...           .result())
    """

    def __init__(self, conn: sqlite3.Connection, table: str = "vaccinations"):
        """
        Initialize SQLDataFilter with database connection.

        Args:
            conn: SQLite database connection
            table: Table name to query (default: 'vaccinations')
        """
        raise NotImplementedError("SQLDataFilter.__init__ not implemented")

    def by_country(self, countries) -> "SQLDataFilter":
        """
        Filter by country using SQL WHERE clause.

        Args:
            countries: Country name (str) or list of countries

        Returns:
            New SQLDataFilter with added WHERE clause
        """
        raise NotImplementedError("SQLDataFilter.by_country not implemented")

    def by_date_range(self, start=None, end=None) -> "SQLDataFilter":
        """
        Filter by date range using SQL WHERE clause.

        Args:
            start: Start date string (inclusive)
            end: End date string (inclusive)

        Returns:
            New SQLDataFilter with added WHERE clause
        """
        raise NotImplementedError("SQLDataFilter.by_date_range not implemented")

    def result(self) -> pd.DataFrame:
        """
        Execute SQL query and return result as DataFrame.

        Returns:
            DataFrame with query results
        """
        raise NotImplementedError("SQLDataFilter.result not implemented")

    @property
    def query(self) -> str:
        """
        Get the SQL query string.

        Returns:
            SQL query string
        """
        raise NotImplementedError("SQLDataFilter.query not implemented")

    @property
    def count(self) -> int:
        """
        Get count of rows matching current filters.

        Returns:
            Row count
        """
        raise NotImplementedError("SQLDataFilter.count not implemented")

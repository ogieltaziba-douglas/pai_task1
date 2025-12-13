"""
Activity Logger Module (OOP-Only)

Provides the ActivityLogger class for tracking user activities
in the Public Health Data Insights Dashboard.

OOP Principles Demonstrated:
- Encapsulation: Private attributes with property accessors
- Methods: Behavior encapsulated in class methods
- Single Responsibility: One class, one purpose

Usage:
    from src.logger import ActivityLogger

    logger = ActivityLogger()
    logger.log('LOAD_DATA', 'Loaded 196,246 records')
    print(logger.session_entries)
"""

import os
from datetime import datetime
from typing import List


class ActivityLogger:
    """
    Activity Logger for tracking user actions.

    Demonstrates OOP principles:
    - Encapsulation: Private _session_log and _log_file attributes
    - Properties: Controlled access via session_entries, file_entries
    - Methods: log(), clear() for behavior

    Attributes:
        _session_log (List[str]): Private session log entries
        _log_file (str): Path to log file

    Example:
        >>> logger = ActivityLogger()
        >>> logger.log('LOAD_DATA', 'Loaded data')
        >>> print(logger.session_entries)
        ['[2025-12-13 18:00:00] LOAD_DATA: Loaded data']
    """

    def __init__(self, log_file: str = "logs/activity.log"):
        """
        Initialize the ActivityLogger.

        Args:
            log_file: Path to log file (default: logs/activity.log)
        """
        self._session_log: List[str] = []
        self._log_file = log_file

        # Ensure log directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

    def log(self, action: str, details: str) -> None:
        """
        Log an activity.

        Args:
            action: Action name (e.g., 'LOAD_DATA', 'FILTER')
            details: Description of the activity
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {action}: {details}"

        # Add to session log
        self._session_log.append(entry)

        # Append to log file
        try:
            with open(self._log_file, "a", encoding="utf-8") as f:
                f.write(entry + "\n")
        except Exception:
            # If file write fails, we still have session log
            pass

    @property
    def session_entries(self) -> List[str]:
        """
        Get session log entries (returns copy for encapsulation).

        Returns:
            Copy of session log entries
        """
        return self._session_log.copy()

    @property
    def file_entries(self) -> List[str]:
        """
        Get log entries from file.

        Returns:
            List of log entries from file
        """
        if not os.path.exists(self._log_file):
            return []

        try:
            with open(self._log_file, "r", encoding="utf-8") as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        except Exception:
            return []

    def clear(self) -> None:
        """Clear all log entries (session and file)."""
        self._session_log = []

        try:
            with open(self._log_file, "w", encoding="utf-8") as f:
                f.write("")
        except Exception:
            pass

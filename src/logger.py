"""
Activity Logger Module

This module handles logging of user activities and actions
in the Public Health Data Insights Dashboard.

Functions:
    log_activity: Log a user activity to file and session
    get_log_entries: Retrieve log entries from file
    clear_log: Clear all log entries
    get_session_log: Get in-memory session log
"""

import os
from datetime import datetime
from typing import List


# Session log for current session (in-memory)
_session_log: List[str] = []


def log_activity(
    action: str, details: str, log_file: str = "logs/activity.log"
) -> None:
    """
    Log a user activity.

    Args:
        action: Action name (e.g., 'LOAD_DATA', 'FILTER', 'EXPORT')
        details: Description of the activity
        log_file: Path to log file
    """
    global _session_log

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {action}: {details}"

    # Add to session log
    _session_log.append(entry)

    # Ensure directory exists
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # Append to log file
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
    except Exception:
        # If we can't write to file, at least we have session log
        pass


def get_log_entries(log_file: str = "logs/activity.log") -> List[str]:
    """
    Get all log entries from file.

    Args:
        log_file: Path to log file

    Returns:
        List of log entry strings
    """
    if not os.path.exists(log_file):
        return []

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            entries = [line.strip() for line in f.readlines() if line.strip()]
        return entries
    except Exception:
        return []


def clear_log(log_file: str = "logs/activity.log") -> None:
    """
    Clear all log entries.

    Args:
        log_file: Path to log file
    """
    global _session_log

    # Clear session log
    _session_log = []

    # Clear file
    try:
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("")
    except Exception:
        pass


def get_session_log() -> List[str]:
    """
    Get log entries from current session (in-memory).

    Returns:
        List of log entry strings for current session
    """
    return _session_log.copy()

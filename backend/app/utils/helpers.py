"""
Helper utilities for common operations
"""

import uuid
import os
import json
from datetime import datetime
from typing import Any, Dict


def generate_id() -> str:
    """
    Generate unique identifier for cases
    
    Returns:
        Unique ID string
    """
    return f"CASE_{uuid.uuid4().hex[:12].upper()}_{int(datetime.now().timestamp())}"


def save_to_json(data: Dict[str, Any], filepath: str) -> bool:
    """
    Save dictionary data to JSON file
    
    Args:
        data: Dictionary to save
        filepath: Path to save file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving to JSON: {str(e)}")
        return False


def load_from_json(filepath: str) -> Dict[str, Any]:
    """
    Load dictionary data from JSON file
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Loaded dictionary or empty dict if error
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading from JSON: {str(e)}")
        return {}


def format_timestamp(dt: datetime = None) -> str:
    """
    Format datetime to ISO format string
    
    Args:
        dt: Datetime object (uses current time if None)
        
    Returns:
        ISO format timestamp string
    """
    if dt is None:
        dt = datetime.now()
    return dt.isoformat()


def parse_timestamp(timestamp_str: str) -> datetime:
    """
    Parse ISO format timestamp string to datetime
    
    Args:
        timestamp_str: ISO format timestamp string
        
    Returns:
        Datetime object
    """
    return datetime.fromisoformat(timestamp_str)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal attacks
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove path components
    filename = os.path.basename(filename)
    # Remove special characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def calculate_processing_time(start_time: datetime, end_time: datetime = None) -> float:
    """
    Calculate processing time in seconds
    
    Args:
        start_time: Start datetime
        end_time: End datetime (uses current time if None)
        
    Returns:
        Processing time in seconds
    """
    if end_time is None:
        end_time = datetime.now()
    delta = end_time - start_time
    return delta.total_seconds()


def log_operation(operation: str, case_id: str, status: str, details: str = "") -> Dict[str, Any]:
    """
    Create a log entry for an operation
    
    Args:
        operation: Operation name
        case_id: Case identifier
        status: Operation status
        details: Additional details
        
    Returns:
        Log entry dictionary
    """
    return {
        "timestamp": format_timestamp(),
        "operation": operation,
        "case_id": case_id,
        "status": status,
        "details": details
    }

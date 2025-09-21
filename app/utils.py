"""
Utility functions for the application
"""
from datetime import datetime
from typing import Dict, Any

def get_current_timestamp() -> str:
    """Aktuellen Zeitstempel als String zurückgeben"""
    return datetime.now().isoformat()

def format_response(data: Any, message: str = "Success") -> Dict[str, Any]:
    """Standardisierte API-Antwort formatieren"""
    return {
        "message": message,
        "data": data,
        "timestamp": get_current_timestamp()
    }

def validate_email(email: str) -> bool:
    """Einfache E-Mail-Validierung"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

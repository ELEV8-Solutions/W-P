# Database configuration and utilities
from typing import Dict, Any

class DatabaseConfig:
    """Datenbank-Konfiguration"""
    
    # Für Demo verwenden wir In-Memory Storage
    # In Produktion würde man eine echte Datenbank verwenden
    DATABASE_URL: str = "sqlite:///./app.db"
    
    @classmethod
    def get_database_config(cls) -> Dict[str, Any]:
        return {
            "database_url": cls.DATABASE_URL,
            "echo": False,  # SQL-Logging
        }

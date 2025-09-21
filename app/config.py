from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Anwendungseinstellungen"""
    
    # App Info
    app_name: str = "FastAPI Vercel App"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # CORS
    allowed_origins: List[str] = ["*"]
    
    # Security
    secret_key: str = "your-secret-key-here"  # In Produktion aus Umgebungsvariablen
    
    # Database
    database_url: str = "sqlite:///./app.db"
    
    # Email Configuration
    sender_email: str = "your-email@gmail.com"
    sender_password: str = "your-app-password"
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    
    class Config:
        env_file = ".env"

# Globale Settings-Instanz
settings = Settings()

import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the application
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)


class Config:
    """Application configuration loaded from environment variables."""

    # General App Config
    APP_NAME = os.getenv("APP_NAME", "OmniPulse Commerce Portal")
    APP_ENV = os.getenv("APP_ENV", "production")
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    PORT = int(os.getenv("PORT", 5000))
    SECRET_KEY = os.getenv("SECRET_KEY", "default-dev-secret-key-change-me")

    # Admin Login Credentials
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "adminpassword")

    # Database Configuration (Managed by Ansible / .env)
    DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()
    DB_NAME = os.getenv("DB_NAME", "dashboard.sqlite3")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_USER = os.getenv("DB_USER", "ecommerce_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_SOCKET = os.getenv("DB_SOCKET", "")

    # SQLite database file path
    SQLITE_PATH = BASE_DIR / DB_NAME

    @classmethod
    def get_db_info(cls):
        """Returns a sanitized dict of DB connection properties for dashboard display."""
        return {
            "type": cls.DB_TYPE.upper(),
            "name": cls.DB_NAME,
            "host": cls.DB_HOST,
            "port": cls.DB_PORT,
            "user": cls.DB_USER,
            "source": ".env file (Ansible-configurable)",
        }

"""Configuration settings for Text-to-SQL pipeline"""

import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "3306"),
    "username": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "vaibhav"),
    "database": os.getenv("DB_NAME", "regional_sales_data"),
}

# LLM Configuration
LLM_CONFIG = {
    "model": "gemini-2.0-flash",
    "provider": "google_genai",
    "api_key": os.getenv("GOOGLE_API_KEY", "AIzaSyDNgg9I19YxUXdnH3m29khFiUG48an1Sbw"),
}

# Agent Configuration
AGENT_CONFIG = {
    "max_iterations": 10,
    "verbose": True,
    "top_k": 5,  # Top K results for SQL queries
}

# Logging Configuration
LOG_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "logs/text_to_sql.log",
}

def get_mysql_uri():
    """Generate MySQL connection URI"""
    config = DB_CONFIG
    return f"mysql+pymysql://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"

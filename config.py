"""Configuration settings for the application."""
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0'))
OPENAI_TIMEOUT = int(os.getenv('OPENAI_TIMEOUT', '30'))

# Data Configuration
DATA_FILE = os.getenv('DATA_FILE', 'data.json')

# Application Configuration
APP_TITLE = "Dumroo Admin Panel - AI Query System"
APP_ICON = "🎓"
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Query Configuration
MAX_QUERY_LENGTH = int(os.getenv('MAX_QUERY_LENGTH', '500'))
DAYS_BACK_DEFAULT = int(os.getenv('DAYS_BACK_DEFAULT', '7'))
DAYS_AHEAD_DEFAULT = int(os.getenv('DAYS_AHEAD_DEFAULT', '7'))

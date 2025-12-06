"""
Production configuration for TextSummarize application.
"""

import os
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()

import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    env: str = os.getenv("ENV", "dev")
    model_name: str = os.getenv("MODEL_NAME", "facebook/bart-large-cnn")
    max_input_tokens: int = int(os.getenv("MAX_INPUT_TOKENS", "2048"))
    port: int = int(os.getenv("PORT", "8000"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        env_file = ".env"

settings = Settings()

# Application Settings
APP_NAME = "TextSummarize"
APP_VERSION = "1.0.0"
DESCRIPTION = "End-to-End Text Summarization with Extractive and Abstractive Methods"

# Environment
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_DIR = PROJECT_ROOT / 'logs'
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / f'{APP_NAME}.log'

# Paths
DATA_DIR = PROJECT_ROOT / 'data'
MODEL_CACHE_DIR = PROJECT_ROOT / '.cache' / 'models'
RESULTS_DIR = PROJECT_ROOT / 'results'

# Create directories if they don't exist
for directory in [DATA_DIR, MODEL_CACHE_DIR, RESULTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Summarization Settings
DEFAULT_SUMMARIZATION_METHOD = 'extractive'  # 'extractive' or 'abstractive'
DEFAULT_NUM_SENTENCES = 3
MIN_NUM_SENTENCES = 1
MAX_NUM_SENTENCES = 10

# Model Settings
EMBEDDING_MODEL = 'bert-base-uncased'
SUMARY_MODEL = 'facebook/bart-large-cnn'
DEVICE = os.getenv('DEVICE', 'cpu')  # 'cpu' or 'cuda'

# Streamlit Settings
STREAMLIT_PAGE_TITLE = "TextSummarize"
STREAMLIT_PAGE_ICON = "📄"
STREAMLIT_LAYOUT = "wide"
STREAMLIT_INITIAL_SIDEBAR_STATE = "expanded"

# API Settings (if needed for future deployment)
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', 8000))
API_WORKERS = int(os.getenv('API_WORKERS', 4))

# Performance Settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MIN_TEXT_LENGTH = 50  # Minimum characters for summarization
MAX_TEXT_LENGTH = 50000  # Maximum characters to process

# Feature Flags
ENABLE_BATCH_PROCESSING = True
ENABLE_FILE_UPLOAD = True
ENABLE_URL_PROCESSING = False  # Future feature
ENABLE_API = False  # Future feature

# Caching
ENABLE_CACHE = True
CACHE_EXPIRY = 3600  # 1 hour in seconds

# Production Deployment
WORKERS = int(os.getenv('WORKERS', 4))
WORKER_CLASS = 'uvicorn.workers.UvicornWorker'
TIMEOUT = 120
KEEP_ALIVE = 5

print(f"Configuration loaded: {ENVIRONMENT} mode")
print(f"Debug mode: {DEBUG}")
print(f"Log level: {LOG_LEVEL}")
print(f"Device: {DEVICE}")

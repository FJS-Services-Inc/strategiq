import enum
from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = BASE_DIR / "backend"
FRONTEND_DIR = BASE_DIR / "frontend"


pg_dialects = [
    "postgres",
    "postgresql",
    "postgresql+asyncpg",
    "postgresql+pg8000",
    "postgresql+psycopg",
    "postgresql+psycopg2",
    "postgresql+psycopg2cffi",
    "postgresql+py-postgresql",
    "postgresql+pygresql",
]

mysql_dialects = [
    "mysql+mysqldb",
    "mysql+pymysql",
    "mariadb+mariadbconnector",
    "mysql+mysqlconnector",
    "mysql+asyncmy",
    "mysql+aiomysql",
    "mysql+cymysql",
    "mysql+pyodbc",
]

sqlite_dialects = [
    "sqlite",
    "sqlite+pysqlite",
    "sqlite+aiosqlite",
    "sqlite+pysqlcipher",
]

all_dialects = enum.Enum(
    "DatabaseDialect",
    {
        x.upper(): x
        for x in [
            *[
                y
                for x in (pg_dialects, mysql_dialects, sqlite_dialects)
                for y in x
            ],
        ]
    },
)

# TODO: include Oracle and MSSQL dialects
SECRET_KEY: str = config("SECRET_KEY")

# Application Configuration Constants
# ===================================

# PDF Generation and Caching
PDF_CACHE_TTL_SECONDS = 300  # 5 minutes
PDF_GENERATION_TIMEOUT_SECONDS = 60

# SWOT Analysis Validation
SWOT_MIN_ITEMS_PER_CATEGORY = 2
SWOT_MAX_ITEMS_PER_CATEGORY = 10
SWOT_MIN_ANALYSIS_LENGTH = 100
SWOT_MAX_ANALYSIS_LENGTH = 5000

# Status Updates and Polling
STATUS_UPDATE_DELAY_MIN_SECONDS = 0
STATUS_UPDATE_DELAY_MAX_SECONDS = 5
STATUS_POLL_INTERVAL_SECONDS = 1

# External API Configuration
HTTP_REQUEST_TIMEOUT_SECONDS = 30
HTTP_CONNECT_TIMEOUT_SECONDS = 10

# Input Validation
MAX_PRIMARY_ENTITY_LENGTH = 500
MAX_COMPARISON_ENTITIES_LENGTH = 2000
MAX_COMPARISON_ENTITIES_COUNT = 10

# Reddit API Configuration
REDDIT_MAX_SUBREDDITS = 10
REDDIT_CONCURRENT_THRESHOLD = 3  # Switch to async when >3 subreddits

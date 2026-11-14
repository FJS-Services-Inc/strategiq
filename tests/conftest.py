"""Test configuration.

The backend reads required settings from the environment at import time.
Dummy values are set here (before any ``backend`` import) so the suite runs
offline; nothing in these tests opens a database connection.
"""

import os

_DUMMY_ENV = {
    "SERVER_ENV": "dev",
    "DEBUG": "False",
    "SECRET_KEY": "test-secret",
    "LOCAL_DB_UN": "user",
    "LOCAL_DB_PW": "pw",
    "LOCAL_DB_DB": "db",
    "LOCAL_DB_HOST": "localhost",
    "LOCAL_DB_PORT": "5432",
    "CLOUD_DB_UN": "user",
    "CLOUD_DB_PW": "pw",
    "CLOUD_DB_DB": "db",
    "CLOUD_DB_HOST": "localhost",
    "CLOUD_DB_PORT": "5432",
    "OPENAI_API_KEY": "test-key",
    "REDDIT_USER_AGENT": "tests",
    "TAVILY_API_KEY": "test-key",
}
os.environ.update(_DUMMY_ENV)

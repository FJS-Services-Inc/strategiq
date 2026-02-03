import enum
import os

from decouple import config

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")


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

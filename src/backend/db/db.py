import asyncio

from fastapi_service_kit import (  # noqa: F401
    as_form,
    async_session_dependency,
    check_db_exists,
    create_db,
    run_out_of_band,
    sync_session_dependency,
)
from sqlalchemy import MetaData, event
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlmodel import Session, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.utils import get_val

# echo, create = True, True
echo, create = False, False
# echo, create = False, True
# echo, create = True, False

db_url = get_val("PROJECT_DB_URL")

schema = "pygentic_ai"
meta = MetaData(schema=schema)


def create_db_engine(
    db_url: str,
    async_bool: bool = False,
    echo_bool: bool = False,
):
    """

    :param db_url:
    :param async_bool:
    :param echo_bool:
    :return:
    """
    engine_inst = (
        create_engine(db_url, echo=echo_bool)
        if async_bool is False
        else create_async_engine(db_url, echo=echo_bool, poolclass=NullPool)
    )

    return engine_inst


engine = create_db_engine(db_url, async_bool=True, echo_bool=False)


@event.listens_for(engine.sync_engine, "connect", insert=True)
def set_current_schema(dbapi_connection, connection_record):
    """
    This is a helper event listener to ensure that the current
    schema is set when bootstrapping the database tables.
    Taken from:

    https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#setting-alternate
    -search-paths-on-connect

    :param dbapi_connection:
    :param connection_record:
    :return:
    """
    existing_autocommit = dbapi_connection.autocommit
    dbapi_connection.autocommit = True
    cursor_obj = dbapi_connection.cursor()
    cursor_obj.execute("SET SESSION search_path='%s'" % schema)
    cursor_obj.close()
    dbapi_connection.autocommit = existing_autocommit


sync_engine = create_db_engine(db_url, echo_bool=echo)

session_inst = Session(sync_engine, expire_on_commit=False)

async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

session_maker = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False,
)

sync_session_maker = sessionmaker(
    bind=sync_engine,
    class_=Session,
    expire_on_commit=False,
)

# FastAPI dependencies (``Depends(get_async_session)``)
get_async_session = async_session_dependency(async_session_maker)
get_sync_session = sync_session_dependency(sync_session_maker)

if __name__ == "__main__":
    import sys

    from backend.db.models import *  # noqa F403

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(create_db(engine, meta, force=True))

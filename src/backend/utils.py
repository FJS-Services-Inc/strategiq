import asyncio
import os
import sys

from decouple import config


class ContextManager:
    """
    Context middleware to inject all variables into the global context
    object. This will ensure that the `request` object is available to all
    components in JinjaX and removes the need to pass it through explicitly.
    """

    def __init__(self):
        self.global_context = {}

    def set_context(self, **kwargs):
        """
        Sets the global context for the application via kwargs

        :param kwargs: dict[str, Any]
        """
        self.global_context.update(kwargs)

    def get_context(self):
        """
        retrieves the global context for the application
        :return: dict[str, Any]
        """
        return self.global_context


def get_db_url(env: str = "dev"):
    """

    :param env:
    :return:
    """
    if env == "dev":
        un, pw, db, host, port = (
            config(x)
            for x in (
                "LOCAL_DB_UN",
                "LOCAL_DB_PW",
                "LOCAL_DB_DB",
                "LOCAL_DB_HOST",
                "LOCAL_DB_PORT",
            )
        )

        # url = f"mysql://{un}:{pw}@{host}:{port}/{db}"
        # url = f"mariadb+pymysql://{un}:{pw}@{host}:{port}/{db}"
    elif env == "prod":
        un, pw, db, host, port = (
            config(x)
            for x in (
                "POSTGRES_USER",
                "POSTGRES_PASSWORD",
                "POSTGRES_DB",
                "db",
                "5432",
            )
        )
    else:
        return None

    url = f"postgresql://{un}:{pw}@{host}:{port}/{db}"
    return url


def get_val(val: str, default: str | int | bool | None = None, **kwargs):
    """
    A utility function that checks the platform environment or an .env file to
    pull a key:value pair and return the value. If the value does not exist, a
    ValueError will be raised
    Args:
        val: str
        default: Union[str, None]: default is None

    Returns val: str

    """
    if os.environ.get(val, None) is not None:
        val = os.environ.get(val)
    elif config(val, None, **kwargs) is not None:
        val = config(val)
    elif default is not None:
        val = default
    else:
        raise ValueError(
            f"Env Var {val} is not populated in the environment "
            f"or within the configuration files",
        )

    return val


def windows_sys_event_loop_check():
    """
    A function that sets the event loop policy to a Windows-specific one.
    This is a workaround to a known bug involving capturing an existing
    asyncio event loop on non-Linux platforms.
    """
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def set_event_loop():
    """
    A utility function to capture the existing event loop if it's running.
    If no event loop is running, then a new one is created and set.
    """
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

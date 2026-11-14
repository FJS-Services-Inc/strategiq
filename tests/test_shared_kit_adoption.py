"""Checks that the helpers now provided by ``fastapi_service_kit`` are wired
into the backend and behave as the backend needs. Fully offline."""

import asyncio
import logging
from pathlib import Path

import fastapi_service_kit as kit
import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from sqlalchemy.engine import make_url
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession


def test_db_module_reexports_kit_helpers():
    from backend.db import db

    assert db.as_form is kit.as_form
    assert db.run_out_of_band is kit.run_out_of_band
    assert db.check_db_exists is kit.check_db_exists
    assert db.create_db is kit.create_db


def test_get_async_session_yields_async_session():
    from backend.db import db

    async def run():
        gen = db.get_async_session()
        session = await gen.__anext__()
        try:
            assert isinstance(session, AsyncSession)
        finally:
            await gen.aclose()

    asyncio.run(run())


def test_get_sync_session_yields_sync_session():
    from backend.db import db

    gen = db.get_sync_session()
    session = next(gen)
    try:
        assert isinstance(session, Session)
        assert session.bind is db.sync_engine
        assert session.expire_on_commit is False
    finally:
        gen.close()


def test_as_form_is_a_working_form_dependency():
    from backend.db.db import as_form

    @as_form
    class Signup(BaseModel):
        email: str = Field(min_length=3)
        age: int | None = None

    app = FastAPI()

    @app.post("/signup")
    async def signup(data: Signup = Depends(Signup.as_form)):
        return data.model_dump()

    client = TestClient(app)
    ok = client.post("/signup", data={"email": "a@b.co", "age": "7"})
    assert ok.status_code == 200
    assert ok.json() == {"email": "a@b.co", "age": 7}
    # a required field stays required, and constraints still apply
    assert client.post("/signup", data={"age": "7"}).status_code == 422
    assert client.post("/signup", data={"email": "a"}).status_code == 422


def test_get_db_url_escapes_credentials(monkeypatch):
    from backend.utils import get_db_url

    monkeypatch.setenv("LOCAL_DB_UN", "app")
    monkeypatch.setenv("LOCAL_DB_PW", "p@ss/w#rd")
    monkeypatch.setenv("LOCAL_DB_DB", "mydb")
    monkeypatch.setenv("LOCAL_DB_HOST", "db.internal")
    monkeypatch.setenv("LOCAL_DB_PORT", "5433")

    url = get_db_url("dev")

    parsed = make_url(url)
    assert parsed.drivername == "postgresql"
    assert parsed.username == "app"
    assert parsed.password == "p@ss/w#rd"
    assert parsed.host == "db.internal"
    assert parsed.port == 5433
    assert parsed.database == "mydb"


def test_get_db_url_plain_credentials_unchanged(monkeypatch):
    from backend.utils import get_db_url

    monkeypatch.setenv("LOCAL_DB_UN", "app")
    monkeypatch.setenv("LOCAL_DB_PW", "secret")
    monkeypatch.setenv("LOCAL_DB_DB", "mydb")
    monkeypatch.setenv("LOCAL_DB_HOST", "localhost")
    monkeypatch.setenv("LOCAL_DB_PORT", "5432")

    assert get_db_url("dev") == "postgresql://app:secret@localhost:5432/mydb"


def test_get_db_url_unknown_env_is_none():
    from backend.utils import get_db_url

    assert get_db_url("staging") is None


def test_event_loop_helpers_are_the_kit_ones():
    from backend.core import tools

    assert tools.set_event_loop is kit.set_event_loop
    assert tools.windows_sys_event_loop_check is (
        kit.windows_sys_event_loop_check
    )


def test_logger_writes_per_level_files_and_bridges_stdlib():
    from backend.logger import dir_path, logger

    logger.error("kit-adoption-sentinel-direct")
    logging.getLogger("uvicorn.error").error("kit-adoption-sentinel-stdlib")
    logger.complete()

    assert any(
        isinstance(h, kit.InterceptHandler)
        for h in logging.getLogger("uvicorn").handlers
    )
    error_files = list(Path(dir_path).glob("error_log_*.log"))
    assert error_files, "per-level error file was not created"
    text = "".join(f.read_text(encoding="utf-8") for f in error_files)
    assert "kit-adoption-sentinel-direct" in text
    assert "kit-adoption-sentinel-stdlib" in text
    # per-level filter: error records do not land in the info file
    info_text = "".join(
        f.read_text(encoding="utf-8")
        for f in Path(dir_path).glob("info_log_*.log")
    )
    assert "kit-adoption-sentinel" not in info_text


@pytest.mark.parametrize(
    "level", ["info", "debug", "error", "success", "warning", "critical"]
)
def test_logger_creates_every_level_file(level):
    from backend.logger import dir_path, logger

    getattr(logger, level)(f"kit-adoption-level-{level}")
    logger.complete()

    files = list(Path(dir_path).glob(f"{level}_log_*.log"))
    assert files, f"{level} sink file missing"

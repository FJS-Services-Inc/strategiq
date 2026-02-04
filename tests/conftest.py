"""
Pytest configuration and shared fixtures for StrategIQ tests.

Provides fixtures for:
- Test client (FastAPI TestClient)
- Database (test database with transactions)
- Mock data (SWOT analysis, entities, etc.)
"""

import asyncio
import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.core.core import SwotAnalysis
from backend.db.base import Base

# Set test environment
os.environ["TESTING"] = "true"
os.environ["DEBUG"] = "false"


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def test_db_engine():
    """
    Create a test database engine using SQLite in-memory.
    Each test gets a fresh database.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create all tables
    Base.metadata.create_all(bind=engine)

    yield engine

    # Drop all tables after test
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_db_session(test_db_engine) -> Generator[Session]:
    """
    Create a test database session.
    Automatically rolls back after each test.
    """
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_db_engine
    )

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope="function")
def test_client() -> Generator[TestClient]:
    """
    Create a FastAPI test client.
    Provides HTTP client for testing API endpoints.
    """
    from app import app

    with TestClient(app) as client:
        yield client


@pytest.fixture
def sample_swot_analysis() -> SwotAnalysis:
    """
    Sample SWOT analysis data for testing.
    """
    return SwotAnalysis(
        primary_entity="Google",
        comparison_entities=["Microsoft", "Amazon"],
        strengths=[
            "Market leader in search",
            "Strong AI capabilities",
            "Diverse product portfolio",
        ],
        weaknesses=[
            "Privacy concerns",
            "Dependence on ad revenue",
            "Regulatory scrutiny",
        ],
        opportunities=[
            "Cloud computing growth",
            "AI market expansion",
            "Emerging markets",
        ],
        threats=[
            "Competition from Microsoft",
            "Regulatory challenges",
            "Market saturation",
        ],
        analysis="Google maintains a dominant position in search and advertising, "
        "but faces increasing competition and regulatory pressure. "
        "Opportunities in AI and cloud computing could drive future growth.",
    )


@pytest.fixture
def mock_session_id() -> str:
    """Mock session ID for testing"""
    return "test_session_12345"


@pytest.fixture
def mock_analysis_data() -> dict:
    """Mock analysis form data"""
    return {
        "primary_entity": "Tesla",
        "comparison_entities": "Ford,General Motors",
    }


@pytest.fixture(autouse=True)
def clear_caches():
    """
    Clear all in-memory caches before each test.
    Ensures test isolation.
    """
    from backend.site.consts import (
        last_message_index,
        result_store,
        status_store,
    )

    status_store.clear()
    result_store.clear()
    last_message_index.clear()

    from backend.core.pdf_cache import pdf_cache

    pdf_cache.clear()

    yield

    # Cleanup after test
    status_store.clear()
    result_store.clear()
    last_message_index.clear()
    pdf_cache.clear()

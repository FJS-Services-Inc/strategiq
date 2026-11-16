"""
Custom Logger Using Loguru
"""

from pathlib import Path

from fastapi_service_kit import InterceptHandler, setup_logging  # noqa: F401

from backend.settings.consts import BACKEND_DIR

dir_path = Path(BACKEND_DIR).joinpath("logs")

# stdout sink + one rotating file per level; stdlib/uvicorn/fastapi records
# are routed through loguru by the kit's InterceptHandler.
logger = setup_logging(
    level="DEBUG",
    log_dir=dir_path,
    per_level_files=True,
    rotation="1 day",
    retention="1 week",
)

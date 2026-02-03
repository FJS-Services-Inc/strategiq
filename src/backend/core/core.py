from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import openai
import praw
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from backend.core.consts import AI_MODEL, default_system_prompt
from backend.db.base import Base
from backend.logger import logger
from backend.utils import get_val


class SwotAnalysis(Base):
    """SQLModel for SWOT Analysis Response Object"""

    primary_entity: str
    comparison_entities: list[str] = []
    strengths: list[str]
    weaknesses: list[str]
    opportunities: list[str]
    threats: list[str]
    analysis: str


def get_reddit_client(
    user_agent: str, check_for_async: bool = False
) -> praw.Reddit | None:
    """
    A function to return a reddit client, provided all env vars are loaded.

    :param user_agent: str
    :param check_for_async: bool = False

    :return: praw.Reddit | None
    """
    try:
        reddit: praw.Reddit = praw.Reddit(
            client_id=get_val("REDDIT_CLIENT_ID"),
            client_secret=get_val("REDDIT_CLIENT_SECRET"),
            user_agent=user_agent,
            check_for_async=check_for_async,
        )
    except ValueError as e:
        reddit = None
        logger.info(
            f"Reddit client not initialized. Please set the "
            f"REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET environment. "
            f"Also please note the error: {e} "
        )

    return reddit


@dataclass
class SwotAgentDeps:
    """Agent Dependencies for SWOT Analysis"""

    request: Any | None = None
    update_status_func: Callable | None = None
    tool_history: list[str] | None = None

    reddit_client: praw.Reddit | None = get_reddit_client(
        user_agent=get_val("REDDIT_USER_AGENT"), check_for_async=False
    )

    client = openai.Client(api_key=get_val("OPENAI_API_KEY"))


swot_agent = Agent(
    OpenAIModel(
        model_name=AI_MODEL,
        provider=OpenAIProvider(api_key=get_val("OPENAI_API_KEY")),
    ),
    deps_type=SwotAgentDeps,
    output_type=SwotAnalysis,
    system_prompt=default_system_prompt,
    retries=5,
)

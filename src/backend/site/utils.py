import asyncio
import random
from pprint import pformat
from typing import Any

from loguru import logger

from backend.core.core import SwotAgentDeps, SwotAnalysis
from backend.core.tools import run_agent
from backend.site.consts import (
    ANALYSIS_COMPLETE_MESSAGE,
    result_store,
    status_store,
)


async def emulate_tool_completion(session_id: str, message: str) -> None:
    """
    Emulate tool completion with random delay.

    Uses asyncio.sleep to avoid blocking the event loop.
    """
    # Sleep a random amount of time between 0 and 5 seconds (async)
    await asyncio.sleep(random.randint(0, 5))
    status_store[session_id].append(message)


async def update_status(session_id: str, message: Any) -> None:
    """
    Updates status messages and handles SWOT analysis results.

    :param session_id: str
    :param message: Any
    :return: None
    """
    logger.debug(f"Updating status for session {session_id}: {message}")

    # Handle SWOT analysis result
    if isinstance(message, SwotAnalysis):
        logger.info(f"SWOT analysis result for session {session_id}: {message}")
        logger.info(
            f"adding to the result store. Existing values: {result_store}"
        )
        result_store[session_id] = message.model_dump()
        status_store[session_id].append(ANALYSIS_COMPLETE_MESSAGE)
        return

    # Handle string messages
    if isinstance(message, str):
        # Instantly store first status message, emulate tool completion for others
        if message == ANALYSIS_COMPLETE_MESSAGE:
            status_store[session_id].append(message)
        else:
            # Call async function directly (no need for run_in_executor)
            await emulate_tool_completion(session_id, message)

    logger.info(
        f"Status messages for session {session_id}: {status_store[session_id]}",
    )


async def run_agent_with_progress(
    session_id, primary_entity, comparison_entities=None
):
    """
    This provides ongoing progress updates for a running agent. A custom deps
    object is used to store the session_id value and then triggers the
    `run_agent` function
    :param session_id: str
    :param primary_entity: str
    :param comparison_entities: list[str] | None
    :return: None
    """
    try:
        deps = SwotAgentDeps(
            request=None,
            update_status_func=lambda request, msg: update_status(
                session_id,
                msg,
            ),
        )

        result = await run_agent(
            primary_entity=primary_entity,
            comparison_entities=comparison_entities,
            deps=deps,
        )

        if not isinstance(result, Exception):
            logger.info(f"Successfully analyzed: {primary_entity}")
            logger.debug(pformat(f"Result object: {result}"))
            result_store[session_id] = result
    except Exception as e:
        logger.error(
            f"An unexpected error occurred. See here: " f"{type(e), e, e.args}",
        )
        await update_status(session_id, f"Unexpected error: {e}")
        raise

import asyncio
import os

from fastapi import APIRouter, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinjax import Catalog, JinjaX
from starlette.responses import HTMLResponse

from backend.logger import logger
from backend.settings import app_settings
from backend.site.consts import (
    ANALYSIS_COMPLETE_MESSAGE,
    ANALYZING_MESSAGE,
    result_store,
    running_tasks,
    status_store,
)
from backend.site.utils import run_agent_with_progress

user_frontend = APIRouter(prefix="", tags=["frontend"])
frontend = app_settings.frontend_dir

templates = Jinja2Templates(directory=os.path.join(frontend, "templates"))
templates.env.add_extension(JinjaX)
catalog = Catalog(jinja_env=templates.env)
list(
    map(
        lambda folder: catalog.add_folder(
            os.path.join(frontend, "templates", "components", folder),  # noqa
        ),
        ("main", "forms", "snippets"),
    ),
)

user_frontend.mount(
    "/static",
    StaticFiles(directory=os.path.join(frontend, "static")),
    name="static",
)


@user_frontend.post("/analyze", response_class=HTMLResponse)
async def analyze_url(
    request: Request,
    primary_entity: str = Form(...),
    comparison_entities: str = Form(""),
) -> HTMLResponse:
    """
    Kick off a SWOT analysis for one or more entities.
    :param request:
    :param primary_entity: main subject (URL or company name)
    :param comparison_entities: comma-separated competitors (optional)
    :return:
    """
    session_id = str(id(request))
    request.session["analysis_id"] = session_id
    request.session["start_time"] = asyncio.get_event_loop().time()

    # Clearing out the status store for the analysis ID session
    status_store[session_id] = []
    result_store[session_id] = None

    status_store[session_id].append(ANALYZING_MESSAGE)

    comp_entities = [
        e.strip() for e in comparison_entities.split(",") if e.strip()
    ]

    logger.info(
        f"Starting analysis — session: {session_id}, "
        f"primary: {primary_entity}, comparing: {comp_entities}"
    )

    task = asyncio.create_task(
        run_agent_with_progress(session_id, primary_entity, comp_entities)
    )
    running_tasks.add(task)
    task.add_done_callback(running_tasks.discard)

    return templates.TemplateResponse(
        "status.html",
        context={
            "request": request,
            "messages": [ANALYZING_MESSAGE],
            "result": False,
        },
    )


@user_frontend.get("/status", response_class=HTMLResponse)
async def get_status(request: Request):
    """
    Returns the current status messages
    :param request:
    :return:
    """
    context = {"request": request, "messages": [], "result": False}
    session_id = request.session.get("analysis_id")
    if session_id:
        # logger.info(f"Found session id!  {session_id}")
        messages = status_store.get(session_id, [])
        result = ANALYSIS_COMPLETE_MESSAGE in messages
        # logger.info(
        #     f"Status check - Session ID: {session_id}, Messages: "
        #     f"{messages}",
        # )

        context.update({"messages": messages, "result": result})

        # logger.info(context)

    return templates.TemplateResponse("status.html", context=context)


@user_frontend.get("/result", response_class=HTMLResponse)
async def get_result(request: Request) -> HTMLResponse:
    """
    Returns the SWOT analysis result from the existing session ID.

    :param request: Request
    :return: HTMLResponse
    """
    session_id = request.session.get("analysis_id")

    if session_id and session_id in result_store:
        result = result_store[session_id]
    else:
        result = None

    return templates.TemplateResponse(
        "result.html",
        {"request": request, "result": result},
    )

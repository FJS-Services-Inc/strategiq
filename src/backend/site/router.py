import asyncio
import os

from fastapi import APIRouter, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinjax import Catalog, JinjaX
from starlette.responses import HTMLResponse, StreamingResponse

from backend.core.pdf_cache import pdf_cache
from backend.core.pdf_service import generate_swot_pdf
from backend.logger import logger
from backend.settings import app_settings
from backend.site.consts import (
    ANALYSIS_COMPLETE_MESSAGE,
    ANALYZING_MESSAGE,
    last_message_index,
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
    Returns new status messages since last poll (incremental updates)
    First poll returns all messages + container, subsequent polls return
    only new items with HTMX OOB swap
    :param request:
    :return:
    """
    session_id = request.session.get("analysis_id")
    if not session_id:
        return templates.TemplateResponse(
            "status.html", {"request": request, "messages": [], "result": False}
        )

    all_messages = status_store.get(session_id, [])
    last_index = last_message_index.get(session_id, 0)
    result = ANALYSIS_COMPLETE_MESSAGE in all_messages

    # First poll: return full container with all messages
    if last_index == 0:
        last_message_index[session_id] = len(all_messages)
        return templates.TemplateResponse(
            "status.html",
            {"request": request, "messages": all_messages, "result": result},
        )

    # Subsequent polls: return only new messages with OOB swap
    new_messages = all_messages[last_index:]
    last_message_index[session_id] = len(all_messages)

    if not new_messages:
        # No new messages, return empty response
        return HTMLResponse(content="", status_code=200)

    # Render new items with OOB swap
    items_html = ""
    for idx, message in enumerate(new_messages):
        is_last = idx == len(new_messages) - 1
        item = templates.get_template("status_item.html").render(
            message=message,
            is_last=is_last,
            result=result,
            request=request,
        )
        items_html += item

    return HTMLResponse(content=items_html, status_code=200)


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


@user_frontend.get("/download-pdf")
async def download_pdf(request: Request) -> StreamingResponse:
    """
    Generate and download SWOT analysis as PDF report.
    Uses composite caching (session_id + content_hash) with 5-minute TTL.

    :param request: Request
    :return: StreamingResponse with PDF file
    """
    session_id = request.session.get("analysis_id")

    if not session_id:
        logger.warning("PDF download attempted without session ID")
        return StreamingResponse(
            content=b"No analysis found. Please run an analysis first.",
            media_type="text/plain",
            status_code=404,
        )

    result = result_store.get(session_id)

    if not result:
        logger.warning(
            f"PDF download attempted but result is None for session: {session_id}"
        )
        return StreamingResponse(
            content=b"Analysis not complete. Please wait for analysis to finish.",
            media_type="text/plain",
            status_code=404,
        )

    # Check cache first
    cached_pdf = pdf_cache.get(session_id, result)

    if cached_pdf:
        logger.info(f"Serving cached PDF for session: {session_id}")
        pdf_buffer = cached_pdf
    else:
        # Generate new PDF
        logger.info(f"Generating new PDF for session: {session_id}")
        pdf_buffer = generate_swot_pdf(result)

        # Cache the generated PDF
        pdf_cache.set(session_id, result, pdf_buffer)

    # Prepare filename
    filename = f"swot-analysis-{session_id[:8]}.pdf"

    # Return as streaming response
    return StreamingResponse(
        content=pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Cache-Control": "no-cache",
        },
    )

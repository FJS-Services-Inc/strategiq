import asyncio
import os

from fastapi import APIRouter, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinjax import Catalog, JinjaX
from starlette.responses import HTMLResponse, Response, StreamingResponse

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

    # Return empty response - HTMX polling will handle rendering via OOB swaps
    return HTMLResponse(content="", status_code=200)


@user_frontend.get("/status", response_class=HTMLResponse)
async def get_status(request: Request):
    """
    Returns new status messages since last poll using pure OOB swaps.
    First poll returns the container + initial messages as OOB.
    Subsequent polls return only new messages as OOB.
    Uses Jinjax components for rendering.
    :param request:
    :return:
    """
    session_id = request.session.get("analysis_id")
    if not session_id:
        return HTMLResponse(content="", status_code=200)

    all_messages = status_store.get(session_id, [])
    last_index = last_message_index.get(session_id, 0)
    result = ANALYSIS_COMPLETE_MESSAGE in all_messages

    # No new messages, return empty response
    if last_index > 0 and last_index >= len(all_messages):
        return HTMLResponse(content="", status_code=200)

    # Determine which messages to send
    new_messages = all_messages[last_index:]
    last_message_index[session_id] = len(all_messages)

    if not new_messages:
        return HTMLResponse(content="", status_code=200)

    # First poll: return container + messages with OOB
    if last_index == 0:
        # Render StatusTimeline container with OOB
        container_html = catalog.render("StatusTimeline", use_oob=True)

        # Render all initial StatusItem components with OOB
        items_html = ""
        for idx, message in enumerate(new_messages):
            is_last = idx == len(new_messages) - 1
            item = catalog.render(
                "StatusItem",
                message=message,
                is_last=is_last,
                result=result,
                use_oob=True,
            )
            items_html += item

        return HTMLResponse(
            content=container_html + items_html, status_code=200
        )

    # Subsequent polls: return only new StatusItem components with OOB swap
    items_html = ""
    for idx, message in enumerate(new_messages):
        is_last = idx == len(new_messages) - 1
        item = catalog.render(
            "StatusItem",
            message=message,
            is_last=is_last,
            result=result,
            use_oob=True,
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
        return Response(
            content=b"No analysis found. Please run an analysis first.",
            media_type="text/plain",
            status_code=404,
        )

    result = result_store.get(session_id)

    if not result:
        logger.warning(
            f"PDF download attempted but result is None for session: {session_id}"
        )
        return Response(
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

    # Prepare filename with company names and date
    import re
    from datetime import datetime

    # Sanitize company names for filename (remove special chars, limit length)
    def sanitize_filename(text: str, max_length: int = 30) -> str:
        # Remove special characters, keep alphanumeric, spaces, hyphens
        text = re.sub(r"[^\w\s-]", "", text)
        # Replace spaces with hyphens
        text = re.sub(r"\s+", "-", text.strip())
        # Limit length
        return text[:max_length].rstrip("-")

    # Build entity string
    primary = sanitize_filename(result.primary_entity)
    if result.comparison_entities:
        # Include first comparison entity
        comparison = sanitize_filename(result.comparison_entities[0])
        entities_str = f"{primary}-vs-{comparison}"
        if len(result.comparison_entities) > 1:
            entities_str += f"-plus{len(result.comparison_entities) - 1}"
    else:
        entities_str = primary

    # Add date
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Build final filename
    filename = f"swot-{entities_str}-{date_str}.pdf"

    # Return as streaming response (iterate over BytesIO in chunks)
    def iterfile():
        pdf_buffer.seek(0)
        yield from pdf_buffer

    return StreamingResponse(
        content=iterfile(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-cache",
        },
    )

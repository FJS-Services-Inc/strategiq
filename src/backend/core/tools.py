import asyncio

import httpx
from bs4 import BeautifulSoup as soup
from pydantic_ai import ModelRetry, RunContext

from backend.core.consts import AI_MODEL
from backend.core.core import SwotAgentDeps, SwotAnalysis, swot_agent
from backend.core.utils import report_tool_usage
from backend.logger import logger
from backend.utils import get_val, set_event_loop, windows_sys_event_loop_check


@swot_agent.tool(prepare=report_tool_usage)
async def fetch_website_content(
    _ctx: RunContext[SwotAgentDeps],
    url: str,
) -> str:
    """
    Fetches the HTML content of the given URL via httpx and beautifulsoup

    :param _ctx: RunContext[SwotAgentDeps]
    :param url: str
    :return: str
    """
    logger.info(f"Fetching website content for: {url}")
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        try:
            response = await http_client.get(url)
            response.raise_for_status()
            html_content = response.text
            content = soup(html_content, "html.parser")
            text_content = content.get_text(separator=" ", strip=True)
            return text_content
        except httpx.HTTPError as e:
            logger.info(f"Request failed: {e}")
            raise


@swot_agent.tool(prepare=report_tool_usage)
async def analyze_competition(
    ctx: RunContext[SwotAgentDeps],
    product_name: str,
    product_description: str,
) -> str:
    """Analyzes the competition for the given product using the OpenAI model."""
    logger.info(f"Analyzing competition for: {product_name}")

    prompt = f"""
    You are a competitive analysis expert. Analyze the competition for the following product:
    Product Name: {product_name}
    Product Description: {product_description}

    Provide a detailed analysis of:
    1. Key competitors and their market position
    2. Competitive advantages and disadvantages
    3. Market trends and potential disruptions
    4. Entry barriers and competitive pressures
    """

    if not ctx.deps.client:
        logger.info("Error: OpenAI client not initialized.")
        return ""
    try:
        response = ctx.deps.client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error analyzing competition: {e}")
        return f"Error analyzing competition: {e}"


@swot_agent.tool(prepare=report_tool_usage)
async def get_reddit_insights(
    ctx: RunContext[SwotAgentDeps],
    query: str,
    subreddit_names: list[str] | None = None,
):
    """
    A tool to gain insights from a subreddit. Data is returned as string
    with newlines

    :param ctx: RunContext[SwotAgentDeps]
    :param query: str
    :param subreddit_names: str
    :return: str
    """
    if not subreddit_names:
        subreddit_names = get_val("REDDIT_SUBREDDIT", "python, ")
        subreddit_names = [x.strip() for x in subreddit_names.split(",")]
    insights = []
    if len(subreddit_names) <= 3:
        for name in subreddit_names:
            subreddit = ctx.deps.reddit_client.subreddit(name)
            search_results = subreddit.search(query)

            for post in search_results:
                insights.append(
                    f"Title: {post.title}\n"
                    f"URL: {post.url}\n"
                    f"Content: {post.selftext}\n",
                )
    else:
        windows_sys_event_loop_check()
        set_event_loop()
        loop = asyncio.get_event_loop()
        tasks = [
            asyncio.ensure_future(
                loop.run_in_executor(
                    None, ctx.deps.reddit_client.subreddit(name).search, query
                )
            )
            for name in subreddit_names
        ]
        results = await asyncio.gather(*tasks)
        for result in results:
            for post in result:
                insights.append(
                    f"Title: {post.title}\n"
                    f"URL: {post.url}\n"
                    f"Content: {post.selftext}\n",
                )

    return "\n".join(insights)


@swot_agent.result_validator
def validate_result(
    _ctx: RunContext[SwotAgentDeps], value: SwotAnalysis
) -> SwotAnalysis:
    """
    A validator for SWOT Analysis results; provides greater completeness and
    quality control
    :param _ctx: RunContext[SwotAgentDeps]
    :param value: SwotAnalysis
    :return: SwotAnalysis
    """
    issues = []
    min = 2
    categories = {
        k.title(): getattr(value, k)
        for k in ("strengths", "weaknesses", "opportunities", "threats")
    }

    for cat_name, points in categories.items():
        if len(points) < min:
            issues.append(
                f"{cat_name} should have at least {min} points. "
                f"Current count is {len(points)}."
            )

    min_len_analysis = 100
    if len(value.analysis) < min_len_analysis:
        issues.append(
            f"Analysis should have at least {min_len_analysis} "
            f"characters. Current count is {len(value.analysis)}."
        )

    if issues:
        logger.info(f"Validation issues: {issues}")
        raise ModelRetry("\n".join(issues))

    return value


async def run_agent(
    url: str,
    deps: SwotAgentDeps = SwotAgentDeps(),
) -> SwotAnalysis | Exception:
    """
    Runs the SWOT Analysis Agent

    :param url: str
    :param deps: SwotAgentDeps
    :return: SwotAnalysis | Exception
    """
    try:
        deps.tool_history = []
        result = await swot_agent.run(
            f"Perform a comprehensive SWOT analysis for this product: {url}",
            deps=deps,
        )
        # logger.debug(f"Agent Result: {pformat(result.data.model_dump())}")

        if deps.update_status_func:
            await deps.update_status_func(deps.request, "Analysis Complete")

        return result.data
    except Exception as e:
        logger.exception(f"Error during agent run: {type(e), e, e.args}")

        if deps.update_status_func:
            await deps.update_status_func(deps.request, f"Error: {e}")

        return e

import asyncio

import httpx
from bs4 import BeautifulSoup as soup
from pydantic_ai import ModelRetry, RunContext
from tavily import TavilyClient

from backend.core.consts import AI_MODEL
from backend.core.core import SwotAgentDeps, SwotAnalysis, swot_agent
from backend.core.exceptions import APIError, ContentError, NetworkError
from backend.core.utils import report_tool_usage
from backend.logger import logger
from backend.settings.consts import (
    HTTP_CONNECT_TIMEOUT_SECONDS,
    HTTP_REQUEST_TIMEOUT_SECONDS,
)
from backend.utils import get_val


@swot_agent.tool(prepare=report_tool_usage)
async def fetch_website_content(
    _ctx: RunContext[SwotAgentDeps],
    url: str,
) -> str:
    """
    Fetches the HTML content of the given URL via httpx and beautifulsoup.

    :param _ctx: RunContext[SwotAgentDeps]
    :param url: str
    :return: str - Extracted text content from the webpage
    :raises NetworkError: If the request fails or times out
    :raises ContentError: If parsing the HTML fails
    """
    logger.info(f"Fetching website content for: {url}")
    try:
        # Configure timeouts to prevent hanging on slow responses
        timeout = httpx.Timeout(
            HTTP_REQUEST_TIMEOUT_SECONDS, connect=HTTP_CONNECT_TIMEOUT_SECONDS
        )
        async with httpx.AsyncClient(
            follow_redirects=True, timeout=timeout
        ) as http_client:
            response = await http_client.get(url)
            response.raise_for_status()
            html_content = response.text

            # Parse HTML content
            content = soup(html_content, "html.parser")
            text_content = content.get_text(separator=" ", strip=True)

            logger.debug(
                f"Successfully fetched {len(text_content)} chars from {url}"
            )
            return text_content

    except httpx.TimeoutException as e:
        logger.warning(f"Timeout fetching {url}: {e}")
        raise NetworkError(
            "fetch_website_content", f"Timeout for {url}", e
        ) from e
    except httpx.HTTPError as e:
        logger.warning(f"HTTP error fetching {url}: {e}")
        raise NetworkError(
            "fetch_website_content", f"Failed to fetch {url}", e
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error parsing {url}: {e}")
        raise ContentError(
            "fetch_website_content", f"Failed to parse content from {url}", e
        ) from e


@swot_agent.tool(prepare=report_tool_usage)
async def search_web(
    _ctx: RunContext[SwotAgentDeps],
    query: str,
) -> str:
    """
    Searches the web using Tavily and returns a formatted summary of results.
    Use this to research companies, products, market trends, or any topic.

    :param _ctx: RunContext[SwotAgentDeps]
    :param query: str - the search query
    :return: str - formatted search results with answer and top snippets
    :raises APIError: If the Tavily API call fails
    """
    logger.info(f"Tavily web search: {query}")

    try:
        client = TavilyClient(api_key=get_val("TAVILY_API_KEY"))

        response = await asyncio.to_thread(
            client.search,
            query,
            include_answer=True,
            max_results=5,
        )

        parts = []
        if response.get("answer"):
            parts.append(f"Summary: {response['answer']}")

        for r in response.get("results", []):
            parts.append(
                f"Title: {r['title']}\n"
                f"URL: {r['url']}\n"
                f"Content: {r.get('content', '')}"
            )

        result = "\n\n".join(parts) if parts else "No results found."
        logger.debug(f"Tavily returned {len(parts)} results for query: {query}")
        return result

    except Exception as e:
        logger.error(f"Tavily search failed for query '{query}': {e}")
        raise APIError(
            "search_web", f"Tavily search failed for '{query}'", e
        ) from e


@swot_agent.tool(prepare=report_tool_usage)
async def analyze_competition(
    ctx: RunContext[SwotAgentDeps],
    product_name: str,
    product_description: str,
) -> str:
    """
    Analyzes the competition for the given product using the OpenAI model.

    :param ctx: RunContext with SwotAgentDeps
    :param product_name: Name of the product
    :param product_description: Description of the product
    :return: str - Detailed competitive analysis
    :raises APIError: If the OpenAI API call fails
    """
    logger.info(f"Analyzing competition for: {product_name}")

    if not ctx.deps.client:
        error_msg = "OpenAI client not initialized"
        logger.error(error_msg)
        raise APIError("analyze_competition", error_msg)

    try:
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

        response = ctx.deps.client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": prompt},
            ],
        )

        content = response.choices[0].message.content
        logger.debug(f"Competition analysis completed for {product_name}")
        return content

    except Exception as e:
        logger.error(f"OpenAI API failed for {product_name}: {e}")
        raise APIError(
            "analyze_competition",
            f"OpenAI analysis failed for {product_name}",
            e,
        ) from e


@swot_agent.tool(prepare=report_tool_usage)
async def get_reddit_insights(
    ctx: RunContext[SwotAgentDeps],
    query: str,
    subreddit_names: list[str] | None = None,
) -> str:
    """
    Gain insights from Reddit subreddits by searching for relevant posts.
    Uses async execution for better performance with multiple subreddits.

    :param ctx: RunContext[SwotAgentDeps]
    :param query: Search query string
    :param subreddit_names: List of subreddit names (e.g., ['python', 'webdev'])
    :return: str - Formatted insights from Reddit posts
    :raises APIError: If Reddit API calls fail
    """
    logger.info(f"Searching Reddit for: {query}")

    try:
        # Get subreddit names from config if not provided
        if not subreddit_names:
            subreddit_names = get_val("REDDIT_SUBREDDIT", "python")
            subreddit_names = [x.strip() for x in subreddit_names.split(",")]

        if not ctx.deps.reddit_client:
            error_msg = "Reddit client not initialized"
            logger.error(error_msg)
            raise APIError("get_reddit_insights", error_msg)

        # Use consistent async pattern for all subreddit counts
        async def search_subreddit(name: str) -> list[str]:
            """Search a single subreddit asynchronously."""
            try:
                loop = asyncio.get_event_loop()
                subreddit = ctx.deps.reddit_client.subreddit(name)
                search_results = await loop.run_in_executor(
                    None, lambda: list(subreddit.search(query, limit=10))
                )

                return [
                    f"Title: {post.title}\n"
                    f"URL: {post.url}\n"
                    f"Content: {post.selftext}\n"
                    for post in search_results
                ]
            except Exception as e:
                logger.warning(f"Failed to search r/{name}: {e}")
                return [f"Error searching r/{name}: {str(e)}"]

        # Search all subreddits concurrently
        results = await asyncio.gather(
            *[search_subreddit(name) for name in subreddit_names],
            return_exceptions=True,
        )

        # Flatten results
        insights = []
        for result in results:
            if isinstance(result, Exception):
                logger.warning(f"Subreddit search failed: {result}")
                continue
            insights.extend(result)

        if not insights:
            return "No Reddit insights found for this query."

        logger.debug(f"Found {len(insights)} Reddit insights")
        return "\n".join(insights)

    except Exception as e:
        logger.error(f"Reddit insights failed for query '{query}': {e}")
        raise APIError(
            "get_reddit_insights", f"Reddit search failed for '{query}'", e
        ) from e


@swot_agent.output_validator
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
    primary_entity: str,
    comparison_entities: list[str] | None = None,
    deps: SwotAgentDeps = SwotAgentDeps(),
) -> SwotAnalysis | Exception:
    """
    Runs the SWOT Analysis Agent.  When comparison_entities is provided the
    agent produces a comparative SWOT focused on primary_entity.

    :param primary_entity: str - main subject (URL or company name)
    :param comparison_entities: list[str] | None - entities to compare against
    :param deps: SwotAgentDeps
    :return: SwotAnalysis | Exception
    """
    try:
        deps.tool_history = []

        if comparison_entities:
            comp_str = ", ".join(comparison_entities)
            prompt = (
                f"Perform a comparative SWOT analysis.\n"
                f"Primary entity: {primary_entity}\n"
                f"Compare against: {comp_str}\n\n"
                f"Research every entity with search_web. If any entity "
                f"looks like a URL, also call fetch_website_content on it.\n"
                f"The SWOT must centre on {primary_entity} but explicitly "
                f"contrast it with {comp_str} in each category.\n"
                f'Set primary_entity to "{primary_entity}" and '
                f"comparison_entities to {comparison_entities} in your output."
            )
        else:
            prompt = (
                f"Perform a comprehensive SWOT analysis for: "
                f"{primary_entity}\n"
                f"Use search_web to research this entity. If it is a URL, "
                f"also use fetch_website_content to gather details.\n"
                f'Set primary_entity to "{primary_entity}" and '
                f"comparison_entities to an empty list in your output."
            )

        result = await swot_agent.run(prompt, deps=deps)

        if deps.update_status_func:
            await deps.update_status_func(deps.request, "Analysis Complete")

        return result.data
    except Exception as e:
        logger.exception(f"Error during agent run: {type(e), e, e.args}")

        if deps.update_status_func:
            await deps.update_status_func(deps.request, f"Error: {e}")

        return e

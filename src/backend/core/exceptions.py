"""
Custom exceptions for SWOT analysis tools.

Provides structured error handling with clear error categorization.
"""


class ToolError(Exception):
    """Base exception for all tool errors."""

    def __init__(
        self, tool_name: str, message: str, original_error: Exception = None
    ):
        self.tool_name = tool_name
        self.message = message
        self.original_error = original_error
        super().__init__(f"[{tool_name}] {message}")


class NetworkError(ToolError):
    """Raised when network requests fail (timeouts, connection errors, etc.)."""

    pass


class APIError(ToolError):
    """Raised when external API calls fail (Tavily, Reddit, OpenAI, etc.)."""

    pass


class ValidationError(ToolError):
    """Raised when input validation fails."""

    pass


class ContentError(ToolError):
    """Raised when content processing fails (parsing, extraction, etc.)."""

    pass

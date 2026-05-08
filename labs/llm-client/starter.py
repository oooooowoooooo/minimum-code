"""LLM API Client Lab
Goal: Build a robust LLM client with timeout, retry, and error handling
"""
import requests
import time
from dataclasses import dataclass
from typing import Optional


class NetworkError(Exception):
    """Raised when network request fails (timeout, connection error)."""
    pass


class HTTPError(Exception):
    """Raised when server returns non-2xx status code."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"HTTP {status_code}: {message}")


class ParseError(Exception):
    """Raised when response is not valid JSON."""
    pass


class BusinessError(Exception):
    """Raised when API returns a business error code."""
    def __init__(self, code: int, message: str):
        self.code = code
        super().__init__(f"Business error {code}: {message}")


@dataclass
class LLMResponse:
    content: str
    model: str
    usage: dict


class LLMClient:
    def __init__(self, base_url: str, api_key: str, timeout: int = 30, max_retries: int = 3):
        """Initialize LLM client.

        Args:
            base_url: API base URL (e.g., "https://api.openai.com/v1")
            api_key: API key for authentication
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        # TODO: store these as instance attributes
        pass

    def chat(self, prompt: str, model: str = "gpt-3.5-turbo") -> LLMResponse:
        """Send a chat completion request.

        Should:
        1. Send POST to {base_url}/chat/completions
        2. Handle timeout -> raise NetworkError
        3. Handle connection errors -> raise NetworkError
        4. Check HTTP status code -> raise HTTPError if not 2xx
        5. Parse JSON response -> raise ParseError if invalid
        6. Check business 'error' field -> raise BusinessError if present
        7. On 5xx errors, retry up to max_retries times with exponential backoff
        8. Return LLMResponse on success

        Headers should include:
        - Content-Type: application/json
        - Authorization: Bearer {api_key}
        """
        # TODO: implement
        pass

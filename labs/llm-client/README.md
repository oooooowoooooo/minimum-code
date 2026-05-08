# Lab 2: LLM API Client

## Objective

Build a robust HTTP client for LLM APIs with proper error classification, timeout handling, and exponential backoff retry on server errors.

## Skills Practiced

- HTTP requests with the `requests` library
- Custom exception hierarchies
- Retry logic with exponential backoff
- Response parsing and validation
- Mocking for unit tests

## Getting Started

```bash
pip install requests pytest
```

1. Open `starter.py`
2. Implement `LLMClient.__init__` and `LLMClient.chat`
3. Run tests: `pytest test_llm_client.py -v`

## Error Hierarchy

| Exception | When |
|---|---|
| `NetworkError` | Timeout or connection failure |
| `HTTPError` | Non-2xx status code (stores `status_code`) |
| `ParseError` | Response body is not valid JSON |
| `BusinessError` | API returns `{"error": {...}}` (stores `code`) |

## Retry Behavior

- Only retry on 5xx server errors
- Use exponential backoff: `sleep(2 ** attempt)`
- Do NOT retry on 4xx, timeouts, or parse errors
- After exhausting retries, raise the last `HTTPError`

## Solution

See `solution.py` when you're ready to check your work.

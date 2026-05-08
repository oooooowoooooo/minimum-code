import requests
import time
from dataclasses import dataclass

class NetworkError(Exception): pass
class HTTPError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        super().__init__(f"HTTP {status_code}: {message}")
class ParseError(Exception): pass
class BusinessError(Exception):
    def __init__(self, code, message):
        self.code = code
        super().__init__(f"Business error {code}: {message}")

@dataclass
class LLMResponse:
    content: str
    model: str
    usage: dict

class LLMClient:
    def __init__(self, base_url, api_key, timeout=30, max_retries=3):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries

    def chat(self, prompt, model="gpt-3.5-turbo"):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        body = {"model": model, "messages": [{"role": "user", "content": prompt}]}

        last_error = None
        for attempt in range(self.max_retries):
            try:
                resp = requests.post(
                    f"{self.base_url}/chat/completions",
                    json=body, headers=headers, timeout=self.timeout
                )
            except requests.Timeout:
                raise NetworkError("Request timed out")
            except requests.ConnectionError:
                raise NetworkError("Connection failed")

            if resp.status_code >= 500:
                last_error = HTTPError(resp.status_code, resp.text)
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise last_error

            if resp.status_code < 200 or resp.status_code >= 300:
                raise HTTPError(resp.status_code, resp.text)

            try:
                data = resp.json()
            except (ValueError, KeyError):
                raise ParseError("Invalid JSON response")

            if "error" in data:
                err = data["error"]
                raise BusinessError(err.get("code", 0), err.get("message", "Unknown"))

            choice = data["choices"][0]["message"]["content"]
            return LLMResponse(
                content=choice,
                model=data.get("model", model),
                usage=data.get("usage", {})
            )

        raise last_error or NetworkError("Max retries exceeded")

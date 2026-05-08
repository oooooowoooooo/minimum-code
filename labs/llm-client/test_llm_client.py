import pytest
from starter import LLMClient, NetworkError, HTTPError, ParseError, BusinessError, LLMResponse


class FakeResponse:
    def __init__(self, status_code, text, json_data=None):
        self.status_code = status_code
        self.text = text
        self._json_data = json_data

    def json(self):
        if self._json_data is None:
            raise ValueError("No JSON")
        return self._json_data


class FakeRequests:
    """Mock requests.post for testing."""
    def __init__(self, responses):
        self.responses = list(responses)
        self.call_count = 0

    def post(self, *args, **kwargs):
        self.call_count += 1
        if not self.responses:
            raise RuntimeError("No more fake responses")
        resp = self.responses.pop(0)
        if isinstance(resp, Exception):
            raise resp
        return resp


def test_successful_chat(monkeypatch):
    """Successful API call returns LLMResponse."""
    fake = FakeRequests([
        FakeResponse(200, '{"choices":[{"message":{"content":"Hello!"}}],"model":"gpt-3.5","usage":{"total_tokens":10}}',
                     {"choices":[{"message":{"content":"Hello!"}}],"model":"gpt-3.5","usage":{"total_tokens":10}})
    ])
    monkeypatch.setattr("starter.requests", fake)

    client = LLMClient("http://fake.api/v1", "test-key", timeout=5, max_retries=1)
    resp = client.chat("Hi")
    assert isinstance(resp, LLMResponse)
    assert resp.content == "Hello!"
    assert resp.model == "gpt-3.5"


def test_timeout_raises_network_error(monkeypatch):
    """Timeout should raise NetworkError."""
    import requests as real_requests
    fake = FakeRequests([real_requests.Timeout("timed out")])
    monkeypatch.setattr("starter.requests", fake)

    client = LLMClient("http://fake.api/v1", "key", timeout=1, max_retries=1)
    with pytest.raises(NetworkError):
        client.chat("Hi")


def test_http_500_raises_http_error(monkeypatch):
    """HTTP 500 should raise HTTPError."""
    fake = FakeRequests([FakeResponse(500, "Internal Server Error")])
    monkeypatch.setattr("starter.requests", fake)

    client = LLMClient("http://fake.api/v1", "key", timeout=5, max_retries=1)
    with pytest.raises(HTTPError) as exc_info:
        client.chat("Hi")
    assert exc_info.value.status_code == 500


def test_invalid_json_raises_parse_error(monkeypatch):
    """Non-JSON response should raise ParseError."""
    fake = FakeRequests([FakeResponse(200, "not json at all", None)])
    monkeypatch.setattr("starter.requests", fake)

    client = LLMClient("http://fake.api/v1", "key", timeout=5, max_retries=1)
    with pytest.raises(ParseError):
        client.chat("Hi")


def test_business_error(monkeypatch):
    """API business error code should raise BusinessError."""
    fake = FakeRequests([
        FakeResponse(200, '{"error":{"code":429,"message":"rate limited"}}',
                     {"error":{"code":429,"message":"rate limited"}})
    ])
    monkeypatch.setattr("starter.requests", fake)

    client = LLMClient("http://fake.api/v1", "key", timeout=5, max_retries=1)
    with pytest.raises(BusinessError):
        client.chat("Hi")


def test_retry_on_500(monkeypatch):
    """Should retry on 5xx errors up to max_retries."""
    monkeypatch.setattr("starter.time", type("FakeTime", (), {"sleep": lambda s: None})())

    fake = FakeRequests([
        FakeResponse(500, "error"),
        FakeResponse(500, "error"),
        FakeResponse(200, '{"choices":[{"message":{"content":"ok"}}],"model":"m","usage":{}}',
                     {"choices":[{"message":{"content":"ok"}}],"model":"m","usage":{}})
    ])
    monkeypatch.setattr("starter.requests", fake)

    client = LLMClient("http://fake.api/v1", "key", timeout=5, max_retries=3)
    resp = client.chat("Hi")
    assert resp.content == "ok"
    assert fake.call_count == 3

import pytest
import os
from pathlib import Path


def test_settings_loads_from_env(monkeypatch):
    """Settings should load values from environment variables."""
    monkeypatch.setenv("API_KEY", "test-key-123")
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/test")
    monkeypatch.setenv("DEBUG", "true")

    from starter import Settings
    s = Settings()
    assert s.api_key == "test-key-123"
    assert s.database_url == "postgresql://localhost/test"
    assert s.debug is True


def test_settings_type_coercion(monkeypatch):
    """String 'true' should become bool True, '30' should become int 30."""
    monkeypatch.setenv("API_KEY", "key")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///test.db")
    monkeypatch.setenv("DEBUG", "false")
    monkeypatch.setenv("MAX_RETRIES", "5")
    monkeypatch.setenv("TIMEOUT", "15.5")

    from starter import Settings
    s = Settings()
    assert s.debug is False
    assert s.max_retries == 5
    assert isinstance(s.max_retries, int)
    assert s.timeout == 15.5
    assert isinstance(s.timeout, float)


def test_settings_defaults(monkeypatch):
    """Optional fields should use defaults when env var is missing."""
    monkeypatch.setenv("API_KEY", "key")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///test.db")

    from starter import Settings
    s = Settings()
    assert s.debug is False
    assert s.log_level == "INFO"
    assert s.max_retries == 3
    assert s.timeout == 30.0


def test_settings_missing_required(monkeypatch):
    """Missing required fields should raise ValidationError."""
    monkeypatch.delenv("API_KEY", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    from starter import Settings
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        Settings()


def test_get_settings_singleton(monkeypatch):
    """get_settings should return the same instance on repeated calls."""
    monkeypatch.setenv("API_KEY", "key")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///test.db")

    from starter import get_settings
    s1 = get_settings()
    s2 = get_settings()
    assert s1 is s2

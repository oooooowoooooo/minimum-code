import pytest
from pathlib import Path


def test_dockerfile_exists():
    """Dockerfile should exist."""
    dockerfile = Path(__file__).parent / "Dockerfile"
    assert dockerfile.exists(), "Dockerfile not found"


def test_dockerfile_multistage():
    """Dockerfile should use multi-stage build."""
    content = Path(__file__).parent / "Dockerfile"
    text = content.read_text()
    assert "FROM" in text
    # Should have at least 2 FROM statements
    from_count = text.count("FROM ")
    assert from_count >= 2, f"Expected multi-stage build (2+ FROM), found {from_count}"


def test_dockerfile_uses_slim():
    """Final stage should use slim image."""
    text = (Path(__file__).parent / "Dockerfile").read_text()
    assert "slim" in text.lower()


def test_dockerfile_exposes_port():
    """Dockerfile should expose port 8000."""
    text = (Path(__file__).parent / "Dockerfile").read_text()
    assert "EXPOSE" in text
    assert "8000" in text


def test_ci_workflow_exists():
    """CI workflow should exist."""
    workflow = Path(__file__).parent / ".github" / "workflows" / "ci.yml"
    assert workflow.exists(), "CI workflow not found"


def test_ci_runs_tests():
    """CI workflow should run tests."""
    text = (Path(__file__).parent / ".github" / "workflows" / "ci.yml").read_text()
    assert "pytest" in text.lower() or "test" in text.lower()


def test_ci_builds_docker():
    """CI workflow should build Docker image."""
    text = (Path(__file__).parent / ".github" / "workflows" / "ci.yml").read_text()
    assert "docker" in text.lower()

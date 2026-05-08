# Lab 6: Docker & CI

## Objective

Write a multi-stage Dockerfile for a FastAPI application and a GitHub Actions CI workflow that runs tests and builds/verifies the Docker image.

## Skills Practiced

- Multi-stage Docker builds for smaller images
- Docker layer caching with requirements.txt
- GitHub Actions workflow syntax
- CI/CD pipeline design
- Container health verification

## Getting Started

1. Open `Dockerfile` and implement a multi-stage build
2. Open `.github/workflows/ci.yml` and implement the CI pipeline
3. Run tests: `pytest test_docker_ci.py -v`

## Dockerfile Requirements

- **Stage 1 (builder):** Install Python dependencies into an isolated prefix
- **Stage 2 (runtime):** Copy only installed packages and app code (no build tools)
- Use `python:3.11-slim` for both stages
- Expose port 8000
- Run with `uvicorn main:app --host 0.0.0.0 --port 8000`

## CI Workflow Requirements

- Trigger on push to `main` and pull requests to `main`
- **Job 1: test** -- setup Python 3.11, install deps, run pytest
- **Job 2: docker** -- build image, start container, verify it responds on `/docs`
- Docker job depends on test job passing first

## Solution

See `solution/Dockerfile` and `solution/.github/workflows/ci.yml` when you're ready.

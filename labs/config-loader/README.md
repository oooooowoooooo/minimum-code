# Lab 1: Config Loader

## Objective
Build a typed configuration loader using `pydantic-settings` that reads from environment variables and `.env` files.

## Skills Practiced
- Pydantic models and validation
- Environment variable parsing
- Type coercion (string → bool, int, float)
- Singleton pattern
- pytest with monkeypatch

## Getting Started
```bash
pip install pydantic-settings pytest
cd labs/config-loader
pytest test_config_loader.py -v
```

## Tasks
1. Open `starter.py`
2. Define the `Settings` class with the required fields (see docstring)
3. Run tests and make them pass
4. Compare with `solution.py` when done

## Field Reference
| Field | Type | Default | Required |
|-------|------|---------|----------|
| `api_key` | `str` | — | Yes |
| `database_url` | `str` | — | Yes |
| `debug` | `bool` | `False` | No |
| `log_level` | `str` | `"INFO"` | No |
| `max_retries` | `int` | `3` | No |
| `timeout` | `float` | `30.0` | No |

## Key Concepts
- `BaseSettings` from `pydantic-settings` automatically reads environment variables
- Field names are case-insensitive when matching env vars
- Type annotations drive automatic coercion
- Use `class Config: env_file = ".env"` to also read from `.env` files

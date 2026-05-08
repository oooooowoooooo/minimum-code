# FastAPI Internals Dissection

## What Is FastAPI?

FastAPI is a modern, high-performance Python web framework for building APIs. It is built on top of **Starlette** (for the ASGI web parts) and **Pydantic** (for data validation). Since its first release in 2018 by Sebastian Ramirez, it has grown to **80,000+ GitHub stars** and has become the de facto standard for building production Python APIs.

Why it matters:

- **Performance**: On par with Node.js and Go thanks to ASGI and async/await
- **Developer experience**: Type hints drive validation, serialization, and documentation simultaneously
- **Standards-based**: Built on OpenAPI and JSON Schema
- **Auto-documentation**: Interactive Swagger UI and ReDoc generated from your code

## Architecture Overview

```
+------------------------------------------------------------------+
|                         Client Request                           |
+------------------------------------------------------------------+
           |
           v
+------------------+
|    ASGI Server   |  (Uvicorn / Hypercorn)
|   (uvicorn.run)  |
+------------------+
           |
           v
+------------------------------------------------------------------+
|                         FastAPI App                              |
|                                                                  |
|  +--------------------+    +----------------------------------+  |
|  |   Middleware Stack  |    |        Router                    |  |
|  |  (CORS, GZip, etc) |    |                                  |  |
|  +--------------------+    |  /users/{id}  -->  endpoint()    |  |
|           |                |  /items/      -->  list_items()  |  |
|           v                |  /auth/login  -->  login()       |  |
|  +--------------------+    +----------------------------------+  |
|  |   Request Object   |              |                          |  |
|  +--------------------+              v                          |
|           |                +----------------------------------+  |
|           v                |    Dependency Injection           |  |
|  +--------------------+    |                                   |  |
|  |  Path/Query/Body   |    |  Depends(get_db) -> db_session   |  |
|  |   Parameter        |    |  Depends(get_user) -> current    |  |
|  |   Extraction       |    +----------------------------------+  |
|  +--------------------+              |                          |
|           |                          v                          |
|           v                +----------------------------------+  |
|  +--------------------+    |   Pydantic Validation            |  |
|  |  Route Handler     |<-->|  (type checking, serialization)  |  |
|  |  (your function)   |    +----------------------------------+  |
|  +--------------------+              |                          |
|           |                          v                          |
|           v                +----------------------------------+  |
|  +--------------------+    |   Response Model                 |  |
|  |   Response Object  |    |   (JSON serialization)           |  |
|  +--------------------+    +----------------------------------+  |
+------------------------------------------------------------------+
           |
           v
+------------------------------------------------------------------+
|                       ASGI Response                              |
+------------------------------------------------------------------+
```

## Key Design Decisions

### 1. Type Hints as the Source of Truth

FastAPI uses Python type hints not just for documentation, but as the **runtime contract** for your API. When you write:

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int, q: str | None = None):
    ...
```

FastAPI reads the type hints at startup and:
- Generates OpenAPI schema
- Creates Pydantic validation models
- Builds interactive docs
- Validates incoming requests at runtime

### 2. Dependency Injection Over Middleware

Instead of a global middleware for auth, database connections, etc., FastAPI uses a fine-grained DI system. Dependencies can be nested, cached per-request, and scoped.

### 3. Async-First, Sync-Compatible

FastAPI runs on ASGI. Endpoint functions can be `async def` or regular `def`. Regular `def` functions are run in a threadpool automatically, so blocking code does not freeze the event loop.

### 4. Composition Over Inheritance

FastAPI uses `APIRouter` for modular composition rather than class-based inheritance. This keeps code flat and testable.

## Learning Objectives

After completing this dissection, you will understand:

1. How decorator-based route registration works internally
2. How dependency injection resolves and caches dependencies
3. How middleware chains execute in order (and reverse order for responses)
4. How Pydantic models validate data at the boundary
5. How ASGI apps receive and produce HTTP messages
6. How to build a minimal but functional web framework from scratch

## Prerequisites

- Python 3.10+ (type hints with `|` syntax)
- Understanding of decorators and closures
- Basic knowledge of HTTP (methods, status codes, headers)
- Familiarity with `async`/`await` (helpful but not required)

## How to Use This Module

1. Read `README.md` for the big picture
2. Study `patterns.md` for design pattern analysis
3. Run and modify `dissect.py` for hands-on understanding

```bash
cd src/python/dissect/fastapi
python dissect.py
```

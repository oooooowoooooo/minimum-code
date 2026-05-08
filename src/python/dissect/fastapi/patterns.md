# FastAPI Design Patterns

## Pattern 1: Dependency Injection

### What It Is

Instead of importing and calling dependencies directly, you **declare** what you need as function parameters. The framework resolves and injects them at runtime.

### Why FastAPI Uses It

- **Testability**: Swap dependencies in tests without monkey-patching
- **Reusability**: A database session dependency can be shared across endpoints
- **Composability**: Dependencies can depend on other dependencies (a dependency tree)
- **Scoping**: Control lifetime (per-request, singleton, etc.)

### How It Works Internally

1. You wrap a callable in `Depends()`:
   ```python
   def get_db():
       db = SessionLocal()
       try:
           yield db
       finally:
           db.close()

   @app.get("/items/")
   async def read_items(db = Depends(get_db)):
       return db.query(Item).all()
   ```

2. At startup, FastAPI inspects the endpoint's signature via `inspect.signature()`
3. For each parameter with `Depends()`, it resolves the dependency callable
4. If the dependency is a generator (uses `yield`), the setup runs before the endpoint, and cleanup runs after the response
5. Results are cached per-request: if two dependencies both depend on `get_db`, the database session is created only once

### Internal Flow

```
Request arrives
    |
    v
Resolve endpoint signature
    |
    v
For each Depends() parameter:
    +-> Check if already resolved (request-scoped cache)
    +-> If not, recursively resolve sub-dependencies
    +-> Call the dependency
    +-> If generator: pause at yield, store cleanup
    +-> Cache the result
    |
    v
Call endpoint with resolved values
    |
    v
Generate response
    |
    v
Run cleanup functions in reverse order (finally blocks)
```

---

## Pattern 2: Middleware Chain

### What It Is

Middleware wraps the entire request-response cycle. Each middleware can inspect/modify the request before it reaches the endpoint, and inspect/modify the response on the way out.

### Why FastAPI Uses It

- **Cross-cutting concerns**: Logging, CORS, authentication, rate limiting
- **Ordering control**: Middleware executes in registration order for requests, reverse for responses
- **Composability**: Add/remove middleware without touching endpoints

### How It Works Internally

FastAPI middleware is Starlette middleware. Under the hood, it implements the ASGI protocol:

```python
async def middleware(scope, receive, send):
    # Before the endpoint
    response = await call_next(request)
    # After the endpoint
    return response
```

Each middleware wraps the next one, forming a chain (like Russian nesting dolls). The innermost layer is the actual route handler.

### Internal Flow

```
Request: middleware1 -> middleware2 -> middleware3 -> endpoint
Response: endpoint -> middleware3 -> middleware2 -> middleware1
```

This is the classic "onion model" or "chain of responsibility" pattern.

### Key Insight

Middleware in FastAPI is NOT the same as middleware in Django/Express. FastAPI middleware operates at the ASGI level (`scope`, `receive`, `send`), which gives it lower-level access but requires understanding the ASGI protocol.

---

## Pattern 3: Lifecycle Management (Startup/Shutdown Events)

### What It Is

FastAPI provides `lifespan` context managers that run code during application startup and shutdown. This is used for initializing resources (database pools, ML models, caches) and cleaning them up.

### Why FastAPI Uses It

- **Resource management**: Database connections, thread pools, and file handles need explicit setup/teardown
- **Graceful shutdown**: Ensure in-flight requests complete before the server stops
- **Health checks**: Verify external dependencies before accepting traffic

### How It Works Internally

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    # Startup
    app.state.db_pool = await create_pool()
    yield
    # Shutdown
    await app.state.db_pool.close()

app = FastAPI(lifespan=lifespan)
```

The ASGI server calls `__aenter__` when the application starts and `__aexit__` when it shuts down. This integrates cleanly with Python's context manager protocol.

### Design Decision

FastAPI moved from `@app.on_event("startup")` decorators to the `lifespan` pattern because:
- A single context manager makes the lifecycle explicit and linear
- Generator-based cleanup (`try/finally` or `yield`) guarantees execution order
- It composes better (you can merge multiple lifespans)

---

## Pattern 4: Path Operations (Decorator-Based Routing)

### What It Is

Decorators like `@app.get("/path")` register functions as route handlers. FastAPI collects these at startup and builds a routing table.

### Why FastAPI Uses It

- **Declarative**: The route is defined right next to the handler
- **Type-driven**: The decorator triggers type hint inspection
- **Discoverable**: The OpenAPI schema is generated from these declarations

### How It Works Internally

1. `@app.get("/users/{user_id}")` calls `app.router.add_api_route()`
2. The route is stored in a trie-like structure for efficient path matching
3. Path parameters like `{user_id}` are extracted via regex matching
4. At request time, the router matches the URL, extracts parameters, and calls the handler

### Path Matching Algorithm

```
Routes:
  /users/{user_id}/posts
  /users/{user_id}/profile
  /items/

Request: GET /users/42/posts

Step 1: Split path into segments: ["users", "42", "posts"]
Step 2: Match static segments first: "users" matches
Step 3: Extract parameter: user_id = 42
Step 4: Match remaining: "posts" matches
Step 5: Return matched route + extracted parameters
```

---

## Pattern 5: Pydantic Models (Boundary Validation)

### What It Is

Pydantic models define the shape of data entering and leaving your API. FastAPI uses them as **boundary validators** -- all external data is validated and converted at the API boundary, and clean Python objects flow through the rest of the system.

### Why FastAPI Uses It

- **Single source of truth**: The model defines validation, serialization, and documentation
- **Fail fast**: Invalid data is rejected before it reaches business logic
- **Type safety**: After validation, you have typed objects, not raw dicts
- **Auto-conversion**: Strings from query params are converted to ints, dates, etc.

### How It Works Internally

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    age: int = 0  # default value

@app.post("/users/")
async def create_user(user: UserCreate):
    # `user` is already validated here
    return {"name": user.name}
```

At startup:
1. FastAPI inspects the endpoint signature
2. Parameters annotated with a `BaseModel` subclass are treated as request bodies
3. A JSON Schema is generated from the model for OpenAPI docs
4. At request time, the JSON body is parsed and passed through Pydantic's validation

### Pydantic Validation Pipeline

```
Raw JSON body (dict)
    |
    v
Field-level validation:
    +-> Type coercion (str "42" -> int 42 if field is int)
    +-> Constraint checks (min_length, max_value, regex)
    +-> Custom validators (@field_validator)
    |
    v
Model-level validation:
    +-> @model_validator (cross-field checks)
    |
    v
Clean Pydantic model instance (typed, validated)
    |
    v
Passed to endpoint function
```

---

## Pattern Summary

| Pattern | Where Used | Core Mechanism |
|---------|-----------|----------------|
| Dependency Injection | Endpoint parameters | `inspect.signature()` + callable resolution |
| Middleware Chain | Request/response lifecycle | ASGI protocol, onion model |
| Lifecycle Management | App startup/shutdown | `asynccontextmanager` + `yield` |
| Path Operations | Route registration | Decorators + trie-based path matching |
| Pydantic Models | Data boundaries | Schema-driven validation + type coercion |

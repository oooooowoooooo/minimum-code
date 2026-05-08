"""
FastAPI Internals: Atomic Code Dissection

This file rebuilds the core mechanisms of FastAPI from scratch.
Each section is self-contained with detailed comments and inline tests.

Run: python dissect.py
"""

import inspect
import re
import json
from typing import Any, Callable, get_type_hints
from dataclasses import dataclass, field
from collections import defaultdict


# =============================================================================
# SECTION 1: Router -- Decorator-Based Route Registration
# =============================================================================
#
# FastAPI's @app.get("/path") decorator registers a function as a route handler.
# Internally, it stores routes in a list and matches them at request time.
# =============================================================================


@dataclass
class Route:
    """Represents a registered API route."""
    path: str
    method: str
    endpoint: Callable
    # Compiled regex for path matching (e.g., /users/{id} -> /users/(?P<id>[^/]+))
    path_regex: re.Pattern = field(init=False)
    # Names of path parameters extracted from the pattern
    path_param_names: list[str] = field(init=False, default_factory=list)

    def __post_init__(post_self):
        self = post_self
        # Convert path template to regex: {param} -> (?P<param>[^/]+)
        pattern = re.sub(r"\{(\w+)\}", r"(?P<\1>[^/]+)", self.path)
        self.path_regex = re.compile(f"^{pattern}$")
        # Extract parameter names
        self.path_param_names = re.findall(r"\{(\w+)\}", self.path)

    def match(self, path: str) -> dict[str, str] | None:
        """Try to match a request path. Returns extracted params or None."""
        m = self.path_regex.match(path)
        if m:
            return m.groupdict()
        return None


class Router:
    """
    Simplified version of FastAPI's router.

    Design decisions:
    - Decorator-based registration: @router.get("/path") is intuitive and declarative
    - Methods stored as a list of Route objects, not a dict, because we need
      regex matching (dict keys must be exact strings)
    - Path parameters extracted via regex for O(n) matching
    """

    def __init__(self):
        self.routes: list[Route] = []

    def _add_route(self, path: str, method: str, endpoint: Callable):
        route = Route(path=path.upper(), method=method.upper(), endpoint=endpoint)
        self.routes.append(route)
        return endpoint

    def get(self, path: str):
        """Decorator: register a GET endpoint."""
        def decorator(func: Callable):
            self._add_route(path, "GET", func)
            return func
        return decorator

    def post(self, path: str):
        """Decorator: register a POST endpoint."""
        def decorator(func: Callable):
            self._add_route(path, "POST", func)
            return func
        return decorator

    def resolve(self, method: str, path: str) -> tuple[Callable, dict] | None:
        """
        Match an incoming request to a registered route.

        Returns (endpoint_function, path_params) or None if no match.
        """
        method = method.upper()
        path = path.upper()
        for route in self.routes:
            if route.method == method:
                params = route.match(path)
                if params is not None:
                    return route.endpoint, params
        return None


def test_router():
    """Test: Router registers and resolves routes correctly."""
    router = Router()

    @router.get("/users/{user_id}")
    def get_user(user_id: int):
        return {"user_id": user_id}

    @router.get("/items/")
    def list_items():
        return []

    @router.post("/items/")
    def create_item():
        return {"created": True}

    # Test exact match
    result = router.resolve("GET", "/items/")
    assert result is not None
    func, params = result
    assert func.__name__ == "list_items"
    assert params == {}

    # Test path parameter extraction
    result = router.resolve("GET", "/users/42")
    assert result is not None
    func, params = result
    assert func.__name__ == "get_user"
    assert params == {"user_id": "42"}

    # Test method mismatch
    result = router.resolve("DELETE", "/items/")
    assert result is None

    # Test no match
    result = router.resolve("GET", "/nonexistent")
    assert result is None

    print("[PASS] Router: route registration and resolution")


# =============================================================================
# SECTION 2: Dependency Injection
# =============================================================================
#
# FastAPI's DI system inspects function signatures, finds Depends() markers,
# resolves the dependency callables, and injects the results.
# Key insight: dependencies can be nested (a dependency can have its own deps).
# =============================================================================


class Depends:
    """
    Marker class that tells FastAPI: "call this function and inject the result".

    Design decision: Uses a wrapper class rather than a bare function reference
    so FastAPI can distinguish DI parameters from regular parameters at
    inspection time.
    """

    def __init__(self, dependency: Callable, use_cache: bool = True):
        self.dependency = dependency
        self.use_cache = use_cache


class DIContainer:
    """
    Simplified dependency injection container.

    How it works:
    1. Inspect the target function's signature
    2. For each parameter with Depends() as default, resolve recursively
    3. Cache results per-request (same dep called once, not twice)
    4. Support generator dependencies (yield = cleanup after response)

    Design decisions:
    - Request-scoped cache prevents duplicate instantiation
    - Generator deps use try/finally for cleanup (like FastAPI's yield deps)
    - Resolution is recursive: deps can depend on other deps
    """

    def __init__(self):
        self._cleanup_funcs: list[Callable] = []

    def resolve(self, func: Callable, overrides: dict | None = None) -> dict[str, Any]:
        """
        Resolve all dependencies for a function and return keyword arguments.

        Args:
            func: The function whose dependencies to resolve
            overrides: Dict of dependency overrides (for testing)

        Returns:
            Dict of resolved keyword arguments
        """
        overrides = overrides or {}
        sig = inspect.signature(func)
        kwargs = {}
        cache: dict[int, Any] = {}  # id(dependency) -> resolved value

        for param_name, param in sig.parameters.items():
            default = param.default

            if isinstance(default, Depends):
                dep = default.dependency

                # Check overrides first (useful for testing)
                if dep in overrides:
                    kwargs[param_name] = overrides[dep]
                    continue

                # Check cache (per-request deduplication)
                dep_id = id(dep)
                if default.use_cache and dep_id in cache:
                    kwargs[param_name] = cache[dep_id]
                    continue

                # Recursively resolve sub-dependencies
                sub_kwargs = self.resolve(dep, overrides)

                # Check if it's a generator dependency (yield-based cleanup)
                if inspect.isgeneratorfunction(dep):
                    gen = dep(**sub_kwargs)
                    value = next(gen)  # Run until yield
                    # Register cleanup to run after the request
                    self._cleanup_funcs.append(lambda g=gen: _run_generator_cleanup(g))
                    cache[dep_id] = value
                    kwargs[param_name] = value
                else:
                    result = dep(**sub_kwargs)
                    cache[dep_id] = result
                    kwargs[param_name] = result

            elif param.default is not inspect.Parameter.empty:
                # Regular parameter with default -- use the default
                kwargs[param_name] = param.default

        return kwargs

    def run_cleanup(self):
        """Run all cleanup functions in reverse order (LIFO)."""
        for cleanup_func in reversed(self._cleanup_funcs):
            cleanup_func()
        self._cleanup_funcs.clear()


def _run_generator_cleanup(gen):
    """Run the remaining part of a generator (after yield)."""
    try:
        next(gen)
    except StopIteration:
        pass


def test_dependency_injection():
    """Test: DI resolves dependencies, caches results, handles generators."""

    # --- Simple dependency ---
    def get_config():
        return {"db_url": "sqlite:///test.db", "debug": True}

    # --- Dependency that depends on another dependency ---
    def get_db(config: dict = Depends(get_config)):
        return {"connection": config["db_url"], "active": True}

    # --- Generator dependency (yield-based cleanup) ---
    cleanup_called = False

    def get_session():
        nonlocal cleanup_called
        session = {"id": "session_123", "data": []}
        yield session  # The "setup" value
        cleanup_called = True  # This runs after the request

    # --- Endpoint that uses all the above ---
    def endpoint(config: dict = Depends(get_config), db: dict = Depends(get_db),
                 session: dict = Depends(get_session)):
        return {"config": config, "db": db, "session": session}

    container = DIContainer()
    kwargs = container.resolve(endpoint)
    result = endpoint(**kwargs)

    assert result["config"]["db_url"] == "sqlite:///test.db"
    assert result["db"]["connection"] == "sqlite:///test.db"
    assert result["session"]["id"] == "session_123"

    # Verify cache: get_config should only be called once
    # (we can verify this by checking the same object is returned)
    kwargs2 = container.resolve(endpoint)
    assert kwargs2["config"] is kwargs["config"]  # Same object = cached

    # Run cleanup and verify generator cleanup executed
    container.run_cleanup()
    assert cleanup_called

    print("[PASS] Dependency Injection: resolution, caching, generator cleanup")


# =============================================================================
# SECTION 3: Middleware Chain
# =============================================================================
#
# Middleware wraps the request-response cycle. Each middleware can:
# - Modify the request before passing it down
# - Modify the response after getting it back
# - Short-circuit (return early without calling the next middleware)
#
# The chain is built at startup time by nesting middleware wrappers.
# =============================================================================


class MiddlewareChain:
    """
    Simplified middleware chain implementing the onion model.

    Design decisions:
    - Middleware is a callable that receives (request, next_handler) -> response
    - Chain is built by wrapping: each middleware wraps the previous one
    - This mirrors how Starlette/FastAPI actually works at the ASGI level

    Internal flow:
        Request:  middleware_1 -> middleware_2 -> middleware_3 -> actual_handler
        Response: actual_handler -> middleware_3 -> middleware_2 -> middleware_1
    """

    def __init__(self, handler: Callable):
        # The core handler (endpoint) is the innermost layer
        self._handler = handler
        self._middlewares: list[Callable] = []

    def add_middleware(self, middleware: Callable):
        """
        Register a middleware function.

        Args:
            middleware: Callable(request, next_handler) -> response
        """
        self._middlewares.append(middleware)

    def execute(self, request: dict) -> dict:
        """
        Build the middleware chain and execute it.

        We build the chain from inside out:
        - Start with the actual handler
        - Wrap it with each middleware in reverse order

        This means the LAST added middleware is the outermost (runs first).
        """
        chain = self._handler

        # Build chain from inside out
        for mw in reversed(self._middlewares):
            chain = _wrap_middleware(mw, chain)

        return chain(request)


def _wrap_middleware(middleware, next_handler):
    """Create a closure that wraps next_handler with middleware."""
    def wrapped(request):
        return middleware(request, next_handler)
    return wrapped


def test_middleware_chain():
    """Test: Middleware chain executes in correct order with logging."""
    execution_log = []

    # The actual endpoint handler
    def endpoint(request):
        execution_log.append("endpoint")
        return {"status": 200, "body": "hello", "headers": {}}

    # Middleware 1: Logging (runs first/last)
    def logging_middleware(request, next_handler):
        execution_log.append("logging_before")
        response = next_handler(request)
        execution_log.append("logging_after")
        response["headers"]["X-Request-Id"] = "abc123"
        return response

    # Middleware 2: Authentication (runs second)
    def auth_middleware(request, next_handler):
        execution_log.append("auth_before")
        if not request.get("headers", {}).get("Authorization"):
            execution_log.append("auth_blocked")
            return {"status": 401, "body": "Unauthorized", "headers": {}}
        response = next_handler(request)
        execution_log.append("auth_after")
        return response

    # Middleware 3: CORS (runs third, closest to endpoint)
    def cors_middleware(request, next_handler):
        execution_log.append("cors_before")
        response = next_handler(request)
        execution_log.append("cors_after")
        response["headers"]["Access-Control-Allow-Origin"] = "*"
        return response

    chain = MiddlewareChain(endpoint)
    chain.add_middleware(logging_middleware)
    chain.add_middleware(auth_middleware)
    chain.add_middleware(cors_middleware)

    # Test 1: Request with auth passes through
    execution_log.clear()
    request = {"path": "/users", "headers": {"Authorization": "Bearer token123"}}
    response = chain.execute(request)

    assert response["status"] == 200
    assert response["headers"]["X-Request-Id"] == "abc123"
    assert response["headers"]["Access-Control-Allow-Origin"] == "*"

    # Verify onion execution order
    assert execution_log == [
        "logging_before", "auth_before", "cors_before",
        "endpoint",
        "cors_after", "auth_after", "logging_after",
    ]

    # Test 2: Request without auth is blocked
    execution_log.clear()
    request = {"path": "/users", "headers": {}}
    response = chain.execute(request)

    assert response["status"] == 401
    assert "auth_blocked" in execution_log

    print("[PASS] Middleware Chain: onion model, ordering, short-circuit")


# =============================================================================
# SECTION 4: Pydantic-Like Validation
# =============================================================================
#
# Pydantic models validate data at the API boundary. This section implements
# a simplified version that shows the core concepts:
# - Type checking at runtime
# - Automatic type coercion (str -> int where appropriate)
# - Field-level constraints
# - Model-level validation
# =============================================================================


class ValidationError(Exception):
    """Raised when validation fails. Mirrors Pydantic's ValidationError."""

    def __init__(self, errors: list[dict]):
        self.errors = errors
        super().__init__(json.dumps(errors, indent=2))


class Field:
    """
    Describes a single field in a model.

    Design decisions:
    - Stores type, default, and constraints in one place
    - validate() returns the coerced value or raises ValidationError
    - This mirrors Pydantic's field_info + field_validator approach
    """

    def __init__(self, field_type: type, default: Any = inspect.Parameter.empty,
                 min_value: int | float | None = None,
                 max_value: int | float | None = None,
                 min_length: int | None = None,
                 max_length: int | None = None):
        self.field_type = field_type
        self.default = default
        self.min_value = min_value
        self.max_value = max_value
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, name: str, value: Any) -> Any:
        """Validate and coerce a single field value."""
        errors = []

        # Handle missing values
        if value is inspect.Parameter.empty or value is None:
            if self.default is not inspect.Parameter.empty:
                return self.default
            if value is None:
                return None
            errors.append({"field": name, "msg": "field required"})
            raise ValidationError(errors)

        # Type coercion
        try:
            if self.field_type is int and isinstance(value, str):
                value = int(value)
            elif self.field_type is float and isinstance(value, (str, int)):
                value = float(value)
            elif self.field_type is str:
                value = str(value)
        except (ValueError, TypeError):
            errors.append({"field": name, "msg": f"could not convert to {self.field_type.__name__}"})
            raise ValidationError(errors)

        # Type check
        if not isinstance(value, self.field_type):
            errors.append({"field": name, "msg": f"expected {self.field_type.__name__}, got {type(value).__name__}"})
            raise ValidationError(errors)

        # Numeric constraints
        if self.min_value is not None and value < self.min_value:
            errors.append({"field": name, "msg": f"value {value} < minimum {self.min_value}"})
        if self.max_value is not None and value > self.max_value:
            errors.append({"field": name, "msg": f"value {value} > maximum {self.max_value}"})

        # String length constraints
        if self.min_length is not None and len(value) < self.min_length:
            errors.append({"field": name, "msg": f"length {len(value)} < minimum {self.min_length}"})
        if self.max_length is not None and len(value) > self.max_length:
            errors.append({"field": name, "msg": f"length {len(value)} > maximum {self.max_length}"})

        if errors:
            raise ValidationError(errors)

        return value


class ModelMeta(type):
    """
    Metaclass that collects Field descriptors from the class definition.

    This is how Pydantic discovers your field definitions at class creation time.
    Without a metaclass, we'd have to scan the class manually after creation.
    """

    def __new__(mcs, name, bases, namespace):
        fields = {}
        for key, value in namespace.items():
            if isinstance(value, Field):
                fields[key] = value
        namespace["_fields"] = fields
        return super().__new__(mcs, name, bases, namespace)


class Model(metaclass=ModelMeta):
    """
    Simplified Pydantic BaseModel.

    Validates incoming data (usually JSON) against the model's field definitions.
    Returns clean, typed Python objects.

    Design decisions:
    - __init__ accepts a dict (like Pydantic's model(**data) pattern)
    - Validation happens at construction time (fail fast)
    - Validated data stored as instance attributes
    - Model instances are immutable by convention (like Pydantic)
    """

    def __init__(self, data: dict | None = None, **kwargs):
        data = data or {}
        data.update(kwargs)
        errors = []

        for field_name, field_obj in self._fields.items():
            value = data.get(field_name, inspect.Parameter.empty)
            try:
                validated = field_obj.validate(field_name, value)
                setattr(self, field_name, validated)
            except ValidationError as e:
                errors.extend(e.errors)

        if errors:
            raise ValidationError(errors)

    def dict(self) -> dict:
        """Serialize model to dict (like Pydantic's .model_dump())."""
        return {name: getattr(self, name) for name in self._fields}

    def __repr__(self):
        fields = ", ".join(f"{k}={getattr(self, k)!r}" for k in self._fields)
        return f"{self.__class__.__name__}({fields})"


def test_pydantic_validation():
    """Test: Model validation, type coercion, and constraints."""

    class UserCreate(Model):
        name = Field(str, min_length=1, max_length=50)
        email = Field(str, min_length=5)
        age = Field(int, default=0, min_value=0, max_value=150)

    # Test 1: Valid data
    user = UserCreate({"name": "Alice", "email": "alice@example.com", "age": "30"})
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert user.age == 30  # coerced from str "30" to int 30
    assert user.dict() == {"name": "Alice", "email": "alice@example.com", "age": 30}

    # Test 2: Default values
    user = UserCreate({"name": "Bob", "email": "bob@example.com"})
    assert user.age == 0

    # Test 3: Validation failure -- name too short
    try:
        UserCreate({"name": "", "email": "test@test.com"})
        assert False, "Should have raised ValidationError"
    except ValidationError as e:
        assert any("minimum" in err["msg"] for err in e.errors)

    # Test 4: Validation failure -- age out of range
    try:
        UserCreate({"name": "Eve", "email": "eve@test.com", "age": 200})
        assert False, "Should have raised ValidationError"
    except ValidationError as e:
        assert any("maximum" in err["msg"] for err in e.errors)

    # Test 5: Missing required field
    try:
        UserCreate({"name": "Charlie"})
        assert False, "Should have raised ValidationError"
    except ValidationError as e:
        assert any("required" in err["msg"] for err in e.errors)

    print("[PASS] Pydantic-like Validation: type coercion, constraints, error reporting")


# =============================================================================
# SECTION 5: Request/Response Lifecycle
# =============================================================================
#
# This section ties everything together into a simplified but complete
# request-response lifecycle that mirrors how FastAPI actually works:
#
#   Request -> Router -> Dependency Resolution -> Validation -> Handler -> Response
# =============================================================================


class Request:
    """Simplified HTTP request object."""

    def __init__(self, method: str, path: str, headers: dict | None = None,
                 body: dict | None = None, query: dict | None = None):
        self.method = method
        self.path = path
        self.headers = headers or {}
        self.body = body or {}
        self.query = query or {}


class Response:
    """Simplified HTTP response object."""

    def __init__(self, status: int = 200, body: Any = None, headers: dict | None = None):
        self.status = status
        self.body = body
        self.headers = headers or {}

    def dict(self) -> dict:
        return {"status": self.status, "body": self.body, "headers": self.headers}


class App:
    """
    Simplified FastAPI application.

    Ties together Router, DI, Validation, and Middleware into a single
    request processing pipeline.

    Processing pipeline:
    1. Router matches the request to an endpoint
    2. DI resolves dependencies for the endpoint
    3. Path parameters and query params are extracted
    4. The endpoint is called with resolved arguments
    5. The result is serialized to a Response

    Design decisions:
    - Middleware wraps the entire pipeline (like FastAPI/Starlette)
    - Dependencies are resolved per-request (new DI container each time)
    - Error handling produces proper HTTP status codes
    """

    def __init__(self):
        self.router = Router()
        self._di_container_factory = DIContainer  # Factory for per-request containers

    def get(self, path: str):
        return self.router.get(path)

    def post(self, path: str):
        return self.router.post(path)

    def handle_request(self, request: Request) -> Response:
        """
        Process a request through the full pipeline.

        This is the simplified equivalent of FastAPI's ASGI __call__ method.
        """
        # Step 1: Route resolution
        result = self.router.resolve(request.method, request.path)
        if result is None:
            return Response(status=404, body={"error": "Not Found"})

        endpoint, path_params = result

        # Step 2: Dependency injection
        di = self._di_container_factory()
        try:
            kwargs = di.resolve(endpoint)
        except Exception as e:
            return Response(status=500, body={"error": f"DI Error: {e}"})

        # Step 3: Merge path params and query params into kwargs
        sig = inspect.signature(endpoint)
        for param_name in sig.parameters:
            if param_name in path_params:
                # Try to coerce to the annotated type
                param_type = sig.parameters[param_name].annotation
                if param_type is not inspect.Parameter.empty and param_type is int:
                    kwargs[param_name] = int(path_params[param_name])
                else:
                    kwargs[param_name] = path_params[param_name]
            elif param_name in request.query:
                kwargs[param_name] = request.query[param_name]

        # Step 4: Call the endpoint
        try:
            body = endpoint(**kwargs)
        except Exception as e:
            return Response(status=500, body={"error": str(e)})

        # Step 5: Cleanup (run generator dependency cleanups)
        di.run_cleanup()

        return Response(status=200, body=body)


def test_full_lifecycle():
    """Test: Complete request-response lifecycle."""
    app = App()

    # Dependency
    def get_db():
        return {"table": "users", "connected": True}

    @app.get("/users/{user_id}")
    def get_user(user_id: int, db: dict = Depends(get_db)):
        return {"user_id": user_id, "db": db["table"]}

    @app.post("/users/")
    def create_user():
        return {"created": True}

    @app.get("/health")
    def health():
        return {"status": "ok"}

    # Test 1: GET with path parameter and dependency injection
    req = Request("GET", "/users/42")
    resp = app.handle_request(req)
    assert resp.status == 200
    assert resp.body == {"user_id": 42, "db": "users"}

    # Test 2: POST request
    req = Request("POST", "/users/", body={"name": "Alice"})
    resp = app.handle_request(req)
    assert resp.status == 200
    assert resp.body == {"created": True}

    # Test 3: Simple endpoint (no params, no DI)
    req = Request("GET", "/health")
    resp = app.handle_request(req)
    assert resp.status == 200
    assert resp.body == {"status": "ok"}

    # Test 4: 404 Not Found
    req = Request("GET", "/nonexistent")
    resp = app.handle_request(req)
    assert resp.status == 404

    # Test 5: Wrong method
    req = Request("DELETE", "/health")
    resp = app.handle_request(req)
    assert resp.status == 404

    print("[PASS] Full Lifecycle: routing + DI + params + response")


# =============================================================================
# SECTION 6: Path Parameter Type Coercion
# =============================================================================
#
# FastAPI automatically converts path parameters from strings to the
# annotated type. This section demonstrates how that works.
# =============================================================================


class PathConverter:
    """
    Converts path parameters from strings to their annotated types.

    FastAPI does this by inspecting the endpoint's type hints and applying
    type constructors to the raw string values from the URL.
    """

    CONVERTERS = {
        int: int,
        float: float,
        str: str,
        bool: lambda v: v.lower() in ("true", "1", "yes"),
    }

    @classmethod
    def convert(cls, value: str, target_type: type) -> Any:
        converter = cls.CONVERTERS.get(target_type, str)
        try:
            return converter(value)
        except (ValueError, TypeError):
            raise ValueError(f"Cannot convert '{value}' to {target_type.__name__}")


def test_path_converter():
    """Test: Path parameter type coercion."""
    assert PathConverter.convert("42", int) == 42
    assert PathConverter.convert("3.14", float) == 3.14
    assert PathConverter.convert("true", bool) is True
    assert PathConverter.convert("false", bool) is False
    assert PathConverter.convert("hello", str) == "hello"

    try:
        PathConverter.convert("abc", int)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

    print("[PASS] Path Converter: type coercion from URL strings")


# =============================================================================
# SECTION 7: Route Grouping with APIRouter
# =============================================================================
#
# FastAPI uses APIRouter to organize routes into modules.
# This is a composition pattern, not inheritance.
# =============================================================================


class APIRouter:
    """
    A sub-router that can be mounted onto a main app.

    Design decisions:
    - Has the same decorator API as the main app (@router.get, @router.post)
    - Can have a prefix (e.g., "/api/v1")
    - Can have its own dependencies (applied to all routes in the group)
    """

    def __init__(self, prefix: str = ""):
        self.prefix = prefix.rstrip("/")
        self.routes: list[Route] = []

    def get(self, path: str):
        def decorator(func: Callable):
            full_path = f"{self.prefix}{path}"
            route = Route(path=full_path, method="GET", endpoint=func)
            self.routes.append(route)
            return func
        return decorator

    def post(self, path: str):
        def decorator(func: Callable):
            full_path = f"{self.prefix}{path}"
            route = Route(path=full_path, method="POST", endpoint=func)
            self.routes.append(route)
            return func
        return decorator


class AppWithRouters(App):
    """App that supports mounting APIRouters."""

    def include_router(self, router: APIRouter):
        for route in router.routes:
            self.router.routes.append(route)


def test_api_router():
    """Test: APIRouter grouping and prefix."""
    app = AppWithRouters()

    users_router = APIRouter(prefix="/api/v1/users")
    items_router = APIRouter(prefix="/api/v1/items")

    @users_router.get("/")
    def list_users():
        return ["alice", "bob"]

    @users_router.get("/{user_id}")
    def get_user(user_id: int):
        return {"id": user_id}

    @items_router.get("/")
    def list_items():
        return ["item1", "item2"]

    app.include_router(users_router)
    app.include_router(items_router)

    # Test: Prefixed routes resolve correctly
    req = Request("GET", "/api/v1/users/")
    resp = app.handle_request(req)
    assert resp.status == 200
    assert resp.body == ["alice", "bob"]

    req = Request("GET", "/api/v1/users/42")
    resp = app.handle_request(req)
    assert resp.status == 200
    assert resp.body == {"id": 42}

    req = Request("GET", "/api/v1/items/")
    resp = app.handle_request(req)
    assert resp.status == 200
    assert resp.body == ["item1", "item2"]

    print("[PASS] API Router: prefix-based route grouping")


# =============================================================================
# MAIN: Run all tests
# =============================================================================


if __name__ == "__main__":
    print("=" * 60)
    print("FastAPI Internals Dissection")
    print("=" * 60)
    print()

    test_router()
    test_dependency_injection()
    test_middleware_chain()
    test_pydantic_validation()
    test_full_lifecycle()
    test_path_converter()
    test_api_router()

    print()
    print("=" * 60)
    print("All tests passed. Read the source code for detailed")
    print("explanations of each mechanism.")
    print("=" * 60)

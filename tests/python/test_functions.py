"""
Tests for Atom 02: Functions & Decorators
==========================================
Validates first-class functions, closures, decorators, lambda,
and the FastAPI-style routing pattern.
"""

import functools
import pytest


# ============================================================================
# FIRST-CLASS FUNCTIONS
# ============================================================================

class TestFirstClassFunctions:
    """Functions can be assigned, passed, and returned."""

    def test_assign_to_variable(self):
        """Functions can be assigned to variables."""
        def add(a, b):
            return a + b
        my_add = add
        assert my_add(3, 4) == 7

    def test_pass_as_argument(self):
        """Functions can be passed as arguments."""
        def apply(func, value):
            return func(value)
        assert apply(str.upper, "hello") == "HELLO"

    def test_store_in_dict(self):
        """Functions can be stored in data structures."""
        registry = {
            "double": lambda x: x * 2,
            "triple": lambda x: x * 3,
        }
        assert registry["double"](5) == 10
        assert registry["triple"](5) == 15

    def test_return_from_function(self):
        """Functions can return other functions."""
        def make_adder(n):
            def adder(x):
                return x + n
            return adder
        add5 = make_adder(5)
        assert add5(10) == 15


# ============================================================================
# HIGHER-ORDER FUNCTIONS
# ============================================================================

class TestHigherOrderFunctions:
    """Functions that take or return other functions."""

    def test_map_equivalent(self):
        """Custom map implementation."""
        def my_map(func, items):
            return [func(item) for item in items]
        assert my_map(str, [1, 2, 3]) == ["1", "2", "3"]

    def test_filter_equivalent(self):
        """Custom filter implementation."""
        def my_filter(pred, items):
            return [item for item in items if pred(item)]
        assert my_filter(lambda x: x > 2, [1, 2, 3, 4]) == [3, 4]

    def test_sorted_with_key(self):
        """sorted() accepts a key function."""
        words = ["banana", "apple", "cherry"]
        result = sorted(words, key=len)
        assert result == ["apple", "banana", "cherry"]

    def test_reduce_pattern(self):
        """Accumulator pattern (like reduce)."""
        from functools import reduce
        result = reduce(lambda acc, x: acc + x, [1, 2, 3, 4], 0)
        assert result == 10


# ============================================================================
# CLOSURES
# ============================================================================

class TestClosures:
    """Functions that capture variables from enclosing scope."""

    def test_basic_closure(self):
        """Inner function captures outer variable."""
        def outer(x):
            def inner():
                return x
            return inner
        f = outer(42)
        assert f() == 42

    def test_closure_with_late_binding(self):
        """Closures capture variables by reference, not value."""
        def make_functions():
            funcs = []
            for i in range(3):
                funcs.append(lambda: i)
            return funcs
        # All functions return 2 because they capture the same `i`
        # which is 2 after the loop ends
        f0, f1, f2 = make_functions()
        assert f0() == 2
        assert f1() == 2
        assert f2() == 2

    def test_closure_fix_late_binding(self):
        """Fix late binding with default argument."""
        def make_functions():
            funcs = []
            for i in range(3):
                funcs.append(lambda i=i: i)  # Capture current value
            return funcs
        f0, f1, f2 = make_functions()
        assert f0() == 0
        assert f1() == 1
        assert f2() == 2

    def test_nonlocal_keyword(self):
        """nonlocal allows modifying enclosing scope variable."""
        def make_counter():
            count = 0
            def counter():
                nonlocal count
                count += 1
                return count
            return counter
        c = make_counter()
        assert c() == 1
        assert c() == 2
        assert c() == 3

    def test_closure_independent_state(self):
        """Each closure has its own independent state."""
        def make_counter(start=0):
            count = start
            def counter():
                nonlocal count
                count += 1
                return count
            return counter
        c1 = make_counter(0)
        c2 = make_counter(100)
        assert c1() == 1
        assert c2() == 101
        assert c1() == 2


# ============================================================================
# LAMBDA
# ============================================================================

class TestLambda:
    """Lambda expressions create anonymous functions."""

    def test_basic_lambda(self):
        """Lambda creates a simple function."""
        square = lambda x: x ** 2
        assert square(5) == 25

    def test_lambda_with_multiple_args(self):
        """Lambda can take multiple arguments."""
        add = lambda a, b: a + b
        assert add(3, 4) == 7

    def test_lambda_as_sort_key(self):
        """Lambda is commonly used as a sort key."""
        students = [("Alice", 90), ("Bob", 85), ("Charlie", 92)]
        result = sorted(students, key=lambda s: s[1], reverse=True)
        assert result[0] == ("Charlie", 92)
        assert result[-1] == ("Bob", 85)

    def test_lambda_in_map(self):
        """Lambda used with map()."""
        result = list(map(lambda x: x ** 2, [1, 2, 3]))
        assert result == [1, 4, 9]

    def test_lambda_in_filter(self):
        """Lambda used with filter()."""
        result = list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5]))
        assert result == [2, 4]


# ============================================================================
# DECORATORS (BASIC)
# ============================================================================

class TestDecorators:
    """Decorators modify or wrap functions."""

    def test_basic_decorator(self):
        """Decorator wraps a function."""
        def uppercase(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs).upper()
            return wrapper

        @uppercase
        def greet(name):
            return f"hello {name}"

        assert greet("world") == "HELLO WORLD"

    def test_decorator_preserves_name(self):
        """@wraps preserves the original function name."""
        def my_decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper

        @my_decorator
        def my_function():
            """My docstring."""
            pass

        assert my_function.__name__ == "my_function"
        assert my_function.__doc__ == "My docstring."

    def test_decorator_preserves_args(self):
        """Decorator passes arguments correctly."""
        def log(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper

        @log
        def add(a, b):
            return a + b

        assert add(3, 4) == 7

    def test_decorator_can_short_circuit(self):
        """Decorator can prevent function execution."""
        def require_auth(func):
            @functools.wraps(func)
            def wrapper(is_authenticated, *args, **kwargs):
                if not is_authenticated:
                    return "Unauthorized"
                return func(*args, **kwargs)
            return wrapper

        @require_auth
        def secret():
            return "Secret data"

        assert secret(True) == "Secret data"
        assert secret(False) == "Unauthorized"

    def test_decorator_with_state(self):
        """Decorator can maintain state via closure."""
        def count_calls(func):
            count = 0
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                nonlocal count
                count += 1
                wrapper.call_count = count
                return func(*args, **kwargs)
            return wrapper

        @count_calls
        def hello():
            return "hi"

        hello()
        hello()
        assert hello.call_count == 2


# ============================================================================
# DECORATORS WITH ARGUMENTS
# ============================================================================

class TestDecoratorsWithArguments:
    """Decorators that accept arguments need 3 levels of nesting."""

    def test_decorator_with_int_arg(self):
        """Decorator that accepts an integer argument."""
        def repeat(n):
            def decorator(func):
                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    results = []
                    for _ in range(n):
                        results.append(func(*args, **kwargs))
                    return results
                return wrapper
            return decorator

        @repeat(3)
        def say_hello():
            return "hello"

        assert say_hello() == ["hello", "hello", "hello"]

    def test_decorator_with_string_arg(self):
        """Decorator that accepts a string argument."""
        def prefix(text):
            def decorator(func):
                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    return f"{text}: {func(*args, **kwargs)}"
                return wrapper
            return decorator

        @prefix("INFO")
        def log_message(msg):
            return msg

        assert log_message("test") == "INFO: test"

    def test_class_based_decorator_with_args(self):
        """Class-based decorator is cleaner for args."""
        class MaxRetries:
            def __init__(self, max_attempts):
                self.max_attempts = max_attempts

            def __call__(self, func):
                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    attempts = 0
                    while attempts < self.max_attempts:
                        try:
                            return func(*args, **kwargs)
                        except Exception:
                            attempts += 1
                    raise RuntimeError("Max retries exceeded")
                return wrapper

        call_count = 0

        @MaxRetries(max_attempts=3)
        def flaky():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Not yet")
            return "success"

        assert flaky() == "success"
        assert call_count == 3


# ============================================================================
# STACKING DECORATORS
# ============================================================================

class TestStackingDecorators:
    """Multiple decorators applied to one function."""

    def test_stacking_order(self):
        """Decorators apply bottom-to-top."""
        def bold(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return f"<b>{func(*args, **kwargs)}</b>"
            return wrapper

        def italic(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return f"<i>{func(*args, **kwargs)}</i>"
            return wrapper

        @bold
        @italic
        def text(t):
            return t

        # Equivalent to: bold(italic(text))
        assert text("hello") == "<b><i>hello</i></b>"

    def test_three_stacked(self):
        """Three decorators stack correctly."""
        def d1(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return f"D1({func(*args, **kwargs)})"
            return wrapper

        def d2(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return f"D2({func(*args, **kwargs)})"
            return wrapper

        def d3(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return f"D3({func(*args, **kwargs)})"
            return wrapper

        @d1
        @d2
        @d3
        def f():
            return "X"

        assert f() == "D1(D2(D3(X)))"


# ============================================================================
# FASTAPI-STYLE ROUTING PATTERN
# ============================================================================

class TestFastAPIPattern:
    """Decorators used for route registration (like FastAPI)."""

    def test_route_registration(self):
        """Decorator registers a function as a route handler."""
        class Router:
            def __init__(self):
                self.routes = {}

            def get(self, path):
                def decorator(func):
                    self.routes[("GET", path)] = func
                    return func
                return decorator

        router = Router()

        @router.get("/hello")
        def hello():
            return "world"

        assert ("GET", "/hello") in router.routes
        assert router.routes[("GET", "/hello")]() == "world"

    def test_multiple_routes(self):
        """Multiple routes registered on same router."""
        class Router:
            def __init__(self):
                self.routes = {}

            def get(self, path):
                def decorator(func):
                    self.routes[("GET", path)] = func
                    return func
                return decorator

            def post(self, path):
                def decorator(func):
                    self.routes[("POST", path)] = func
                    return func
                return decorator

        router = Router()

        @router.get("/items")
        def list_items():
            return ["item1", "item2"]

        @router.post("/items")
        def create_item():
            return {"created": True}

        assert len(router.routes) == 2
        assert router.routes[("GET", "/items")]() == ["item1", "item2"]
        assert router.routes[("POST", "/items")]() == {"created": True}


# ============================================================================
# *ARGS AND **KWARGS
# ============================================================================

class TestArgsKwargs:
    """Flexible argument handling with *args and **kwargs."""

    def test_args(self):
        """*args captures positional arguments as a tuple."""
        def func(*args):
            return args
        assert func(1, 2, 3) == (1, 2, 3)
        assert func() == ()

    def test_kwargs(self):
        """**kwargs captures keyword arguments as a dict."""
        def func(**kwargs):
            return kwargs
        assert func(a=1, b=2) == {"a": 1, "b": 2}
        assert func() == {}

    def test_combined(self):
        """*args and **kwargs can be combined."""
        def func(*args, **kwargs):
            return args, kwargs
        args, kwargs = func(1, 2, a=3, b=4)
        assert args == (1, 2)
        assert kwargs == {"a": 3, "b": 4}

    def test_unpack_args(self):
        """Unpack a list/tuple as positional arguments."""
        def add(a, b, c):
            return a + b + c
        args = [1, 2, 3]
        assert add(*args) == 6

    def test_unpack_kwargs(self):
        """Unpack a dict as keyword arguments."""
        def greet(name, greeting):
            return f"{greeting}, {name}!"
        kwargs = {"name": "World", "greeting": "Hello"}
        assert greet(**kwargs) == "Hello, World!"


# ============================================================================
# FUNCTOOLS DECORATORS
# ============================================================================

class TestFunctoolsDecorators:
    """Standard library decorators from functools."""

    def test_lru_cache(self):
        """@lru_cache memoizes function results."""
        call_count = 0

        @functools.lru_cache(maxsize=32)
        def expensive(x):
            nonlocal call_count
            call_count += 1
            return x ** 2

        assert expensive(5) == 25
        assert expensive(5) == 25  # Cached
        assert call_count == 1     # Only called once

    def test_lru_cache_different_args(self):
        """Different arguments create separate cache entries."""
        @functools.lru_cache()
        def add(a, b):
            return a + b

        assert add(1, 2) == 3
        assert add(2, 3) == 5
        info = add.cache_info()
        assert info.hits == 0
        assert info.misses == 2

        add(1, 2)  # Cache hit
        info = add.cache_info()
        assert info.hits == 1

    def test_property(self):
        """@property creates a computed attribute."""
        class Circle:
            def __init__(self, radius):
                self._radius = radius

            @property
            def area(self):
                return 3.14159 * self._radius ** 2

        c = Circle(5)
        assert abs(c.area - 78.53975) < 0.001

"""
Atom 02: Functions & Decorators
================================
First-class functions, closures, decorators, and lambda expressions.

Architecture:
    Functions in Python are first-class objects -- they can be assigned to
    variables, passed as arguments, returned from other functions, and stored
    in data structures. This enables powerful patterns like higher-order
    functions, closures, and decorators.

    Decorators are syntactic sugar for higher-order functions. `@decorator`
    above a function definition is equivalent to `func = decorator(func)`.
    This pattern is the backbone of modern Python frameworks:
    - Flask: @app.route("/path")
    - FastAPI: @app.get("/items/{item_id}")
    - pytest: @pytest.fixture
    - click: @click.command()

Transferability:
    - TypeScript: Functions are also first-class. Decorators exist via
      `@decorator` syntax (used in Angular, NestJS). Closures work similarly.
    - Rust: Functions are first-class (closures: |x| x + 1). No decorators,
      but trait impls serve a similar role.
    - Java: Lambda expressions (Java 8+), functional interfaces. No decorators
      per se, but annotations + reflection achieve similar patterns.

Application:
    - Web frameworks (FastAPI, Flask, Django) use decorators for routing.
    - Testing (pytest) uses decorators for fixtures and parametrize.
    - Caching (@functools.lru_cache), logging, authentication middleware.

Run: python functions.py
"""

from functools import wraps, lru_cache
from typing import Callable, Any


# ============================================================================
# SECTION 1: FUNCTIONS AS FIRST-CLASS OBJECTS
# ============================================================================
# Functions can be assigned to variables, passed as arguments, and returned.

def greet(name: str) -> str:
    """A simple function."""
    return f"Hello, {name}!"

# Assign function to a variable
say_hello = greet
print(f"say_hello('World'): {say_hello('World')}")
# Output: say_hello('World'): Hello, World!

# Functions can be stored in data structures
function_registry = {
    "greet": greet,
    "upper": str.upper,
}
print(f"registry['greet']('Python'): {function_registry['greet']('Python')}")
# Output: registry['greet']('Python'): Hello, Python!

# Functions can be passed as arguments (higher-order function)
def apply(func, value):
    """Apply a function to a value."""
    return func(value)

print(f"apply(str.upper, 'hello'): {apply(str.upper, 'hello')}")
# Output: apply(str.upper, 'hello'): HELLO


# ============================================================================
# SECTION 2: HIGHER-ORDER FUNCTIONS
# ============================================================================
# A higher-order function takes a function as argument or returns one.

def transform_list(items: list, func: Callable) -> list:
    """Apply a function to each item -- like built-in map()."""
    return [func(item) for item in items]

numbers = [1, 2, 3, 4, 5]
squared = transform_list(numbers, lambda x: x ** 2)
print(f"Squared: {squared}")
# Output: Squared: [1, 4, 9, 16, 25]

# Built-in higher-order functions: map, filter, sorted
print(f"map(str, [1,2,3]): {list(map(str, [1, 2, 3]))}")
# Output: map(str, [1,2,3]): ['1', '2', '3']

print(f"filter(even): {list(filter(lambda x: x % 2 == 0, numbers))}")
# Output: filter(even): [2, 4]

words = ["banana", "apple", "cherry"]
print(f"sorted by len: {sorted(words, key=len)}")
# Output: sorted by len: ['apple', 'banana', 'cherry']


# ============================================================================
# SECTION 3: CLOSURES
# ============================================================================
# A closure is a function that captures variables from its enclosing scope.
# The captured variables persist even after the outer function returns.

def make_multiplier(factor):
    """Return a function that multiplies by factor."""
    def multiply(x):
        return x * factor  # `factor` is captured from enclosing scope
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
print(f"double(5): {double(5)}")   # 10
print(f"triple(5): {triple(5)}")   # 15
# Output: double(5): 10
# Output: triple(5): 15

# The captured variable is shared (not copied)
def make_counter():
    """Return a counter function that increments each call."""
    count = 0
    def counter():
        nonlocal count  # Required to modify enclosing variable
        count += 1
        return count
    return counter

c = make_counter()
print(f"c(): {c()}")  # 1
print(f"c(): {c()}")  # 2
print(f"c(): {c()}")  # 3
# Output: c(): 1
# Output: c(): 2
# Output: c(): 3


# ============================================================================
# SECTION 4: LAMBDA EXPRESSIONS
# ============================================================================
# Lambda creates an anonymous function. Limited to a single expression.
# Use for short, throwaway functions. For anything complex, use def.

square = lambda x: x ** 2
print(f"square(5): {square(5)}")  # 25
# Output: square(5): 25

# Common use: sorting with custom key
students = [("Alice", 90), ("Bob", 85), ("Charlie", 92)]
by_grade = sorted(students, key=lambda s: s[1], reverse=True)
print(f"Sorted by grade: {by_grade}")
# Output: Sorted by grade: [('Charlie', 92), ('Alice', 90), ('Bob', 85)]

# Lambda with multiple arguments
add = lambda a, b: a + b
print(f"add(3, 4): {add(3, 4)}")  # 7
# Output: add(3, 4): 7


# ============================================================================
# SECTION 5: DECORATORS (Basic)
# ============================================================================
# A decorator is a function that takes a function and returns a new function.
# @decorator syntax is sugar for: func = decorator(func)

def log_calls(func):
    """Decorator that logs function calls."""
    @wraps(func)  # Preserves original function's name, docstring, etc.
    def wrapper(*args, **kwargs):
        print(f"  [LOG] Calling {func.__name__}({args}, {kwargs})")
        result = func(*args, **kwargs)
        print(f"  [LOG] {func.__name__} returned {result}")
        return result
    return wrapper

@log_calls
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

print("Decorated function call:")
result = add_numbers(3, 5)
print(f"Result: {result}")
# Output:
# Decorated function call:
#   [LOG] Calling add_numbers((3, 5), {})
#   [LOG] add_numbers returned 8
# Result: 8

# The @wraps decorator preserves the original function's metadata
print(f"Function name: {add_numbers.__name__}")  # "add_numbers" (not "wrapper")
print(f"Docstring: {add_numbers.__doc__}")        # "Add two numbers."
# Output: Function name: add_numbers
# Output: Docstring: Add two numbers.


# ============================================================================
# SECTION 6: DECORATORS WITH ARGUMENTS
# ============================================================================
# A decorator that takes arguments needs THREE levels of nesting:
# 1. Outer: accepts decorator arguments, returns the decorator
# 2. Middle: accepts the function, returns the wrapper
# 3. Inner: the actual wrapper that calls the function

def repeat(n: int):
    """Decorator that calls the function n times."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(n):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(3)
def say(message: str) -> str:
    """Print and return a message."""
    print(f"  {message}")
    return message

print("\nRepeat decorator (n=3):")
results = say("hello")
print(f"Results: {results}")
# Output:
# Repeat decorator (n=3):
#   hello
#   hello
#   hello
# Results: ['hello', 'hello', 'hello']

# Alternative: use a class-based decorator for cleaner arg handling
class Retry:
    """Decorator that retries a function on failure."""
    def __init__(self, max_attempts: int = 3):
        self.max_attempts = max_attempts

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, self.max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"  Attempt {attempt} failed: {e}")
            raise last_exception
        return wrapper

@Retry(max_attempts=3)
def unreliable_function():
    """Simulates a function that sometimes fails."""
    import random
    if random.random() < 0.7:
        raise ValueError("Random failure!")
    return "Success!"

# Uncomment to test (random behavior):
# print(unreliable_function())


# ============================================================================
# SECTION 7: STACKING DECORATORS
# ============================================================================
# Multiple decorators are applied bottom-to-top (innermost first).

def bold(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper

def italic(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper

@bold
@italic
def format_text(text: str) -> str:
    """Format text (applied: italic first, then bold)."""
    return text

# Equivalent to: format_text = bold(italic(format_text))
print(f"\nStacked decorators: {format_text('Hello')}")
# Output: Stacked decorators: <b><i>Hello</i></b>


# ============================================================================
# SECTION 8: THE FASTAPI DECORATOR PATTERN
# ============================================================================
# This is how FastAPI uses decorators in real applications.
# The decorator registers the function as a route handler.

class MiniRouter:
    """Simplified version of FastAPI's routing decorator."""

    def __init__(self):
        self._routes = {}

    def get(self, path: str):
        """Register a GET route handler."""
        def decorator(func):
            self._routes[("GET", path)] = func
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def post(self, path: str):
        """Register a POST route handler."""
        def decorator(func):
            self._routes[("POST", path)] = func
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def handle(self, method: str, path: str, **kwargs):
        """Simulate handling a request."""
        func = self._routes.get((method, path))
        if func is None:
            return {"error": "Not found"}
        return func(**kwargs)

# Usage -- mirrors FastAPI exactly
app = MiniRouter()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    """Read an item by ID."""
    return {"item_id": item_id, "name": f"Item {item_id}"}

@app.post("/items/")
def create_item(name: str, price: float):
    """Create a new item."""
    return {"name": name, "price": price, "created": True}

# Simulate requests
print("\nFastAPI-style routing:")
print(f"GET /items/42: {app.handle('GET', '/items/42', item_id=42)}")
print(f"POST /items/: {app.handle('POST', '/items/', name='Widget', price=9.99)}")
# Output: GET /items/42: {'item_id': 42, 'name': 'Item 42'}
# Output: POST /items/: {'name': 'Widget', 'price': 9.99, 'created': True}


# ============================================================================
# SECTION 9: FUNCTOOLS BUILT-IN DECORATORS
# ============================================================================

# @lru_cache -- memoize function results
@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    """Compute nth Fibonacci number with caching."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(f"\nfibonacci(30): {fibonacci(30)}")
print(f"Cache info: {fibonacci.cache_info()}")
# Output: fibonacci(30): 832040
# Output: Cache info: CacheInfo(hits=28, misses=31, maxsize=128, currsize=31)

# @property -- computed attribute
class Circle:
    def __init__(self, radius: float):
        self._radius = radius

    @property
    def radius(self) -> float:
        """Get the radius."""
        return self._radius

    @property
    def area(self) -> float:
        """Computed property: area of the circle."""
        import math
        return math.pi * self._radius ** 2

c = Circle(5)
print(f"Circle radius: {c.radius}, area: {c.area:.2f}")
# Output: Circle radius: 5, area: 78.54


# ============================================================================
# SECTION 10: *ARGS AND **KWARGS
# ============================================================================
# *args captures positional arguments as a tuple.
# **kwargs captures keyword arguments as a dict.

def flexible(*args, **kwargs):
    """Accept any arguments."""
    print(f"  args: {args}")
    print(f"  kwargs: {kwargs}")

print("\nFlexible function:")
flexible(1, 2, 3, name="Alice", age=30)
# Output:
#   args: (1, 2, 3)
#   kwargs: {'name': 'Alice', 'age': 30}

# Unpacking arguments when calling
def power(base, exponent):
    return base ** exponent

args = [2, 10]
print(f"power(*[2, 10]): {power(*args)}")  # 1024
kwargs = {"base": 2, "exponent": 10}
print(f"power(**kwargs): {power(**kwargs)}")  # 1024


# ============================================================================
# MINI-EXERCISES
# ============================================================================

def exercises():
    print("\n" + "=" * 60)
    print("MINI-EXERCISES")
    print("=" * 60)

    print("""
--- Multiple Choice ---

Q1: What does @wraps(func) do?
    A) Makes the decorator faster
    B) Preserves the original function's __name__ and __doc__
    C) Makes the function async
    D) Caches the function results
""")
    print("Answer: B) @wraps preserves the original function's metadata.\n")

    print("""
Q2: What is the output of this code?
    def outer():
        x = 10
        def inner():
            return x
        return inner
    f = outer()
    print(f())

    A) 10    B) Error    C) None    D) <function>
""")
    print("Answer: A) 10 -- inner() captures x from the enclosing scope.\n")

    print("""
Q3: Decorators with arguments require how many levels of nesting?
    A) 1    B) 2    C) 3    D) 4
""")
    print("Answer: C) 3 -- outer(decorator args), middle(func), inner(wrapper).\n")

    print("""
--- Q&A ---

Q: What is the difference between *args and **kwargs?
A: *args collects extra POSITIONAL arguments as a tuple.
   **kwargs collects extra KEYWORD arguments as a dict.
   Use them when you don't know how many arguments will be passed.

Q: Why is nonlocal needed in closures?
A: Without `nonlocal`, assigning to a variable in an enclosing scope
   creates a NEW local variable. `nonlocal` tells Python to use the
   enclosing scope's variable instead.

Q: When should you use lambda vs def?
A: Use lambda for short, throwaway expressions (sorting keys, callbacks).
   Use def for anything with logic, docstrings, or type hints.
""")


def progress_check():
    print("\n" + "=" * 60)
    print("PROGRESS CHECK")
    print("=" * 60)

    questions = [
        "1. Can you write a basic decorator from scratch?",
        "2. Can you write a decorator that accepts arguments?",
        "3. Do you understand why @wraps is important?",
        "4. Can you explain closures and nonlocal?",
        "5. Do you know when to use lambda vs def?",
        "6. Can you explain how FastAPI uses decorators?",
        "7. Do you understand *args and **kwargs?",
        "8. Can you stack multiple decorators?",
        "9. Do you know what functools provides?",
        "10. Can you explain the decorator execution order?",
    ]

    print("\nRate your confidence (1-5) for each:\n")
    for q in questions:
        print(f"  {q}")

    print("""
Scoring:
  40-50: Excellent! You understand one of Python's most powerful features.
  30-39: Good. Practice writing your own decorators.
  20-29: Review closures first -- they are the foundation of decorators.
  < 20:  Work through the examples line by line.
""")


def key_takeaways():
    print("\n" + "=" * 60)
    print("KEY TAKEAWAYS")
    print("=" * 60)
    print("""
* Functions are first-class objects in Python.
* Higher-order functions take or return other functions.
* Closures capture variables from enclosing scopes.
* Decorators are higher-over functions: @dec is sugar for f = dec(f).
* @wraps preserves the original function's metadata.
* Decorators with args need 3 levels of nesting.
* Stacking: @A @B @C applies C first, then B, then A.
* FastAPI/Flask use decorators to register route handlers.
* functools provides @lru_cache, @wraps, @total_ordering, etc.
* Use lambda for short expressions; def for everything else.
""")


def transferability():
    print("\n" + "=" * 60)
    print("TRANSFERABILITY TO OTHER LANGUAGES")
    print("=" * 60)
    print("""
Python Concept       | TypeScript           | Rust
---------------------|----------------------|------------------------
First-class func     | Yes (arrow funcs)    | Yes (closures)
Closures             | Yes (identical)      | Yes (Fn, FnMut, FnOnce)
Decorators           | @dec (experimental)  | No (use macros/traits)
lambda               | (x) => x * 2        | |x| x * 2
*args / **kwargs     | ...args / destruct.  | *args not supported
@wraps               | N/A                  | N/A
@lru_cache           | No (use Map)         | No (use memoize crate)
""")


if __name__ == "__main__":
    exercises()
    progress_check()
    key_takeaways()
    transferability()

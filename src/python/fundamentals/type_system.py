"""
Atom 05: Type Annotations
===========================
Python's type system: annotations, generics, TypeVar, Callable,
TypeAlias, Literal, and overloads.

Architecture:
    Python is dynamically typed, but since 3.5 it supports optional type
    annotations. These are NOT enforced at runtime -- they are hints for
    type checkers (mypy, pyright, pyrefly) and IDEs.

    The type system has evolved rapidly:
    - 3.5: typing module (List, Dict, Optional, Union)
    - 3.9: Built-in generics (list[int], dict[str, int])
    - 3.10: X | Y union syntax
    - 3.11: TypeVar constraints, Required/NotRequired
    - 3.12: Type parameter syntax (def f[T](x: T) -> T)

    Type annotations serve three purposes:
    1. Documentation: types tell developers what functions expect/return
    2. Tooling: IDEs provide better autocomplete and error detection
    3. Verification: type checkers catch bugs before runtime

Transferability:
    - TypeScript: Very similar type system. TypeScript's generics map to
      Python's TypeVar. Union types (A | B) are identical.
    - Rust: Statically enforced. No optional typing.
    - Java: Generics with type erasure. Python's generics are similar but
      erased at runtime too.

Application:
    - Every function signature should have type annotations.
    - API boundaries (request/response models) MUST be typed.
    - Complex data structures benefit from TypedDict or dataclass.
    - Use Protocol for structural typing (duck typing made explicit).

Run: python type_system.py
"""

from typing import (
    Any, Union, Optional, TypeVar, Generic, Callable,
    TypeAlias, Literal, overload, TypeVarTuple, Unpack,
    Sequence, Mapping, Iterator, Generator
)
from dataclasses import dataclass
import json


## ============================================================================
# SECTION 1: BASIC TYPE ANNOTATIONS
# ============================================================================
# Type annotations are added after a colon (:) for variables
# and after an arrow (->) for return types.

# Variable annotations
name: str = "Alice"
age: int = 30
scores: list[float] = [98.5, 87.0, 92.3]
config: dict[str, Any] = {"debug": True, "port": 8080}

# Function annotations
def greet(name: str) -> str:
    """Function with type annotations."""
    return f"Hello, {name}!"

def process_items(items: list[int], threshold: float = 0.5) -> dict[str, int]:
    """Multiple parameter types and complex return type."""
    return {"count": len(items), "above": sum(1 for x in items if x > threshold)}

print(f"greet('World'): {greet('World')}")
print(f"process_items([1,2,3]): {process_items([1, 2, 3])}")
# Output: greet('World'): Hello, World!
# Output: process_items([1,2,3]): {'count': 3, 'above': 3}


## ============================================================================
# SECTION 2: UNION AND OPTIONAL
# ============================================================================
# Union[X, Y] means X OR Y.
# Optional[X] is shorthand for Union[X, None].
# Python 3.10+ supports X | Y syntax.

def find_user(user_id: int) -> Optional[dict]:
    """Returns a user dict or None."""
    if user_id == 1:
        return {"id": 1, "name": "Alice"}
    return None

# Python 3.10+ syntax (preferred):
def find_user_modern(user_id: int) -> dict | None:
    """Same thing with modern syntax."""
    if user_id == 1:
        return {"id": 1, "name": "Alice"}
    return None

# Union with multiple types
def process(value: int | str | float) -> str:
    """Accept multiple types."""
    return str(value)

print(f"find_user(1): {find_user(1)}")
print(f"find_user(999): {find_user(999)}")
print(f"process(42): {process(42)}")
print(f"process('hello'): {process('hello')}")
# Output: find_user(1): {'id': 1, 'name': 'Alice'}
# Output: find_user(999): None
# Output: process(42): 42
# Output: process('hello'): hello


## ============================================================================
# SECTION 3: GENERICS WITH TypeVar
# ============================================================================
# TypeVar creates type parameters for generic functions and classes.
# The type checker ensures consistency: if input is list[int], output is int.

T = TypeVar('T')  # Unconstrained: any type
U = TypeVar('U')  # Another type variable

def first(items: Sequence[T]) -> T | None:
    """Return the first item or None. Type: (Sequence[T]) -> T | None."""
    for item in items:
        return item
    return None

# Usage: type checker infers T from the argument
result = first([1, 2, 3])      # T = int, returns int | None
print(f"first([1,2,3]): {result}")
# Output: first([1,2,3]): 1

# TypeVar with constraints (must be one of specific types)
Numeric = TypeVar('Numeric', int, float)

def add(a: Numeric, b: Numeric) -> Numeric:
    """Add two numbers. Type checker ensures both are int or both are float."""
    return a + b

print(f"add(1, 2): {add(1, 2)}")         # OK: both int
print(f"add(1.0, 2.0): {add(1.0, 2.0)}") # OK: both float
# Output: add(1, 2): 3
# Output: add(1.0, 2.0): 3.0


## ============================================================================
# SECTION 4: GENERIC CLASSES
# ============================================================================
# Generic classes use TypeVar to parameterize their types.
# Common examples: Container[T], Repository[T], Response[T].

class Stack(Generic[T]):
    """A generic stack data structure."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items.pop()

    def peek(self) -> T | None:
        return self._items[-1] if self._items else None

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Stack({self._items})"

# Type checker knows Stack[int] only accepts ints
int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
print(f"int_stack.pop(): {int_stack.pop()}")
print(f"int_stack: {int_stack}")
# Output: int_stack.pop(): 2
# Output: int_stack: Stack([1])

# Stack[str] is a different type
str_stack: Stack[str] = Stack()
str_stack.push("hello")
print(f"str_stack.pop(): {str_stack.pop()}")
# Output: str_stack.pop(): hello


## ============================================================================
# SECTION 5: TWO TYPE PARAMETERS
# ============================================================================
# Classes and functions can use multiple TypeVars.

class Pair(Generic[T, U]):
    """A generic pair of two different types."""

    def __init__(self, first: T, second: U):
        self.first = first
        self.second = second

    def __repr__(self) -> str:
        return f"Pair({self.first!r}, {self.second!r})"

p: Pair[str, int] = Pair("age", 30)
print(f"p: {p}")
# Output: p: Pair('age', 30)

def zip_with(items: Sequence[T], func: Callable[[T], U]) -> list[U]:
    """Apply a function to each item."""
    return [func(item) for item in items]

result = zip_with([1, 2, 3], lambda x: x ** 2)
print(f"zip_with([1,2,3], square): {result}")
# Output: zip_with([1,2,3], square): [1, 4, 9]


## ============================================================================
# SECTION 6: CALLABLE TYPES
# ============================================================================
# Callable[[param_types], return_type] describes function signatures.
# Used for callbacks, higher-order functions, and dependency injection.

def apply_func(func: Callable[[int], int], value: int) -> int:
    """Apply a function to a value."""
    return func(value)

# Type checker verifies the function signature
print(f"apply_func(lambda x: x*2, 5): {apply_func(lambda x: x*2, 5)}")
# Output: apply_func(lambda x: x*2, 5): 10

# More complex Callable
Transform = Callable[[list[int]], dict[str, int]]

def transform_data(data: list[int], transform: Transform) -> dict[str, int]:
    return transform(data)

result = transform_data([1, 2, 3], lambda d: {"sum": sum(d), "len": len(d)})
print(f"transform_data: {result}")
# Output: transform_data: {'sum': 6, 'len': 3}

# Callable with keyword arguments (Python 3.10+)
from typing import Protocol

class DataProcessor(Protocol):
    """Protocol for data processors."""
    def __call__(self, data: list[int], *, verbose: bool = False) -> dict: ...


## ============================================================================
# SECTION 7: TypeAlias
# ============================================================================
# TypeAlias creates readable names for complex types.
# Python 3.12+ supports the `type` keyword.

# Python 3.10+ syntax
UserId: TypeAlias = int
UserName: TypeAlias = str
UserDict: TypeAlias = dict[UserId, UserName]
ApiResponse: TypeAlias = dict[str, Any]

# Python 3.12+ syntax (preferred):
# type UserId = int
# type UserDict = dict[int, str]

def get_user(user_id: UserId, users: UserDict) -> UserName | None:
    """Type alias makes signatures more readable."""
    return users.get(user_id)

users: UserDict = {1: "Alice", 2: "Bob"}
print(f"get_user(1, users): {get_user(1, users)}")
# Output: get_user(1, users): Alice

# Complex type alias
JsonSerializable: TypeAlias = dict[str, "JsonSerializable"] | list["JsonSerializable"] | str | int | float | bool | None


## ============================================================================
# SECTION 8: LITERAL TYPES
# ============================================================================
# Literal restricts values to specific literals (strings, ints, bools).
# Useful for mode flags, HTTP methods, status codes, etc.

def set_log_level(level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]) -> str:
    """Only accepts specific log level strings."""
    return f"Log level set to {level}"

print(set_log_level("INFO"))
# Output: Log level set to INFO
# set_log_level("TRACE")  # Type checker error!

# Literal with integers
def set_priority(priority: Literal[1, 2, 3]) -> str:
    """Only accepts priority 1, 2, or 3."""
    return f"Priority: {priority}"

print(set_priority(1))
# Output: Priority: 1

# Literal with multiple types
def configure(mode: Literal["auto", "manual"], retries: Literal[0, 1, 2, 3]) -> str:
    return f"mode={mode}, retries={retries}"

print(configure("auto", 3))
# Output: mode=auto, retries=3


## ============================================================================
# SECTION 9: OVERLOADS
# ============================================================================
# @overload defines multiple signatures for a single function.
# The type checker uses these to infer the return type based on input types.
# Only ONE implementation exists; the overloads are just type hints.

@overload
def double(value: int) -> int: ...

@overload
def double(value: str) -> str: ...

def double(value: int | str) -> int | str:
    """Double an int or repeat a string."""
    if isinstance(value, int):
        return value * 2
    return value * 2

print(f"double(5): {double(5)}")         # 10 (type checker: int -> int)
print(f"double('ab'): {double('ab')}")   # "abab" (type checker: str -> str)
# Output: double(5): 10
# Output: double('ab'): abab

@overload
def fetch(resource: str) -> dict: ...

@overload
def fetch(resource: str, raw: Literal[True]) -> bytes: ...

def fetch(resource: str, raw: bool = False) -> dict | bytes:
    """Fetch a resource. Returns dict by default, bytes if raw=True."""
    if raw:
        return b"raw bytes"
    return {"resource": resource}

print(f"fetch('/api'): {fetch('/api')}")
print(f"fetch('/api', raw=True): {fetch('/api', raw=True)}")
# Output: fetch('/api'): {'resource': '/api'}
# Output: fetch('/api', raw=True): b'raw bytes'


## ============================================================================
# SECTION 10: DATACLASS WITH TYPES
# ============================================================================
# Type annotations shine with dataclasses for API models.

@dataclass
class UserCreate:
    """Request model for creating a user."""
    name: str
    email: str
    age: int | None = None
    tags: list[str] = None  # type: ignore

    def __post_init__(self):
        if self.tags is None:
            self.tags = []

    def validate(self) -> list[str]:
        """Return list of validation errors."""
        errors = []
        if not self.name:
            errors.append("Name is required")
        if "@" not in self.email:
            errors.append("Invalid email")
        if self.age is not None and self.age < 0:
            errors.append("Age must be non-negative")
        return errors

user = UserCreate(name="Alice", email="alice@example.com", age=30)
print(f"user: {user}")
print(f"validation: {user.validate()}")
# Output: user: UserCreate(name='Alice', email='alice@example.com', age=30, tags=[])
# Output: validation: []

# TypedDict for dict-based models (lighter than dataclass)
from typing import TypedDict

class UserResponse(TypedDict):
    id: int
    name: str
    email: str
    active: bool

def create_response(user_id: int, name: str, email: str) -> UserResponse:
    return {"id": user_id, "name": name, "email": email, "active": True}

resp = create_response(1, "Alice", "alice@example.com")
print(f"response: {resp}")
print(f"resp['name']: {resp['name']}")
# Output: response: {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'active': True}
# Output: resp['name']: Alice


## ============================================================================
# MINI-EXERCISES
## ============================================================================

def exercises():
    print("\n" + "=" * 60)
    print("MINI-EXERCISES")
    print("=" * 60)

    print("""
--- Multiple Choice ---

Q1: What does Optional[int] mean?
    A) int or float    B) int or None    C) int or str    D) int and None
""")
    print("Answer: B) Optional[int] = Union[int, None] = int | None.\n")

    print("""
Q2: When are type annotations enforced?
    A) Always at runtime
    B) Never -- they are hints for type checkers and IDEs
    C) Only in production
    D) Only with mypy installed
""")
    print("Answer: B) Python does NOT enforce types at runtime.\n")

    print("""
Q3: What does TypeVar('T') create?
    A) A concrete type
    B) A type parameter for generic functions/classes
    C) A runtime type check
    D) A new class
""")
    print("Answer: B) TypeVar creates a type parameter placeholder.\n")

    print("""
--- Q&A ---

Q: What is the difference between list[int] and List[int]?
A: Since Python 3.9, list[int] works directly (built-in generic).
   List[int] requires `from typing import List`. Prefer list[int].

Q: When should you use Literal instead of str?
A: When the function only accepts specific string values (like HTTP methods,
   log levels, mode flags). Literal catches typos at type-check time.

Q: What is @overload used for?
A: When a function's return type depends on input types. For example,
   fetch(url) returns dict, but fetch(url, raw=True) returns bytes.
   The overloads tell the type checker about these relationships.
""")


def progress_check():
    print("\n" + "=" * 60)
    print("PROGRESS CHECK")
    print("=" * 60)
    questions = [
        "1. Can you annotate function parameters and return types?",
        "2. Do you understand Union, Optional, and X | Y syntax?",
        "3. Can you create generic functions with TypeVar?",
        "4. Can you create generic classes with Generic[T]?",
        "5. Do you understand Callable types?",
        "6. Can you use TypeAlias for complex types?",
        "7. Can you use Literal to restrict values?",
        "8. Can you use @overload for multiple signatures?",
        "9. Do you know when to use dataclass vs TypedDict?",
        "10. Can you explain the difference between runtime and type-check time?",
    ]
    print("\nRate your confidence (1-5) for each:\n")
    for q in questions:
        print(f"  {q}")
    print("""
Scoring:
  40-50: Excellent! You can write well-typed Python code.
  30-39: Good. Practice annotating real code.
  20-29: Focus on basic annotations and Optional first.
  < 20:  Start with function annotations (param: type -> return_type).
""")


def key_takeaways():
    print("\n" + "=" * 60)
    print("KEY TAKEAWAYS")
    print("=" * 60)
    print("""
* Type annotations are hints, NOT enforced at runtime.
* param: type and -> return_type are the basic syntax.
* Union[X, Y] / X | Y for multiple possible types.
* Optional[X] is shorthand for X | None.
* TypeVar creates type parameters for generics.
* Generic[T] makes classes accept type parameters.
* Callable[[param_types], return_type] for function signatures.
* TypeAlias creates readable names for complex types.
* Literal restricts values to specific literals.
* @overload defines multiple function signatures.
* dataclass and TypedDict are typed data containers.
* Use mypy or pyright to check types at development time.
""")


def transferability():
    print("\n" + "=" * 60)
    print("TRANSFERABILITY TO OTHER LANGUAGES")
    print("=" * 60)
    print("""
Python Concept       | TypeScript           | Rust
---------------------|----------------------|------------------------
Type annotations     | type x: number       | let x: i32
Union (X | Y)        | X | Y               | enum
Optional (X | None)  | X | null             | Option<T>
TypeVar / Generic<T> | <T> generics         | <T> generics
Callable             | (x: number) => void  | fn(i32) -> ()
TypeAlias            | type X = ...         | type X = ...
Literal              | "a" | "b" (literal)  | enum (exhaustive)
@overload            | function overloads   | N/A (use traits)
TypedDict            | interface / type     | struct
dataclass            | class + interface    | struct (derive)
""")


if __name__ == "__main__":
    exercises()
    progress_check()
    key_takeaways()
    transferability()

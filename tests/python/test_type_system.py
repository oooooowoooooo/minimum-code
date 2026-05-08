"""
Tests for Atom 05: Type Annotations
====================================
Validates type annotations, generics, TypeVar, Callable,
TypeAlias, Literal, and overloads.

Note: These tests verify RUNTIME behavior. Type checking itself
is done by mypy/pyright, not pytest. We test that the annotated
code runs correctly.
"""

from typing import (
    Any, Union, Optional, TypeVar, Generic, Callable,
    TypeAlias, Literal, overload, Sequence
)
from dataclasses import dataclass
import pytest


# ============================================================================
# BASIC ANNOTATION TESTS
# ============================================================================

class TestBasicAnnotations:
    """Type annotations are optional hints; code must still work correctly."""

    def test_function_with_annotations(self):
        """Annotated functions work correctly at runtime."""
        def add(a: int, b: int) -> int:
            return a + b
        assert add(3, 4) == 7

    def test_annotations_dont_enforce_types(self):
        """Python does NOT enforce annotations at runtime."""
        def add(a: int, b: int) -> int:
            return a + b
        # This works at runtime even though types are "wrong"
        result = add("hello", " world")  # type: ignore
        assert result == "hello world"

    def test_complex_annotations(self):
        """Complex type annotations work at runtime."""
        def process(items: list[int], config: dict[str, Any]) -> dict[str, int]:
            return {"count": len(items), "threshold": config.get("threshold", 0)}
        result = process([1, 2, 3], {"threshold": 5})
        assert result == {"count": 3, "threshold": 5}

    def test_none_return_annotation(self):
        """None as return type works."""
        def log(message: str) -> None:
            pass  # Returns None
        assert log("test") is None


# ============================================================================
# UNION AND OPTIONAL TESTS
# ============================================================================

class TestUnionOptional:
    """Test Union, Optional, and X | Y syntax."""

    def test_optional_returns_none(self):
        """Optional return can be None."""
        def find(id: int) -> Optional[str]:
            if id == 1:
                return "Alice"
            return None
        assert find(1) == "Alice"
        assert find(999) is None

    def test_optional_with_pipe_syntax(self):
        """Python 3.10+ pipe syntax for Optional."""
        def find(id: int) -> str | None:
            if id == 1:
                return "Alice"
            return None
        assert find(1) == "Alice"
        assert find(999) is None

    def test_union_multiple_types(self):
        """Union with multiple types."""
        def process(value: int | str | float) -> str:
            return str(value)
        assert process(42) == "42"
        assert process("hi") == "hi"
        assert process(3.14) == "3.14"

    def test_union_type_check(self):
        """isinstance works with Union types at runtime."""
        def check(value: int | str) -> str:
            if isinstance(value, int):
                return "int"
            return "str"
        assert check(42) == "int"
        assert check("hello") == "str"


# ============================================================================
# TYPEVAR TESTS
# ============================================================================

class TestTypeVar:
    """Test TypeVar for generic functions."""

    def test_unconstrained_typevar(self):
        """TypeVar works with any type."""
        T = TypeVar('T')

        def first(items: Sequence[T]) -> T | None:
            for item in items:
                return item
            return None

        assert first([1, 2, 3]) == 1
        assert first(["a", "b"]) == "a"
        assert first([]) is None

    def test_constrained_typevar(self):
        """TypeVar with constraints limits to specific types."""
        Numeric = TypeVar('Numeric', int, float)

        def double(x: Numeric) -> Numeric:
            return x * 2

        assert double(5) == 10
        assert double(2.5) == 5.0

    def test_two_typevars(self):
        """Multiple TypeVars in one function."""
        T = TypeVar('T')
        U = TypeVar('U')

        def pair(a: T, b: U) -> tuple[T, U]:
            return (a, b)

        result = pair("hello", 42)
        assert result == ("hello", 42)


# ============================================================================
# GENERIC CLASS TESTS
# ============================================================================

class TestGenericClass:
    """Test generic classes with TypeVar."""

    def test_generic_stack(self):
        """Generic Stack works with any type."""
        T = TypeVar('T')

        class Stack(Generic[T]):
            def __init__(self):
                self._items: list[T] = []
            def push(self, item: T) -> None:
                self._items.append(item)
            def pop(self) -> T:
                return self._items.pop()

        int_stack: Stack[int] = Stack()
        int_stack.push(1)
        int_stack.push(2)
        assert int_stack.pop() == 2
        assert int_stack.pop() == 1

    def test_generic_container(self):
        """Generic container holds any type."""
        T = TypeVar('T')

        class Box(Generic[T]):
            def __init__(self, value: T):
                self.value = value
            def get(self) -> T:
                return self.value

        box: Box[str] = Box("hello")
        assert box.get() == "hello"

    def test_generic_with_two_params(self):
        """Generic class with two type parameters."""
        T = TypeVar('T')
        U = TypeVar('U')

        class Pair(Generic[T, U]):
            def __init__(self, first: T, second: U):
                self.first = first
                self.second = second

        p: Pair[str, int] = Pair("age", 30)
        assert p.first == "age"
        assert p.second == 30


# ============================================================================
# CALLABLE TESTS
# ============================================================================

class TestCallable:
    """Test Callable type hints for function signatures."""

    def test_callable_basic(self):
        """Callable type for simple functions."""
        def apply(func: Callable[[int], int], value: int) -> int:
            return func(value)

        assert apply(lambda x: x * 2, 5) == 10

    def test_callable_with_different_sigs(self):
        """Different Callable signatures."""
        def transform(func: Callable[[str], int], value: str) -> int:
            return func(value)

        assert transform(len, "hello") == 5

    def test_callable_stored(self):
        """Callable stored in a variable."""
        op: Callable[[int, int], int] = lambda a, b: a + b
        assert op(3, 4) == 7

    def test_callable_list(self):
        """List of Callables."""
        funcs: list[Callable[[int], int]] = [
            lambda x: x + 1,
            lambda x: x * 2,
            lambda x: x ** 2,
        ]
        results = [f(5) for f in funcs]
        assert results == [6, 10, 25]


# ============================================================================
# TYPEALIAS TESTS
# ============================================================================

class TestTypeAlias:
    """Test TypeAlias for readable type names."""

    def test_basic_type_alias(self):
        """TypeAlias creates readable names."""
        UserId: TypeAlias = int
        UserName: TypeAlias = str

        def get_name(uid: UserId, users: dict[UserId, UserName]) -> UserName:
            return users.get(uid, "Unknown")

        users = {1: "Alice", 2: "Bob"}
        assert get_name(1, users) == "Alice"
        assert get_name(99, users) == "Unknown"

    def test_complex_type_alias(self):
        """TypeAlias for complex nested types."""
        JsonDict: TypeAlias = dict[str, Any]
        ApiResponse: TypeAlias = dict[str, JsonDict | list[JsonDict] | None]

        def make_response(data: JsonDict) -> ApiResponse:
            return {"status": "ok", "data": data}

        result = make_response({"id": 1})
        assert result["status"] == "ok"


# ============================================================================
# LITERAL TESTS
# ============================================================================

class TestLiteral:
    """Test Literal types for restricted values."""

    def test_literal_string(self):
        """Literal restricts to specific strings."""
        def set_mode(mode: Literal["auto", "manual"]) -> str:
            return f"Mode: {mode}"

        assert set_mode("auto") == "Mode: auto"
        assert set_mode("manual") == "Mode: manual"

    def test_literal_int(self):
        """Literal restricts to specific integers."""
        def set_level(level: Literal[1, 2, 3]) -> str:
            return f"Level: {level}"

        assert set_level(1) == "Level: 1"
        assert set_level(3) == "Level: 3"

    def test_literal_mixed(self):
        """Literal with mixed types."""
        def configure(debug: Literal[True, False], mode: Literal["fast", "slow"]) -> str:
            return f"debug={debug}, mode={mode}"

        assert configure(True, "fast") == "debug=True, mode=fast"


# ============================================================================
# OVERLOAD TESTS
# ============================================================================

class TestOverload:
    """Test @overload for multiple function signatures."""

    def test_overload_int(self):
        """Overloaded function returns correct type for int input."""
        @overload
        def double(value: int) -> int: ...

        @overload
        def double(value: str) -> str: ...

        def double(value: int | str) -> int | str:
            return value * 2

        assert double(5) == 10
        assert double("ab") == "abab"

    def test_overload_with_literal(self):
        """Overload with Literal for precise return types."""
        @overload
        def fetch(url: str) -> dict: ...

        @overload
        def fetch(url: str, raw: Literal[True]) -> bytes: ...

        def fetch(url: str, raw: bool = False) -> dict | bytes:
            if raw:
                return b"raw"
            return {"url": url}

        assert fetch("/api") == {"url": "/api"}
        assert fetch("/api", raw=True) == b"raw"

    def test_overload_signature_count(self):
        """Each overload defines a separate signature."""
        @overload
        def process(x: int) -> int: ...
        @overload
        def process(x: str) -> str: ...
        @overload
        def process(x: list) -> int: ...

        def process(x):
            if isinstance(x, list):
                return len(x)
            return x

        assert process(42) == 42
        assert process("hi") == "hi"
        assert process([1, 2, 3]) == 3


# ============================================================================
# DATACLASS WITH TYPES TESTS
# ============================================================================

class TestTypedDataclass:
    """Test dataclasses with type annotations."""

    def test_dataclass_types(self):
        """Dataclass with typed fields."""
        @dataclass
        class User:
            name: str
            age: int
            email: str | None = None

        u = User("Alice", 30, "alice@example.com")
        assert u.name == "Alice"
        assert u.age == 30
        assert u.email == "alice@example.com"

    def test_dataclass_optional_field(self):
        """Dataclass with Optional field defaults to None."""
        @dataclass
        class Config:
            host: str = "localhost"
            port: int = 8080
            debug: bool | None = None

        c = Config()
        assert c.host == "localhost"
        assert c.debug is None

    def test_dataclass_with_list(self):
        """Dataclass with list field."""
        @dataclass
        class Result:
            values: list[int]
            metadata: dict[str, Any]

        r = Result(values=[1, 2, 3], metadata={"source": "test"})
        assert r.values == [1, 2, 3]
        assert r.metadata["source"] == "test"

    def test_dataclass_validation(self):
        """Dataclass with validation method."""
        @dataclass
        class Input:
            value: int

            def validate(self) -> list[str]:
                errors = []
                if self.value < 0:
                    errors.append("Must be non-negative")
                if self.value > 100:
                    errors.append("Must be <= 100")
                return errors

        assert Input(50).validate() == []
        assert Input(-1).validate() == ["Must be non-negative"]
        assert Input(101).validate() == ["Must be <= 100"]


# ============================================================================
# TYPEDDICT TESTS
# ============================================================================

class TestTypedDict:
    """Test TypedDict for typed dictionaries."""

    def test_typed_dict_creation(self):
        """Create a TypedDict instance."""
        from typing import TypedDict

        class UserDict(TypedDict):
            name: str
            age: int
            active: bool

        user: UserDict = {"name": "Alice", "age": 30, "active": True}
        assert user["name"] == "Alice"
        assert user["age"] == 30

    def test_typed_dict_as_return(self):
        """TypedDict as function return type."""
        from typing import TypedDict

        class Response(TypedDict):
            status: str
            data: dict[str, Any]

        def make_response(data: dict) -> Response:
            return {"status": "ok", "data": data}

        result = make_response({"id": 1})
        assert result["status"] == "ok"

    def test_typed_dict_optional_keys(self):
        """TypedDict with NotRequired for optional keys."""
        from typing import TypedDict, NotRequired

        class UserInput(TypedDict):
            name: str
            email: str
            age: NotRequired[int]

        user: UserInput = {"name": "Alice", "email": "a@b.com"}
        assert user.get("age") is None

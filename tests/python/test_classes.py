"""
Tests for Atom 03: Classes & Inheritance
=========================================
Validates dataclasses, dunder methods, ABC, Protocol, and composition.
"""

from dataclasses import dataclass, field, FrozenInstanceError
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable
import pytest


# ============================================================================
# BASIC CLASS TESTS
# ============================================================================

class TestBasicClass:
    """Test basic class definition, instance variables, and methods."""

    def test_init_sets_attributes(self):
        class Dog:
            def __init__(self, name, age):
                self.name = name
                self.age = age
        dog = Dog("Rex", 5)
        assert dog.name == "Rex"
        assert dog.age == 5

    def test_class_variable_shared(self):
        class Counter:
            count = 0
            def __init__(self):
                Counter.count += 1
        c1 = Counter()
        c2 = Counter()
        assert Counter.count == 2

    def test_instance_variable_independent(self):
        class Item:
            def __init__(self, value):
                self.value = value
        a = Item(1)
        b = Item(2)
        assert a.value == 1
        assert b.value == 2

    def test_method(self):
        class Calculator:
            def __init__(self, value=0):
                self.value = value
            def add(self, n):
                self.value += n
                return self
        calc = Calculator(10)
        result = calc.add(5).add(3)
        assert result.value == 18

    def test_repr_and_str(self):
        class Point:
            def __init__(self, x, y):
                self.x = x
                self.y = y
            def __repr__(self):
                return f"Point({self.x}, {self.y})"
            def __str__(self):
                return f"({self.x}, {self.y})"
        p = Point(1, 2)
        assert repr(p) == "Point(1, 2)"
        assert str(p) == "(1, 2)"


# ============================================================================
# DUNDER METHOD TESTS
# ============================================================================

class TestDunderMethods:
    """Test magic/dunder methods for operator overloading."""

    def test_eq(self):
        class Value:
            def __init__(self, v):
                self.v = v
            def __eq__(self, other):
                if not isinstance(other, Value):
                    return NotImplemented
                return self.v == other.v
        assert Value(5) == Value(5)
        assert Value(5) != Value(6)

    def test_add(self):
        class Num:
            def __init__(self, v):
                self.v = v
            def __add__(self, other):
                return Num(self.v + other.v)
        result = Num(3) + Num(4)
        assert result.v == 7

    def test_len(self):
        class Collection:
            def __init__(self, items):
                self.items = items
            def __len__(self):
                return len(self.items)
        assert len(Collection([1, 2, 3])) == 3

    def test_getitem(self):
        class Array:
            def __init__(self, data):
                self.data = data
            def __getitem__(self, index):
                return self.data[index]
        arr = Array([10, 20, 30])
        assert arr[0] == 10
        assert arr[2] == 30

    def test_iter(self):
        class Range:
            def __init__(self, start, end):
                self.start = start
                self.end = end
            def __iter__(self):
                current = self.start
                while current < self.end:
                    yield current
                    current += 1
        assert list(Range(0, 5)) == [0, 1, 2, 3, 4]

    def test_bool(self):
        class Flag:
            def __init__(self, active):
                self.active = active
            def __bool__(self):
                return self.active
        assert bool(Flag(True))
        assert not bool(Flag(False))

    def test_contains(self):
        class Bag:
            def __init__(self, items):
                self.items = set(items)
            def __contains__(self, item):
                return item in self.items
        bag = Bag([1, 2, 3])
        assert 2 in bag
        assert 4 not in bag

    def test_abs(self):
        class Temperature:
            def __init__(self, celsius):
                self.celsius = celsius
            def __abs__(self):
                return abs(self.celsius)
        assert abs(Temperature(-10)) == 10
        assert abs(Temperature(5)) == 5


# ============================================================================
# DATACLASS TESTS
# ============================================================================

class TestDataclass:
    """Test @dataclass decorator and its options."""

    def test_auto_init(self):
        @dataclass
        class Point:
            x: float
            y: float
        p = Point(1.0, 2.0)
        assert p.x == 1.0
        assert p.y == 2.0

    def test_auto_repr(self):
        @dataclass
        class Point:
            x: float
            y: float
        r = repr(Point(1, 2))
        assert "x=1" in r and "y=2" in r

    def test_auto_eq(self):
        @dataclass
        class Point:
            x: float
            y: float
        assert Point(1, 2) == Point(1, 2)
        assert Point(1, 2) != Point(3, 4)

    def test_default_values(self):
        @dataclass
        class Config:
            host: str = "localhost"
            port: int = 8080
        c = Config()
        assert c.host == "localhost"
        assert c.port == 8080
        c2 = Config(port=3000)
        assert c2.port == 3000

    def test_field_default_factory(self):
        @dataclass
        class Items:
            items: list = field(default_factory=list)
        a = Items()
        b = Items()
        a.items.append(1)
        assert a.items == [1]
        assert b.items == []  # Independent lists

    def test_frozen(self):
        @dataclass(frozen=True)
        class Color:
            r: int
            g: int
            b: int
        c = Color(255, 0, 0)
        with pytest.raises(FrozenInstanceError):
            c.r = 100

    def test_frozen_is_hashable(self):
        @dataclass(frozen=True)
        class Color:
            r: int
            g: int
            b: int
        c = Color(255, 0, 0)
        d = {c: "red"}
        assert d[c] == "red"

    def test_post_init(self):
        @dataclass
        class Rectangle:
            width: float
            height: float
            area: float = field(init=False)
            def __post_init__(self):
                self.area = self.width * self.height
        r = Rectangle(3, 4)
        assert r.area == 12


# ============================================================================
# INHERITANCE TESTS
# ============================================================================

class TestInheritance:
    """Test class inheritance and method resolution."""

    def test_basic_inheritance(self):
        class Animal:
            def __init__(self, name):
                self.name = name
            def speak(self):
                return f"{self.name} speaks"
        class Dog(Animal):
            def speak(self):
                return f"{self.name} barks"
        dog = Dog("Rex")
        assert dog.speak() == "Rex barks"

    def test_super_call(self):
        class Base:
            def __init__(self, value):
                self.value = value
        class Child(Base):
            def __init__(self, value, extra):
                super().__init__(value)
                self.extra = extra
        c = Child(10, "hello")
        assert c.value == 10
        assert c.extra == "hello"

    def test_isinstance(self):
        class A:
            pass
        class B(A):
            pass
        class C(B):
            pass
        c = C()
        assert isinstance(c, C)
        assert isinstance(c, B)
        assert isinstance(c, A)

    def test_issubclass(self):
        class A:
            pass
        class B(A):
            pass
        assert issubclass(B, A)
        assert issubclass(B, B)
        assert not issubclass(A, B)

    def test_mro(self):
        class A:
            pass
        class B(A):
            pass
        class C(B):
            pass
        mro = C.__mro__
        assert mro == (C, B, A, object)

    def test_multiple_inheritance(self):
        class Flyer:
            def fly(self):
                return "flying"
        class Swimmer:
            def swim(self):
                return "swimming"
        class Duck(Flyer, Swimmer):
            pass
        d = Duck()
        assert d.fly() == "flying"
        assert d.swim() == "swimming"


# ============================================================================
# ABC TESTS
# ============================================================================

class TestABC:
    """Test Abstract Base Classes."""

    def test_cannot_instantiate_abc(self):
        class Shape(ABC):
            @abstractmethod
            def area(self):
                ...
        with pytest.raises(TypeError):
            Shape()

    def test_concrete_subclass(self):
        class Shape(ABC):
            @abstractmethod
            def area(self):
                ...
        class Square(Shape):
            def __init__(self, side):
                self.side = side
            def area(self):
                return self.side ** 2
        sq = Square(5)
        assert sq.area() == 25

    def test_abc_with_concrete_method(self):
        class Shape(ABC):
            @abstractmethod
            def area(self):
                ...
            def describe(self):
                return f"Area: {self.area()}"
        class Square(Shape):
            def __init__(self, side):
                self.side = side
            def area(self):
                return self.side ** 2
        sq = Square(5)
        assert sq.describe() == "Area: 25"

    def test_incomplete_subclass_raises(self):
        class Shape(ABC):
            @abstractmethod
            def area(self):
                ...
            @abstractmethod
            def perimeter(self):
                ...
        class IncompleteShape(Shape):
            def area(self):
                return 0
        with pytest.raises(TypeError):
            IncompleteShape()


# ============================================================================
# PROTOCOL TESTS
# ============================================================================

class TestProtocol:
    """Test structural typing with Protocol."""

    def test_protocol_structural_match(self):
        @runtime_checkable
        class HasArea(Protocol):
            def area(self) -> float: ...

        class Square:
            def __init__(self, side):
                self.side = side
            def area(self):
                return self.side ** 2

        sq = Square(5)
        assert isinstance(sq, HasArea)

    def test_protocol_no_inheritance_needed(self):
        @runtime_checkable
        class Drawable(Protocol):
            def draw(self) -> str: ...

        class Widget:
            def draw(self):
                return "widget"

        w = Widget()
        assert isinstance(w, Drawable)  # No inheritance!

    def test_protocol_no_match(self):
        @runtime_checkable
        class Drawable(Protocol):
            def draw(self) -> str: ...

        class NotDrawable:
            def render(self):
                return "nope"

        assert not isinstance(NotDrawable(), Drawable)

    def test_protocol_as_type_hint(self):
        @runtime_checkable
        class Serializable(Protocol):
            def to_dict(self) -> dict: ...

        class User:
            def __init__(self, name):
                self.name = name
            def to_dict(self):
                return {"name": self.name}

        def save(obj: Serializable) -> dict:
            return obj.to_dict()

        result = save(User("Alice"))
        assert result == {"name": "Alice"}


# ============================================================================
# COMPOSITION TESTS
# ============================================================================

class TestComposition:
    """Test composition over inheritance pattern."""

    def test_has_a_relationship(self):
        class Logger:
            def log(self, msg):
                return f"[LOG] {msg}"

        class Service:
            def __init__(self):
                self.logger = Logger()

            def do_work(self):
                return self.logger.log("done")

        svc = Service()
        assert svc.do_work() == "[LOG] done"

    def test_injectable_components(self):
        class ConsoleLogger:
            def log(self, msg):
                return f"CONSOLE: {msg}"

        class FileLogger:
            def log(self, msg):
                return f"FILE: {msg}"

        class App:
            def __init__(self, logger):
                self.logger = logger

            def run(self):
                return self.logger.log("running")

        assert App(ConsoleLogger()).run() == "CONSOLE: running"
        assert App(FileLogger()).run() == "FILE: running"

    def test_strategy_pattern(self):
        class BubbleSort:
            def sort(self, data):
                return sorted(data)

        class ReverseSort:
            def sort(self, data):
                return sorted(data, reverse=True)

        class Sorter:
            def __init__(self, strategy):
                self.strategy = strategy

            def sort(self, data):
                return self.strategy.sort(data)

        data = [3, 1, 4, 1, 5]
        assert Sorter(BubbleSort()).sort(data) == [1, 1, 3, 4, 5]
        assert Sorter(ReverseSort()).sort(data) == [5, 4, 3, 1, 1]


# ============================================================================
# CLASS AND STATIC METHOD TESTS
# ============================================================================

class TestClassAndStaticMethods:
    """Test @classmethod and @staticmethod."""

    def test_classmethod_factory(self):
        class Date:
            def __init__(self, year, month, day):
                self.year = year
                self.month = month
                self.day = day

            @classmethod
            def from_string(cls, s):
                y, m, d = s.split("-")
                return cls(int(y), int(m), int(d))

            def __repr__(self):
                return f"{self.year}-{self.month:02d}-{self.day:02d}"

        d = Date.from_string("2024-06-15")
        assert d.year == 2024
        assert d.month == 6
        assert d.day == 15

    def test_staticmethod_utility(self):
        class Math:
            @staticmethod
            def is_even(n):
                return n % 2 == 0

        assert Math.is_even(4)
        assert not Math.is_even(3)

    def test_classmethod_inherits_correctly(self):
        class Base:
            name = "Base"
            @classmethod
            def get_name(cls):
                return cls.name
        class Child(Base):
            name = "Child"
        assert Base.get_name() == "Base"
        assert Child.get_name() == "Child"

"""
Atom 03: Classes & Inheritance
===============================
Object-oriented programming in Python: classes, inheritance, dataclasses,
abstract classes, protocols, and composition.

Architecture:
    Python's OOP is built on two core ideas:
    1. Everything is an object (even classes themselves are objects of type 'type')
    2. Attribute lookup follows the Method Resolution Order (MRO)

    Modern Python favors:
    - dataclasses for data containers (reduce boilerplate)
    - Protocol (structural typing) over ABC (nominal typing)
    - Composition over inheritance (favor has-a over is-a)
    - Dunder methods for Pythonic interfaces (__len__, __iter__, __eq__, etc.)

Transferability:
    - TypeScript: Classes work similarly. No dataclasses (use interfaces).
      Protocol maps to TypeScript interfaces (structural typing).
    - Rust: No classes -- use structs + traits. Traits are like Protocols.
    - Java: Classes, interfaces, abstract classes. Python's ABC is similar.

Application:
    - dataclass: API request/response models, configuration, data transfer
    - ABC: Plugin systems, abstract interfaces for swappable implementations
    - Protocol: Type checking without inheritance (dependency injection)
    - Composition: Service layers, strategy pattern, dependency injection

Run: python classes.py
"""

from dataclasses import dataclass, field, asdict, astuple
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable, Sequence
import json


# ============================================================================
# SECTION 1: BASIC CLASS
# ============================================================================
# Classes define blueprints for objects. __init__ is the constructor.
# self is the instance -- always the first parameter.

class Dog:
    """A simple class representing a dog."""

    # Class variable (shared by all instances)
    species = "Canis familiaris"

    def __init__(self, name: str, age: int):
        """Initialize instance variables."""
        self.name = name    # Instance variable
        self.age = age      # Instance variable

    def bark(self) -> str:
        """Instance method -- has access to self."""
        return f"{self.name} says Woof!"

    def __repr__(self) -> str:
        """Developer-friendly string representation."""
        return f"Dog(name='{self.name}', age={self.age})"

    def __str__(self) -> str:
        """User-friendly string representation."""
        return f"{self.name} (age {self.age})"

dog = Dog("Rex", 5)
print(f"dog.name: {dog.name}")
print(f"dog.bark(): {dog.bark()}")
print(f"repr: {repr(dog)}")
print(f"str: {str(dog)}")
print(f"species: {Dog.species}")
# Output: dog.name: Rex
# Output: dog.bark(): Rex says Woof!
# Output: repr: Dog(name='Rex', age=5)
# Output: str: Rex (age 5)
# Output: species: Canis familiaris


# ============================================================================
# SECTION 2: DUNDER (MAGIC) METHODS
# ============================================================================
# Dunder methods define how objects behave with built-in operations.
# They are the foundation of Python's data model.

class Vector:
    """A 2D vector with operator overloading."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __eq__(self, other) -> bool:
        """== operator: compare by value."""
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __add__(self, other) -> "Vector":
        """+ operator: vector addition."""
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> "Vector":
        """* operator: scalar multiplication."""
        return Vector(self.x * scalar, self.y * scalar)

    def __abs__(self) -> float:
        """abs() function: vector magnitude."""
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __len__(self) -> int:
        """len() function: number of components."""
        return 2

    def __bool__(self) -> bool:
        """bool(): True if non-zero vector."""
        return self.x != 0 or self.y != 0

    def __getitem__(self, index: int) -> float:
        """Indexing: v[0], v[1]."""
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError(f"Vector index out of range: {index}")

    def __iter__(self):
        """Iteration: for component in v."""
        yield self.x
        yield self.y

v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(f"\nv1: {v1}")                    # Vector(3, 4)
print(f"v1 + v2: {v1 + v2}")            # Vector(4, 6)
print(f"v1 * 2: {v1 * 2}")              # Vector(6, 8)
print(f"abs(v1): {abs(v1)}")            # 5.0
print(f"len(v1): {len(v1)}")            # 2
print(f"v1[0]: {v1[0]}, v1[1]: {v1[1]}")  # 3, 4
print(f"v1 == v2: {v1 == v2}")          # False
print(f"list(v1): {list(v1)}")          # [3, 4]
print(f"bool(Vector(0,0)): {bool(Vector(0, 0))}")  # False
# Output: v1: Vector(3, 4)
# Output: v1 + v2: Vector(4, 6)
# Output: v1 * 2: Vector(6, 8)
# Output: abs(v1): 5.0
# Output: len(v1): 2
# Output: v1[0]: 3, v1[1]: 4
# Output: v1 == v2: False
# Output: list(v1): [3, 4]
# Output: bool(Vector(0,0)): False


# ============================================================================
# SECTION 3: DATACLASSES
# ============================================================================
# @dataclass auto-generates __init__, __repr__, __eq__, and more.
# Use for data containers where you don't need custom behavior.

@dataclass
class Point:
    """A 2D point. Auto-generated: __init__, __repr__, __eq__."""
    x: float
    y: float

p1 = Point(1.0, 2.0)
p2 = Point(1.0, 2.0)
p3 = Point(3.0, 4.0)

print(f"\np1: {p1}")              # Point(x=1.0, y=2.0)
print(f"p1 == p2: {p1 == p2}")    # True (value equality)
print(f"p1 == p3: {p1 == p3}")    # False
# Output: p1: Point(x=1.0, y=2.0)
# Output: p1 == p2: True
# Output: p1 == p3: False

# Dataclass with default values and field options
@dataclass
class Config:
    """Configuration with defaults."""
    host: str = "localhost"
    port: int = 8080
    debug: bool = False
    tags: list = field(default_factory=list)  # Mutable default needs factory

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)

config = Config(port=3000, tags=["web", "api"])
print(f"\nconfig: {config}")
print(f"config.to_dict(): {config.to_dict()}")
# Output: config: Config(host='localhost', port=3000, debug=False, tags=['web', 'api'])
# Output: config.to_dict(): {'host': 'localhost', 'port': 3000, 'debug': False, 'tags': ['web', 'api']}

# Frozen dataclass (immutable, hashable)
@dataclass(frozen=True)
class Color:
    """Immutable color value."""
    r: int
    g: int
    b: int

    def hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

red = Color(255, 0, 0)
print(f"\nred.hex(): {red.hex()}")   # #ff0000
# Can be used as dict key (hashable)
color_names = {Color(255, 0, 0): "red", Color(0, 255, 0): "green"}
print(f"color_names[red]: {color_names[red]}")
# Output: red.hex(): #ff0000
# Output: color_names[red]: red


# ============================================================================
# SECTION 4: INHERITANCE
# ============================================================================
# Use inheritance for "is-a" relationships.
# Python supports multiple inheritance (use carefully).

class Animal:
    """Base class for animals."""

    def __init__(self, name: str, sound: str):
        self.name = name
        self.sound = sound

    def speak(self) -> str:
        return f"{self.name} says {self.sound}!"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"

class Cat(Animal):
    """Cat inherits from Animal."""

    def __init__(self, name: str, indoor: bool = True):
        super().__init__(name, sound="Meow")  # Call parent constructor
        self.indoor = indoor

    def purr(self) -> str:
        return f"{self.name} purrs..."

cat = Cat("Whiskers")
print(f"\ncat.speak(): {cat.speak()}")   # Whiskers says Meow!
print(f"cat.purr(): {cat.purr()}")       # Whiskers purrs...
print(f"isinstance(cat, Cat): {isinstance(cat, Cat)}")       # True
print(f"isinstance(cat, Animal): {isinstance(cat, Animal)}") # True
# Output: cat.speak(): Whiskers says Meow!
# Output: cat.purr(): Whiskers purrs...
# Output: isinstance(cat, Cat): True
# Output: isinstance(cat, Animal): True

# Method Resolution Order (MRO)
print(f"Cat MRO: {Cat.__mro__}")
# Output: Cat MRO: (<class 'Cat'>, <class 'Animal'>, <class 'object'>)


# ============================================================================
# SECTION 5: ABSTRACT BASE CLASSES (ABC)
# ============================================================================
# ABC defines interfaces that MUST be implemented by subclasses.
# Use when you want to enforce a contract (nominal typing).

class Shape(ABC):
    """Abstract shape -- cannot be instantiated directly."""

    @abstractmethod
    def area(self) -> float:
        """Compute the area. MUST be implemented by subclasses."""
        ...

    @abstractmethod
    def perimeter(self) -> float:
        """Compute the perimeter. MUST be implemented by subclasses."""
        ...

    def describe(self) -> str:
        """Concrete method -- can be used as-is or overridden."""
        return f"{self.__class__.__name__}: area={self.area():.2f}, peri={self.perimeter():.2f}"

class Rectangle(Shape):
    """Rectangle implements Shape."""

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

class Circle(Shape):
    """Circle implements Shape."""

    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        import math
        return 2 * math.pi * self.radius

rect = Rectangle(5, 3)
circ = Circle(4)
print(f"\nrect.describe(): {rect.describe()}")
print(f"circ.describe(): {circ.describe()}")
# Output: rect.describe(): Rectangle: area=15.00, peri=16.00
# Output: circ.describe(): Circle: area=50.27, peri=25.13

# This would raise TypeError:
# shape = Shape()  # Can't instantiate abstract class


# ============================================================================
# SECTION 6: PROTOCOL (Structural Typing)
# ============================================================================
# Protocol defines interfaces by structure, not inheritance.
# A class satisfies a protocol if it has the right methods/attributes.
# This is "duck typing" made explicit for type checkers.

@runtime_checkable
class Drawable(Protocol):
    """Anything with a draw() method is Drawable."""
    def draw(self) -> str: ...

@runtime_checkable
class Serializable(Protocol):
    """Anything with to_dict() is Serializable."""
    def to_dict(self) -> dict: ...

class Widget:
    """Not inheriting from Drawable, but satisfies the protocol."""
    def __init__(self, label: str):
        self.label = label

    def draw(self) -> str:
        return f"[Widget: {self.label}]"

    def to_dict(self) -> dict:
        return {"label": self.label}

class Button(Widget):
    """Button extends Widget."""
    def __init__(self, label: str, onclick: str = ""):
        super().__init__(label)
        self.onclick = onclick

    def draw(self) -> str:
        return f"[Button: {self.label} -> {self.onclick}]"

# Widget satisfies Drawable protocol without inheriting from it
widget = Widget("Test")
button = Button("Click Me", onclick="submit")

print(f"\nisinstance(widget, Drawable): {isinstance(widget, Drawable)}")  # True
print(f"isinstance(button, Drawable): {isinstance(button, Drawable)}")    # True
print(f"isinstance(widget, Serializable): {isinstance(widget, Serializable)}")  # True

def render(item: Drawable) -> str:
    """Accepts anything that has a draw() method."""
    return item.draw()

print(f"render(widget): {render(widget)}")
print(f"render(button): {render(button)}")
# Output: isinstance(widget, Drawable): True
# Output: isinstance(button, Drawable): True
# Output: isinstance(widget, Serializable): True
# Output: render(widget): [Widget: Test]
# Output: render(button): [Button: Click Me -> submit]


# ============================================================================
# SECTION 7: COMPOSITION OVER INHERITANCE
# ============================================================================
# "Favor composition over inheritance" -- Gang of Four
# Use has-a relationships instead of is-a when possible.

class Logger:
    """Logging component."""
    def log(self, message: str) -> str:
        return f"[LOG] {message}"

class Validator:
    """Validation component."""
    def validate_email(self, email: str) -> bool:
        return "@" in email and "." in email

class UserService:
    """Uses composition: has-a Logger and Validator."""

    def __init__(self):
        self.logger = Logger()           # has-a Logger
        self.validator = Validator()     # has-a Validator
        self.users: dict[str, str] = {}

    def register(self, email: str, name: str) -> str:
        if not self.validator.validate_email(email):
            return self.logger.log(f"Invalid email: {email}")
        self.users[email] = name
        return self.logger.log(f"Registered: {name} ({email})")

service = UserService()
print(f"\n{service.register('alice@example.com', 'Alice')}")
print(f"{service.register('invalid-email', 'Bob')}")
# Output: [LOG] Registered: Alice (alice@example.com)
# Output: [LOG] Invalid email: invalid-email


# ============================================================================
# SECTION 8: CLASS METHODS AND STATIC METHODS
# ============================================================================

class Date:
    """Date with alternative constructors."""

    def __init__(self, year: int, month: int, day: int):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def from_string(cls, date_str: str) -> "Date":
        """Alternative constructor from 'YYYY-MM-DD' string."""
        parts = date_str.split("-")
        return cls(int(parts[0]), int(parts[1]), int(parts[2]))

    @staticmethod
    def is_valid(year: int, month: int, day: int) -> bool:
        """Utility: check if date components are valid."""
        return 1 <= month <= 12 and 1 <= day <= 31 and year > 0

    def __repr__(self) -> str:
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"

d1 = Date(2024, 6, 15)
d2 = Date.from_string("2024-12-25")
print(f"\nd1: {d1}")
print(f"d2: {d2}")
print(f"Date.is_valid(2024, 13, 1): {Date.is_valid(2024, 13, 1)}")
# Output: d1: 2024-06-15
# Output: d2: 2024-12-25
# Output: Date.is_valid(2024, 13, 1): False


# ============================================================================
# MINI-EXERCISES
# ============================================================================

def exercises():
    print("\n" + "=" * 60)
    print("MINI-EXERCISES")
    print("=" * 60)

    print("""
--- Multiple Choice ---

Q1: What does @dataclass automatically generate?
    A) __init__, __repr__, __eq__    B) __init__ only
    C) __str__ and __hash__          D) Nothing
""")
    print("Answer: A) __init__, __repr__, __eq__ (and optionally __hash__, __lt__, etc.)\n")

    print("""
Q2: What is the difference between ABC and Protocol?
    A) ABC uses nominal typing (inheritance); Protocol uses structural typing
    B) ABC is faster than Protocol
    C) Protocol requires inheritance; ABC does not
    D) They are identical
""")
    print("Answer: A) ABC requires explicit inheritance. Protocol matches by structure.\n")

    print("""
Q3: What does @dataclass(frozen=True) do?
    A) Makes the class faster
    B) Makes instances immutable and hashable
    C) Prevents subclassing
    D) Disables __repr__
""")
    print("Answer: B) Frozen dataclasses are immutable and can be dict keys.\n")

    print("""
--- Q&A ---

Q: When should you use inheritance vs composition?
A: Use inheritance for "is-a" (Cat is an Animal).
   Use composition for "has-a" (UserService has a Logger).
   Favor composition when the relationship is about capabilities, not identity.

Q: Why are dunder methods important?
A: They let your objects work with Python's built-in functions and operators.
   __len__ lets len() work. __eq__ lets == work. __iter__ lets for-loops work.

Q: What is MRO?
A: Method Resolution Order -- the order Python searches for methods in
   a class hierarchy. It uses C3 linearization. Check with MyClass.__mro__.
""")


def progress_check():
    print("\n" + "=" * 60)
    print("PROGRESS CHECK")
    print("=" * 60)
    questions = [
        "1. Can you create a dataclass with defaults and field factories?",
        "2. Can you implement common dunder methods (__eq__, __repr__, __len__)?",
        "3. Do you understand the difference between class and instance variables?",
        "4. Can you create and use an abstract base class?",
        "5. Can you define and use a Protocol?",
        "6. Do you know when to use @classmethod vs @staticmethod?",
        "7. Can you explain composition over inheritance?",
        "8. Do you understand MRO?",
        "9. Can you use frozen dataclasses?",
        "10. Can you explain when to use ABC vs Protocol?",
    ]
    print("\nRate your confidence (1-5) for each:\n")
    for q in questions:
        print(f"  {q}")
    print("""
Scoring:
  40-50: Excellent! You understand Python's OOP deeply.
  30-39: Good. Practice building class hierarchies.
  20-29: Focus on dunder methods and dataclasses first.
  < 20:  Start with basic classes, then add features.
""")


def key_takeaways():
    print("\n" + "=" * 60)
    print("KEY TAKEAWAYS")
    print("=" * 60)
    print("""
* @dataclass reduces boilerplate for data containers.
* Dunder methods make objects Pythonic (__len__, __eq__, __iter__, etc.)
* ABC enforces interfaces via inheritance (nominal typing).
* Protocol matches by structure (structural typing, duck typing).
* frozen=True makes dataclass immutable and hashable.
* field(default_factory=list) for mutable defaults in dataclasses.
* Favor composition over inheritance for flexible design.
* @classmethod for alternative constructors; @staticmethod for utilities.
* MRO determines method lookup order in inheritance hierarchies.
* Every class inherits from object.
""")


def transferability():
    print("\n" + "=" * 60)
    print("TRANSFERABILITY TO OTHER LANGUAGES")
    print("=" * 60)
    print("""
Python Concept       | TypeScript           | Rust
---------------------|----------------------|------------------------
dataclass            | interface/type       | struct (derive)
ABC                  | abstract class       | trait (abstract)
Protocol             | interface             | trait
Dunder methods       | Symbol.toPrimitive   | std::ops traits
@classmethod         | static factory       | impl (associated fn)
@staticmethod        | static method        | impl (associated fn)
frozen=True          | readonly interface   | immutable by default
MRO                  | linearization        | N/A (no multiple inherit)
""")


if __name__ == "__main__":
    exercises()
    progress_check()
    key_takeaways()
    transferability()

"""
Atom 01: Variables & Types
==========================
Understanding Python's dynamic type system, references, and mutability.

Architecture:
    Python is dynamically typed -- variables are names bound to objects, not
    boxes holding values. Every value is an object on the heap with a type tag
    and a reference count. The name `x = 42` creates an integer object 42 and
    binds the name `x` to it. Reassigning `x = "hello"` does not change the
    old object; it unbinds `x` from 42 and binds it to a new string object.
    This "name binding" model is the foundation of Python's memory management
    (reference counting + cycle GC).

Transferability:
    - TypeScript: `let x: number = 42` is a typed box; `x = "hello"` is a
      compile error. Python's `x` is more like TypeScript's `let x: unknown`.
    - Rust: Python references resemble `Rc<RefCell<T>>` -- shared, mutable,
      reference-counted. But Python has no borrow checker.
    - Java: Python's `int` is like Java's `Integer` (boxed), not `int` (primitive).

Application:
    - Every Python program. Understanding this prevents subtle bugs with
      default arguments, aliasing, and data corruption.

Run: python variables.py
"""

# ============================================================================
# SECTION 1: NAME BINDING (Assignment)
# ============================================================================
# In Python, assignment is NOT copying a value into a variable.
# It BINDS a name to an object.

x = 42          # Name `x` -> int object 42 (refcount=1)
y = x           # Name `y` -> SAME int object 42 (refcount=2)
print(f"x={x}, y={y}")
# Output: x=42, y=42

# Proof: both names point to the same object
print(f"x is y: {x is y}")   # True -- identity check
print(f"id(x) == id(y): {id(x) == id(y)}")  # True
# Output: x is y: True
# Output: id(x) == id(y): True

# Rebinding x does NOT affect y
x = 100
print(f"After rebind: x={x}, y={y}")
# Output: After rebind: x=100, y=42
# y still points to the original 42 object.


# ============================================================================
# SECTION 2: DYNAMIC TYPING
# ============================================================================
# A name can be rebound to any type at any time.
# Type is a property of the OBJECT, not the name.

value = 42              # int
print(f"value={value}, type={type(value)}")
# Output: value=42, type=<class 'int'>

value = "hello"         # now a str
print(f"value={value}, type={type(value)}")
# Output: value=hello, type=<class 'str'>

value = [1, 2, 3]       # now a list
print(f"value={value}, type={type(value)}")
# Output: value=[1, 2, 3], type=<class 'list'>

# Runtime type checking
print(f"isinstance(42, int): {isinstance(42, int)}")       # True
print(f"isinstance(42, (int, str)): {isinstance(42, (int, str))}")  # True
print(f"type(42) is int: {type(42) is int}")               # True


# ============================================================================
# SECTION 3: MUTABILITY vs IMMUTABILITY
# ============================================================================
# Immutable objects (int, str, tuple, frozenset, bytes) cannot be changed.
# Mutable objects (list, dict, set, bytearray) CAN be changed in place.

# --- Immutable example: str ---
original = "hello"
modified = original.upper()   # Creates a NEW string object
print(f"original: {original}")  # "hello" -- unchanged
print(f"modified: {modified}")  # "HELLO" -- new object
print(f"original is modified: {original is modified}")  # False
# Output: original: hello
# Output: modified: HELLO
# Output: original is modified: False

# --- Mutable example: list ---
a = [1, 2, 3]
b = a             # b and a refer to the SAME list object
b.append(4)       # Mutate the object in place
print(f"a: {a}")  # [1, 2, 3, 4] -- a is also affected!
print(f"b: {b}")  # [1, 2, 3, 4]
print(f"a is b: {a is b}")  # True
# Output: a: [1, 2, 3, 4]
# Output: b: [1, 2, 3, 4]
# Output: a is b: True

# How to create an independent copy:
c = a.copy()      # or a[:] or list(a)
c.append(5)
print(f"After copy+append: a={a}, c={c}")
# Output: After copy+append: a=[1, 2, 3, 4], c=[1, 2, 3, 4, 5]


# ============================================================================
# SECTION 4: IDENTITY vs EQUALITY
# ============================================================================
# `is` checks identity (same object in memory)
# `==` checks equality (same value)

a = [1, 2, 3]
b = [1, 2, 3]     # Different object, same value
print(f"a == b: {a == b}")   # True  -- same content
print(f"a is b: {a is b}")   # False -- different objects
# Output: a == b: True
# Output: a is b: False

# Small integers are cached (-5 to 256), so identity may coincidentally hold
x = 256
y = 256
print(f"256: x is y = {x is y}")   # True (cached)
x = 257
y = 257
print(f"257: x is y = {x is y}")   # False (not cached, usually)
# Output: 256: x is y = True
# Output: 257: x is y = False

# ALWAYS use `==` for value comparison.
# Use `is` only for singletons: None, True, False
flag = None
print(f"flag is None: {flag is None}")   # Correct way
# Output: flag is None: True


# ============================================================================
# SECTION 5: TYPE HIERARCHY
# ============================================================================
# Python's type system is a hierarchy. Everything inherits from object.
# Numbers: int, float, complex
# Sequences: str, list, tuple, range, bytes
# Mappings: dict
# Sets: set, frozenset
# Other: bool, NoneType, type

print(f"int MRO: {int.__mro__}")
# Output: int MRO: (<class 'int'>, <class 'object'>)

print(f"bool is subclass of int: {issubclass(bool, int)}")  # True!
# In Python, bool IS an int subclass: True == 1, False == 0
print(f"True + True = {True + True}")  # 2
# Output: True + True = 2

# Useful type conversions
print(int("42"))          # 42
print(float("3.14"))      # 3.14
print(str(42))            # "42"
print(list("abc"))        # ['a', 'b', 'c']
print(tuple([1, 2]))      # (1, 2)
print(set([1, 1, 2]))     # {1, 2}


# ============================================================================
# SECTION 6: SHALLOW vs DEEP COPY
# ============================================================================
import copy

# Shallow copy: copies the outer container, but inner elements are still
# references to the same objects.
outer = [[1, 2], [3, 4]]
shallow = copy.copy(outer)
shallow[0].append(999)
print(f"outer after shallow[0].append(999): {outer}")
# Output: outer after shallow[0].append(999): [[1, 2, 999], [3, 4]]
# The inner list is shared!

# Deep copy: recursively copies everything.
outer2 = [[1, 2], [3, 4]]
deep = copy.deepcopy(outer2)
deep[0].append(999)
print(f"outer2 after deep[0].append(999): {outer2}")
# Output: outer2 after deep[0].append(999): [[1, 2], [3, 4]]
# Completely independent.


# ============================================================================
# SECTION 7: DEFAULT ARGUMENTS (Mutable Default Trap)
# ============================================================================

# WRONG: mutable default is evaluated ONCE at function definition time
def append_to_bad(element, target=[]):
    target.append(element)
    return target

print(append_to_bad(1))  # [1]
print(append_to_bad(2))  # [1, 2] -- BUG! Same list reused.
print(append_to_bad(3))  # [1, 2, 3]
# Output: [1]
# Output: [1, 2]
# Output: [1, 2, 3]

# CORRECT: use None as sentinel
def append_to_good(element, target=None):
    if target is None:
        target = []
    target.append(element)
    return target

print(append_to_good(1))  # [1]
print(append_to_good(2))  # [2] -- fresh list each time
# Output: [1]
# Output: [2]


# ============================================================================
# SECTION 8: UNPACKING
# ============================================================================

# Tuple/list unpacking
a, b, c = [1, 2, 3]
print(f"a={a}, b={b}, c={c}")
# Output: a=1, b=2, c=3

# Star unpacking (Python 3+)
first, *rest = [1, 2, 3, 4, 5]
print(f"first={first}, rest={rest}")
# Output: first=1, rest=[2, 3, 4, 5]

*init, last = [1, 2, 3, 4, 5]
print(f"init={init}, last={last}")
# Output: init=[1, 2, 3, 4], last=5

# Swapping
x, y = 1, 2
x, y = y, x
print(f"After swap: x={x}, y={y}")
# Output: After swap: x=2, y=1

# Dict unpacking
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
merged = {**d1, **d2}
print(f"Merged: {merged}")  # {'a': 1, 'b': 3, 'c': 4} -- d2 wins on 'b'
# Output: Merged: {'a': 1, 'b': 3, 'c': 4}


# ============================================================================
# MINI-EXERCISES
# ============================================================================

def exercises():
    """Run through exercises to test understanding."""

    print("\n" + "=" * 60)
    print("MINI-EXERCISES")
    print("=" * 60)

    # --- Multiple Choice ---
    print("\n--- Multiple Choice ---")

    # Q1
    print("""
Q1: What does this output?
    a = [1, 2, 3]
    b = a
    b.append(4)
    print(len(a))

    A) 3    B) 4    C) Error    D) None
""")
    print("Answer: B) 4 -- b and a refer to the same list object.\n")

    # Q2
    print("""
Q2: What does `type(True)` return?
    A) <class 'bool'>    B) <class 'int'>
    C) <class 'str'>     D) <class 'object'>
""")
    print("Answer: A) <class 'bool'> -- bool is a subclass of int, "
          "but type(True) is bool.\n")

    # Q3
    print("""
Q3: Which comparison checks if two variables point to the same object?
    A) ==     B) is     C) =      D) !=
""")
    print("Answer: B) `is` checks identity (same object in memory).\n")

    # --- Q&A ---
    print("\n--- Q&A ---")

    print("""
Q: Why does this happen?
    x = 256
    y = 256
    print(x is y)  # True
    x = 257
    y = 257
    print(x is y)  # False (usually)

A: Python caches small integers (-5 to 256) as singletons.
   256 is in the cache range, so both names point to the same object.
   257 is not cached, so two separate objects are created.
   NEVER rely on this -- always use == for value comparison.
""")

    print("""
Q: How do you safely copy a nested list?
A: Use copy.deepcopy(). A shallow copy (list.copy() or copy.copy())
   only copies the outer container. Inner elements are still shared.
""")

    print("""
Q: Why is `def f(x=[])` dangerous?
A: The default list is created ONCE when the function is defined,
   not each time it's called. All calls share the same list.
   Use `def f(x=None)` and `if x is None: x = []` instead.
""")


# ============================================================================
# PROGRESS CHECK
# ============================================================================

def progress_check():
    """Self-assessment to gauge understanding."""

    print("\n" + "=" * 60)
    print("PROGRESS CHECK")
    print("=" * 60)

    questions = [
        "1. Can you explain the difference between `is` and `==`?",
        "2. What happens when you do `b = a` where a is a list?",
        "3. Why does `b = a` not create a copy?",
        "4. What is the mutable default argument trap?",
        "5. How do you safely copy a nested list?",
        "6. What types are immutable in Python?",
        "7. Why is `bool` a subclass of `int`?",
        "8. What does `*rest` do in unpacking?",
        "9. When should you use `is` instead of `==`?",
        "10. What is the difference between shallow and deep copy?",
    ]

    print("\nRate your confidence (1-5) for each:\n")
    for q in questions:
        print(f"  {q}")

    print("""
Scoring:
  40-50: Excellent! Move to the next atom.
  30-39: Good foundation. Review weak areas.
  20-29: Re-read the sections you scored low on.
  < 20:  No rush. Work through the examples again.
""")


# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

def key_takeaways():
    print("\n" + "=" * 60)
    print("KEY TAKEAWAYS")
    print("=" * 60)
    print("""
* Python variables are NAME BINDINGS, not typed boxes.
* Assignment creates a reference, not a copy.
* `is` checks identity; `==` checks equality. Use `==` for values.
* Mutable objects (list, dict, set) can be changed in place.
* Immutable objects (int, str, tuple) create new objects on "change".
* Shallow copy copies the container; deep copy copies everything.
* Never use mutable objects as default arguments.
* Python caches small integers (-5 to 256) -- do not rely on this.
* Use unpacking for clean, readable assignments.
* type() returns the exact type; isinstance() handles inheritance.
""")


# ============================================================================
# TRANSFERABILITY MAP
# ============================================================================

def transferability():
    print("\n" + "=" * 60)
    print("TRANSFERABILITY TO OTHER LANGUAGES")
    print("=" * 60)
    print("""
Python Concept       | TypeScript           | Rust
---------------------|----------------------|------------------------
Dynamic typing       | let x: unknown       | No equivalent (static)
Name binding         | Reference semantics   | let (move/copy)
Mutable default      | N/A (no default expr) | N/A (no default expr)
Shallow copy         | { ...obj } / [...a]  | .clone() (deep by default)
Deep copy            | structuredClone()     | .clone() (if impl)
is vs ==             | === vs Object.is()   | == vs ptr::eq()
Unpacking            | Destructuring        | Pattern matching
""")


# ============================================================================
# MAIN: Run all sections
# ============================================================================

if __name__ == "__main__":
    exercises()
    progress_check()
    key_takeaways()
    transferability()

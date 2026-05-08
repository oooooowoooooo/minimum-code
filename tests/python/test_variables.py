"""
Tests for Atom 01: Variables & Types
=====================================
Validates understanding of name binding, mutability, identity, copying,
and the mutable default argument trap.
"""

import copy
import pytest


# ============================================================================
# NAME BINDING TESTS
# ============================================================================

class TestNameBinding:
    """Variables are names bound to objects, not typed boxes."""

    def test_assignment_binds_name(self):
        """Assignment binds a name to an object."""
        x = 42
        assert x == 42

    def test_rebinding_changes_reference(self):
        """Rebinding a name points it to a different object."""
        x = 42
        y = x
        x = 100
        assert x == 100
        assert y == 42  # y still points to original object

    def test_multiple_names_same_object(self):
        """Multiple names can refer to the same object."""
        a = [1, 2, 3]
        b = a
        assert a is b  # Same object
        assert id(a) == id(b)

    def test_rebinding_does_not_affect_other_names(self):
        """Rebinding one name does not affect other names bound to same object."""
        x = [1, 2, 3]
        y = x
        x = [4, 5, 6]  # Rebind x to new list
        assert y == [1, 2, 3]  # y unchanged


# ============================================================================
# DYNAMIC TYPING TESTS
# ============================================================================

class TestDynamicTyping:
    """Python is dynamically typed -- type is a property of the object."""

    def test_name_can_change_type(self):
        """A name can be rebound to a different type."""
        x = 42
        assert isinstance(x, int)
        x = "hello"
        assert isinstance(x, str)
        x = [1, 2, 3]
        assert isinstance(x, list)

    def test_type_function(self):
        """type() returns the exact type of an object."""
        assert type(42) is int
        assert type("hello") is str
        assert type([1, 2]) is list
        assert type(True) is bool

    def test_isinstance_with_tuple(self):
        """isinstance() can check against multiple types."""
        assert isinstance(42, (int, str))
        assert isinstance("hello", (int, str))
        assert not isinstance([1], (int, str))

    def test_isinstance_respects_inheritance(self):
        """isinstance() returns True for parent types."""
        assert isinstance(True, bool)
        assert isinstance(True, int)  # bool is a subclass of int
        assert isinstance(True, (int,))


# ============================================================================
# MUTABILITY TESTS
# ============================================================================

class TestMutability:
    """Immutable objects cannot be changed; mutable objects can."""

    def test_string_is_immutable(self):
        """Strings are immutable -- methods return new objects."""
        s = "hello"
        s_upper = s.upper()
        assert s == "hello"  # Original unchanged
        assert s_upper == "HELLO"
        assert s is not s_upper

    def test_int_is_immutable(self):
        """Integers are immutable."""
        x = 42
        y = x
        x = x + 1
        assert x == 43
        assert y == 42

    def test_list_is_mutable(self):
        """Lists can be changed in place."""
        a = [1, 2, 3]
        b = a
        b.append(4)
        assert a == [1, 2, 3, 4]  # a is also affected
        assert a is b

    def test_dict_is_mutable(self):
        """Dicts can be changed in place."""
        d = {"a": 1}
        d2 = d
        d2["b"] = 2
        assert d == {"a": 1, "b": 2}

    def test_set_is_mutable(self):
        """Sets can be changed in place."""
        s = {1, 2, 3}
        s2 = s
        s2.add(4)
        assert 4 in s

    def test_tuple_is_immutable(self):
        """Tuples cannot be changed in place."""
        t = (1, 2, 3)
        with pytest.raises(TypeError):
            t[0] = 99  # type: ignore

    def test_frozenset_is_immutable(self):
        """Frozensets cannot be changed in place."""
        fs = frozenset([1, 2, 3])
        assert 1 in fs
        # frozenset has no add/remove methods


# ============================================================================
# IDENTITY vs EQUALITY TESTS
# ============================================================================

class TestIdentityVsEquality:
    """`is` checks identity; `==` checks equality."""

    def test_equality_with_different_objects(self):
        """Two different objects can be equal."""
        a = [1, 2, 3]
        b = [1, 2, 3]
        assert a == b   # Same value
        assert a is not b  # Different objects

    def test_identity_with_same_object(self):
        """Same object is identical to itself."""
        a = [1, 2, 3]
        b = a
        assert a is b

    def test_none_identity(self):
        """Use `is` to check for None."""
        x = None
        assert x is None
        assert not (x is not None)

    def test_small_int_caching(self):
        """Small integers (-5 to 256) are cached singletons."""
        a = 256
        b = 256
        assert a is b  # Cached

    def test_large_int_not_cached(self):
        """Large integers are NOT cached (usually)."""
        a = 257
        b = 257
        # In CPython, this is False when run as separate statements,
        # but may be True in the same code block due to compiler optimization.
        # The key lesson: never rely on `is` for value comparison.
        assert a == b  # Always check value with ==


# ============================================================================
# COPY TESTS
# ============================================================================

class TestCopying:
    """Shallow copy copies the container; deep copy copies everything."""

    def test_shallow_copy_shared_inner(self):
        """Shallow copy shares inner mutable objects."""
        original = [[1, 2], [3, 4]]
        shallow = copy.copy(original)
        shallow[0].append(999)
        assert original[0] == [1, 2, 999]  # Inner list is shared

    def test_deep_copy_independent(self):
        """Deep copy creates fully independent objects."""
        original = [[1, 2], [3, 4]]
        deep = copy.deepcopy(original)
        deep[0].append(999)
        assert original[0] == [1, 2]  # Inner list is independent

    def test_list_copy_method(self):
        """list.copy() creates a shallow copy."""
        a = [[1], [2]]
        b = a.copy()
        b[0].append(99)
        assert a[0] == [1, 99]  # Shared inner list

    def test_slice_copy(self):
        """Slice [:] creates a shallow copy."""
        a = [[1], [2]]
        b = a[:]
        b[0].append(99)
        assert a[0] == [1, 99]  # Shared inner list


# ============================================================================
# MUTABLE DEFAULT ARGUMENT TESTS
# ============================================================================

class TestMutableDefault:
    """Mutable default arguments are evaluated once at definition time."""

    def test_mutable_default_is_shared(self):
        """Mutable default list is shared across calls."""
        def append_to(element, target=[]):
            target.append(element)
            return target

        result1 = append_to(1)
        result2 = append_to(2)
        assert result1 == [1, 2]  # BUG: result1 is the same list as result2
        assert result1 is result2

    def test_none_sentinel_pattern(self):
        """Using None as default avoids the shared list trap."""
        def append_to(element, target=None):
            if target is None:
                target = []
            target.append(element)
            return target

        result1 = append_to(1)
        result2 = append_to(2)
        assert result1 == [1]
        assert result2 == [2]
        assert result1 is not result2

    def test_immutable_default_is_fine(self):
        """Immutable defaults (int, str, tuple) are safe."""
        def add(a, b=0):
            return a + b

        assert add(5) == 5
        assert add(5, 10) == 15


# ============================================================================
# UNPACKING TESTS
# ============================================================================

class TestUnpacking:
    """Python supports tuple/list unpacking and star expressions."""

    def test_basic_unpacking(self):
        """Basic tuple unpacking."""
        a, b, c = [1, 2, 3]
        assert a == 1
        assert b == 2
        assert c == 3

    def test_star_unpacking_rest(self):
        """Star expression captures remaining elements."""
        first, *rest = [1, 2, 3, 4, 5]
        assert first == 1
        assert rest == [2, 3, 4, 5]

    def test_star_unpacking_init(self):
        """Star expression at the beginning."""
        *init, last = [1, 2, 3, 4, 5]
        assert init == [1, 2, 3, 4]
        assert last == 5

    def test_swap(self):
        """Pythonic swap using tuple unpacking."""
        x, y = 1, 2
        x, y = y, x
        assert x == 2
        assert y == 1

    def test_dict_unpacking_merge(self):
        """Dict unpacking with ** for merging."""
        d1 = {"a": 1, "b": 2}
        d2 = {"b": 3, "c": 4}
        merged = {**d1, **d2}
        assert merged == {"a": 1, "b": 3, "c": 4}  # d2 wins on 'b'

    def test_nested_unpacking(self):
        """Unpacking works with nested structures."""
        (a, b), (c, d) = [(1, 2), (3, 4)]
        assert a == 1 and b == 2
        assert c == 3 and d == 4


# ============================================================================
# TYPE HIERARCHY TESTS
# ============================================================================

class TestTypeHierarchy:
    """Python's type hierarchy and useful conversions."""

    def test_bool_is_int_subclass(self):
        """bool is a subclass of int."""
        assert issubclass(bool, int)
        assert True + True == 2
        assert False + False == 0

    def test_int_inherits_from_object(self):
        """All types inherit from object."""
        assert issubclass(int, object)
        assert issubclass(str, object)
        assert issubclass(list, object)

    def test_type_conversions(self):
        """Common type conversions work as expected."""
        assert int("42") == 42
        assert float("3.14") == 3.14
        assert str(42) == "42"
        assert list("abc") == ["a", "b", "c"]
        assert tuple([1, 2]) == (1, 2)
        assert set([1, 1, 2]) == {1, 2}

    def test_none_is_singleton(self):
        """None is a singleton -- use `is` to check."""
        x = None
        y = None
        assert x is y
        assert type(None).__name__ == "NoneType"

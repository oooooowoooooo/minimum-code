"""
Tests for Atom 06: Modules & Packages
======================================
Validates import system, __init__.py, __all__, dynamic imports,
circular import handling, and package structure.
"""

import importlib
import sys
import os
import pytest
from pathlib import Path
from types import ModuleType
from collections import Counter, defaultdict, OrderedDict
import collections


# ============================================================================
# MODULE BASICS TESTS
# ============================================================================

class TestModuleBasics:
    """Test basic module concepts."""

    def test_import_standard_library(self):
        """Standard library modules can be imported."""
        import math
        assert math.pi == 3.141592653589793

    def test_import_creates_module_object(self):
        """Importing creates a module object in sys.modules."""
        import json
        assert "json" in sys.modules
        assert isinstance(sys.modules["json"], ModuleType)

    def test_module_has_name(self):
        """Modules have a __name__ attribute."""
        import math
        assert math.__name__ == "math"

    def test_module_has_file(self):
        """Modules have a __file__ attribute."""
        import json
        assert json.__file__ is not None
        assert json.__file__.endswith(".py")

    def test_main_module_name(self):
        """The main module has __name__ == '__main__' when run directly."""
        # When run via pytest, __name__ is the test module name
        assert isinstance(__name__, str)


# ============================================================================
# IMPORT STYLES TESTS
# ============================================================================

class TestImportStyles:
    """Test different import syntaxes."""

    def test_import_module(self):
        """import module -- access via module.name."""
        import json
        result = json.dumps({"key": "value"})
        assert '"key"' in result

    def test_import_module_alias(self):
        """import module as alias."""
        import json as j
        result = j.dumps([1, 2, 3])
        assert result == "[1, 2, 3]"

    def test_from_import(self):
        """from module import name."""
        from json import loads
        result = loads('{"a": 1}')
        assert result == {"a": 1}

    def test_from_import_alias(self):
        """from module import name as alias."""
        from json import loads as parse
        result = parse('[1, 2, 3]')
        assert result == [1, 2, 3]

    def test_from_import_multiple(self):
        """from module import name1, name2."""
        from collections import Counter, defaultdict
        c = Counter([1, 1, 2])
        d = defaultdict(int)
        assert c[1] == 2
        assert d["missing"] == 0


# ============================================================================
# __all__ TESTS
# ============================================================================

class TestAll:
    """Test __all__ for controlling wildcard imports."""

    def test_all_controls_wildcard(self):
        """__all__ defines what from module import * exposes."""
        import types
        mod = types.ModuleType("test_all_mod")
        mod.public_func = lambda: "public"
        mod._private_func = lambda: "private"
        mod.__all__ = ["public_func"]

        assert "public_func" in mod.__all__
        assert "_private_func" not in mod.__all__

    def test_all_is_list_of_strings(self):
        """__all__ should be a list of strings."""
        assert isinstance(collections.__all__, list)
        assert all(isinstance(name, str) for name in collections.__all__)

    def test_all_includes_expected_names(self):
        """__all__ includes the module's public names."""
        expected = ["Counter", "defaultdict", "OrderedDict"]
        for name in expected:
            assert name in collections.__all__

    def test_json_all(self):
        """json module has __all__ with expected names."""
        import json
        assert hasattr(json, "__all__")
        assert "loads" in json.__all__
        assert "dumps" in json.__all__


# ============================================================================
# DYNAMIC IMPORT TESTS
# ============================================================================

class TestDynamicImport:
    """Test importlib for dynamic imports."""

    def test_import_module_by_string(self):
        """importlib.import_module imports by string name."""
        mod = importlib.import_module("json")
        assert hasattr(mod, "dumps")
        assert hasattr(mod, "loads")

    def test_import_submodule(self):
        """importlib can import submodules."""
        mod = importlib.import_module("os.path")
        assert hasattr(mod, "join")

    def test_import_and_getattr(self):
        """Combine importlib with getattr for dynamic attribute access."""
        mod = importlib.import_module("collections")
        cls = getattr(mod, "Counter")
        result = cls([1, 1, 2, 3])
        assert result[1] == 2

    def test_reload_module(self):
        """importlib.reload() re-executes a module."""
        import json
        reloaded = importlib.reload(json)
        assert reloaded is json
        assert hasattr(reloaded, 'loads')

    def test_import_nonexistent_raises(self):
        """Importing a nonexistent module raises ImportError."""
        with pytest.raises(ModuleNotFoundError):
            importlib.import_module("nonexistent_module_xyz")


# ============================================================================
# PACKAGE STRUCTURE TESTS
# ============================================================================

class TestPackageStructure:
    """Test package structure concepts."""

    def test_init_file(self):
        """__init__.py makes a directory a package."""
        init_path = Path(__file__).parent.parent.parent / "src" / "python" / "fundamentals" / "__init__.py"
        assert init_path.exists()

    def test_module_dunder_name(self):
        """Module __name__ reflects its import path."""
        import json
        assert json.__name__ == "json"

    def test_module_dunder_file(self):
        """Module __file__ points to the .py file."""
        import json
        assert json.__file__ is not None
        assert json.__file__.endswith(".py")

    def test_module_dunder_doc(self):
        """Modules can have docstrings."""
        import json
        assert json.__doc__ is not None
        assert len(json.__doc__) > 0


# ============================================================================
# CIRCULAR IMPORT HANDLING TESTS
# ============================================================================

class TestCircularImport:
    """Test patterns for avoiding circular imports."""

    def test_lazy_import_pattern(self):
        """Lazy import defers import to function call time."""
        def get_counter():
            from collections import Counter
            return Counter([1, 1, 2])

        result = get_counter()
        assert result[1] == 2

    def test_import_inside_function(self):
        """Import inside function works correctly."""
        def process(data):
            import json
            return json.dumps(data)

        result = process({"key": "value"})
        assert '"key"' in result

    def test_type_checking_guard(self):
        """TYPE_CHECKING guard for type-only imports."""
        from typing import TYPE_CHECKING
        assert TYPE_CHECKING is False


# ============================================================================
# sys.path TESTS
# ============================================================================

class TestSysPath:
    """Test sys.path and module search."""

    def test_sys_path_is_list(self):
        """sys.path is a list of directory paths."""
        assert isinstance(sys.path, list)
        assert len(sys.path) > 0

    def test_sys_path_contains_current_dir(self):
        """sys.path typically includes the current directory or ''."""
        assert "" in sys.path or any(
            os.getcwd() in p for p in sys.path
        )

    def test_sys_path_contains_site_packages(self):
        """sys.path includes site-packages."""
        assert any("site-packages" in p for p in sys.path)


# ============================================================================
# MODULE-LEVEL PATTERNS TESTS
# ============================================================================

class TestModulePatterns:
    """Test common module-level patterns."""

    def test_module_level_constants(self):
        """Module-level constants are accessible."""
        DEFAULT_TIMEOUT = 30
        MAX_RETRIES = 3
        assert DEFAULT_TIMEOUT == 30
        assert MAX_RETRIES == 3

    def test_sentinel_pattern(self):
        """Sentinel object pattern for distinguishing None from missing."""
        _MISSING = object()

        def get(data, key, default=_MISSING):
            if key in data:
                return data[key]
            if default is not _MISSING:
                return default
            raise KeyError(key)

        assert get({"a": 1}, "a") == 1
        assert get({"a": 1}, "b", "default") == "default"
        with pytest.raises(KeyError):
            get({"a": 1}, "b")

    def test_logger_pattern(self):
        """Module-level logger using __name__."""
        import logging
        logger = logging.getLogger(__name__)
        assert isinstance(logger, logging.Logger)
        assert logger.name == __name__


# ============================================================================
# PRACTICAL IMPORT TESTS
# ============================================================================

class TestPracticalImports:
    """Test practical import scenarios."""

    def test_import_with_side_effects(self):
        """Some imports have side effects (like registering codecs)."""
        assert "json" in sys.modules
        assert "os" in sys.modules
        assert "sys" in sys.modules

    def test_conditional_import(self):
        """Import only if available."""
        result = None
        try:
            import nonexistent_module  # type: ignore
            result = "available"
        except ImportError:
            result = "not available"
        assert result == "not available"

    def test_import_from_string(self):
        """Dynamic import from string (plugin pattern)."""
        module_name = "collections"
        attr_name = "Counter"

        mod = importlib.import_module(module_name)
        cls = getattr(mod, attr_name)
        assert cls.__name__ == "Counter"


# ============================================================================
# PACKAGE CREATION TESTS
# ============================================================================

class TestPackageCreation:
    """Test creating packages programmatically."""

    def test_create_package_structure(self, tmp_path):
        """Create a package structure and verify it works."""
        pkg_dir = tmp_path / "mypkg"
        pkg_dir.mkdir()

        init_file = pkg_dir / "__init__.py"
        init_file.write_text(
            'from .core import hello\n'
            '__all__ = ["hello"]\n'
        )

        core_file = pkg_dir / "core.py"
        core_file.write_text(
            'def hello():\n'
            '    return "Hello from mypkg!"\n'
        )

        sys.path.insert(0, str(tmp_path))
        try:
            mod = importlib.import_module("mypkg")
            assert hasattr(mod, "hello")
            assert mod.hello() == "Hello from mypkg!"
            assert mod.__all__ == ["hello"]
        finally:
            sys.path.remove(str(tmp_path))
            if "mypkg" in sys.modules:
                del sys.modules["mypkg"]
            if "mypkg.core" in sys.modules:
                del sys.modules["mypkg.core"]

    def test_subpackage(self, tmp_path):
        """Create a package with sub-packages."""
        pkg_dir = tmp_path / "mainpkg"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("")

        sub_dir = pkg_dir / "sub"
        sub_dir.mkdir()
        (sub_dir / "__init__.py").write_text(
            'from .utils import helper\n'
        )
        (sub_dir / "utils.py").write_text(
            'def helper():\n'
            '    return "helper result"\n'
        )

        sys.path.insert(0, str(tmp_path))
        try:
            mod = importlib.import_module("mainpkg.sub")
            assert hasattr(mod, "helper")
            assert mod.helper() == "helper result"
        finally:
            sys.path.remove(str(tmp_path))
            for key in list(sys.modules.keys()):
                if key.startswith("mainpkg"):
                    del sys.modules[key]

    def test_package_with_all(self, tmp_path):
        """Package with __all__ controls exports."""
        pkg_dir = tmp_path / "controlled"
        pkg_dir.mkdir()

        init_file = pkg_dir / "__init__.py"
        init_file.write_text(
            'from .a import func_a\n'
            'from .b import func_b\n'
            'from .c import func_c\n'
            '__all__ = ["func_a", "func_b"]\n'  # func_c not exported
        )

        (pkg_dir / "a.py").write_text('def func_a(): return "a"\n')
        (pkg_dir / "b.py").write_text('def func_b(): return "b"\n')
        (pkg_dir / "c.py").write_text('def func_c(): return "c"\n')

        sys.path.insert(0, str(tmp_path))
        try:
            mod = importlib.import_module("controlled")
            assert mod.__all__ == ["func_a", "func_b"]
            assert "func_c" not in mod.__all__
        finally:
            sys.path.remove(str(tmp_path))
            for key in list(sys.modules.keys()):
                if key.startswith("controlled"):
                    del sys.modules[key]

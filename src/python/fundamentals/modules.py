"""
Atom 06: Modules & Packages
=============================
Python's import system, package structure, and module organization.

Architecture:
    Python's module system is based on the filesystem:
    - A .py file is a module
    - A directory with __init__.py is a package
    - Packages can contain sub-packages (nesting)
    - import searches sys.path for modules

    The import system has several important features:
    - __init__.py controls what `from package import *` exposes (__all__)
    - __all__ is a list of public names
    - Relative imports (from . import x) work within packages
    - importlib provides programmatic import capabilities
    - Circular imports are a common pitfall

    Modern Python (3.3+) supports namespace packages (no __init__.py),
    but __init__.py is still recommended for clarity and __all__ control.

Transferability:
    - TypeScript: ES modules (import/export) are similar. package.json
      is like __init__.py. npm is like PyPI.
    - Rust: mod keyword for modules, crate for packages. Cargo.toml
      is like setup.py/pyproject.toml.
    - Java: packages map to directories. import is similar.

Application:
    - Every Python project uses modules and packages.
    - __init__.py is used to expose public API.
    - __all__ controls wildcard imports.
    - Dynamic imports are used for plugin systems.

Run: python modules.py
"""

import importlib
import sys
from pathlib import Path


## ============================================================================
# SECTION 1: MODULE BASICS
## ============================================================================
# A module is any .py file. Importing it executes the file and creates
# a module object with all top-level names.

# This file itself is a module: src.python.fundamentals.modules
# Its __name__ is "__main__" when run directly
print(f"This module's __name__: {__name__}")
# Output: This module's __name__: __main__

# Common module attributes
print(f"This file: {__file__}")
# Output: This file: /path/to/modules.py

# Importing standard library modules
import os
import json
import math

print(f"math.pi: {math.pi}")
print(f"os.getcwd(): {os.getcwd()}")
# Output: math.pi: 3.141592653589793
# Output: os.getcwd(): /path/to/current/dir


## ============================================================================
# SECTION 2: IMPORT STYLES
## ============================================================================
# There are several ways to import modules.

# 1. import module
import collections
counter = collections.Counter([1, 1, 2, 3])
print(f"Counter: {counter}")
# Output: Counter: Counter({1: 2, 2: 1, 3: 1})

# 2. import module as alias
import collections as coll
deque = coll.deque([1, 2, 3])
print(f"deque: {deque}")
# Output: deque: deque([1, 2, 3])

# 3. from module import name
from collections import Counter, defaultdict
print(f"Counter: {Counter([1, 1, 2])}")
# Output: Counter: Counter({1: 2, 2: 1})

# 4. from module import name as alias
from collections import OrderedDict as OD
d = OD([("b", 2), ("a", 1)])
print(f"OrderedDict: {d}")
# Output: OrderedDict: OrderedDict([('b', 2), ('a', 1)])

# 5. from module import * (discouraged -- pollutes namespace)
# from collections import *  # DON'T DO THIS


## ============================================================================
# SECTION 3: __init__.py AND PACKAGES
## ============================================================================
# A directory with __init__.py is a package.
# __init__.py can:
# 1. Be empty (just marks the directory as a package)
# 2. Import and re-export names for convenience
# 3. Define __all__ to control `from package import *`

# Example package structure:
# mypackage/
#     __init__.py       # from .core import main; __all__ = ["main"]
#     core.py           # def main(): ...
#     utils.py          # def helper(): ...
#     subpackage/
#         __init__.py
#         deep.py       # def deep_func(): ...

# When you do `import mypackage`, __init__.py runs.
# When you do `from mypackage import main`, __init__.py's import is used.

# Demonstration: creating a mini package structure
def show_package_structure():
    """Show what a typical package looks like."""
    structure = """
mypackage/
    __init__.py          # Controls public API, re-exports
    core.py              # Main functionality
    utils.py             # Utility functions
    config.py            # Configuration
    models/              # Sub-package
        __init__.py      # from .user import User
        user.py          # class User: ...
        product.py       # class Product: ...
    tests/               # Test package
        __init__.py
        test_core.py
    pyproject.toml       # Package metadata
"""
    print(f"Package structure:{structure}")


## ============================================================================
# SECTION 4: __all__ AND PUBLIC API
## ============================================================================
# __all__ is a list of strings that defines what `from module import *` exposes.
# It's the public API of your module/package.

# Example: what __init__.py should contain
EXAMPLE_INIT = '''
# mypackage/__init__.py

from .core import process, validate
from .models.user import User
from .models.product import Product

__all__ = [
    "process",
    "validate",
    "User",
    "Product",
]

__version__ = "1.0.0"
'''
print(f"\nExample __init__.py:\n{EXAMPLE_INIT}")

# Without __all__, `from module import *` exports everything that doesn't
# start with underscore.
# With __all__, ONLY the listed names are exported.


## ============================================================================
# SECTION 5: RELATIVE IMPORTS
## ============================================================================
# Within a package, use relative imports with dots:
# from . import sibling_module
# from .sibling import function
# from .. import parent_module
# from ..sibling import function

RELATIVE_IMPORTS = '''
# In mypackage/models/user.py:

# Import from same package (models/)
from .product import Product

# Import from parent package (mypackage/)
from ..core import validate
from ..utils import hash_password

# Import from parent's sibling
from ..config import DATABASE_URL
'''
print(f"\nRelative imports:\n{RELATIVE_IMPORTS}")


## ============================================================================
# SECTION 6: DYNAMIC IMPORTS (importlib)
## ============================================================================
# importlib allows importing modules by string name at runtime.
# Used for plugin systems, lazy loading, and configuration-driven imports.

def dynamic_import_example():
    """Demonstrate dynamic imports."""

    # Import a module by name
    module_name = "json"
    module = importlib.import_module(module_name)
    data = module.loads('{"key": "value"}')
    print(f"Dynamic import '{module_name}': {data}")
    # Output: Dynamic import 'json': {'key': 'value'}

    # Import a specific attribute
    module_name = "collections"
    attr_name = "Counter"
    module = importlib.import_module(module_name)
    cls = getattr(module, attr_name)
    counter = cls([1, 1, 2, 3])
    print(f"Dynamic import {module_name}.{attr_name}: {counter}")
    # Output: Dynamic import collections.Counter: Counter({1: 2, 2: 1, 3: 1})

    # Reload a module (useful during development)
    import json as json_module
    reloaded = importlib.reload(json_module)
    print(f"Reloaded module: {reloaded.__name__}")
    # Output: Reloaded module: json


## ============================================================================
# SECTION 7: CIRCULAR IMPORTS
# ============================================================================
# Circular imports happen when module A imports module B, and B imports A.
# This is a common pitfall. Solutions:
# 1. Move the import inside the function (lazy import)
# 2. Move shared code to a third module
# 3. Use TYPE_CHECKING guard for type-only imports

CIRCULAR_IMPORT_SOLUTION = '''
# PROBLEM: circular import
# a.py: from b import func_b
# b.py: from a import func_a  # CIRCULAR!

# SOLUTION 1: Lazy import (inside function)
# b.py:
def func_b():
    from a import func_a  # Import when needed, not at module level
    return func_a() + 1

# SOLUTION 2: Move shared code to c.py
# c.py: shared code
# a.py: from c import shared_func
# b.py: from c import shared_func

# SOLUTION 3: TYPE_CHECKING guard
# b.py:
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from a import SomeType  # Only imported by type checkers, not at runtime
'''
print(f"\nCircular import solutions:\n{CIRCULAR_IMPORT_SOLUTION}")


## ============================================================================
# SECTION 8: MODULE-LEVEL PATTERNS
## ============================================================================
# Common patterns found in well-structured Python modules.

# Pattern 1: Logger at module level
import logging
logger = logging.getLogger(__name__)
# __name__ is the module's dotted name (e.g., "mypackage.core")

# Pattern 2: Module-level constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
API_BASE_URL = "https://api.example.com"

# Pattern 3: Sentinel object
_MISSING = object()  # Unique sentinel

def get_value(data, key, default=_MISSING):
    """Get value with sentinel default."""
    if key in data:
        return data[key]
    if default is not _MISSING:
        return default
    raise KeyError(key)

print(f"\nget_value: {get_value({'a': 1}, 'a')}")
print(f"get_value with default: {get_value({'a': 1}, 'b', 'fallback')}")
# Output: get_value: 1
# Output: get_value with default: fallback

# Pattern 4: __all__ for clean public API
__all__ = [
    "show_package_structure",
    "dynamic_import_example",
    "get_value",
]


## ============================================================================
# SECTION 9: sys.path AND MODULE SEARCH
# ============================================================================
# When you do `import foo`, Python searches:
# 1. Built-in modules (sys.builtin_module_names)
# 2. sys.path entries (in order):
#    a. Directory of the script being run
#    b. PYTHONPATH environment variable
#    c. Installation-dependent defaults (site-packages)

def show_module_search():
    """Show how Python finds modules."""
    print(f"\nsys.path (first 3 entries):")
    for i, path in enumerate(sys.path[:3]):
        print(f"  [{i}] {path}")

    # Check if a module is importable
    try:
        import json
        print(f"json is importable: True")
    except ImportError:
        print(f"json is importable: False")


## ============================================================================
# SECTION 10: PRACTICAL PACKAGE EXAMPLE
## ============================================================================
# A real-world package structure for an API client.

PRACTICAL_EXAMPLE = '''
# Real-world package structure for an API client:

api_client/
    __init__.py           # from .client import APIClient
                          # from .exceptions import APIError
                          # __all__ = ["APIClient", "APIError"]
                          # __version__ = "2.1.0"

    client.py             # Main client class
    auth.py               # Authentication handlers
    exceptions.py         # Custom exceptions
    models/               # Data models
        __init__.py       # from .request import Request
                          # from .response import Response
        request.py        # @dataclass Request
        response.py       # @dataclass Response
    utils/                # Utilities
        __init__.py
        retry.py          # Retry logic
        logging.py        # Request logging
    py.typed              # PEP 561 marker (this package has types)

# Usage:
from api_client import APIClient, APIError
client = APIClient(base_url="https://api.example.com")
'''
print(f"\nPractical example:\n{PRACTICAL_EXAMPLE}")


## ============================================================================
# MINI-EXERCISES
## ============================================================================

def exercises():
    print("\n" + "=" * 60)
    print("MINI-EXERCISES")
    print("=" * 60)

    print("""
--- Multiple Choice ---

Q1: What makes a directory a Python package?
    A) It contains .py files
    B) It has an __init__.py file
    C) It is in sys.path
    D) It has a pyproject.toml
""")
    print("Answer: B) __init__.py marks a directory as a package.\n")

    print("""
Q2: What does __all__ control?
    A) What `import module` exposes
    B) What `from module import *` exposes
    C) What the type checker sees
    D) What is listed in __init__.py
""")
    print("Answer: B) __all__ controls wildcard imports only.\n")

    print("""
Q3: How do you fix a circular import?
    A) Delete one of the modules
    B) Move the import inside the function (lazy import)
    C) Use `import *` instead
    D) Add both modules to __all__
""")
    print("Answer: B) Lazy imports defer the import until the function is called.\n")

    print("""
--- Q&A ---

Q: What is the difference between `import x` and `from x import y`?
A: `import x` creates the module object x. You access names as x.y.
   `from x import y` imports y directly into the current namespace.
   Prefer `import x` for clarity; use `from x import y` for frequently used names.

Q: When should you use __all__?
A: In any module or package __init__.py that others will import from.
   It defines the public API and prevents internal names from leaking.

Q: What is the difference between a package and a module?
A: A module is a single .py file. A package is a directory with __init__.py
   that can contain multiple modules and sub-packages.
""")


def progress_check():
    print("\n" + "=" * 60)
    print("PROGRESS CHECK")
    print("=" * 60)
    questions = [
        "1. Can you explain the module search order (sys.path)?",
        "2. Do you know the difference between a module and a package?",
        "3. Can you write a proper __init__.py with __all__?",
        "4. Can you use relative imports within a package?",
        "5. Do you understand how to fix circular imports?",
        "6. Can you use importlib for dynamic imports?",
        "7. Do you know what __name__ and __file__ represent?",
        "8. Can you explain when to use `import x` vs `from x import y`?",
        "9. Do you understand the PEP 561 py.typed marker?",
        "10. Can you design a clean package structure?",
    ]
    print("\nRate your confidence (1-5) for each:\n")
    for q in questions:
        print(f"  {q}")
    print("""
Scoring:
  40-50: Excellent! You can organize any Python project.
  30-39: Good. Practice structuring a real project.
  20-29: Focus on __init__.py and __all__ first.
  < 20:  Start with simple module imports.
""")


def key_takeaways():
    print("\n" + "=" * 60)
    print("KEY TAKEAWAYS")
    print("=" * 60)
    print("""
* A .py file is a module; a directory with __init__.py is a package.
* __all__ controls what `from module import *` exposes.
* Relative imports (from . import x) work within packages.
* Circular imports: fix with lazy imports or shared modules.
* importlib.import_module() imports modules by string name at runtime.
* __name__ is "__main__" when run directly, dotted path when imported.
* sys.path determines where Python searches for modules.
* Prefer `import module` over `from module import *`.
* __init__.py should define the package's public API.
* py.typed marker indicates the package ships type annotations.
""")


def transferability():
    print("\n" + "=" * 60)
    print("TRANSFERABILITY TO OTHER LANGUAGES")
    print("=" * 60)
    print("""
Python Concept       | TypeScript           | Rust
---------------------|----------------------|------------------------
module (.py file)    | .ts file             | mod (file or inline)
package (__init__.py)| directory + index.ts  | crate
__all__              | export {}            | pub
import x             | import * as x        | use crate::x
from x import y      | import { y } from x  | use crate::x::y
__init__.py          | index.ts             | mod.rs
sys.path             | tsconfig paths       | Cargo.toml deps
importlib            | import() (dynamic)   | N/A (static)
pyproject.toml       | package.json         | Cargo.toml
""")


if __name__ == "__main__":
    show_package_structure()
    dynamic_import_example()
    show_module_search()
    exercises()
    progress_check()
    key_takeaways()
    transferability()

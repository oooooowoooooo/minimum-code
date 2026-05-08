"""
FastAPI Backend for AI Era Learning Platform
=============================================
Serves course content from source files, tracks progress.
This is a meta-example: the project teaches FastAPI, and uses FastAPI.

Run: cd web/backend && uv run uvicorn main:app --reload --port 8000
"""

import json
import random
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="AI Era Learning Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Project root (3 levels up from web/backend/)
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "web" / "backend" / "data"
DATA_DIR.mkdir(exist_ok=True)

PROGRESS_FILE = DATA_DIR / "progress.json"
KNOWLEDGE_POINTS_FILE = DATA_DIR / "knowledge_points.json"


# ============================================================================
# MODELS
# ============================================================================

class ModuleInfo(BaseModel):
    id: str
    title: str
    category: str
    icon: str
    description: str
    week: int
    order: int

class Section(BaseModel):
    title: str
    content: str
    type: str = "text"  # text, code, exercise
    language: Optional[str] = None

class ModuleContent(BaseModel):
    id: str
    title: str
    category: str
    icon: str
    sections: list[Section]

class ProgressUpdate(BaseModel):
    module_id: str
    completed: bool

class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    correct: int
    explanation: str


# ============================================================================
# MODULE REGISTRY
# ============================================================================

MODULES = [
    # Week 1: Cognitive
    {"id": "cognitive-why", "title": "Why Learn Programming", "category": "cognitive", "icon": "🧠", "description": "Understand why programming matters in the AI era", "week": 1, "order": 1},
    {"id": "cognitive-thinking", "title": "AI-Era Thinking", "category": "cognitive", "icon": "💡", "description": "Mental models that make you irreplaceable", "week": 1, "order": 2},
    {"id": "cognitive-languages", "title": "Why Python + TypeScript", "category": "cognitive", "icon": "🐍", "description": "The two languages you actually need", "week": 1, "order": 3},
    # Week 1: Python
    {"id": "py-variables", "title": "Variables & Types", "category": "python", "icon": "📦", "description": "Name binding, mutability, references", "week": 1, "order": 4},
    {"id": "py-functions", "title": "Functions & Decorators", "category": "python", "icon": "⚡", "description": "First-class functions, closures, decorators", "week": 1, "order": 5},
    {"id": "py-classes", "title": "Classes & Inheritance", "category": "python", "icon": "🏗️", "description": "OOP, dataclasses, protocols", "week": 1, "order": 6},
    {"id": "py-async", "title": "Async Programming", "category": "python", "icon": "🔄", "description": "Coroutines, gather, TaskGroup", "week": 1, "order": 7},
    {"id": "py-types", "title": "Type Annotations", "category": "python", "icon": "🏷️", "description": "Generics, TypeVar, Literal", "week": 1, "order": 8},
    {"id": "py-modules", "title": "Modules & Packages", "category": "python", "icon": "📚", "description": "Import system, package structure", "week": 1, "order": 9},
    # Week 1: TypeScript
    {"id": "ts-types", "title": "Type System", "category": "typescript", "icon": "🔷", "description": "Primitives, interfaces, narrowing", "week": 1, "order": 10},
    {"id": "ts-functions", "title": "Functions & Generics", "category": "typescript", "icon": "⚙️", "description": "Generics, overloads, currying", "week": 1, "order": 11},
    {"id": "ts-interfaces", "title": "Interfaces & Type Manipulation", "category": "typescript", "icon": "🔧", "description": "Mapped types, conditional types, utility types", "week": 1, "order": 12},
    {"id": "ts-async", "title": "Async Programming", "category": "typescript", "icon": "⏳", "description": "Promises, async/await, AbortController", "week": 1, "order": 13},
    {"id": "ts-modules", "title": "Module System", "category": "typescript", "icon": "📁", "description": "ES modules, dynamic import, barrel files", "week": 1, "order": 14},
    {"id": "ts-decorators", "title": "Decorators & Metaprogramming", "category": "typescript", "icon": "🎨", "description": "Class/method/property decorators", "week": 1, "order": 15},
    # Week 1: Patterns
    {"id": "pat-di", "title": "Dependency Injection", "category": "patterns", "icon": "💉", "description": "Inversion of control", "week": 1, "order": 16},
    {"id": "pat-middleware", "title": "Middleware", "category": "patterns", "icon": "🔗", "description": "Request interception chain", "week": 1, "order": 17},
    {"id": "pat-builder", "title": "Builder", "category": "patterns", "icon": "🔨", "description": "Step-by-step construction", "week": 1, "order": 18},
    {"id": "pat-strategy", "title": "Strategy", "category": "patterns", "icon": "🎯", "description": "Interchangeable algorithms", "week": 1, "order": 19},
    {"id": "pat-observer", "title": "Observer", "category": "patterns", "icon": "👁️", "description": "Event notification", "week": 1, "order": 20},
    {"id": "pat-factory", "title": "Factory", "category": "patterns", "icon": "🏭", "description": "Object creation", "week": 1, "order": 21},
    {"id": "pat-repository", "title": "Repository", "category": "patterns", "icon": "🗄️", "description": "Data access abstraction", "week": 1, "order": 22},
    {"id": "pat-pipeline", "title": "Pipeline", "category": "patterns", "icon": "🔧", "description": "Sequential processing", "week": 1, "order": 23},
    # Week 2: Python Dissection
    {"id": "py-fastapi", "title": "FastAPI", "category": "python-dissect", "icon": "🚀", "description": "Dependency injection, middleware, lifecycle", "week": 2, "order": 24},
    {"id": "py-langchain", "title": "LangChain", "category": "python-dissect", "icon": "🦜", "description": "Chain pattern, Agent, RAG", "week": 2, "order": 25},
    {"id": "py-crewai", "title": "CrewAI", "category": "python-dissect", "icon": "👥", "description": "Multi-agent collaboration", "week": 2, "order": 26},
    {"id": "py-dify", "title": "Dify", "category": "python-dissect", "icon": "🔄", "description": "Workflow engine, plugin system", "week": 2, "order": 27},
    {"id": "py-ragflow", "title": "RAGFlow", "category": "python-dissect", "icon": "📖", "description": "Document parsing, vector retrieval", "week": 2, "order": 28},
    # Week 3: TypeScript Dissection
    {"id": "ts-nextjs", "title": "Next.js", "category": "typescript-dissect", "icon": "▲", "description": "SSR/SSG, App Router, middleware", "week": 3, "order": 29},
    {"id": "ts-trpc", "title": "tRPC", "category": "typescript-dissect", "icon": "🔌", "description": "End-to-end type safety", "week": 3, "order": 30},
    {"id": "ts-tauri", "title": "Tauri", "category": "typescript-dissect", "icon": "🖥️", "description": "Cross-platform desktop", "week": 3, "order": 31},
    {"id": "ts-shadcn", "title": "shadcn/ui", "category": "typescript-dissect", "icon": "🎨", "description": "Component design, theming", "week": 3, "order": 32},
    {"id": "ts-bun", "title": "Bun", "category": "typescript-dissect", "icon": "🍞", "description": "Runtime, bundler, test runner", "week": 3, "order": 33},
    # Week 4: AI Mastery
    {"id": "ai-prompt", "title": "Prompt Engineering", "category": "ai-mastery", "icon": "✍️", "description": "System prompts, few-shot, chain-of-thought", "week": 4, "order": 34},
    {"id": "ai-architecture", "title": "AI-Assisted Architecture", "category": "ai-mastery", "icon": "🏛️", "description": "Design decisions with AI", "week": 4, "order": 35},
    {"id": "ai-review", "title": "AI Code Review", "category": "ai-mastery", "icon": "🔍", "description": "Find bugs, security, performance", "week": 4, "order": 36},
    {"id": "ai-development", "title": "AI-Driven Development", "category": "ai-mastery", "icon": "🤖", "description": "Complete workflow with AI", "week": 4, "order": 37},
    # Week 4: Practice
    {"id": "practice-planning", "title": "Project Planning", "category": "practice", "icon": "📋", "description": "Requirements, scope, timeline", "week": 4, "order": 38},
    {"id": "practice-architecture", "title": "Architecture Design", "category": "practice", "icon": "🏗️", "description": "Patterns, boundaries, data flow", "week": 4, "order": 39},
    {"id": "practice-implementation", "title": "Implementation", "category": "practice", "icon": "💻", "description": "Build the complete project", "week": 4, "order": 40},
    {"id": "practice-deployment", "title": "Deployment", "category": "practice", "icon": "🚀", "description": "Docker, CI/CD, monitoring", "week": 4, "order": 41},
]


# ============================================================================
# HELPER: Read source file content
# ============================================================================

def read_file(path: Path) -> str:
    """Read a file safely."""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""

def extract_sections_from_python(filepath: Path) -> list[Section]:
    """Extract teaching sections from a Python file."""
    content = read_file(filepath)
    if not content:
        return []

    sections = []
    current_title = ""
    current_lines = []

    for line in content.split("\n"):
        if line.startswith("# ==="):
            if current_title and current_lines:
                text = "\n".join(current_lines).strip()
                if text:
                    sections.append(Section(
                        title=current_title,
                        content=text,
                        type="code" if any(kw in text for kw in ["def ", "class ", "import ", "print("]) else "text",
                        language="python",
                    ))
            current_lines = []
        elif line.startswith("# ") and not line.startswith("# ===") and not current_lines:
            current_title = line[2:].strip()
        else:
            current_lines.append(line)

    if current_title and current_lines:
        text = "\n".join(current_lines).strip()
        if text:
            sections.append(Section(
                title=current_title,
                content=text,
                type="code" if any(kw in text for kw in ["def ", "class ", "import ", "print("]) else "text",
                language="python",
            ))

    return sections[:10]  # Limit sections

def extract_sections_from_markdown(filepath: Path) -> list[Section]:
    """Extract sections from a markdown file."""
    content = read_file(filepath)
    if not content:
        return []

    sections = []
    current_title = ""
    current_lines = []

    for line in content.split("\n"):
        if line.startswith("## "):
            if current_title and current_lines:
                sections.append(Section(
                    title=current_title,
                    content="\n".join(current_lines).strip(),
                    type="text",
                ))
            current_title = line[3:].strip()
            current_lines = []
        elif line.startswith("```"):
            current_lines.append(line)
        else:
            current_lines.append(line)

    if current_title and current_lines:
        sections.append(Section(
            title=current_title,
            content="\n".join(current_lines).strip(),
            type="text",
        ))

    return sections[:10]


def extract_sections_from_ts(filepath: Path) -> list[Section]:
    """Extract teaching sections from a TypeScript/TSX file.

    Handles two formats:
      // SECTION N: TITLE          (title marker)
      // ===...===                 (delimiter, used to box title and separate sections)
      // Title                     (fallback: bare comment as title before any content)
    """
    content = read_file(filepath)
    if not content:
        return []

    sections = []
    current_title = ""
    current_lines = []
    in_section = False  # True once we've seen a section header

    for line in content.split("\n"):
        # Detect "SECTION N:" title markers
        section_match = line.startswith("// SECTION ") and ":" in line

        if line.startswith("// ==="):
            # Delimiter: flush previous section if we have one
            if current_title and current_lines:
                text = "\n".join(current_lines).strip()
                if text:
                    sections.append(Section(
                        title=current_title,
                        content=text,
                        type="code" if any(kw in text for kw in ["function ", "class ", "interface ", "const ", "import "]) else "text",
                        language="typescript",
                    ))
                current_title = ""
                current_lines = []
                in_section = False
        elif section_match:
            # SECTION N: TITLE — start a new section
            if current_title and current_lines:
                text = "\n".join(current_lines).strip()
                if text:
                    sections.append(Section(
                        title=current_title,
                        content=text,
                        type="code" if any(kw in text for kw in ["function ", "class ", "interface ", "const ", "import "]) else "text",
                        language="typescript",
                    ))
            current_title = line.split(":", 1)[1].strip()
            current_lines = []
            in_section = True
        elif in_section:
            # Collect content lines inside a section
            current_lines.append(line)
        elif not current_title and line.startswith("// ") and not line.startswith("// ==="):
            # Fallback: bare comment title (for files without SECTION markers)
            current_title = line[3:].strip()

    if current_title and current_lines:
        text = "\n".join(current_lines).strip()
        if text:
            sections.append(Section(
                title=current_title,
                content=text,
                type="code" if any(kw in text for kw in ["function ", "class ", "interface ", "const ", "import "]) else "text",
                language="typescript",
            ))

    return sections[:10]


# ============================================================================
# API ROUTES
# ============================================================================

@app.get("/api/modules")
def list_modules() -> list[ModuleInfo]:
    """List all modules."""
    return [ModuleInfo(**m) for m in MODULES]


@app.get("/api/modules/{module_id}")
def get_module(module_id: str) -> ModuleContent:
    """Get module content by ID. Reads actual source files."""
    module = next((m for m in MODULES if m["id"] == module_id), None)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    sections = []

    # Map module ID to source file
    source_map = {
        "py-variables": PROJECT_ROOT / "src" / "python" / "fundamentals" / "variables.py",
        "py-functions": PROJECT_ROOT / "src" / "python" / "fundamentals" / "functions.py",
        "py-classes": PROJECT_ROOT / "src" / "python" / "fundamentals" / "classes.py",
        "py-async": PROJECT_ROOT / "src" / "python" / "fundamentals" / "async_io.py",
        "py-types": PROJECT_ROOT / "src" / "python" / "fundamentals" / "type_system.py",
        "py-modules": PROJECT_ROOT / "src" / "python" / "fundamentals" / "modules.py",
        "ts-types": PROJECT_ROOT / "src" / "typescript" / "fundamentals" / "types.ts",
        "ts-functions": PROJECT_ROOT / "src" / "typescript" / "fundamentals" / "functions.ts",
        "ts-interfaces": PROJECT_ROOT / "src" / "typescript" / "fundamentals" / "interfaces.ts",
        "ts-async": PROJECT_ROOT / "src" / "typescript" / "fundamentals" / "async.ts",
        "ts-modules": PROJECT_ROOT / "src" / "typescript" / "fundamentals" / "modules.ts",
        "ts-decorators": PROJECT_ROOT / "src" / "typescript" / "fundamentals" / "decorators.ts",
        "py-fastapi": PROJECT_ROOT / "src" / "python" / "dissect" / "fastapi" / "dissect.py",
        "py-langchain": PROJECT_ROOT / "src" / "python" / "dissect" / "langchain" / "dissect.py",
        "py-crewai": PROJECT_ROOT / "src" / "python" / "dissect" / "crewai" / "dissect.py",
        "py-dify": PROJECT_ROOT / "src" / "python" / "dissect" / "dify" / "dissect.py",
        "py-ragflow": PROJECT_ROOT / "src" / "python" / "dissect" / "ragflow" / "dissect.py",
        "ts-nextjs": PROJECT_ROOT / "src" / "typescript" / "dissect" / "nextjs" / "dissect.ts",
        "ts-trpc": PROJECT_ROOT / "src" / "typescript" / "dissect" / "trpc" / "dissect.ts",
        "ts-tauri": PROJECT_ROOT / "src" / "typescript" / "dissect" / "tauri" / "dissect.ts",
        "ts-shadcn": PROJECT_ROOT / "src" / "typescript" / "dissect" / "shadcn-ui" / "dissect.tsx",
        "ts-bun": PROJECT_ROOT / "src" / "typescript" / "dissect" / "bun" / "dissect.ts",
        "cognitive-why": PROJECT_ROOT / "docs" / "cognitive" / "why-learn-programming.md",
        "cognitive-thinking": PROJECT_ROOT / "docs" / "cognitive" / "ai-era-thinking.md",
        "cognitive-languages": PROJECT_ROOT / "docs" / "cognitive" / "why-py-and-ts.md",
        "pat-di": PROJECT_ROOT / "src" / "patterns" / "dependency_injection.md",
        "pat-middleware": PROJECT_ROOT / "src" / "patterns" / "middleware.md",
        "pat-builder": PROJECT_ROOT / "src" / "patterns" / "builder.md",
        "pat-strategy": PROJECT_ROOT / "src" / "patterns" / "strategy.md",
        "pat-observer": PROJECT_ROOT / "src" / "patterns" / "observer.md",
        "pat-factory": PROJECT_ROOT / "src" / "patterns" / "factory.md",
        "pat-repository": PROJECT_ROOT / "src" / "patterns" / "repository.md",
        "pat-pipeline": PROJECT_ROOT / "src" / "patterns" / "pipeline.md",
        "ai-prompt": PROJECT_ROOT / "docs" / "ai-mastery" / "prompt-engineering.md",
        "ai-architecture": PROJECT_ROOT / "docs" / "ai-mastery" / "ai-assisted-architecture.md",
        "ai-review": PROJECT_ROOT / "docs" / "ai-mastery" / "ai-code-review.md",
        "ai-development": PROJECT_ROOT / "docs" / "ai-mastery" / "ai-driven-development.md",
        "practice-planning": PROJECT_ROOT / "docs" / "practice" / "project-planning.md",
        "practice-architecture": PROJECT_ROOT / "docs" / "practice" / "architecture-design.md",
        "practice-implementation": PROJECT_ROOT / "docs" / "practice" / "implementation.md",
        "practice-deployment": PROJECT_ROOT / "docs" / "practice" / "deployment.md",
    }

    filepath = source_map.get(module_id)
    if filepath:
        if filepath.suffix == ".py":
            sections = extract_sections_from_python(filepath)
        elif filepath.suffix in (".ts", ".tsx"):
            sections = extract_sections_from_ts(filepath)
        elif filepath.suffix == ".md":
            sections = extract_sections_from_markdown(filepath)

    # Fallback if no sections extracted
    if not sections:
        sections = [
            Section(title="Overview", content=f"This module covers {module['title']}.", type="text"),
            Section(title="Key Concepts", content="Refer to the source files in the project for detailed content.", type="text"),
        ]

    return ModuleContent(
        id=module["id"],
        title=module["title"],
        category=module["category"],
        icon=module["icon"],
        sections=sections,
    )


@app.get("/api/modules/{module_id}/quiz")
def get_quiz(module_id: str) -> list[QuizQuestion]:
    """Get quiz questions for a module."""
    quizzes = {
        "py-variables": [
            QuizQuestion(
                question="What does `a = [1, 2, 3]; b = a; b.append(4)` make `a`?",
                options=["[1, 2, 3]", "[1, 2, 3, 4]", "Error", "[4, 1, 2, 3]"],
                correct=1,
                explanation="b and a point to the SAME list object. Modifying b modifies a.",
            ),
            QuizQuestion(
                question="Which of these is IMMUTABLE in Python?",
                options=["list", "dict", "tuple", "set"],
                correct=2,
                explanation="Tuples cannot be modified after creation. Lists, dicts, and sets are mutable.",
            ),
        ],
        "py-functions": [
            QuizQuestion(
                question="What is a decorator?",
                options=["A function that takes a function and returns a new function", "A type annotation", "A class method", "A loop construct"],
                correct=0,
                explanation="A decorator wraps a function to add behavior before/after it runs.",
            ),
        ],
        "ts-types": [
            QuizQuestion(
                question="What does `unknown` do differently from `any`?",
                options=["Nothing, they're the same", "unknown is safer — you must narrow before using", "any is safer", "unknown only works with generics"],
                correct=1,
                explanation="unknown requires type narrowing before use. any allows all operations without checking.",
            ),
        ],
        "cognitive-why": [
            QuizQuestion(
                question="In the AI era, what's the most valuable skill?",
                options=["Writing code fast", "Knowing many languages", "Judging code quality and designing systems", "Memorizing syntax"],
                correct=2,
                explanation="AI can write code. Humans judge quality, design systems, and make tradeoffs.",
            ),
        ],
        "cognitive-thinking": [
            QuizQuestion(
                question="What's the AI-era thinking hierarchy?",
                options=["Write code > Read code > Design systems", "Design systems > Write code > Read code", "Define problems > Make tradeoffs > Design systems > Read code > Write code", "Memorize syntax > Write code > Debug"],
                correct=2,
                explanation="The highest value is defining problems. AI handles the lowest level (writing code).",
            ),
        ],
        "cognitive-languages": [
            QuizQuestion(
                question="Why Python + TypeScript?",
                options=["They're the easiest languages", "Python dominates AI/ML, TypeScript dominates web — together they cover most industrial scenarios", "They have the most syntax", "Everyone uses them"],
                correct=1,
                explanation="Python owns AI/ML/data. TypeScript owns web/frontend. Together they cover 90%+ of modern development.",
            ),
        ],
        "py-classes": [
            QuizQuestion(
                question="What does @dataclass do?",
                options=["Makes a class abstract", "Auto-generates __init__, __repr__, __eq__ from type hints", "Makes a class immutable", "Adds a constructor"],
                correct=1,
                explanation="@dataclass reads type annotations and generates boilerplate methods automatically.",
            ),
            QuizQuestion(
                question="What is a Protocol?",
                options=["A network protocol", "A structural typing interface — if it has the methods, it fits", "A base class", "A decorator"],
                correct=1,
                explanation="Protocol enables structural (duck) typing: 'if it walks like a duck...'",
            ),
        ],
        "py-async": [
            QuizQuestion(
                question="What does `await` do?",
                options=["Blocks the thread", "Yields control back to the event loop while waiting", "Creates a new thread", "Stops the program"],
                correct=1,
                explanation="await suspends the coroutine and lets the event loop run other tasks.",
            ),
        ],
        "py-types": [
            QuizQuestion(
                question="What is TypeVar used for?",
                options=["Creating variables", "Defining generic type parameters", "Type checking", "Importing types"],
                correct=1,
                explanation="TypeVar creates a placeholder type that gets resolved when the function is called.",
            ),
        ],
        "py-modules": [
            QuizQuestion(
                question="What does `if __name__ == '__main__'` do?",
                options=["Defines the main function", "Runs code only when the file is executed directly, not imported", "Makes the file a package", "Exports all symbols"],
                correct=1,
                explanation="This guard prevents code from running when the file is imported as a module.",
            ),
        ],
        "ts-functions": [
            QuizQuestion(
                question="What is a generic function?",
                options=["A function that works with any type", "A function that takes a type parameter and works with that specific type", "A function without parameters", "An async function"],
                correct=1,
                explanation="Generics let you write type-safe code that works with multiple types.",
            ),
        ],
        "ts-interfaces": [
            QuizQuestion(
                question="What does `Partial<T>` do?",
                options=["Makes all properties required", "Makes all properties optional", "Removes all properties", "Makes T readonly"],
                correct=1,
                explanation="Partial<T> maps every property of T to optional (?).",
            ),
        ],
        "ts-async": [
            QuizQuestion(
                question="What does Promise.allSettled do differently from Promise.all?",
                options=["Nothing, they're the same", "allSettled waits for all promises to settle (resolve or reject); all rejects on first rejection", "allSettled is faster", "allSettled only works with arrays"],
                correct=1,
                explanation="Promise.allSettled never short-circuits — it waits for every promise to complete.",
            ),
        ],
        "ts-modules": [
            QuizQuestion(
                question="What is a barrel file?",
                options=["A file that stores data", "An index.ts that re-exports from multiple modules", "A configuration file", "A test file"],
                correct=1,
                explanation="Barrel files (index.ts) aggregate exports for cleaner imports.",
            ),
        ],
        "ts-decorators": [
            QuizQuestion(
                question="What does a class decorator receive?",
                options=["The class instance", "The class constructor function", "The class name", "Nothing"],
                correct=1,
                explanation="A class decorator receives the constructor and can return a new one.",
            ),
        ],
        "pat-di": [
            QuizQuestion(
                question="What is Dependency Injection?",
                options=["Creating dependencies inside a function", "Passing dependencies from outside instead of creating them internally", "A testing framework", "A database pattern"],
                correct=1,
                explanation="DI inverts control: dependencies are provided, not created. This enables testing and flexibility.",
            ),
        ],
        "pat-middleware": [
            QuizQuestion(
                question="How does middleware work?",
                options=["Each middleware handles the request completely", "Request passes through a chain; each middleware can modify it or pass it on", "Only one middleware runs", "Middleware replaces the handler"],
                correct=1,
                explanation="Middleware forms a chain: request → middleware1 → middleware2 → handler → response.",
            ),
        ],
        "pat-builder": [
            QuizQuestion(
                question="When should you use the Builder pattern?",
                options=["For simple objects with 2-3 fields", "For complex objects with many optional parameters", "For all objects", "Only for database queries"],
                correct=1,
                explanation="Builder shines when objects have many optional parameters or complex construction logic.",
            ),
        ],
        "pat-strategy": [
            QuizQuestion(
                question="What does the Strategy pattern enable?",
                options=["Faster algorithms", "Swapping algorithms at runtime without changing the caller", "Parallel execution", "Memory optimization"],
                correct=1,
                explanation="Strategy encapsulates algorithms behind a common interface, making them interchangeable.",
            ),
        ],
        "pat-observer": [
            QuizQuestion(
                question="What is the Observer pattern?",
                options=["A logging system", "A one-to-many dependency: when one object changes, all dependents are notified", "A database pattern", "A caching strategy"],
                correct=1,
                explanation="Observer enables event-driven communication without tight coupling.",
            ),
        ],
        "pat-factory": [
            QuizQuestion(
                question="What does a Factory do?",
                options=["Manufactures hardware", "Creates objects without specifying the exact class", "Stores data", "Handles errors"],
                correct=1,
                explanation="Factory encapsulates object creation, letting subclasses decide what to instantiate.",
            ),
        ],
        "pat-repository": [
            QuizQuestion(
                question="What does the Repository pattern abstract?",
                options=["The UI layer", "Data access — business logic doesn't know about the database", "The network layer", "The file system"],
                correct=1,
                explanation="Repository provides a collection-like interface for data access, hiding storage details.",
            ),
        ],
        "pat-pipeline": [
            QuizQuestion(
                question="What is a Pipeline pattern?",
                options=["A single function that does everything", "Sequential processing stages where output of one feeds the next", "A parallel processing pattern", "A database query"],
                correct=1,
                explanation="Pipeline chains processing stages: input → stage1 → stage2 → ... → output.",
            ),
        ],
        "py-fastapi": [
            QuizQuestion(
                question="How does FastAPI resolve dependencies?",
                options=["You call them manually", "It reads function parameter types and auto-injects matching dependencies", "Through configuration files", "Via environment variables"],
                correct=1,
                explanation="FastAPI's DI system inspects type hints and automatically resolves the dependency chain.",
            ),
        ],
        "py-langchain": [
            QuizQuestion(
                question="What is the pipe operator (|) in LangChain?",
                options=["Unix pipe", "Chains Runnables: output of one feeds input of the next", "Bitwise OR", "Type union"],
                correct=1,
                explanation="The | operator composes Runnables into chains: prompt | model | parser.",
            ),
        ],
        "py-crewai": [
            QuizQuestion(
                question="What makes CrewAI different from single-agent systems?",
                options=["It's faster", "Multiple agents with different roles collaborate on tasks", "It uses fewer tokens", "It has a better UI"],
                correct=1,
                explanation="CrewAI assigns specialized roles (researcher, writer, etc.) to different agents.",
            ),
        ],
        "py-dify": [
            QuizQuestion(
                question="What is Dify's workflow engine?",
                options=["A simple if-else chain", "A DAG-based visual workflow with nodes for LLM, code, conditions, and tools", "A cron scheduler", "A database migration tool"],
                correct=1,
                explanation="Dify's workflow engine processes nodes in a directed acyclic graph, enabling complex AI workflows.",
            ),
        ],
        "py-ragflow": [
            QuizQuestion(
                question="What does RAGFlow do?",
                options=["Generates images", "Parses documents into chunks, embeds them, and retrieves relevant context for LLM queries", "Runs CI/CD pipelines", "Manages cloud infrastructure"],
                correct=1,
                explanation="RAGFlow implements RAG: parse documents → chunk → embed → store → retrieve relevant chunks for LLM context.",
            ),
        ],
        "ts-nextjs": [
            QuizQuestion(
                question="What is the Server/Client boundary in Next.js?",
                options=["Server and client are the same", "Server Components run on the server; Client Components run in the browser. 'use client' marks the boundary.", "Only server-side rendering", "Only client-side rendering"],
                correct=1,
                explanation="Server Components (default) run on the server. Add 'use client' to make a component run in the browser.",
            ),
        ],
        "ts-trpc": [
            QuizQuestion(
                question="What does tRPC provide?",
                options=["A REST API framework", "End-to-end type safety: client calls server functions with full TypeScript types, zero code generation", "A database ORM", "A UI library"],
                correct=1,
                explanation="tRPC lets you call server functions from the client with full type inference — no code generation needed.",
            ),
        ],
        "ts-tauri": [
            QuizQuestion(
                question="What is Tauri's architecture?",
                options=["Electron-based", "Rust backend + web frontend — smaller binary, native performance, cross-platform", "Node.js only", "Python backend"],
                correct=1,
                explanation="Tauri uses Rust for the backend and web technologies for the frontend, producing tiny binaries.",
            ),
        ],
        "ts-shadcn": [
            QuizQuestion(
                question="How does shadcn/ui distribute components?",
                options=["As an npm package", "You copy component source code directly into your project — full ownership", "As a CDN", "As a binary"],
                correct=1,
                explanation="shadcn/ui copies component source into your project. You own the code and can modify anything.",
            ),
        ],
        "ts-bun": [
            QuizQuestion(
                question="What makes Bun different from Node.js?",
                options=["It's written in Java", "It's built on JavaScriptCore (Safari's engine) with native bundler, test runner, and package manager", "It only runs TypeScript", "It has no npm support"],
                correct=1,
                explanation="Bun bundles a runtime, bundler, test runner, and package manager into one tool built on JSC.",
            ),
        ],
        "ai-prompt": [
            QuizQuestion(
                question="What is chain-of-thought prompting?",
                options=["Writing very long prompts", "Asking the AI to show its reasoning step by step", "Using multiple AI models", "Prompting in a chain of emails"],
                correct=1,
                explanation="Chain-of-thought asks the model to reason step-by-step before answering, improving accuracy.",
            ),
        ],
        "ai-architecture": [
            QuizQuestion(
                question="How should you use AI for architecture decisions?",
                options=["Let AI decide everything", "Use AI to explore options and tradeoffs, but you make the final call", "Ignore AI for architecture", "Only use AI for code generation"],
                correct=1,
                explanation="AI is great at listing options and tradeoffs. Humans must make the final judgment call.",
            ),
        ],
        "ai-review": [
            QuizQuestion(
                question="What should AI code review focus on?",
                options=["Style only", "Bugs, security vulnerabilities, performance issues, and architecture violations", "Line length", "Variable names only"],
                correct=1,
                explanation="AI review is most valuable for catching bugs, security holes, and architectural issues humans miss.",
            ),
        ],
        "ai-development": [
            QuizQuestion(
                question="What's the ideal AI development workflow?",
                options=["AI does everything", "You design and review, AI implements and tests — tight feedback loop", "You write all code, AI just watches", "AI only writes tests"],
                correct=1,
                explanation="The best workflow: human designs, AI implements, human reviews, iterate quickly.",
            ),
        ],
        "practice-planning": [
            QuizQuestion(
                question="What comes first in project planning?",
                options=["Writing code", "Understanding requirements and defining scope", "Choosing a framework", "Setting up CI/CD"],
                correct=1,
                explanation="Requirements first. You can't build the right thing if you don't know what 'right' means.",
            ),
        ],
        "practice-architecture": [
            QuizQuestion(
                question="What's the most important architectural principle?",
                options=["Use the latest framework", "Clear boundaries between components with well-defined interfaces", "Minimize lines of code", "Use microservices"],
                correct=1,
                explanation="Clear boundaries and interfaces make systems maintainable, testable, and evolvable.",
            ),
        ],
        "practice-implementation": [
            QuizQuestion(
                question="What's the best implementation strategy?",
                options=["Build everything at once", "Build the smallest working end-to-end slice, then iterate", "Perfect the database first", "Write all tests first"],
                correct=1,
                explanation="Start with a thin vertical slice that works end-to-end. Then add features iteratively.",
            ),
        ],
        "practice-deployment": [
            QuizQuestion(
                question="What should you automate first?",
                options=["Social media posts", "Build, test, and deployment pipeline — CI/CD", "Documentation", "Code reviews"],
                correct=1,
                explanation="CI/CD automation catches errors early and makes deployments reliable and repeatable.",
            ),
        ],
    }

    return quizzes.get(module_id, [])


# ============================================================================
# KNOWLEDGE POINTS DATA
# ============================================================================

knowledge_points_data: dict = {"total_points": 0, "weeks": 0, "points": []}

def load_knowledge_points():
    global knowledge_points_data
    if KNOWLEDGE_POINTS_FILE.exists():
        knowledge_points_data = json.loads(KNOWLEDGE_POINTS_FILE.read_text(encoding="utf-8"))

@app.on_event("startup")
def startup_event():
    load_knowledge_points()


# ============================================================================
# KNOWLEDGE POINTS ENDPOINTS
# ============================================================================

@app.get("/api/knowledge-points/stats")
def get_knowledge_points_stats():
    """Return aggregate statistics about knowledge points."""
    points = knowledge_points_data.get("points", [])
    points_per_week: dict[str, int] = {}
    points_per_module: dict[str, int] = {}
    games_per_type: dict[str, int] = {}
    for p in points:
        w = str(p["week"])
        m = p["module"]
        points_per_week[w] = points_per_week.get(w, 0) + 1
        points_per_module[m] = points_per_module.get(m, 0) + 1
        game = p.get("game")
        if game and game.get("type"):
            gt = game["type"]
            games_per_type[gt] = games_per_type.get(gt, 0) + 1
    return {
        "total_points": len(points),
        "points_per_week": points_per_week,
        "points_per_module": points_per_module,
        "games_per_type": games_per_type,
    }


@app.get("/api/knowledge-points")
def list_knowledge_points(
    week: Optional[int] = None,
    module: Optional[str] = None,
    search: Optional[str] = None,
    game_type: Optional[str] = None,
    page: int = 1,
    per_page: int = 20,
):
    """Return all knowledge points with optional filtering and pagination.

    Query params:
        week: Filter by week number
        module: Filter by module id
        search: Search in title and explanation (case-insensitive)
        game_type: Filter by game type (e.g. predict_output, find_bug)
        page: Page number (default 1)
        per_page: Items per page (default 20)
    """
    points = knowledge_points_data.get("points", [])

    if week is not None:
        points = [p for p in points if p["week"] == week]
    if module is not None:
        points = [p for p in points if p["module"] == module]
    if search is not None:
        q = search.lower()
        points = [p for p in points if q in p.get("title", "").lower() or q in p.get("explanation", "").lower()]
    if game_type is not None:
        points = [p for p in points if p.get("game", {}).get("type") == game_type]

    total = len(points)
    start = (page - 1) * per_page
    end = start + per_page
    paginated = points[start:end]

    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page if per_page > 0 else 0,
        "points": paginated,
    }


@app.get("/api/knowledge-points/random")
def get_random_knowledge_points(count: int = 10):
    """Return random knowledge points for review.

    Query params:
        count: Number of random points to return (default 10, max 100)
    """
    points = knowledge_points_data.get("points", [])
    if not points:
        raise HTTPException(status_code=404, detail="No knowledge points available")
    count = max(1, min(count, 100, len(points)))
    sampled = random.sample(points, count)
    return {"count": len(sampled), "points": sampled}


@app.get("/api/knowledge-points/id/{point_id}")
def get_knowledge_point_by_id(point_id: int):
    """Return a single knowledge point by its index in the array.

    Path params:
        point_id: Zero-based index into the points array
    """
    points = knowledge_points_data.get("points", [])
    if point_id < 0 or point_id >= len(points):
        raise HTTPException(status_code=404, detail=f"Knowledge point {point_id} not found (valid range: 0-{len(points)-1})")
    return {"id": point_id, "point": points[point_id]}


@app.get("/api/knowledge-points/by-week/{week}")
def get_knowledge_points_by_week(week: int):
    """Return all knowledge points for a specific week."""
    points = [p for p in knowledge_points_data.get("points", []) if p["week"] == week]
    if not points:
        raise HTTPException(status_code=404, detail=f"No knowledge points found for week {week}")
    return {"week": week, "count": len(points), "points": points}


@app.get("/api/weeks")
def list_weeks():
    """Return list of weeks with their modules and point counts."""
    points = knowledge_points_data.get("points", [])
    weeks_map: dict[int, dict] = {}
    for p in points:
        w = p["week"]
        m = p["module"]
        if w not in weeks_map:
            weeks_map[w] = {"week": w, "modules": {}}
        if m not in weeks_map[w]["modules"]:
            weeks_map[w]["modules"][m] = {"module": m, "count": 0}
        weeks_map[w]["modules"][m]["count"] += 1

    result = []
    for w in sorted(weeks_map):
        entry = weeks_map[w]
        result.append({
            "week": entry["week"],
            "modules": list(entry["modules"].values()),
            "total_points": sum(md["count"] for md in entry["modules"].values()),
        })
    return result


# ============================================================================
# PROGRESS ENDPOINTS
# ============================================================================

def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {"completed": [], "started_at": None}

def save_progress(data: dict):
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))

@app.get("/api/progress")
def get_progress():
    return load_progress()

@app.post("/api/progress")
def update_progress(update: ProgressUpdate):
    from datetime import datetime
    data = load_progress()
    if data["started_at"] is None:
        data["started_at"] = datetime.now().isoformat()
    if update.completed:
        if update.module_id not in data["completed"]:
            data["completed"].append(update.module_id)
    else:
        data["completed"] = [m for m in data["completed"] if m != update.module_id]
    save_progress(data)
    return {"ok": True, "completed": len(data["completed"])}

@app.get("/api/stats")
def get_stats():
    data = load_progress()
    total = len(MODULES)
    done = len(data["completed"])
    return {
        "total": total,
        "completed": done,
        "percentage": round(done / total * 100) if total else 0,
    }

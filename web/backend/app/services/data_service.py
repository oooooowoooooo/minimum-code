"""Data service: file loading, caching, source extraction."""
from pathlib import Path

from app.schemas.module import Section
from app.repositories import json_repository

# Project root for source file access
PROJECT_ROOT = json_repository.PROJECT_ROOT


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

    return sections[:10]


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
    """Extract teaching sections from a TypeScript/TSX file."""
    content = read_file(filepath)
    if not content:
        return []

    sections = []
    current_title = ""
    current_lines = []
    in_section = False

    for line in content.split("\n"):
        section_match = line.startswith("// SECTION ") and ":" in line

        if line.startswith("// ==="):
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
            current_lines.append(line)
        elif not current_title and line.startswith("// ") and not line.startswith("// ==="):
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


# Module registry
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

# Source file mapping for module content
SOURCE_MAP = {
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


def get_module_sections(module_id: str) -> list[Section]:
    """Get sections for a module by reading its source file."""
    filepath = SOURCE_MAP.get(module_id)
    if not filepath:
        return []

    if filepath.suffix == ".py":
        return extract_sections_from_python(filepath)
    elif filepath.suffix in (".ts", ".tsx"):
        return extract_sections_from_ts(filepath)
    elif filepath.suffix == ".md":
        return extract_sections_from_markdown(filepath)

    return []


# Cached knowledge points data
_knowledge_points_data: dict = {"total_points": 0, "weeks": 0, "points": []}


def load_knowledge_points():
    """Load knowledge points from JSON into memory cache."""
    global _knowledge_points_data
    data = json_repository.read_json("knowledge_points.json")
    if data:
        _knowledge_points_data = data


def get_knowledge_points_data() -> dict:
    """Return the cached knowledge points data."""
    return _knowledge_points_data


# Progress helpers
def load_progress() -> dict:
    """Load progress from JSON file."""
    return json_repository.read_json("progress.json", default={"completed": [], "started_at": None})


def save_progress(data: dict):
    """Save progress to JSON file."""
    json_repository.write_json("progress.json", data)

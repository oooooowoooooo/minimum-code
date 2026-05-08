"""Module routes: list modules, get module content, quizzes."""
from fastapi import APIRouter, HTTPException

from app.schemas.module import ModuleInfo, ModuleContent, Section, QuizQuestion
from app.services import data_service

router = APIRouter(prefix="/api/modules", tags=["modules"])


@router.get("", response_model=list[ModuleInfo])
def list_modules():
    """List all modules."""
    return [ModuleInfo(**m) for m in data_service.MODULES]


@router.get("/{module_id}", response_model=ModuleContent)
def get_module(module_id: str):
    """Get module content by ID. Reads actual source files."""
    module = next((m for m in data_service.MODULES if m["id"] == module_id), None)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    sections = data_service.get_module_sections(module_id)

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


@router.get("/{module_id}/quiz", response_model=list[QuizQuestion])
def get_quiz(module_id: str):
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

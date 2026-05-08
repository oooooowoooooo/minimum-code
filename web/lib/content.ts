// Content registry: all learning content embedded from source files.
// Each module has sections with text explanations, code examples, and quizzes.

export interface QuizQuestion {
  question: string;
  options: string[];
  correct: number;
  explanation: string;
}

export interface Section {
  title: string;
  type: 'text' | 'code' | 'quiz';
  content: string;
  language?: 'python' | 'typescript' | 'markdown';
  quiz?: QuizQuestion[];
}

export interface ModuleContent {
  id: string;
  title: string;
  category: string;
  icon: string;
  sections: Section[];
}

// ────────────────────────────────────────────────────────────────
// Helper: build content quickly
// ────────────────────────────────────────────────────────────────

function text(title: string, content: string): Section {
  return { title, type: 'text', content };
}

function code(title: string, content: string, language: 'python' | 'typescript' | 'markdown' = 'python'): Section {
  return { title, type: 'code', content, language };
}

function quiz(title: string, questions: QuizQuestion[]): Section {
  return { title, type: 'quiz', content: '', quiz: questions };
}

// ────────────────────────────────────────────────────────────────
// COGNITIVE MODULES
// ────────────────────────────────────────────────────────────────

const cognitiveWhyLearn: ModuleContent = {
  id: 'cog-2',
  title: 'Why Learn Programming in the AI Era',
  category: 'cognitive',
  icon: '🧠',
  sections: [
    text('The Question Everyone Is Asking', `"AI can write code. Why should I learn to program?"

This question is everywhere. The answers are usually wrong — either dismissive ("AI will never replace real programmers") or fatalistic ("programming is dead, learn to prompt instead").

The truth is more interesting than either extreme.`),
    text('What AI Can Actually Do', `AI coding tools handle well:

• Generating boilerplate — REST APIs, React components, migrations in seconds
• Pattern matching across vast codebases — recognizes common patterns
• Translating between languages and formats
• Explaining existing code — paste code, get a clear explanation
• Writing tests — unit tests, edge cases, integration scaffolding`),
    text('What AI Cannot Do', `What AI consistently fails at:

• Understanding the problem — AI does not know your users are frustrated
• Making tradeoffs — monolith vs microservices requires context AI lacks
• Knowing what not to build — the most valuable skill is saying "we should not build this"
• Debugging novel failures — race conditions that only appear under specific load
• Defining quality — AI writes code that works, not code that is maintainable and elegant`),
    text('The Skill Hierarchy', `Level 5: Defining Problems     — What should we build and why?
Level 4: Making Tradeoffs      — What do we sacrifice for what we gain?
Level 3: Designing Systems     — How do the pieces fit together?
Level 2: Reading Code          — Understanding what exists
Level 1: Writing Code          — Typing out the implementation

AI is rapidly automating Level 1. It barely touches Level 4 and 5.

Most programming courses teach from the bottom up. The AI era demands starting from the top.`),
    text('The Autopilot Analogy', `AI is autopilot. You are the pilot.

Modern autopilot can fly the plane in normal conditions. It cannot decide where to fly, handle unexpected situations, or make judgment calls.

A pilot who only knows how to hand-fly is less valuable than one who understands navigation, weather, and decision-making. But a pilot who has never hand-flown — who does not understand what the autopilot is doing — is dangerous.

The same applies to programming. You need to understand code well enough to:
1. Direct AI to write the right thing
2. Evaluate whether what AI wrote is correct
3. Fix it when AI gets it wrong
4. Know when AI is the wrong tool entirely`),
    text('The New Career Path', `Traditional: Junior Developer → Senior Developer → Staff Engineer → Architect

AI-era: Problem Definer → System Designer → AI Director → Technical Leader

At each level, the human does less typing and more thinking. The value shifts from "I can implement this" to "I know this is the right thing to implement, and here is why."`),
    quiz('Test Your Understanding', [
      { question: 'What is the most valuable programming skill in the AI era?', options: ['Typing speed', 'Memorizing syntax', 'Knowing what code is worth writing', 'Using AI tools'], correct: 2, explanation: 'The programmers who thrive will be the ones who know what code is worth writing, not the ones who write the most code.' },
      { question: 'Which level of the skill hierarchy is AI worst at?', options: ['Writing code', 'Reading code', 'Designing systems', 'Defining problems'], correct: 3, explanation: 'AI cannot understand your business context, user needs, or organizational constraints. Defining problems is fundamentally human work.' },
      { question: 'In the autopilot analogy, what is your role?', options: ['The autopilot', 'The passenger', 'The pilot', 'The engineer'], correct: 2, explanation: 'You are the pilot. AI handles routine execution, but you make the decisions, handle exceptions, and know when to override.' },
    ]),
  ],
};

const cognitiveThinking: ModuleContent = {
  id: 'cog-1',
  title: 'AI-Era Thinking Models',
  category: 'cognitive',
  icon: '💡',
  sections: [
    text('Why Mental Models Matter', `Syntax changes. Frameworks come and go. But the way you think about problems determines your effectiveness across all tools, all languages, all eras.

These five mental models are practical thinking tools you will use every time you sit down to build something.`),
    text('Model 1: Pattern Recognition', `Pattern recognition is the ability to see structure before you see details. When you look at a problem, identify: "This is a data transformation problem" or "This is a request-response problem."

Why it matters for AI: When you describe a problem in terms of patterns, AI can apply the right solution template. When you describe it vaguely, AI guesses — and often guesses wrong.

Example: You need a notification system. Instead of thinking about email APIs, think: "This is a pub/sub problem. There are producers and consumers. I need a message broker between them." Now when you ask AI to help, it has a clear pattern to work with.`),
    text('Model 2: Abstraction Levels', `Every system exists at multiple levels of abstraction. Effective programmers move between levels fluidly.

Three levels to think at:
1. User level — what the user experiences
2. System level — how the pieces interact
3. Implementation level — how each piece works internally

When directing AI, work at the system level. Let AI handle implementation details.`),
    text('Model 3: Separation of Concerns', `Every piece of a system should have one reason to change. When you mix concerns, you create code that is hard to understand, test, and modify.

The "and" test: if you use the word "and" more than once when describing what code does, it is doing too much.

The "who cares" test: when you change one part, how many other parts need to change? If many, your concerns are not separated.`),
    text('Model 4: Type Safety as Documentation', `Types are not just compiler checks — they are documentation that never goes out of date. A function signature that says fetchUser(id: string): Promise<User> tells you more than any comment.

Think in types before you think in implementations. Before writing code, define your data shapes. What goes in? What comes out? What can go wrong?`),
    text('Model 5: Error Handling Philosophy', `Most code handles the happy path. Production code is defined by how it handles everything else.

Errors are not exceptions to the normal flow — they are an expected part of it. List what can go wrong before writing code. Use result types instead of exceptions. Fail fast in development, degrade gracefully in production.`),
    text('The AI-Era Workflow', `1. Define the problem clearly (what, not how)
2. Identify the pattern (what kind of problem is this?)
3. Choose the abstraction level (system level, not implementation level)
4. Separate concerns (one responsibility per piece)
5. Define types (what goes in, what comes out)
6. Enumerate errors (what can go wrong)
7. Direct AI to implement
8. Review AI output against your models

Steps 1-6 are your job. Step 7 is AI's job. Step 8 is your job again.`),
    quiz('Thinking Models Quiz', [
      { question: 'When directing AI, you should work at which abstraction level?', options: ['User level', 'System level', 'Implementation level', 'All levels equally'], correct: 1, explanation: 'Work at the system level. Define what the pieces do and how they interact. Let AI handle implementation details.' },
      { question: 'What does the "and" test check for?', options: ['Type safety', 'Separation of concerns', 'Pattern recognition', 'Error handling'], correct: 1, explanation: 'If describing code requires "and" more than once, the code is doing too many things and concerns are not separated.' },
    ]),
  ],
};

const cognitiveLanguages: ModuleContent = {
  id: 'cog-3',
  title: 'Why Python + TypeScript',
  category: 'cognitive',
  icon: '🎯',
  sections: [
    text('The Two Languages You Actually Need', `Not 10 languages. Not just one. Two.

Python = AI + Data + Backend
TypeScript = Frontend + Type Safety + Developer Experience
Together = Full-stack AI application development`),
    text('Python: The AI Language', `Why Python dominates AI:
1. Every AI framework is Python-first — PyTorch, TensorFlow, LangChain, OpenAI SDK
2. Data science ecosystem — pandas, numpy, scikit-learn
3. Fast prototyping — express ideas in fewer lines
4. Industry standard — 80%+ of AI/ML jobs require Python

Python is good at: AI/ML, data processing, backend APIs, scripting
Python is NOT good at: frontend UI, high-performance computing, mobile apps`),
    text('TypeScript: The Everything-Else Language', `Why TypeScript dominates web:
1. Type safety catches bugs before runtime
2. Frontend + Backend — same language for React + Node.js
3. Best DX — IDE autocomplete, refactoring, error detection
4. Industry standard — every major frontend framework uses TypeScript

TypeScript is good at: web frontend, backend APIs, desktop apps, type-safe APIs
TypeScript is NOT good at: AI/ML, systems programming, embedded systems`),
    text('The AI Application Stack', `Frontend (TypeScript)
├── React/Next.js UI
├── tRPC for type-safe API calls
└── Real-time updates (WebSocket/SSE)

Backend (Python)
├── FastAPI for REST/GraphQL
├── LangChain for LLM orchestration
├── Vector databases for RAG
└── Model training and inference`),
    text('The Numbers', `| Metric           | Python  | TypeScript |
|------------------|---------|------------|
| GitHub repos     | 2M+     | 1.5M+      |
| AI/ML jobs       | 85%     | 15%        |
| Frontend jobs    | 5%      | 90%        |
| Average salary   | $120k   | $115k      |

Python + TypeScript covers 90% of modern software development.`),
    quiz('Language Strategy Quiz', [
      { question: 'Which language should you use for an LLM orchestration backend?', options: ['TypeScript', 'Python', 'Either equally', 'Neither — use Rust'], correct: 1, explanation: 'Python has the best AI/ML ecosystem: LangChain, LlamaIndex, OpenAI SDK are all Python-first.' },
      { question: 'What does TypeScript give you that Python does not?', options: ['AI capabilities', 'Frontend ecosystem with type safety', 'Better performance', 'More libraries'], correct: 1, explanation: 'TypeScript provides the best frontend ecosystem (React, Next.js) with compile-time type safety that Python lacks.' },
    ]),
  ],
};

// ────────────────────────────────────────────────────────────────
// PYTHON FUNDAMENTALS
// ────────────────────────────────────────────────────────────────

const pyVariables: ModuleContent = {
  id: 'py-f-1',
  title: 'Variables & Types',
  category: 'python',
  icon: '📦',
  sections: [
    text('Architecture', `Python is dynamically typed — variables are names bound to objects, not boxes holding values. Every value is an object on the heap with a type tag and a reference count.

The name x = 42 creates an integer object 42 and binds the name x to it. Reassigning x = "hello" does not change the old object; it unbinds x from 42 and binds it to a new string object.`),
    code('Name Binding (Assignment)', `x = 42          # Name 'x' -> int object 42 (refcount=1)
y = x           # Name 'y' -> SAME int object 42 (refcount=2)

# Proof: both names point to the same object
print(x is y)           # True -- identity check
print(id(x) == id(y))   # True

# Rebinding x does NOT affect y
x = 100
print(f"x={x}, y={y}")  # x=100, y=42`, 'python'),
    code('Mutability vs Immutability', `# Immutable: str, int, tuple, frozenset, bytes
original = "hello"
modified = original.upper()   # Creates a NEW string object
print(original)               # "hello" -- unchanged

# Mutable: list, dict, set
a = [1, 2, 3]
b = a             # b and a refer to the SAME list
b.append(4)       # Mutate in place
print(a)          # [1, 2, 3, 4] -- a is affected!

# Independent copy
c = a.copy()
c.append(5)
print(a)          # [1, 2, 3, 4] -- a unchanged`, 'python'),
    code('Identity vs Equality', `a = [1, 2, 3]
b = [1, 2, 3]     # Different object, same value
print(a == b)      # True  -- same content
print(a is b)      # False -- different objects

# ALWAYS use == for value comparison.
# Use 'is' only for singletons: None, True, False
flag = None
print(flag is None)  # Correct way to check None`, 'python'),
    code('The Mutable Default Trap', `# WRONG: mutable default is evaluated ONCE
def append_to_bad(element, target=[]):
    target.append(element)
    return target

print(append_to_bad(1))  # [1]
print(append_to_bad(2))  # [1, 2] -- BUG! Same list reused.

# CORRECT: use None as sentinel
def append_to_good(element, target=None):
    if target is None:
        target = []
    target.append(element)
    return target`, 'python'),
    code('Shallow vs Deep Copy', `import copy

# Shallow copy: copies outer container, inner elements shared
outer = [[1, 2], [3, 4]]
shallow = copy.copy(outer)
shallow[0].append(999)
print(outer)  # [[1, 2, 999], [3, 4]] -- inner list shared!

# Deep copy: recursively copies everything
deep = copy.deepcopy(outer)
deep[0].append(999)
print(outer)  # [[1, 2, 999], [3, 4]] -- completely independent`, 'python'),
    text('Transferability', `Python Concept       | TypeScript           | Rust
Dynamic typing       | let x: unknown       | No equivalent (static)
Name binding         | Reference semantics   | let (move/copy)
Shallow copy         | { ...obj } / [...a]  | .clone() (deep by default)
is vs ==             | === vs Object.is()   | == vs ptr::eq()
Unpacking            | Destructuring        | Pattern matching`),
    quiz('Variables & Types Quiz', [
      { question: 'What does `a = [1, 2, 3]; b = a; b.append(4)` produce for `print(a)`?', options: ['[1, 2, 3]', '[1, 2, 3, 4]', 'Error', '[4, 1, 2, 3]'], correct: 1, explanation: 'b and a refer to the same list object. Mutating b also affects a.' },
      { question: 'Which comparison checks if two variables point to the same object?', options: ['==', 'is', '=', '!='], correct: 1, explanation: '`is` checks identity (same object in memory). `==` checks equality (same value).' },
      { question: 'Why is `def f(x=[])` dangerous?', options: ['It is not dangerous', 'The default list is created once and shared across calls', 'It causes a syntax error', 'It makes the function slower'], correct: 1, explanation: 'The default list is created ONCE when the function is defined, not each time it is called. All calls share the same list.' },
    ]),
  ],
};

const pyFunctions: ModuleContent = {
  id: 'py-f-2',
  title: 'Functions & Decorators',
  category: 'python',
  icon: '⚡',
  sections: [
    text('Architecture', `Functions in Python are first-class objects — they can be assigned to variables, passed as arguments, returned from other functions, and stored in data structures.

Decorators are syntactic sugar for higher-order functions. @decorator above a function definition is equivalent to func = decorator(func). This pattern is the backbone of modern Python frameworks:
- Flask: @app.route("/path")
- FastAPI: @app.get("/items/{item_id}")
- pytest: @pytest.fixture`),
    code('First-Class Functions', `def greet(name: str) -> str:
    return f"Hello, {name}!"

# Assign function to a variable
say_hello = greet
print(say_hello("World"))  # Hello, World!

# Functions can be stored in data structures
function_registry = {"greet": greet, "upper": str.upper}

# Functions can be passed as arguments
def apply(func, value):
    return func(value)

print(apply(str.upper, "hello"))  # HELLO`, 'python'),
    code('Closures', `def make_multiplier(factor):
    """Return a function that multiplies by factor."""
    def multiply(x):
        return x * factor  # captured from enclosing scope
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(5))   # 10
print(triple(5))   # 15

# Counter with nonlocal
def make_counter():
    count = 0
    def counter():
        nonlocal count  # Required to modify enclosing variable
        count += 1
        return count
    return counter`, 'python'),
    code('Basic Decorators', `from functools import wraps

def log_calls(func):
    """Decorator that logs function calls."""
    @wraps(func)  # Preserves original function's metadata
    def wrapper(*args, **kwargs):
        print(f"  [LOG] Calling {func.__name__}({args})")
        result = func(*args, **kwargs)
        print(f"  [LOG] {func.__name__} returned {result}")
        return result
    return wrapper

@log_calls
def add_numbers(a: int, b: int) -> int:
    return a + b

result = add_numbers(3, 5)
# [LOG] Calling add_numbers((3, 5))
# [LOG] add_numbers returned 8`, 'python'),
    code('Decorators with Arguments', `# Decorators with arguments need THREE levels of nesting
def repeat(n: int):
    """Decorator that calls the function n times."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(n):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(3)
def say(message: str) -> str:
    print(message)
    return message

say("hello")  # prints "hello" three times`, 'python'),
    code('The FastAPI Decorator Pattern', `class MiniRouter:
    """Simplified version of FastAPI's routing decorator."""
    def __init__(self):
        self._routes = {}

    def get(self, path: str):
        def decorator(func):
            self._routes[("GET", path)] = func
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

app = MiniRouter()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

# This mirrors FastAPI exactly`, 'python'),
    quiz('Functions & Decorators Quiz', [
      { question: 'What does @wraps(func) do?', options: ['Makes the decorator faster', 'Preserves the original function __name__ and __doc__', 'Makes the function async', 'Caches function results'], correct: 1, explanation: '@wraps preserves the original function\'s metadata (__name__, __doc__, etc.).' },
      { question: 'Decorators with arguments require how many levels of nesting?', options: ['1', '2', '3', '4'], correct: 2, explanation: 'Three levels: outer (decorator args), middle (func), inner (wrapper).' },
      { question: 'What is the output of: def outer(): x=10; def inner(): return x; return inner; f=outer(); print(f())', options: ['10', 'Error', 'None', '<function>'], correct: 0, explanation: 'inner() captures x from the enclosing scope via closure.' },
    ]),
  ],
};

const pyClasses: ModuleContent = {
  id: 'py-f-3',
  title: 'Classes & Inheritance',
  category: 'python',
  icon: '🏗️',
  sections: [
    text('Architecture', `Python's OOP is built on two core ideas:
1. Everything is an object (even classes themselves are objects of type 'type')
2. Attribute lookup follows the Method Resolution Order (MRO)

Modern Python favors:
- dataclasses for data containers (reduce boilerplate)
- Protocol (structural typing) over ABC (nominal typing)
- Composition over inheritance
- Dunder methods for Pythonic interfaces`),
    code('Dataclasses', `from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float

p1 = Point(1.0, 2.0)
p2 = Point(1.0, 2.0)
print(p1 == p2)  # True (value equality, auto-generated)

@dataclass
class Config:
    host: str = "localhost"
    port: int = 8080
    tags: list = field(default_factory=list)  # Mutable default needs factory

# Frozen dataclass (immutable, hashable)
@dataclass(frozen=True)
class Color:
    r: int; g: int; b: int
    def hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"`, 'python'),
    code('Dunder Methods', `class Vector:
    def __init__(self, x: float, y: float):
        self.x = x; self.y = y

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __add__(self, other) -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __abs__(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __len__(self) -> int:
        return 2

    def __iter__(self):
        yield self.x; yield self.y

v = Vector(3, 4)
print(abs(v))        # 5.0
print(list(v))       # [3, 4]`, 'python'),
    code('Protocol (Structural Typing)', `from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...

class Widget:
    def __init__(self, label: str):
        self.label = label
    def draw(self) -> str:
        return f"[Widget: {self.label}]"

# Widget satisfies Drawable without inheriting from it
widget = Widget("Test")
print(isinstance(widget, Drawable))  # True

def render(item: Drawable) -> str:
    return item.draw()  # Accepts anything with draw()`, 'python'),
    code('Composition over Inheritance', `class Logger:
    def log(self, message: str) -> str:
        return f"[LOG] {message}"

class Validator:
    def validate_email(self, email: str) -> bool:
        return "@" in email

class UserService:
    """Uses composition: has-a Logger and Validator."""
    def __init__(self):
        self.logger = Logger()
        self.validator = Validator()

    def register(self, email: str, name: str) -> str:
        if not self.validator.validate_email(email):
            return self.logger.log(f"Invalid email: {email}")
        return self.logger.log(f"Registered: {name}")`, 'python'),
    quiz('Classes Quiz', [
      { question: 'What does @dataclass automatically generate?', options: ['__init__, __repr__, __eq__', '__init__ only', '__str__ and __hash__', 'Nothing'], correct: 0, explanation: '@dataclass auto-generates __init__, __repr__, __eq__, and optionally __hash__, __lt__, etc.' },
      { question: 'What is the difference between ABC and Protocol?', options: ['ABC uses nominal typing; Protocol uses structural typing', 'ABC is faster', 'Protocol requires inheritance', 'They are identical'], correct: 0, explanation: 'ABC requires explicit inheritance (nominal). Protocol matches by structure (duck typing made explicit).' },
      { question: 'What does @dataclass(frozen=True) do?', options: ['Makes the class faster', 'Makes instances immutable and hashable', 'Prevents subclassing', 'Disables __repr__'], correct: 1, explanation: 'Frozen dataclasses are immutable and can be used as dict keys (hashable).' },
    ]),
  ],
};

const pyAsync: ModuleContent = {
  id: 'py-f-5',
  title: 'Async Programming',
  category: 'python',
  icon: '🔄',
  sections: [
    text('Architecture', `Python's async model is built on coroutines — functions that can suspend and resume execution. When a coroutine awaits (e.g., network I/O), the event loop runs other coroutines.

Key insight: async is for I/O-bound work (network, file, database), NOT CPU-bound work. For CPU-bound tasks, use multiprocessing.`),
    code('Coroutines and Await', `import asyncio

async def fetch_data(source: str, delay: float) -> str:
    print(f"  Fetching from {source}...")
    await asyncio.sleep(delay)  # Simulate network delay
    return f"Data from {source}"

# Sequential: each await waits for the previous one (~0.3s)
data1 = await fetch_data("API-1", 0.1)
data2 = await fetch_data("API-2", 0.1)

# Concurrent with gather: all start simultaneously (~0.1s)
results = await asyncio.gather(
    fetch_data("API-1", 0.1),
    fetch_data("API-2", 0.1),
    fetch_data("API-3", 0.1),
)`, 'python'),
    code('TaskGroup (Python 3.11+)', `# Structured concurrency with better error handling
async with asyncio.TaskGroup() as tg:
    task1 = tg.create_task(fetch_data("API-1", 0.1))
    task2 = tg.create_task(fetch_data("API-2", 0.1))
    task3 = tg.create_task(fetch_data("API-3", 0.1))

# All tasks done when we exit the block
results = [task1.result(), task2.result(), task3.result()]

# If any task fails, all others are cancelled
try:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(slow_ok())
        tg.create_task(fast_fail())
except* ValueError as eg:
    print(f"Caught {len(eg.exceptions)} error(s)")`, 'python'),
    code('Async Context Managers', `class AsyncDatabaseConnection:
    async def __aenter__(self):
        print("Connecting...")
        await asyncio.sleep(0.01)
        self.connected = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await asyncio.sleep(0.01)
        self.connected = False
        print("Disconnected")

# Usage
async with AsyncDatabaseConnection() as db:
    result = await db.query("SELECT * FROM users")`, 'python'),
    code('Semaphores for Rate Limiting', `async def rate_limited_task(task_id, semaphore):
    async with semaphore:
        print(f"Task {task_id} started")
        await asyncio.sleep(0.1)
        return f"result-{task_id}"

semaphore = asyncio.Semaphore(2)  # Max 2 concurrent
results = await asyncio.gather(*[
    rate_limited_task(i, semaphore) for i in range(6)
])
# 6 tasks run in 3 batches of 2`, 'python'),
    text('Transferability', `Python Concept       | TypeScript           | Rust
async/await          | async/await          | async/await
gather()             | Promise.all()        | tokio::join!()
TaskGroup            | Promise.allSettled()  | tokio::JoinSet
Semaphore            | p-limit              | tokio::Semaphore
event loop           | Node.js event loop   | tokio runtime`),
    quiz('Async Programming Quiz', [
      { question: 'What does `await` do?', options: ['Creates a new thread', 'Pauses the coroutine until the awaited task completes', 'Blocks the entire program', 'Creates a new process'], correct: 1, explanation: 'await pauses the coroutine, allowing other coroutines to run on the event loop.' },
      { question: 'When should you use async?', options: ['CPU-bound work', 'I/O-bound work (network, file, database)', 'Always', 'Never'], correct: 1, explanation: 'Async is for I/O-bound work. Use multiprocessing for CPU-bound work.' },
    ]),
  ],
};

const pyTypes: ModuleContent = {
  id: 'py-f-6',
  title: 'Type Annotations',
  category: 'python',
  icon: '🏷️',
  sections: [
    text('Architecture', `Python is dynamically typed, but since 3.5 it supports optional type annotations. These are NOT enforced at runtime — they are hints for type checkers (mypy, pyright) and IDEs.

Type annotations serve three purposes:
1. Documentation: types tell developers what functions expect/return
2. Tooling: IDEs provide better autocomplete and error detection
3. Verification: type checkers catch bugs before runtime`),
    code('Basic Annotations', `# Variable annotations
name: str = "Alice"
age: int = 30
scores: list[float] = [98.5, 87.0, 92.3]

# Function annotations
def greet(name: str) -> str:
    return f"Hello, {name}!"

def process_items(items: list[int], threshold: float = 0.5) -> dict[str, int]:
    return {"count": len(items), "above": sum(1 for x in items if x > threshold)}`, 'python'),
    code('Generics with TypeVar', `from typing import TypeVar, Generic, Sequence

T = TypeVar('T')  # Unconstrained: any type

def first(items: Sequence[T]) -> T | None:
    """Return the first item or None."""
    for item in items:
        return item
    return None

# Generic class
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []
    def push(self, item: T) -> None:
        self._items.append(item)
    def pop(self) -> T:
        return self._items.pop()

int_stack: Stack[int] = Stack()
int_stack.push(1)  # Type checker ensures only ints`, 'python'),
    code('Literal Types and Overloads', `from typing import Literal, overload

# Literal restricts to specific values
def set_log_level(level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]) -> str:
    return f"Log level set to {level}"

# Overloads: multiple signatures for one function
@overload
def double(value: int) -> int: ...
@overload
def double(value: str) -> str: ...
def double(value: int | str) -> int | str:
    return value * 2

print(double(5))       # 10 (type: int)
print(double("ab"))    # "abab" (type: str)`, 'python'),
    quiz('Type Annotations Quiz', [
      { question: 'When are type annotations enforced in Python?', options: ['Always at runtime', 'Never — they are hints for type checkers', 'Only in production', 'Only with mypy installed'], correct: 1, explanation: 'Python does NOT enforce types at runtime. Annotations are hints for type checkers and IDEs.' },
      { question: 'What does TypeVar create?', options: ['A concrete type', 'A type parameter for generic functions/classes', 'A runtime type check', 'A new class'], correct: 1, explanation: 'TypeVar creates a type parameter placeholder for generics.' },
    ]),
  ],
};

const pyModules: ModuleContent = {
  id: 'py-f-4',
  title: 'Modules & Packages',
  category: 'python',
  icon: '📚',
  sections: [
    text('Architecture', `Python's module system is based on the filesystem:
- A .py file is a module
- A directory with __init__.py is a package
- import searches sys.path for modules
- __all__ controls what "from package import *" exposes`),
    code('Import Styles', `# 1. import module
import collections
counter = collections.Counter([1, 1, 2])

# 2. import module as alias
import collections as coll
deque = coll.deque([1, 2, 3])

# 3. from module import name
from collections import Counter, defaultdict

# 4. from module import name as alias
from collections import OrderedDict as OD

# 5. from module import * (discouraged -- pollutes namespace)`, 'python'),
    code('__init__.py and __all__', `# mypackage/__init__.py
from .core import process, validate
from .models.user import User

__all__ = ["process", "validate", "User"]
__version__ = "1.0.0"

# __all__ controls what "from package import *" exposes
# Without __all__, everything without _prefix is exported`, 'python'),
    code('Fixing Circular Imports', `# PROBLEM: a.py imports from b.py, b.py imports from a.py

# SOLUTION 1: Lazy import (inside function)
def func_b():
    from a import func_a  # Import when needed
    return func_a() + 1

# SOLUTION 2: Move shared code to c.py
# SOLUTION 3: TYPE_CHECKING guard
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from a import SomeType  # Only for type checkers`, 'python'),
    quiz('Modules Quiz', [
      { question: 'What makes a directory a Python package?', options: ['It contains .py files', 'It has an __init__.py file', 'It is in sys.path', 'It has a pyproject.toml'], correct: 1, explanation: '__init__.py marks a directory as a package.' },
      { question: 'What does __all__ control?', options: ['What import module exposes', 'What from module import * exposes', 'What the type checker sees', 'What is listed in __init__.py'], correct: 1, explanation: '__all__ controls wildcard imports only.' },
    ]),
  ],
};

// ────────────────────────────────────────────────────────────────
// TYPESCRIPT FUNDAMENTALS
// ────────────────────────────────────────────────────────────────

const tsTypes: ModuleContent = {
  id: 'ts-f-1',
  title: 'TypeScript Type System',
  category: 'typescript',
  icon: '🔷',
  sections: [
    text('Architecture', `TypeScript adds a structural type system on top of JavaScript's dynamic nature. Types are erased at compile time — they exist only to help the developer catch bugs before runtime. Zero runtime cost with maximum developer ergonomics.`),
    code('Primitives and unknown vs any', `let appName: string = "TypeScript";
let version: number = 1;
let isProduction: boolean = false;

// "any" disables type checking -- avoid it.
let dangerous: any = 42;
dangerous = "now a string"; // No error

// "unknown" is the type-safe alternative to "any"
let safeValue: unknown = 42;
// safeValue.toFixed(2); // ERROR: Object is of type 'unknown'
if (typeof safeValue === "number") {
  safeValue.toFixed(2); // OK after narrowing
}`, 'typescript'),
    code('Discriminated Unions (The Most Powerful Pattern)', `type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };

function calculateArea(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "rectangle":
      return shape.width * shape.height;
    case "triangle":
      return 0.5 * shape.base * shape.height;
  }
}

// Exhaustiveness check: compiler ensures all cases handled
function describeShape(shape: Shape): string {
  switch (shape.kind) {
    case "circle": return \`Circle r=\${shape.radius}\`;
    case "rectangle": return \`Rect \${shape.width}x\${shape.height}\`;
    default:
      const _exhaustive: never = shape;
      return _exhaustive; // compile error if case missing
  }
}`, 'typescript'),
    code('Type Narrowing', `// typeof narrowing
function processValue(value: string | number): string {
  if (typeof value === "string") return value.toUpperCase();
  return value.toFixed(2); // narrowed to number
}

// Custom type guards
function isFish(animal: Fish | Bird): animal is Fish {
  return "swim" in animal;
}

// keyof and indexed access
type UserKeys = keyof User; // "id" | "name" | "email"
type UserName = User["name"]; // string`, 'typescript'),
    quiz('TypeScript Types Quiz', [
      { question: 'What is the type-safe alternative to "any"?', options: ['void', 'unknown', 'object', 'never'], correct: 1, explanation: 'unknown requires narrowing before use. any disables all type checking.' },
      { question: 'What is a discriminated union?', options: ['A union with a shared literal property for type narrowing', 'A class with multiple constructors', 'A generic type parameter', 'An intersection of two types'], correct: 0, explanation: 'A discriminated union uses a shared literal property (like "kind") to narrow the type in switch/if.' },
      { question: 'What does the "never" type represent?', options: ['An empty object', 'Values that never occur', 'A null value', 'An undefined value'], correct: 1, explanation: 'never represents values that never occur — used for exhaustive checks and functions that never return.' },
    ]),
  ],
};

const tsFunctions: ModuleContent = {
  id: 'ts-f-2',
  title: 'Functions & Generics',
  category: 'typescript',
  icon: '⚙️',
  sections: [
    text('Architecture', `Functions are the primary unit of composition in TypeScript. Generics enable writing code once that works across many types. Function overloads handle multiple call signatures.`),
    code('Generics', `// Basic generic function
function identity<T>(value: T): T {
  return value;
}
identity<string>("hello"); // type: string
identity(42);              // type: number, inferred

// Generic with constraints
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
const person = { name: "Alice", age: 30 };
getProperty(person, "name"); // type: string
// getProperty(person, "email"); // compile error`, 'typescript'),
    code('Generic Repository Pattern', `interface Repository<T> {
  findById(id: string): Promise<T | undefined>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<T>;
  delete(id: string): Promise<boolean>;
}

class InMemoryRepository<T extends { id: string }> implements Repository<T> {
  private store = new Map<string, T>();

  async findById(id: string): Promise<T | undefined> {
    return this.store.get(id);
  }
  async save(entity: T): Promise<T> {
    this.store.set(entity.id, entity);
    return entity;
  }
}`, 'typescript'),
    code('Function Overloads', `// Overloads: different signatures, one implementation
function parseInput(input: string): object;
function parseInput(input: object): string;
function parseInput(input: string | object): string | object {
  if (typeof input === "string") return JSON.parse(input);
  return JSON.stringify(input);
}

parseInput('{"a":1}'); // returns { a: 1 }
parseInput({ a: 1 }); // returns '{"a":1}'`, 'typescript'),
    code('Higher-Order Functions and Currying', `// Curried function
function curry<A, B, C>(fn: (a: A, b: B) => C): (a: A) => (b: B) => C {
  return (a) => (b) => fn(a, b);
}

const curriedAdd = curry((a: number, b: number) => a + b);
const add5 = curriedAdd(5);
add5(3); // 8

// Type predicates for narrowing
function isNonNullable<T>(value: T | null | undefined): value is T {
  return value !== null && value !== undefined;
}

const values: (string | null)[] = ["a", null, "b"];
const nonNull = values.filter(isNonNullable); // string[]`, 'typescript'),
    quiz('TypeScript Functions Quiz', [
      { question: 'What does <T> in a function signature mean?', options: ['A runtime type parameter', 'A compile-time type parameter for generics', 'A template literal', 'A decorator'], correct: 1, explanation: '<T> is a type parameter that lets functions work with any type while preserving type safety.' },
      { question: 'What does "K extends keyof T" mean?', options: ['K must be a string', 'K must be a key that exists in T', 'K must be a number', 'K must be optional'], correct: 1, explanation: 'It constrains K to only be a valid key of T, preventing invalid property access.' },
    ]),
  ],
};

const tsInterfaces: ModuleContent = {
  id: 'ts-f-3',
  title: 'Interfaces & Type Manipulation',
  category: 'typescript',
  icon: '🔧',
  sections: [
    text('Architecture', `TypeScript's type system is TURING-COMPLETE. You can compute types from other types, transforming shapes, extracting subsets, and building new types at compile time.`),
    code('Mapped Types', `// Transform every property in a type
type MyPartial<T> = { [K in keyof T]?: T[K] };
type MyReadonly<T> = { readonly [K in keyof T]: T[K] };

// Key remapping (TS 4.1+)
type Getters<T> = {
  [K in keyof T as \`get\${Capitalize<string & K>}\`]: () => T[K];
};
type UserGetters = Getters<User>;
// { getId: () => number; getName: () => string; ... }`, 'typescript'),
    code('Conditional Types with infer', `// Extract return type of a function
type MyReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
type R1 = MyReturnType<() => string>; // string

// Extract array element type
type ElementOf<T> = T extends (infer E)[] ? E : never;
type El = ElementOf<string[]>; // string

// Unwrap Promise
type Unwrap<T> = T extends Promise<infer U> ? U : T;
type DeepUnwrap<T> = T extends Promise<infer U> ? DeepUnwrap<U> : T;
type Deep = DeepUnwrap<Promise<Promise<string>>>; // string`, 'typescript'),
    code('Template Literal Types', `type Color = "red" | "blue" | "green";
type Size = "sm" | "md" | "lg";
type ColorSize = \`\${Color}-\${Size}\`;
// "red-sm" | "red-md" | ... (9 combinations)

type EventName = "click" | "focus" | "blur";
type HandlerName = \`on\${Capitalize<EventName>}\`;
// "onClick" | "onFocus" | "onBlur"`, 'typescript'),
    code('Branded Types (Nominal Typing)', `type Brand<T, B extends string> = T & { readonly __brand: B };

type UserId = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;

function getUser(id: UserId): string { return \`User: \${id}\`; }

const userId = "user-123" as UserId;
const orderId = "order-456" as OrderId;

getUser(userId);   // OK
// getUser(orderId); // ERROR: OrderId is not assignable to UserId`, 'typescript'),
    quiz('Type Manipulation Quiz', [
      { question: 'What does "infer" do in conditional types?', options: ['Creates a new variable', 'Extracts a type from within another type', 'Makes a type optional', 'Creates a union type'], correct: 1, explanation: 'infer extracts a type from within another type in a conditional type.' },
      { question: 'What are branded types used for?', options: ['Making types faster', 'Adding nominal typing to TypeScript\'s structural system', 'Creating new classes', 'Defining interfaces'], correct: 1, explanation: 'Branded types add nominal typing so UserId and OrderId (both strings) are not interchangeable.' },
    ]),
  ],
};

const tsAsync: ModuleContent = {
  id: 'ts-f-5',
  title: 'Async Programming',
  category: 'typescript',
  icon: '⏳',
  sections: [
    text('Architecture', `JavaScript is single-threaded with an event loop. Async is concurrency via cooperative multitasking, not parallelism. Promises represent future values; async/await is syntactic sugar over Promises.`),
    code('Promises and async/await', `// Creating a Promise
function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// async function returns Promise<T>
async function getUserProfile(userId: number) {
  const user = await fetchUser(userId);
  const email = await fetchEmail(user.name);
  return { name: user.name, email };
}`, 'typescript'),
    code('Promise.all vs Promise.allSettled', `// Promise.all: fails fast if ANY rejects
const results = await Promise.all([
  fetchUser(1),
  fetchUser(2),
  fetchUser(3),
]);

// Promise.allSettled: waits for ALL, never fails
const results = await Promise.allSettled([
  fetchUser(1),
  fetchUser(-1), // rejects, but we still get results
]);
for (const r of results) {
  if (r.status === "fulfilled") console.log(r.value);
  else console.error(r.reason);
}`, 'typescript'),
    code('Concurrency Patterns', `// Concurrent with limit
async function concurrentLimit<T, R>(
  items: T[],
  fn: (item: T) => Promise<R>,
  limit: number
): Promise<R[]> {
  const results: R[] = new Array(items.length);
  let index = 0;
  async function worker() {
    while (index < items.length) {
      const i = index++;
      results[i] = await fn(items[i]);
    }
  }
  await Promise.all(
    Array.from({ length: Math.min(limit, items.length) }, () => worker())
  );
  return results;
}`, 'typescript'),
    code('AbortController for Cancellation', `async function fetchWithAbort(url: string, signal: AbortSignal) {
  return fetch(url, { signal });
}

const controller = new AbortController();
setTimeout(() => controller.abort(), 5000); // cancel after 5s

try {
  const response = await fetchWithAbort("/api/data", controller.signal);
} catch (error) {
  if (error instanceof DOMException && error.name === "AbortError") {
    console.log("Request was cancelled");
  }
}`, 'typescript'),
    quiz('TypeScript Async Quiz', [
      { question: 'What is the difference between Promise.all and Promise.allSettled?', options: ['They are identical', 'all fails fast; allSettled waits for all', 'allSettled fails fast', 'all is faster'], correct: 1, explanation: 'Promise.all rejects immediately if any promise rejects. Promise.allSettled waits for all to settle.' },
      { question: 'What does AbortController do?', options: ['Pauses execution', 'Cancels async operations cleanly', 'Creates a new thread', 'Retries failed operations'], correct: 1, explanation: 'AbortController provides a signal that can cancel fetch requests and other async operations.' },
    ]),
  ],
};

const tsModules: ModuleContent = {
  id: 'ts-f-4',
  title: 'Module System',
  category: 'typescript',
  icon: '📁',
  sections: [
    text('Architecture', `TypeScript supports ES Modules (standard) and CommonJS (Node.js legacy). Each file is a module. TypeScript compiles ES module syntax to the target module system in tsconfig.json.`),
    code('ES Module Exports', `// Named exports
export const API_VERSION = "v1";
export function formatEndpoint(path: string): string {
  return \`\${API_VERSION}/\${path}\`;
}
export interface ApiResponse<T> { data: T; status: number; }

// Default export (one per file)
export default class ApiClient { /* ... */ }

// Re-exports
export { User } from "./types.js";
export * from "./utils.js";`, 'typescript'),
    code('Dynamic Import (Code Splitting)', `// Load modules on demand
async function loadChartLibrary() {
  const chartModule = await import("./chart-library.js");
  return chartModule.Chart;
}

// Lazy initialization
let cachedModule: typeof import("./expensive.js") | null = null;
async function getExpensiveModule() {
  if (!cachedModule) cachedModule = await import("./expensive.js");
  return cachedModule;
}`, 'typescript'),
    text('Key Patterns', `Barrel files: index.ts re-exports from sub-modules for clean imports.
Module augmentation: extend existing modules (e.g., add userId to Express Request).
import type: erased at compile time, zero runtime cost.
Path mapping: "@utils/*" -> "./src/utils/*" in tsconfig.json.

ES Modules are the standard. Use named exports for tree-shaking. Default exports are one per file. Dynamic import() enables code splitting and lazy loading.`),
    quiz('TypeScript Modules Quiz', [
      { question: 'What is a barrel file?', options: ['A file that stores data', 'An index.ts that re-exports from sub-modules', 'A configuration file', 'A test file'], correct: 1, explanation: 'A barrel file (index.ts) re-exports everything from a directory, providing a clean import API.' },
      { question: 'What does "import type" do?', options: ['Imports at runtime', 'Imports only for type checking, erased at compile time', 'Creates a new type', 'Imports a class'], correct: 1, explanation: 'import type is erased at compile time — zero runtime cost. Used for type-only imports.' },
    ]),
  ],
};

const tsDecorators: ModuleContent = {
  id: 'ts-f-6',
  title: 'Decorators & Metaprogramming',
  category: 'typescript',
  icon: '🎨',
  sections: [
    text('Architecture', `Decorators are functions that receive the decorated target and can modify it. They are applied at CLASS DEFINITION TIME, not at runtime method calls. Used extensively by NestJS, Angular, TypeORM.`),
    code('Class and Method Decorators', `// Class decorator: adds a timestamp
function Timestamped<T extends new (...args: any[]) => {}>(constructor: T) {
  return class extends constructor {
    createdAt = new Date();
  };
}

// Method decorator: logs calls
function Log(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
  const originalMethod = descriptor.value;
  descriptor.value = function (...args: any[]) {
    console.log(\`Calling \${propertyKey} with \${args}\`);
    const result = originalMethod.apply(this, args);
    console.log(\`\${propertyKey} returned \${result}\`);
    return result;
  };
}

class Calculator {
  @Log
  add(a: number, b: number) { return a + b; }
}`, 'typescript'),
    code('Decorator Factories', `// Parameterized decorator
function Retry(maxAttempts: number = 3) {
  return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;
    descriptor.value = async function (...args: any[]) {
      let lastError: Error | undefined;
      for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        try {
          return await originalMethod.apply(this, args);
        } catch (error) {
          lastError = error as Error;
        }
      }
      throw lastError;
    };
  };
}

class ApiService {
  @Retry(3)
  async fetchData() { /* ... */ }
}`, 'typescript'),
    text('Execution Order', `Multiple decorators on a single target are applied BOTTOM-UP.

@First
@Second
method() {}

// Execution: Second first, then First
// At call time: First wraps Second wraps the original method
// So execution goes: First -> Second -> method

This is identical to Python's decorator stacking behavior.`),
    quiz('TypeScript Decorators Quiz', [
      { question: 'When are decorators applied?', options: ['At runtime when the method is called', 'At class definition time', 'At compile time', 'At import time'], correct: 1, explanation: 'Decorators are applied at class definition time, not at runtime method calls.' },
      { question: 'What is the execution order of @First @Second method()?', options: ['First, then Second', 'Second, then First', 'Simultaneous', 'Random'], correct: 1, explanation: 'Decorators are applied bottom-up: Second wraps first, then First wraps Second.' },
    ]),
  ],
};

// ────────────────────────────────────────────────────────────────
// DESIGN PATTERNS
// ────────────────────────────────────────────────────────────────

function makePatternModule(id: string, title: string, icon: string, what: string, why: string, pyCode: string, tsCode: string, takeaways: string[], quizQs: QuizQuestion[]): ModuleContent {
  return {
    id, title, category: 'patterns', icon,
    sections: [
      text('What It Is', what),
      text('Why It Matters in the AI Era', why),
      code('Python Example', pyCode, 'python'),
      code('TypeScript Example', tsCode, 'typescript'),
      text('Key Takeaways', takeaways.map(t => `• ${t}`).join('\n')),
      quiz('Test Your Understanding', quizQs),
    ],
  };
}

const patFactory: ModuleContent = makePatternModule('pat-2', 'Factory', '🏭',
  `The Factory pattern provides an interface for creating objects without specifying their exact class. A factory function decides which concrete class to instantiate based on input parameters.`,
  `AI applications juggle multiple model providers, embedding backends, and data sources. A factory centralizes creation logic so callers ask for "an LLM client" by name.`,
  `from abc import ABC, abstractmethod

class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, text: str) -> list[float]: ...

class OpenAIEmbeddings(EmbeddingProvider):
    def __init__(self, api_key: str): self.api_key = api_key
    def embed(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]

def create_embedding_provider(provider: str, api_key: str = "") -> EmbeddingProvider:
    providers = {
        "openai": lambda: OpenAIEmbeddings(api_key),
        "cohere": lambda: CohereEmbeddings(api_key),
    }
    return providers[provider]()

embedder = create_embedding_provider("openai", api_key="sk-...")`,
  `interface EmbeddingProvider {
  embed(text: string): Promise<number[]>;
}

function createEmbeddingProvider(config: { provider: string; apiKey?: string }): EmbeddingProvider {
  switch (config.provider) {
    case "openai": return new OpenAIEmbeddings(config.apiKey!);
    case "cohere": return new CohereEmbeddings(config.apiKey!);
    default: throw new Error(\`Unknown provider: \${config.provider}\`);
  }
}`,
  ['Factories centralize object creation logic in one place.',
   'Callers program against an interface, not a concrete class.',
   'In AI apps, factories handle provider selection cleanly.'],
  [
    { question: 'What is the main benefit of the Factory pattern?', options: ['Faster execution', 'Centralized creation logic, easy to add new implementations', 'Less code', 'Better type safety'], correct: 1, explanation: 'Factories centralize creation so adding new implementations requires changes in one place.' },
  ]
);

const patObserver: ModuleContent = makePatternModule('pat-4', 'Observer', '👁️',
  `The Observer pattern defines a one-to-many dependency. When one object changes state, all dependents are notified automatically. The subject broadcasts events without knowing who observes.`,
  `AI systems are event-driven: streaming LLM responses emit tokens, training loops emit metrics. Observer decouples producers from consumers.`,
  `class EventEmitter:
    def __init__(self):
        self._observers: dict[str, list] = {}

    def on(self, event: str, observer) -> None:
        self._observers.setdefault(event, []).append(observer)

    def emit(self, event: str, data=None) -> None:
        for obs in self._observers.get(event, []):
            obs(event, data)

# Streaming LLM example
llm = StreamingLLM()
llm.on("token", lambda e, data: print(f"Token: {data}"))
llm.on("done", lambda e, data: print(f"Total: {data['total_tokens']}"))
llm.generate("Say hello")`,
  `class EventEmitter {
  private listeners = new Map<string, Function[]>();

  on(event: string, handler: Function): void {
    const handlers = this.listeners.get(event) ?? [];
    handlers.push(handler);
    this.listeners.set(event, handlers);
  }

  emit(event: string, data?: unknown): void {
    for (const handler of this.listeners.get(event) ?? []) {
      handler(data);
    }
  }
}`,
  ['Observer decouples event producers from consumers.',
   'Streaming LLM responses are a natural fit: tokens are events.',
   'Beware of observer loops and memory leaks from forgotten subscriptions.'],
  [
    { question: 'What does the Observer pattern decouple?', options: ['Data from storage', 'Event producers from consumers', 'Functions from arguments', 'Classes from interfaces'], correct: 1, explanation: 'Observer decouples the event producer from consumers — neither needs to know about the other.' },
  ]
);

const patStrategy: ModuleContent = makePatternModule('pat-3', 'Strategy', '🎯',
  `The Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable. The context holds a reference to a strategy interface and delegates work to whichever strategy is plugged in.`,
  `AI systems face constant model churn. Strategy lets you swap the inference backend without changing application logic.`,
  `from abc import ABC, abstractmethod
from dataclasses import dataclass

class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, input_tokens: int, output_tokens: int) -> float: ...

class OpenAIPricing(PricingStrategy):
    def calculate(self, input_tokens, output_tokens):
        return input_tokens / 1000 * 0.005 + output_tokens / 1000 * 0.015

@dataclass
class CostTracker:
    strategy: PricingStrategy
    total_cost: float = 0.0

    def record_call(self, input_tokens, output_tokens) -> float:
        cost = self.strategy.calculate(input_tokens, output_tokens)
        self.total_cost += cost
        return cost

# Swap strategies at runtime
tracker = CostTracker(strategy=OpenAIPricing())`,
  `interface PricingStrategy {
  calculate(inputTokens: number, outputTokens: number): number;
}

class CostTracker {
  private totalCost = 0;
  constructor(public strategy: PricingStrategy) {}

  recordCall(inputTokens: number, outputTokens: number): number {
    const cost = this.strategy.calculate(inputTokens, outputTokens);
    this.totalCost += cost;
    return cost;
  }
}`,
  ['Strategy eliminates long if/elif/else chains.',
   'Strategies can be swapped at runtime based on config.',
   'In AI systems, strategy handles model selection, pricing, retry logic.'],
  [
    { question: 'What does the Strategy pattern eliminate?', options: ['Loops', 'Long if/elif/else chains for algorithm selection', 'Type errors', 'Memory leaks'], correct: 1, explanation: 'Strategy replaces conditional branches with interchangeable algorithm objects.' },
  ]
);

const patPipeline: ModuleContent = makePatternModule('pat-7', 'Pipeline', '🔧',
  `The Pipeline pattern chains processing stages where each stage's output becomes the next stage's input. Each stage is self-contained and performs one transformation.`,
  `AI workflows are inherently sequential: preprocess → build prompt → call LLM → parse response → validate. Pipelines make these steps explicit, testable, and rearrangeable.`,
  `from dataclasses import dataclass, field

@dataclass
class PipelineContext:
    query: str
    documents: list[str] = field(default_factory=list)
    prompt: str = ""
    response: str = ""

class Pipeline:
    def __init__(self):
        self.stages = []

    def add_stage(self, name, fn):
        self.stages.append(fn)
        return self

    def execute(self, ctx: PipelineContext) -> PipelineContext:
        for stage in self.stages:
            ctx = stage(ctx)
        return ctx

rag = Pipeline()
rag.add_stage("normalize", normalize_query)
rag.add_stage("retrieve", retrieve_documents)
rag.add_stage("llm_call", call_llm)
result = rag.execute(PipelineContext(query="What is DI?"))`,
  `type StageFn = (ctx: PipelineContext) => PipelineContext | Promise<PipelineContext>;

class Pipeline {
  private stages: Stage[] = [];
  addStage(name: string, fn: StageFn): this {
    this.stages.push({ name, execute: fn });
    return this;
  }
  async execute(context: PipelineContext): Promise<PipelineContext> {
    let ctx = context;
    for (const stage of this.stages) {
      ctx = await stage.execute(ctx);
    }
    return ctx;
  }
}`,
  ['Pipelines decompose complex workflows into sequential, single-responsibility stages.',
   'RAG, summarization, and multi-step reasoning are natural pipelines.',
   'Unlike middleware, pipelines are the central flow — stages transform data in sequence.'],
  [
    { question: 'What is RAG an example of?', options: ['Observer pattern', 'Pipeline pattern', 'Factory pattern', 'Singleton pattern'], correct: 1, explanation: 'RAG is a textbook pipeline: embed query → search → retrieve → construct prompt → call LLM → return answer.' },
  ]
);

const patMiddleware: ModuleContent = makePatternModule('pat-5', 'Middleware', '🔗',
  `Middleware is a chain of processing units between request and response. Each middleware can inspect, modify, or short-circuit a request before passing it to the next handler.`,
  `AI applications need cross-cutting concerns: authentication, rate limiting, token counting, prompt injection detection. Middleware lets you add these without touching the LLM call.`,
  `Handler = Callable[[Request], Response]
Middleware = Callable[[Request, Handler], Response]

def logging_middleware(request, next_handler):
    start = time.time()
    response = next_handler(request)
    print(f"Completed in {time.time() - start:.2f}s")
    return response

def auth_middleware(request, next_handler):
    if not request.metadata.get("api_key"):
        return Response(text="Unauthorized")
    return next_handler(request)

def build_chain(middlewares, final_handler):
    handler = final_handler
    for mw in reversed(middlewares):
        handler = lambda req, h=handler, m=mw: m(req, h)
    return handler`,
  `type Middleware = (req: Request, next: Handler) => Promise<Response>;

const loggingMiddleware: Middleware = async (req, next) => {
  const start = Date.now();
  const response = await next(req);
  console.log(\`Completed in \${Date.now() - start}ms\`);
  return response;
};

function buildChain(middlewares: Middleware[], handler: Handler): Handler {
  let chain = handler;
  for (const mw of [...middlewares].reverse()) {
    const prev = chain;
    chain = (req) => mw(req, prev);
  }
  return chain;
}`,
  ['Middleware decomposes cross-cutting concerns into composable units.',
   'Each middleware decides: handle, pass along, or short-circuit.',
   'Order matters: the sequence determines which checks run first.'],
  [
    { question: 'What is the key difference between middleware and pipeline?', options: ['There is no difference', 'Middleware wraps a central handler; pipeline is the central flow', 'Pipeline is faster', 'Middleware is async'], correct: 1, explanation: 'Middleware wraps around a handler (Russian doll). Pipeline is the flow itself — stages transform data sequentially.' },
  ]
);

const patRepository: ModuleContent = makePatternModule('pat-6', 'Repository', '🗄️',
  `The Repository pattern mediates between the domain layer and data storage. It provides a collection-like interface for accessing domain objects, abstracting away storage details.`,
  `AI applications have diverse storage needs: embeddings in vector DB, conversations in PostgreSQL, cached responses in Redis. Repository lets business logic work against a clean interface.`,
  `from abc import ABC, abstractmethod

class ConversationRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Conversation]: ...
    @abstractmethod
    def save(self, conversation: Conversation) -> None: ...

class InMemoryConversationRepository(ConversationRepository):
    def __init__(self):
        self._store: dict[str, Conversation] = {}

    def get_by_id(self, id: str) -> Optional[Conversation]:
        return self._store.get(id)
    def save(self, conversation: Conversation) -> None:
        self._store[conversation.id] = conversation

class ChatService:
    def __init__(self, repo: ConversationRepository):
        self.repo = repo  # depends on interface, not implementation`,
  `interface ConversationRepository {
  getById(id: string): Promise<Conversation | null>;
  save(conversation: Conversation): Promise<void>;
}

class ChatService {
  constructor(private repo: ConversationRepository) {}

  async sendMessage(conversationId: string, message: string): Promise<string> {
    let conversation = await this.repo.getById(conversationId);
    if (!conversation) {
      conversation = { id: conversationId, messages: [] };
    }
    conversation.messages.push({ role: "user", content: message });
    await this.repo.save(conversation);
    return "response";
  }
}`,
  ['Repository abstracts data access behind a clean interface.',
   'Business logic depends on the interface, not the storage implementation.',
   'In-memory implementations are ideal for unit tests.'],
  [
    { question: 'What does the Repository pattern abstract?', options: ['User interface', 'Data access behind a collection-like interface', 'Network requests', 'File system operations'], correct: 1, explanation: 'Repository provides a collection-like interface for data access, hiding storage details.' },
  ]
);

const patDI: ModuleContent = makePatternModule('pat-8', 'Dependency Injection', '💉',
  `Dependency Injection (DI) is a technique where an object receives its dependencies from an external source rather than creating them itself. This inverts control of dependency creation.`,
  `Modern AI applications compose many services: LLM clients, vector databases, embedding models. DI lets you swap any of these without rewriting core logic. Testability: inject mock LLMs for deterministic tests.`,
  `class ChatbotService:
    def __init__(self, llm: LLMClient):  # injected dependency
        self.llm = llm

    def chat(self, user_input: str) -> str:
        return self.llm.generate(user_input)

# Wiring: external code decides implementation
service = ChatbotService(llm=OpenAIClient(api_key="sk-..."))

# Testing: swap in mock
test_service = ChatbotService(llm=MockLLMClient("expected"))
assert test_service.chat("anything") == "expected"`,
  `class ChatbotService {
  constructor(private llm: LLMClient) {} // injected

  async chat(input: string): Promise<string> {
    return this.llm.generate(input);
  }
}

// Wiring
const service = new ChatbotService(new OpenAIClient("sk-..."));

// Testing
const testService = new ChatbotService(new MockLLMClient("expected"));`,
  ['DI separates "what to use" from "how to use it".',
   'Testing becomes trivial: swap real implementations for mocks.',
   'FastAPI uses Depends(), NestJS uses constructor injection.'],
  [
    { question: 'What is the main benefit of Dependency Injection?', options: ['Faster execution', 'Testability and swappable implementations', 'Less code', 'Better security'], correct: 1, explanation: 'DI makes testing trivial by allowing mock injection, and enables swapping implementations without code changes.' },
  ]
);

const patBuilder: ModuleContent = makePatternModule('pat-1', 'Builder', '🔨',
  `The Builder pattern separates construction of a complex object from its representation. Instead of a constructor with dozens of parameters, you use a step-by-step builder with sensible defaults.`,
  `AI API calls have many optional parameters: model, temperature, max_tokens, top_p, stop sequences. Builders handle this complexity elegantly.`,
  `@dataclass(frozen=True)
class LLMConfig:
    model: str
    temperature: float = 0.7
    max_tokens: int = 1024

class LLMConfigBuilder:
    def __init__(self, model: str):
        self._model = model
        self._temperature = 0.7
        self._max_tokens = 1024

    def with_temperature(self, temp: float) -> "LLMConfigBuilder":
        if not 0.0 <= temp <= 2.0:
            raise ValueError(f"Temperature must be 0-2")
        self._temperature = temp
        return self

    def build(self) -> LLMConfig:
        return LLMConfig(model=self._model, temperature=self._temperature,
                        max_tokens=self._max_tokens)

config = LLMConfigBuilder("gpt-4").with_temperature(0.3).build()`,
  `class LLMConfigBuilder {
  private temperature = 0.7;
  private maxTokens = 1024;
  constructor(private model: string) {}

  withTemperature(temp: number): this {
    if (temp < 0 || temp > 2) throw new Error("Temperature must be 0-2");
    this.temperature = temp;
    return this;
  }

  build(): LLMConfig {
    return Object.freeze({ model: this.model, temperature: this.temperature, maxTokens: this.maxTokens });
  }
}

const config = new LLMConfigBuilder("gpt-4").withTemperature(0.3).build();`,
  ['Builders turn "constructor with 15 parameters" into readable, chainable method calls.',
   'Validation logic lives in the builder, not scattered across callers.',
   'Builders handle the explosion of LLM parameters elegantly.'],
  [
    { question: 'What problem does the Builder pattern solve?', options: ['Slow constructors', 'Complex object construction with many optional parameters', 'Memory management', 'Thread safety'], correct: 1, explanation: 'Builders replace constructors with many parameters with readable, chainable method calls.' },
  ]
);

// ────────────────────────────────────────────────────────────────
// AI MASTERY
// ────────────────────────────────────────────────────────────────

const aiPrompt: ModuleContent = {
  id: 'ai-1',
  title: 'Prompt Engineering for Code',
  category: 'ai-mastery',
  icon: '✍️',
  sections: [
    text('Why Prompt Engineering Matters', `The same AI model can produce brilliant code or garbage code depending on the prompt. Prompt engineering is not about tricks — it is about clear communication of intent, constraints, and context.

A high-quality code prompt has five components:
1. Context — What is the broader system?
2. Task — What specific thing should be built?
3. Constraints — What are the rules and limitations?
4. Examples — What does good output look like?
5. Format — How should the output be structured?`),
    code('The Few-Shot Template Pattern', `Here is an example of how our service layer functions should look:

[TYPES]
type UserId = string & { readonly __brand: "UserId" };
type ServiceResult<T> = { ok: true; data: T } | { ok: false; error: string };

[EXAMPLE FUNCTION]
export async function createUser(input: CreateUserInput): Promise<ServiceResult<User>> {
    const existing = await db.user.findByEmail(input.email);
    if (existing) return { ok: false, error: "Email already registered" };
    const user = await db.user.create({ data: { ...input, id: generateId() } });
    return { ok: true, data: user };
}

Now write a function getUserById that fetches a user by ID.
Return { ok: false, error: "User not found" } if the ID does not exist.`, 'typescript'),
    text('Chain-of-Thought for Code', `Ask the AI to think before it writes code:

"I need a function that calculates shipping costs. Before writing code, think through:
1. What are all the inputs?
2. What are the business rules?
3. What are the edge cases?
4. What should the return type be?

After thinking through these, write the function with full error handling."

Without chain-of-thought, AI might write: def calculate_shipping(weight, destination): return weight * 0.5
With chain-of-thought, AI produces a well-considered function that handles edge cases.`),
    text('Common Pitfalls', `1. The Vague Prompt: "Write me a user auth system" → AI has no context. Be specific about tech stack, security requirements, data model.

2. The Overloaded Prompt: "Build me a complete e-commerce platform" → Break into focused prompts: data model, then API, then UI.

3. Trust-But-Don't-Verify: Never copy AI output directly into production. Review every line. Run it. Test it.

4. The Context-Free Prompt: "Fix this bug" without showing code, errors, or what you tried. AI cannot debug what it cannot see.

5. Ignoring the System Prompt: Maintain a long-running conversation with accumulated context.`),
    text('Iterative Refinement', `The best code rarely comes from a single prompt:

Round 1: "Here is the problem. Propose a design."
Round 2: "The design is good, but [concern]. Address that."
Round 3: "Now implement the core logic."
Round 4: "Add error handling and edge cases."
Round 5: "Write tests for this."
Round 6: "Review this code for security issues."

Each round builds on the previous one. The AI has full context from earlier rounds.`),
    quiz('Prompt Engineering Quiz', [
      { question: 'What is the most underused technique in code prompting?', options: ['System prompts', 'Few-shot examples', 'Temperature settings', 'Token limits'], correct: 1, explanation: 'Showing AI what good output looks like (few-shot) dramatically improves generation quality.' },
      { question: 'Why is chain-of-thought prompting useful for complex logic?', options: ['It makes AI faster', 'It forces AI to consider edge cases before coding', 'It uses fewer tokens', 'It works offline'], correct: 1, explanation: 'Chain-of-thought makes AI think through inputs, business rules, and edge cases before writing code.' },
    ]),
  ],
};

const aiArchitecture: ModuleContent = {
  id: 'ai-2',
  title: 'AI-Assisted Architecture',
  category: 'ai-mastery',
  icon: '🏛️',
  sections: [
    text('The Right Mindset', `AI cannot design your system. But it can be an exceptional thinking partner for exploring design options, identifying risks, and stress-testing your decisions.

Architecture is about tradeoffs, not solutions. There is no "correct" architecture — there are architectures that optimize for different constraints.`),
    code('Design Exploration Prompt', `I am designing [system/feature description].

Context:
- Team size: [number]
- Expected scale: [users/requests/data volume]
- Timeline: [duration]
- Key constraint: [the one thing that cannot be compromised]
- Tech stack: [current technologies]

Please:
1. Propose 3 distinct architectural approaches
2. For each: components, data flow, strengths, weaknesses
3. For the best approach: top 3 risks
4. Mitigation strategies for each risk`, 'markdown'),
    text('How to Evaluate AI Suggestions', `1. Does it solve YOUR problem, or a generic problem? Push back on "best practice" architectures.

2. What is the operational cost? Every choice has operational cost. Ask: "What does my team need to do to keep this running at 3 AM?"

3. Does it match your team's skills? A microservices architecture with Kubernetes is elegant — but if your team has never operated containers, it is a disaster.

4. Can you start simple and evolve? The best architecture starts simple and evolves as needs change.

5. What are the failure modes? Ask: "When this fails, how does it fail?"`),
    text('Red Flags in AI Suggestions', `Over-engineering: AI suggests event sourcing, CQRS, and a message queue for a CRUD app.

Resume-driven architecture: AI suggests trendy technologies without justifying why they fit your constraints.

Ignoring the boring option: AI overlooks simple, proven solutions. Explicitly ask: "What is the simplest approach that works?"

Missing the human factor: AI designs for machines, not for humans who operate them. Ask: "How does a developer debug this at 2 AM?"`),
    quiz('Architecture Quiz', [
      { question: 'What should you ask when AI suggests an architecture?', options: ['Is it popular?', 'Does it solve MY problem with MY constraints?', 'Is it the newest technology?', 'How many GitHub stars does it have?'], correct: 1, explanation: 'Always evaluate against YOUR specific constraints: team size, budget, timeline, skill level.' },
    ]),
  ],
};

const aiReview: ModuleContent = {
  id: 'ai-3',
  title: 'AI Code Review',
  category: 'ai-mastery',
  icon: '🔍',
  sections: [
    text('The Review Workflow', `1. AI performs initial review (automated, fast)
2. You evaluate AI findings (judgment required)
3. Human reviewer performs deep review (context, design, intent)
4. Final decision by the team

AI handles mechanical checks. Humans handle judgment calls.`),
    code('General Code Review Prompt', `Review the following code. Check for:

1. Bugs and logic errors
2. Security vulnerabilities
3. Performance issues
4. Error handling gaps
5. Code clarity and maintainability
6. Edge cases not handled
7. Type safety issues

For each finding:
- Severity: critical / high / medium / low / nit
- Category: bug / security / performance / style
- Location: exact line or range
- Explanation: what is wrong and why
- Suggestion: how to fix it (with code)

Code to review:
[paste code]`, 'markdown'),
    text('The Human-AI Review Partnership', `AI handles: pattern-based checks, consistency, completeness, exhaustive line-by-line inspection.

Humans handle: design intent, business logic correctness, contextual judgment, code readability, architecture alignment.

The back-and-forth produces better code than either AI or human alone.`),
    text('Anti-Patterns to Avoid', `1. Blindly applying all AI suggestions — not every suggestion is worth implementing.
2. Using AI review as replacement for human review — AI catches patterns, humans catch intent.
3. Reviewing too much at once — review one function at a time.
4. Ignoring suggestions you disagree with — articulate why. This forces you to understand the tradeoff.
5. Not providing context — without context, AI can only check for generic issues.`),
    quiz('Code Review Quiz', [
      { question: 'What should AI code review be used for?', options: ['Replacing human review entirely', 'Mechanical checks; humans handle judgment calls', 'Only security reviews', 'Only performance reviews'], correct: 1, explanation: 'AI handles pattern-based mechanical checks. Humans handle design intent, business logic, and contextual judgment.' },
    ]),
  ],
};

const aiDevelopment: ModuleContent = {
  id: 'ai-4',
  title: 'AI-Driven Development Workflow',
  category: 'ai-mastery',
  icon: '🤖',
  sections: [
    text('The Five Stages', `Problem Definition → Architecture → Implementation → Review → Deploy

At each stage, you lead. AI assists. The quality depends on how well you direct the process.`),
    text('Stage 1: Problem Definition', `Before touching any code or AI tool, define the problem clearly.

Your checklist:
- Who has the problem?
- What is the current state?
- What is the desired state?
- What are the constraints?
- What are the non-goals?

Use AI to challenge your definition: "Challenge this definition. What assumptions am I making? What edge cases am I ignoring?"`),
    text('Stage 2-3: Architecture and Implementation', `Architecture: You design, AI helps explore options. Document decisions in ADRs.

Implementation sequence:
1. Data model / types (the contracts)
2. Core business logic (the brain)
3. Data access layer (the persistence)
4. API / interface layer (the face)
5. Error handling and validation (the safety net)
6. Tests (the verification)

For each unit, provide AI with: architecture context, this component's role, inputs/outputs, dependencies, error cases, and a code example.`),
    text('Key Principles', `1. You architect, AI implements. Never let AI make design decisions.
2. Small, focused prompts beat large, vague ones.
3. Always provide context — AI works best with surrounding code and business rules.
4. Iterate, do not batch. Build in small increments.
5. Trust but verify — AI output needs testing and review. Always.
6. Document decisions — use ADRs to capture the "why."
7. Keep a learning loop — after each project, reflect on what worked.`),
    quiz('Development Workflow Quiz', [
      { question: 'What is the correct implementation sequence?', options: ['UI first, then backend', 'Types first, then business logic, then data access, then API', 'Tests first, then implementation', 'Database first, then everything else'], correct: 1, explanation: 'Start with contracts (types), then core logic, then persistence, then interface, then safety nets.' },
      { question: 'Who makes design decisions in AI-driven development?', options: ['AI', 'You', 'The product manager', 'The team lead'], correct: 1, explanation: 'You make design decisions. AI assists with exploration and implementation. Never let AI make design decisions.' },
    ]),
  ],
};

// ────────────────────────────────────────────────────────────────
// PRACTICE
// ────────────────────────────────────────────────────────────────

const practicePlanning: ModuleContent = {
  id: 'prac-1',
  title: 'Project Planning',
  category: 'practice',
  icon: '📋',
  sections: [
    text('Why Planning Matters', `The biggest mistake is jumping straight to code. The second biggest is planning so much that you never start.

Planning applies every mental model:
- Pattern Recognition — What kind of system is this?
- Abstraction Levels — At what level do I plan?
- Separation of Concerns — How do I break this into pieces?
- Type Safety — What are the inputs and outputs of each piece?
- Error Handling — What can go wrong at each stage?`),
    text('Requirements Gathering', `Write requirements as testable user stories:

As a user, I can:
- Upload a document to the knowledge base
- Ask a question and receive an answer based on documents
- See which documents were used (citations)
- View conversation history

Non-functional requirements:
- Process 100-page PDF in under 60 seconds
- Return answers within 5 seconds for 95% of queries
- Support 100 concurrent users`),
    text('The MoSCoW Method', `Categorize every requirement:

Must Have (Version 0.1):
- Document upload and processing
- Text chunking and embedding generation
- Semantic search
- Conversational query interface

Should Have (Version 0.2):
- Web interface
- Multi-user auth
- Citation display

Could Have (Version 0.3):
- Admin panel, usage statistics, multiple LLM providers

Won't Have (for now):
- Real-time collaboration, mobile app, voice interface`),
    text('Timeline and Phases', `Phase 1: Foundation (Days 1-3) — setup, data model, document pipeline
Phase 2: Core AI (Days 4-6) — embeddings, search, LLM integration
Phase 3: Web Interface (Days 7-9) — API, frontend, auth, conversation UI
Phase 4: Polish (Days 10-12) — admin, error handling, Docker, CI/CD

The Buffer Rule: Whatever timeline AI suggests, add 50%. You will encounter unexpected problems, learn things that change your approach, and want to refactor.`),
    quiz('Planning Quiz', [
      { question: 'What is the MoSCoW method?', options: ['A city in Russia', 'A prioritization technique: Must/Should/Could/Won\'t', 'A testing framework', 'A deployment strategy'], correct: 1, explanation: 'MoSCoW categorizes requirements into Must Have, Should Have, Could Have, and Won\'t Have.' },
    ]),
  ],
};

const practiceArchitecture: ModuleContent = {
  id: 'prac-2',
  title: 'Architecture Design',
  category: 'practice',
  icon: '🏗️',
  sections: [
    text('What Architecture Is', `Architecture is the set of decisions that are hard to change later. Choosing a database is architecture. Choosing a function name is not.

Three questions:
1. What are the pieces?
2. How do they communicate?
3. What are the rules?`),
    text('Component Responsibilities', `API Server (FastAPI): Route requests, validate data, authenticate, serialize responses. NO business logic.

Document Service: Upload, extract text, chunk, generate embeddings, store, track status.

Query Service: Accept queries, generate embeddings, semantic search, construct prompts, call LLM, return answers with citations.

User Service: Registration, login, JWT tokens, password hashing, role-based access control.`),
    text('The Processing Pipeline', `Upload → Validate → Extract Text → Chunk → Embed → Store → Index

Each step can fail. The pipeline handles failures gracefully:
- Upload fails: return error, no DB record
- Extraction fails: mark as "failed", log error
- Embedding fails: retry 3x with exponential backoff
- Failed documents can be re-processed without re-uploading`),
    text('Architecture Decision Records', `Document every significant decision:

ADR-004: Use pgvector Instead of Dedicated Vector Database

Context: Need to store and search embeddings. Options: pgvector, Qdrant, Weaviate.

Decision: Use pgvector (PostgreSQL extension).

Consequences:
+ Single database, transactional consistency, simpler operations
- Less optimized at very large scale
Mitigation: Monitor performance; migrate if we exceed 5M vectors`),
    quiz('Architecture Design Quiz', [
      { question: 'What is architecture?', options: ['Diagrams and buzzwords', 'The set of decisions hard to change later', 'Code organization', 'Technology selection'], correct: 1, explanation: 'Architecture is the decisions that are expensive to change: database, communication patterns, system boundaries.' },
    ]),
  ],
};

const practiceImplementation: ModuleContent = {
  id: 'prac-3',
  title: 'Implementation',
  category: 'practice',
  icon: '💻',
  sections: [
    text('Implementation Principles', `1. Build incrementally — get one piece working before starting the next
2. Use AI for generation, not for decisions
3. Test as you go — do not wait until the end
4. Refactor when you see mess
5. Document decisions, not code`),
    code('Backend Setup Prompt', `I need to set up a FastAPI project with the following structure:

backend/src/
  api/            # Route handlers
  services/       # Business logic
  models/         # SQLAlchemy models and Pydantic schemas
  processing/     # Document processing pipeline
  ai/             # LLM and embedding integration
  config/         # Settings management

Generate:
1. src/config/settings.py - Pydantic settings with environment variables
2. src/main.py - FastAPI app with CORS, lifespan, router inclusion
3. src/api/dependencies.py - Dependency injection for DB sessions`, 'markdown'),
    code('Document Service Design', `class DocumentService:
    async def upload_document(user_id, file) -> Document:
        # Validate file type and size
        # Save file to disk
        # Create Document record with status "uploading"
        # Trigger async processing
        return document

    async def process_document(document_id) -> None:
        # Update status to "processing"
        # Extract text from file
        # Chunk the text
        # Generate embeddings for chunks
        # Store chunks in database
        # Update status to "ready"`, 'python'),
    text('Using AI During Implementation', `When starting a new component:
"I am implementing [component]. Here is the architecture context, data model, dependencies, and a similar component as an example. Generate the implementation."

When stuck on a bug:
"This code is supposed to [expected], but [actual]. I have already checked: [what you verified]. What are the most likely causes?"

When refactoring:
"This code works but is messy. Refactor it to [goals]. Do not change the external API."`),
    quiz('Implementation Quiz', [
      { question: 'What is the correct order for building a component?', options: ['UI first', 'Types first, then logic, then persistence', 'Tests first', 'Database first'], correct: 1, explanation: 'Start with contracts (types/data model), then business logic, then data access, then API layer.' },
    ]),
  ],
};

const practiceDeployment: ModuleContent = {
  id: 'prac-4',
  title: 'Deployment',
  category: 'practice',
  icon: '🚀',
  sections: [
    text('Deployment Checklist', `Configuration: Environment variables, secrets management
Infrastructure: Servers, databases, networking
CI/CD: Automated build, test, and deploy pipeline
Monitoring: Logs, metrics, alerts
Documentation: API docs, runbooks, architecture diagrams`),
    code('Dockerfile Generation Prompt', `Generate a production-ready Dockerfile:
- Multi-stage build (build stage + production stage)
- Non-root user
- Only production dependencies in final image
- Health check endpoint
- Proper signal handling for graceful shutdown`, 'markdown'),
    code('CI/CD Pipeline Prompt', `Generate a GitHub Actions workflow:
- Trigger on push to main and on pull requests
- Steps: install, lint, type-check, test, build
- Deploy to [platform] on merge to main
- Cache node_modules between runs
- Environment variables from GitHub secrets`, 'markdown'),
    text('Monitoring Setup', `Add observability to your service:
1. Structured logging (JSON format, with request ID, user ID, duration)
2. Key metrics (request count, error rate, latency percentiles)
3. Health check endpoint (check DB connectivity, external service reachability)
4. Alert rules (error rate spike, high latency, service down)`),
    quiz('Deployment Quiz', [
      { question: 'What should a production Dockerfile use?', options: ['Single stage build', 'Multi-stage build with non-root user', 'Install all dev dependencies', 'Run as root for simplicity'], correct: 1, explanation: 'Multi-stage builds minimize image size. Non-root users improve security.' },
    ]),
  ],
};

// ────────────────────────────────────────────────────────────────
// DISSECT MODULES (simplified — real content from source repos)
// ────────────────────────────────────────────────────────────────

function makeDissectModule(id: string, title: string, icon: string, category: string, overview: string, patterns: string[], quizQs: QuizQuestion[]): ModuleContent {
  return {
    id, title, category, icon,
    sections: [
      text('Overview', overview),
      text('Key Patterns', patterns.map((p, i) => `${i + 1}. ${p}`).join('\n\n')),
      quiz('Test Your Understanding', quizQs),
    ],
  };
}

// Python dissect modules
const pyFastapi = makeDissectModule('py-d-fastapi-1', 'FastAPI', '🚀', 'python-dissect',
  'FastAPI is a modern Python web framework (GitHub 80k+ stars). Async-first, type-safe, automatic API documentation via OpenAPI. Built on Starlette and Pydantic.',
  ['Dependency Injection: Functions declare dependencies as parameters. FastAPI resolves them automatically via Depends().',
   'Middleware: @app.middleware("http") intercepts every request/response for logging, timing, CORS.',
   'Lifecycle: @asynccontextmanager async def lifespan(app) handles startup/shutdown (DB connections, cache warm-up).',
   'Pydantic Models: Request/response validation is automatic. Models define the contract.'],
  [{ question: 'How does FastAPI handle dependency injection?', options: ['Constructor injection', 'Depends() in function parameters', 'Global variables', 'Config files'], correct: 1, explanation: 'FastAPI uses Depends() to declare dependencies as function parameters. The framework resolves them automatically.' }]
);

const pyLangchain = makeDissectModule('py-d-langchain-1', 'LangChain', '🦜', 'python-dissect',
  'LangChain is the most popular framework for building LLM applications. It provides chains, agents, memory, and integrations with every major LLM provider.',
  ['Chain Pattern: Sequential processing pipeline — prompt | llm | parser. Each step is composable.',
   'Agent Pattern: LLM decides which tools to use and in what order. The agent is a loop: think → act → observe → repeat.',
   'RAG Pattern: Retrieve relevant documents, construct prompt with context, call LLM, return answer with citations.',
   'Memory: Conversation history stored and injected into prompts. Multiple memory strategies (buffer, summary, vector).'],
  [{ question: 'What is the RAG pattern?', options: ['Random Access Generation', 'Retrieve documents, add context to prompt, generate answer', 'Recursive Agent Generation', 'Real-time Analysis Gateway'], correct: 1, explanation: 'RAG = Retrieval-Augmented Generation. Retrieve relevant docs, add them as context to the prompt, then generate an answer.' }]
);

const pyCrewai = makeDissectModule('py-d-crewai-1', 'CrewAI', '👥', 'python-dissect',
  'CrewAI is a framework for orchestrating multiple AI agents that collaborate to accomplish tasks. Each agent has a role, goal, and backstory.',
  ['Multi-Agent Collaboration: Agents have roles (researcher, writer, reviewer) and delegate tasks to each other.',
   'Task Decomposition: Complex tasks are broken into sub-tasks assigned to specialized agents.',
   'Sequential and Parallel Execution: Tasks can run in sequence or parallel based on dependencies.'],
  [{ question: 'What is the key idea behind CrewAI?', options: ['Single agent does everything', 'Multiple specialized agents collaborate', 'Agents compete with each other', 'Agents replace human workers'], correct: 1, explanation: 'CrewAI orchestrates multiple agents with different roles (researcher, writer, reviewer) that collaborate to accomplish complex tasks.' }]
);

const pyDify = makeDissectModule('py-d-dify-1', 'Dify', '🔮', 'python-dissect',
  'Dify is an open-source LLM app development platform. It provides a visual workflow builder, RAG pipeline, agent capabilities, and enterprise features.',
  ['Workflow Engine: Visual drag-and-drop workflow builder. Nodes represent LLM calls, tools, conditionals.',
   'Plugin System: Extensible architecture. Add new tools, models, and integrations via plugins.',
   'RAG Pipeline: Built-in document ingestion, chunking, embedding, and retrieval.'],
  [{ question: 'What makes Dify different from LangChain?', options: ['It is written in TypeScript', 'It provides a visual workflow builder and platform', 'It only works with OpenAI', 'It has no RAG support'], correct: 1, explanation: 'Dify is a platform with a visual workflow builder, not just a library. It provides a complete development environment.' }]
);

const pyRagflow = makeDissectModule('py-d-ragflow-1', 'RAGFlow', '📖', 'python-dissect',
  'RAGFlow is an open-source RAG engine focused on document parsing and retrieval. It handles complex document layouts including tables, images, and multi-column text.',
  ['Document Parsing: Handles PDFs with complex layouts — tables, images, multi-column text, headers/footers.',
   'Chunking Strategies: Multiple strategies (fixed-size, semantic, document-aware) for different document types.',
   'Vector Retrieval: Hybrid search combining semantic (vector) and keyword (BM25) retrieval.'],
  [{ question: 'What is RAGFlow\'s main strength?', options: ['Chat interface', 'Document parsing with complex layouts', 'Agent orchestration', 'Code generation'], correct: 1, explanation: 'RAGFlow specializes in parsing complex document layouts (tables, images, multi-column) for RAG applications.' }]
);

// TypeScript dissect modules
const tsNextjs = makeDissectModule('ts-d-nextjs-1', 'Next.js', '▲', 'typescript-dissect',
  'Next.js is the production-grade React framework (GitHub 130k+ stars). SSR, SSG, App Router, middleware, API routes, image optimization.',
  ['File-Based Routing: app/blog/[slug]/page.tsx maps to /blog/:slug. The file system IS the router.',
   'Server/Client Boundary: Components are server by default. Add "use client" for interactivity. Direct DB access in server components.',
   'Middleware: export function middleware(request) runs before the route handler. Auth, redirects, headers.',
   'Data Fetching: Server components fetch data directly. No useEffect, no loading states, no API layers for server data.'],
  [{ question: 'What is the default component type in Next.js App Router?', options: ['Client component', 'Server component', 'API route', 'Middleware'], correct: 1, explanation: 'In Next.js App Router, components are server components by default. Add "use client" for client-side interactivity.' }]
);

const tsTrpc = makeDissectModule('ts-d-trpc-1', 'tRPC', '📡', 'typescript-dissect',
  'tRPC enables end-to-end type safety between frontend and backend with zero code generation. Change a backend type, and the frontend gets instant compile errors.',
  ['End-to-End Type Safety: Backend procedures define types. Frontend calls them with full autocomplete and type checking. No code generation.',
   'Procedure Pattern: publicProcedure.input(schema).query(async ({ input }) => { ... }) defines a typed API endpoint.',
   'Middleware Chain: Procedures compose with .use() to add authentication, logging, rate limiting.'],
  [{ question: 'What is tRPC\'s key advantage over REST?', options: ['Faster runtime performance', 'End-to-end type safety without code generation', 'Smaller bundle size', 'Better SEO'], correct: 1, explanation: 'tRPC provides end-to-end type safety between frontend and backend with zero code generation or schema definitions.' }]
);

const tsTauri = makeDissectModule('ts-d-tauri-1', 'Tauri', '🦀', 'typescript-dissect',
  'Tauri builds cross-platform desktop apps with a web frontend and Rust backend. Smaller binaries, better security, and native performance compared to Electron.',
  ['Rust Backend: Core logic in Rust for performance and security. TypeScript frontend for UI.',
   'Command Pattern: Rust functions exposed to frontend via #[tauri::command]. Type-safe bridge between Rust and TypeScript.',
   'Security Model: Fine-grained permissions. Frontend can only access explicitly allowed APIs.'],
  [{ question: 'How does Tauri differ from Electron?', options: ['Tauri uses Python backend', 'Tauri uses Rust backend with smaller binaries and better security', 'Tauri only works on Windows', 'Tauri has no frontend support'], correct: 1, explanation: 'Tauri uses a Rust backend instead of Node.js, producing smaller binaries with better security and native performance.' }]
);

const tsShadcn = makeDissectModule('ts-d-shadcn-ui-1', 'shadcn/ui', '🎨', 'typescript-dissect',
  'shadcn/ui is a collection of copy-paste components built on Radix UI and Tailwind CSS. Not a dependency — you own the code.',
  ['Component Design: Accessible, composable components built on Radix UI primitives. Copy-paste, not npm install.',
   'Theming: CSS variables for colors, spacing, typography. One config file changes the entire design system.',
   'Composition: Small, focused components composed into complex UIs. Each component does one thing well.'],
  [{ question: 'What is shadcn/ui\'s unique approach?', options: ['Install as npm dependency', 'Copy-paste components you own', 'Only works with Vue', 'Requires a paid license'], correct: 1, explanation: 'shadcn/ui components are copied into your project, not installed as dependencies. You own and can modify the code.' }]
);

const tsBun = makeDissectModule('ts-d-bun-1', 'Bun', '🍞', 'typescript-dissect',
  'Bun is an all-in-one JavaScript runtime, bundler, and package manager. Built on JavaScriptCore (Safari\'s engine) for speed.',
  ['Runtime: Drop-in replacement for Node.js. Faster startup, lower memory usage. Native TypeScript support without transpilation.',
   'Bundler: Built-in bundler replaces webpack/esbuild for many use cases. Fast, zero-config.',
   'Package Manager: bun install is 10-100x faster than npm install. Compatible with package.json.'],
  [{ question: 'What JavaScript engine does Bun use?', options: ['V8 (Chrome)', 'JavaScriptCore (Safari)', 'SpiderMonkey (Firefox)', 'Hermes (React Native)'], correct: 1, explanation: 'Bun uses JavaScriptCore, Safari\'s JavaScript engine, optimized for fast startup and low memory usage.' }]
);

// ────────────────────────────────────────────────────────────────
// CONTENT REGISTRY
// ────────────────────────────────────────────────────────────────

export const ALL_CONTENT: ModuleContent[] = [
  // Cognitive
  cognitiveWhyLearn, cognitiveThinking, cognitiveLanguages,
  // Python fundamentals
  pyVariables, pyFunctions, pyClasses, pyAsync, pyTypes, pyModules,
  // TypeScript fundamentals
  tsTypes, tsFunctions, tsInterfaces, tsAsync, tsModules, tsDecorators,
  // Patterns
  patFactory, patObserver, patStrategy, patPipeline, patMiddleware, patRepository, patDI, patBuilder,
  // Python dissect
  pyFastapi, pyLangchain, pyCrewai, pyDify, pyRagflow,
  // TypeScript dissect
  tsNextjs, tsTrpc, tsTauri, tsShadcn, tsBun,
  // AI mastery
  aiPrompt, aiArchitecture, aiReview, aiDevelopment,
  // Practice
  practicePlanning, practiceArchitecture, practiceImplementation, practiceDeployment,
];

export function getContentById(id: string): ModuleContent | undefined {
  // Direct match
  const direct = ALL_CONTENT.find(c => c.id === id);
  if (direct) return direct;

  // For dissect modules: py-d-{slug}-2 or py-d-{slug}-3 → py-d-{slug}-1
  // Same for ts-d-{slug}-2/-3 → ts-d-{slug}-1
  const dissectMatch = id.match(/^((?:py|ts)-d-\w+)-[23]$/);
  if (dissectMatch) {
    return ALL_CONTENT.find(c => c.id === `${dissectMatch[1]}-1`);
  }

  return undefined;
}

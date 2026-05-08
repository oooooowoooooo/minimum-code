"""
Atom 04: Async Programming
============================
Asynchronous programming with asyncio: coroutines, tasks, semaphores,
async context managers, and async iterators.

Architecture:
    Python's async model is built on coroutines -- functions that can suspend
    and resume execution. When a coroutine awaits (e.g., network I/O), the
    event loop runs other coroutines. This achieves concurrency with a single
    thread, avoiding the overhead of thread context switching.

    The key insight: async is for I/O-bound work (network, file, database),
    NOT CPU-bound work. For CPU-bound tasks, use multiprocessing.

    asyncio.run() creates an event loop, runs the coroutine, and cleans up.
    await pauses the coroutine until the awaited task completes.
    asyncio.gather() runs multiple coroutines concurrently.
    TaskGroup (Python 3.11+) provides structured concurrency with better
    error handling.

Transferability:
    - TypeScript: async/await is nearly identical. Promises map to Futures.
      Event loop exists in Node.js. Promise.all() = asyncio.gather().
    - Rust: async/await with tokio runtime. Futures are lazy (must be polled).
    - Java: CompletableFuture, reactive programming (Project Reactor).
    - C#: async/await with Task<T>. Very similar to Python.

Application:
    - Web servers (FastAPI, aiohttp) handle thousands of concurrent requests.
    - WebSockets for real-time communication.
    - Database queries (asyncpg, aiomysql).
    - API calls to external services.
    - File I/O (aiofiles).

Run: python async_io.py
"""

import asyncio
from typing import AsyncIterator, AsyncGenerator
from contextlib import asynccontextmanager
import time


## ============================================================================
# SECTION 1: COROUTINES -- THE BASICS
# ============================================================================
# A coroutine is a function defined with `async def`.
# Calling a coroutine returns a coroutine object (it does NOT execute).
# Use `await` to run it.

async def say_hello(name: str) -> str:
    """A simple coroutine."""
    await asyncio.sleep(0.01)  # Simulate async work
    return f"Hello, {name}!"

async def basic_coroutine_demo():
    """Demonstrate basic coroutine usage."""
    # Calling a coroutine returns a coroutine object
    coro = say_hello("World")
    print(f"Type: {type(coro)}")
    # Output: Type: <class 'coroutine'>

    # Await it to get the result
    result = await coro
    print(f"Result: {result}")
    # Output: Result: Hello, World!

    # Or await directly
    result = await say_hello("Python")
    print(f"Direct: {result}")
    # Output: Direct: Hello, Python!


## ============================================================================
# SECTION 2: AWAIT AND SEQUENTIAL EXECUTION
# ============================================================================
# `await` pauses the coroutine until the awaited task completes.
# Sequential awaits run one after another (no concurrency).

async def fetch_data(source: str, delay: float) -> str:
    """Simulate fetching data from a source."""
    print(f"  Fetching from {source}...")
    await asyncio.sleep(delay)  # Simulate network delay
    print(f"  Got data from {source}")
    return f"Data from {source}"

async def sequential_demo():
    """Sequential execution: each await waits for the previous one."""
    print("\nSequential execution:")
    start = time.time()

    data1 = await fetch_data("API-1", 0.1)
    data2 = await fetch_data("API-2", 0.1)
    data3 = await fetch_data("API-3", 0.1)

    elapsed = time.time() - start
    print(f"  Results: {[data1, data2, data3]}")
    print(f"  Time: {elapsed:.2f}s (sequential: ~0.3s)")
    # Output: Time: ~0.30s (each waits for the previous)


## ============================================================================
# SECTION 3: CONCURRENT EXECUTION WITH GATHER
# ============================================================================
# asyncio.gather() runs multiple coroutines concurrently.
# All tasks start at the same time, and we wait for all to complete.

async def concurrent_gather_demo():
    """Concurrent execution with gather()."""
    print("\nConcurrent execution (gather):")
    start = time.time()

    # All three start simultaneously
    results = await asyncio.gather(
        fetch_data("API-1", 0.1),
        fetch_data("API-2", 0.1),
        fetch_data("API-3", 0.1),
    )

    elapsed = time.time() - start
    print(f"  Results: {results}")
    print(f"  Time: {elapsed:.2f}s (concurrent: ~0.1s)")
    # Output: Time: ~0.10s (all run at the same time)

async def gather_with_exception():
    """gather() with return_exceptions=True to handle errors."""
    async def success():
        await asyncio.sleep(0.01)
        return "ok"

    async def failure():
        await asyncio.sleep(0.01)
        raise ValueError("Something went wrong")

    print("\ngather with return_exceptions=True:")
    results = await asyncio.gather(
        success(), failure(), success(),
        return_exceptions=True  # Don't raise, return exception objects
    )
    print(f"  Results: {results}")
    # Output: Results: ['ok', ValueError('Something went wrong'), 'ok']


## ============================================================================
# SECTION 4: TASKGROUP (Python 3.11+) -- Structured Concurrency
# ============================================================================
# TaskGroup provides better error handling than gather().
# If any task fails, all other tasks are cancelled and the exception propagates.

async def taskgroup_demo():
    """Structured concurrency with TaskGroup."""
    print("\nTaskGroup (structured concurrency):")
    start = time.time()

    results = []
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch_data("API-1", 0.1))
        task2 = tg.create_task(fetch_data("API-2", 0.1))
        task3 = tg.create_task(fetch_data("API-3", 0.1))

    # All tasks are done when we exit the `async with` block
    results = [task1.result(), task2.result(), task3.result()]
    elapsed = time.time() - start
    print(f"  Results: {results}")
    print(f"  Time: {elapsed:.2f}s")
    # Output: Time: ~0.10s

async def taskgroup_error_handling():
    """TaskGroup cancels remaining tasks on failure."""
    print("\nTaskGroup error handling:")

    async def slow_ok():
        await asyncio.sleep(0.5)
        return "ok"

    async def fast_fail():
        await asyncio.sleep(0.01)
        raise ValueError("Boom!")

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(slow_ok())
            tg.create_task(fast_fail())
    except* ValueError as eg:
        print(f"  Caught {len(eg.exceptions)} error(s): {eg.exceptions}")
    # Output: Caught 1 error(s): (ValueError('Boom!'),)


## ============================================================================
# SECTION 5: ASYNC CONTEXT MANAGERS
# ============================================================================
# `async with` manages resources that need async setup/teardown.
# Common use: database connections, HTTP sessions, file handles.

class AsyncDatabaseConnection:
    """Simulated async database connection."""

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connected = False

    async def __aenter__(self):
        """Async setup: connect to database."""
        print(f"  Connecting to {self.db_name}...")
        await asyncio.sleep(0.01)  # Simulate connection time
        self.connected = True
        print(f"  Connected to {self.db_name}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async teardown: close connection."""
        await asyncio.sleep(0.01)  # Simulate cleanup
        self.connected = False
        print(f"  Disconnected from {self.db_name}")
        return False  # Don't suppress exceptions

    async def query(self, sql: str) -> str:
        if not self.connected:
            raise RuntimeError("Not connected")
        await asyncio.sleep(0.01)
        return f"Result of '{sql}'"

async def async_context_manager_demo():
    """Demonstrate async context managers."""
    print("\nAsync context manager:")
    async with AsyncDatabaseConnection("mydb") as db:
        result = await db.query("SELECT * FROM users")
        print(f"  Query result: {result}")
    # Output: Connecting to mydb...
    # Output: Connected to mydb
    # Output: Query result: Result of 'SELECT * FROM users'
    # Output: Disconnected from mydb

# Using @asynccontextmanager decorator (simpler)
@asynccontextmanager
async def timer(label: str):
    """Async context manager that measures time."""
    print(f"  [{label}] Starting...")
    start = time.time()
    yield start  # Value available as `as start`
    elapsed = time.time() - start
    print(f"  [{label}] Done in {elapsed:.3f}s")

async def timer_demo():
    """Demonstrate @asynccontextmanager."""
    print("\n@asynccontextmanager:")
    async with timer("operation") as start:
        await asyncio.sleep(0.05)
        print(f"  [{timer}] Working...")


## ============================================================================
# SECTION 6: ASYNC ITERATORS
# ============================================================================
# Async iterators use __aiter__ and __anext__ (both async).
# `async for` iterates over them.

class AsyncCounter:
    """Async iterator that counts from 0 to n-1."""

    def __init__(self, n: int):
        self.n = n
        self.current = 0

    def __aiter__(self):
        return self

    async def __anext__(self) -> int:
        if self.current >= self.n:
            raise StopAsyncIteration
        await asyncio.sleep(0.01)  # Simulate async work
        value = self.current
        self.current += 1
        return value

async def async_iterator_demo():
    """Demonstrate async iterators."""
    print("\nAsync iterator:")
    async for num in AsyncCounter(5):
        print(f"  Got: {num}")
    # Output: Got: 0, Got: 1, ..., Got: 4

# Async generator (simpler syntax for async iterators)
async def async_range(n: int) -> AsyncGenerator[int, None]:
    """Async generator -- simpler than a full async iterator class."""
    for i in range(n):
        await asyncio.sleep(0.01)
        yield i

async def async_generator_demo():
    """Demonstrate async generators."""
    print("\nAsync generator:")
    async for num in async_range(5):
        print(f"  Got: {num}")
    # Output: Got: 0, Got: 1, ..., Got: 4

    # Collect all values
    values = [num async for num in async_range(3)]
    print(f"  Collected: {values}")
    # Output: Collected: [0, 1, 2]


## ============================================================================
# SECTION 7: SEMAPHORES -- Limiting Concurrency
# ============================================================================
# Semaphore limits how many coroutines can run concurrently.
# Useful for rate limiting API calls, database connections, etc.

async def rate_limited_task(task_id: int, semaphore: asyncio.Semaphore):
    """Task that respects a semaphore limit."""
    async with semaphore:
        print(f"  Task {task_id} started")
        await asyncio.sleep(0.1)
        print(f"  Task {task_id} done")
        return f"result-{task_id}"

async def semaphore_demo():
    """Demonstrate semaphore for concurrency limiting."""
    print("\nSemaphore (max 2 concurrent):")
    semaphore = asyncio.Semaphore(2)  # Allow max 2 concurrent tasks

    start = time.time()
    results = await asyncio.gather(*[
        rate_limited_task(i, semaphore) for i in range(6)
    ])
    elapsed = time.time() - start
    print(f"  Results: {results}")
    print(f"  Time: {elapsed:.2f}s (6 tasks, max 2 concurrent)")
    # Output: Time: ~0.30s (3 batches of 2)


## ============================================================================
# SECTION 8: REAL-WORLD PATTERN: CONCURRENT API CALLS
# ============================================================================
# This pattern is used extensively in production code.

async def fetch_json(url: str) -> dict:
    """Simulate fetching JSON from a URL."""
    await asyncio.sleep(0.05)  # Simulate network latency
    return {"url": url, "status": 200, "data": f"Response from {url}"}

async def fetch_all_concurrently():
    """Fetch multiple URLs concurrently with error handling."""
    urls = [
        "https://api.example.com/users",
        "https://api.example.com/products",
        "https://api.example.com/orders",
    ]

    print("\nConcurrent API calls:")
    start = time.time()

    # Create tasks for all URLs
    tasks = [fetch_json(url) for url in urls]
    results = await asyncio.gather(*tasks)

    elapsed = time.time() - start
    for result in results:
        print(f"  {result['url']}: {result['status']}")
    print(f"  Total time: {elapsed:.2f}s")


## ============================================================================
# SECTION 9: TIMEOUTS
# ============================================================================
# asyncio.wait_for() adds a timeout to any coroutine.

async def slow_operation():
    """A slow operation."""
    await asyncio.sleep(10)
    return "done"

async def timeout_demo():
    """Demonstrate timeout handling."""
    print("\nTimeout handling:")
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=0.1)
    except TimeoutError:
        print("  Operation timed out!")
    # Output: Operation timed out!

# Python 3.11+ alternative: asyncio.timeout()
async def timeout_context_demo():
    """Demonstrate timeout as context manager (Python 3.11+)."""
    print("\nTimeout context manager:")
    try:
        async with asyncio.timeout(0.1):
            await slow_operation()
    except TimeoutError:
        print("  Timed out via context manager!")


## ============================================================================
# MINI-EXERCISES
## ============================================================================

def exercises():
    print("\n" + "=" * 60)
    print("MINI-EXERCISES")
    print("=" * 60)

    print("""
--- Multiple Choice ---

Q1: What does `await` do?
    A) Creates a new thread
    B) Pauses the coroutine until the awaited task completes
    C) Blocks the entire program
    D) Creates a new process
""")
    print("Answer: B) Pauses the coroutine, allowing other coroutines to run.\n")

    print("""
Q2: What is the difference between gather() and TaskGroup?
    A) gather() is faster
    B) TaskGroup cancels remaining tasks on failure; gather() does not
    C) They are identical
    D) TaskGroup does not support concurrency
""")
    print("Answer: B) TaskGroup provides structured concurrency with automatic cancellation.\n")

    print("""
Q3: When should you use async?
    A) CPU-bound work
    B) I/O-bound work (network, file, database)
    C) Always
    D) Never
""")
    print("Answer: B) Async is for I/O-bound work. Use multiprocessing for CPU-bound.\n")

    print("""
--- Q&A ---

Q: What happens if you call an async function without await?
A: You get a coroutine object, but it doesn't execute. The coroutine
   is never scheduled. This is a common bug -- always await coroutines.

Q: How does a semaphore limit concurrency?
A: A semaphore maintains a counter. acquire() decrements it (blocking if 0).
   release() increments it. The counter represents available "slots".

Q: What is structured concurrency?
A: A paradigm where child tasks must complete before the parent scope exits.
   TaskGroup enforces this: all tasks complete (or are cancelled) before
   the `async with` block exits.
""")


def progress_check():
    print("\n" + "=" * 60)
    print("PROGRESS CHECK")
    print("=" * 60)
    questions = [
        "1. Can you explain the difference between async and threading?",
        "2. Can you write a basic coroutine with async/await?",
        "3. Do you understand why gather() is faster than sequential await?",
        "4. Can you use TaskGroup for structured concurrency?",
        "5. Can you write an async context manager?",
        "6. Can you write an async iterator or async generator?",
        "7. Do you understand how semaphores limit concurrency?",
        "8. Can you handle timeouts with wait_for()?",
        "9. Do you know when to use async vs multiprocessing?",
        "10. Can you explain the event loop?",
    ]
    print("\nRate your confidence (1-5) for each:\n")
    for q in questions:
        print(f"  {q}")
    print("""
Scoring:
  40-50: Excellent! You can build high-performance async applications.
  30-39: Good. Practice with real async libraries (aiohttp, asyncpg).
  20-29: Focus on coroutines and gather() first.
  < 20:  Start with the basic coroutine examples.
""")


def key_takeaways():
    print("\n" + "=" * 60)
    print("KEY TAKEAWAYS")
    print("=" * 60)
    print("""
* async def defines a coroutine; calling it returns a coroutine object.
* await pauses the coroutine until the awaited task completes.
* asyncio.gather() runs multiple coroutines concurrently.
* TaskGroup (3.11+) provides structured concurrency with auto-cancellation.
* Async context managers use __aenter__/__aexit__ (or @asynccontextmanager).
* Async iterators use __aiter__/__anext__ (or async generators with yield).
* Semaphores limit concurrent execution (rate limiting).
* asyncio.wait_for() adds timeouts to any coroutine.
* Use async for I/O-bound work; multiprocessing for CPU-bound work.
* The event loop schedules and runs coroutines.
""")


def transferability():
    print("\n" + "=" * 60)
    print("TRANSFERABILITY TO OTHER LANGUAGES")
    print("=" * 60)
    print("""
Python Concept       | TypeScript           | Rust
---------------------|----------------------|------------------------
async/await          | async/await          | async/await
gather()             | Promise.all()        | tokio::join!()
TaskGroup            | Promise.allSettled()  | tokio::JoinSet
Semaphore            | p-limit              | tokio::Semaphore
async context mgr    | try/finally          | async Drop (limited)
async iterator       | AsyncIterator        | Stream (futures)
timeout              | AbortController      | tokio::time::timeout
event loop           | Node.js event loop   | tokio runtime
""")


async def main():
    """Run all async demos."""
    await basic_coroutine_demo()
    await sequential_demo()
    await concurrent_gather_demo()
    await gather_with_exception()
    await taskgroup_demo()
    await taskgroup_error_handling()
    await async_context_manager_demo()
    await timer_demo()
    await async_iterator_demo()
    await async_generator_demo()
    await semaphore_demo()
    await fetch_all_concurrently()
    await timeout_demo()
    await timeout_context_demo()


if __name__ == "__main__":
    exercises()
    progress_check()
    key_takeaways()
    transferability()

    print("\n" + "=" * 60)
    print("ASYNC DEMOS")
    print("=" * 60)
    asyncio.run(main())

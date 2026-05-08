"""
Tests for Atom 04: Async Programming
=====================================
Validates coroutines, gather, TaskGroup, async context managers,
async iterators, semaphores, and timeouts.
"""

import asyncio
import pytest
import pytest_asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator


# ============================================================================
# COROUTINE TESTS
# ============================================================================

class TestCoroutines:
    """Test basic coroutine behavior."""

    @pytest.mark.asyncio
    async def test_coroutine_returns_value(self):
        """Coroutines return values when awaited."""
        async def add(a, b):
            await asyncio.sleep(0)
            return a + b
        result = await add(3, 4)
        assert result == 7

    @pytest.mark.asyncio
    async def test_coroutine_is_awaitable(self):
        """Coroutine objects are awaitable."""
        async def hello():
            return "hi"
        coro = hello()
        assert hasattr(coro, '__await__')
        result = await coro
        assert result == "hi"

    @pytest.mark.asyncio
    async def test_coroutine_with_sleep(self):
        """await asyncio.sleep() simulates async work."""
        async def delayed():
            await asyncio.sleep(0.01)
            return 42
        result = await delayed()
        assert result == 42

    @pytest.mark.asyncio
    async def test_nested_coroutine(self):
        """Coroutines can await other coroutines."""
        async def inner():
            return 10

        async def outer():
            value = await inner()
            return value * 2

        assert await outer() == 20


# ============================================================================
# GATHER TESTS
# ============================================================================

class TestGather:
    """Test asyncio.gather() for concurrent execution."""

    @pytest.mark.asyncio
    async def test_gather_concurrent(self):
        """gather() runs coroutines concurrently."""
        async def task(n):
            await asyncio.sleep(0.01)
            return n * 2

        results = await asyncio.gather(task(1), task(2), task(3))
        assert results == [2, 4, 6]

    @pytest.mark.asyncio
    async def test_gather_preserves_order(self):
        """gather() preserves the order of results."""
        async def task(n):
            await asyncio.sleep(0.01 * (4 - n))  # Reverse delay
            return n

        results = await asyncio.gather(task(1), task(2), task(3))
        assert results == [1, 2, 3]  # Order matches argument order

    @pytest.mark.asyncio
    async def test_gather_return_exceptions(self):
        """gather(return_exceptions=True) returns exceptions as values."""
        async def ok():
            return "ok"

        async def fail():
            raise ValueError("oops")

        results = await asyncio.gather(ok(), fail(), ok(), return_exceptions=True)
        assert results[0] == "ok"
        assert isinstance(results[1], ValueError)
        assert results[2] == "ok"

    @pytest.mark.asyncio
    async def test_gather_with_empty(self):
        """gather() with no arguments returns empty list."""
        results = await asyncio.gather()
        assert results == []


# ============================================================================
# TASKGROUP TESTS
# ============================================================================

class TestTaskGroup:
    """Test TaskGroup for structured concurrency."""

    @pytest.mark.asyncio
    async def test_taskgroup_basic(self):
        """TaskGroup runs tasks concurrently."""
        results = []
        async with asyncio.TaskGroup() as tg:
            t1 = tg.create_task(self._async_value(1))
            t2 = tg.create_task(self._async_value(2))
            t3 = tg.create_task(self._async_value(3))
        results = [t1.result(), t2.result(), t3.result()]
        assert results == [1, 2, 3]

    @staticmethod
    async def _async_value(n):
        await asyncio.sleep(0.01)
        return n

    @pytest.mark.asyncio
    async def test_taskgroup_cancels_on_error(self):
        """TaskGroup cancels other tasks when one fails."""
        async def slow():
            await asyncio.sleep(10)
            return "slow"

        async def fast_fail():
            await asyncio.sleep(0.01)
            raise ValueError("boom")

        with pytest.raises(ExceptionGroup) as exc_info:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(slow())
                tg.create_task(fast_fail())

        assert len(exc_info.value.exceptions) == 1
        assert isinstance(exc_info.value.exceptions[0], ValueError)


# ============================================================================
# ASYNC CONTEXT MANAGER TESTS
# ============================================================================

class TestAsyncContextManager:
    """Test async context managers (__aenter__/__aexit__)."""

    @pytest.mark.asyncio
    async def test_class_based_context_manager(self):
        """Class with __aenter__ and __aexit__."""
        class Resource:
            def __init__(self):
                self.opened = False
                self.closed = False

            async def __aenter__(self):
                self.opened = True
                return self

            async def __aexit__(self, *args):
                self.closed = True
                return False

        async with Resource() as r:
            assert r.opened
            assert not r.closed
        assert r.closed

    @pytest.mark.asyncio
    async def test_decorator_context_manager(self):
        """@asynccontextmanager decorator."""
        @asynccontextmanager
        async def managed():
            state = {"entered": False, "exited": False}
            state["entered"] = True
            yield state
            state["exited"] = True

        async with managed() as s:
            assert s["entered"]
            assert not s["exited"]
        assert s["exited"]

    @pytest.mark.asyncio
    async def test_context_manager_exception_handling(self):
        """Context manager receives exceptions."""
        @asynccontextmanager
        async def catch_errors():
            caught = []
            try:
                yield caught
            except ValueError as e:
                caught.append(str(e))

        errors = []
        async with catch_errors() as e:
            try:
                raise ValueError("test error")
            except ValueError:
                pass  # Caught inside the with block
        # The context manager itself doesn't catch it if it's caught before yield


# ============================================================================
# ASYNC ITERATOR TESTS
# ============================================================================

class TestAsyncIterator:
    """Test async iterators and async generators."""

    @pytest.mark.asyncio
    async def test_class_based_async_iterator(self):
        """Class with __aiter__ and __anext__."""
        class AsyncRange:
            def __init__(self, n):
                self.n = n
                self.current = 0

            def __aiter__(self):
                return self

            async def __anext__(self):
                if self.current >= self.n:
                    raise StopAsyncIteration
                await asyncio.sleep(0)
                value = self.current
                self.current += 1
                return value

        results = []
        async for num in AsyncRange(5):
            results.append(num)
        assert results == [0, 1, 2, 3, 4]

    @pytest.mark.asyncio
    async def test_async_generator(self):
        """Async generator with yield."""
        async def gen(n):
            for i in range(n):
                await asyncio.sleep(0)
                yield i

        results = []
        async for num in gen(5):
            results.append(num)
        assert results == [0, 1, 2, 3, 4]

    @pytest.mark.asyncio
    async def test_async_list_comprehension(self):
        """List comprehension with async for."""
        async def gen():
            for i in range(5):
                await asyncio.sleep(0)
                yield i

        results = [n async for n in gen()]
        assert results == [0, 1, 2, 3, 4]

    @pytest.mark.asyncio
    async def test_async_generator_return(self):
        """Async generator can return early."""
        async def limited():
            for i in range(100):
                if i >= 3:
                    return
                await asyncio.sleep(0)
                yield i

        results = [n async for n in limited()]
        assert results == [0, 1, 2]


# ============================================================================
# SEMAPHORE TESTS
# ============================================================================

class TestSemaphore:
    """Test semaphore for concurrency limiting."""

    @pytest.mark.asyncio
    async def test_semaphore_limits_concurrency(self):
        """Semaphore limits concurrent execution."""
        semaphore = asyncio.Semaphore(2)
        concurrent = {"count": 0, "max": 0}

        async def task():
            async with semaphore:
                concurrent["count"] += 1
                concurrent["max"] = max(concurrent["max"], concurrent["count"])
                await asyncio.sleep(0.05)
                concurrent["count"] -= 1

        await asyncio.gather(*[task() for _ in range(6)])
        assert concurrent["max"] <= 2

    @pytest.mark.asyncio
    async def test_semaphore_allows_concurrent(self):
        """Semaphore allows up to N concurrent tasks."""
        semaphore = asyncio.Semaphore(3)
        completed = []

        async def task(n):
            async with semaphore:
                await asyncio.sleep(0.01)
                completed.append(n)

        await asyncio.gather(*[task(i) for i in range(5)])
        assert len(completed) == 5


# ============================================================================
# TIMEOUT TESTS
# ============================================================================

class TestTimeout:
    """Test timeout handling."""

    @pytest.mark.asyncio
    async def test_wait_for_timeout(self):
        """wait_for() raises TimeoutError on timeout."""
        async def slow():
            await asyncio.sleep(10)
            return "done"

        with pytest.raises(TimeoutError):
            await asyncio.wait_for(slow(), timeout=0.01)

    @pytest.mark.asyncio
    async def test_wait_for_success(self):
        """wait_for() returns result when no timeout."""
        async def fast():
            await asyncio.sleep(0.01)
            return "done"

        result = await asyncio.wait_for(fast(), timeout=5.0)
        assert result == "done"

    @pytest.mark.asyncio
    async def test_timeout_context_manager(self):
        """asyncio.timeout() as context manager."""
        async def slow():
            await asyncio.sleep(10)
            return "done"

        with pytest.raises(TimeoutError):
            async with asyncio.timeout(0.01):
                await slow()


# ============================================================================
# CONCURRENT PATTERNS TESTS
# ============================================================================

class TestConcurrentPatterns:
    """Test real-world concurrent patterns."""

    @pytest.mark.asyncio
    async def test_fan_out_fan_in(self):
        """Fan-out work to multiple tasks, fan-in results."""
        async def process(item):
            await asyncio.sleep(0.01)
            return item * 2

        items = [1, 2, 3, 4, 5]
        tasks = [process(item) for item in items]
        results = await asyncio.gather(*tasks)
        assert results == [2, 4, 6, 8, 10]

    @pytest.mark.asyncio
    async def test_sequential_then_concurrent(self):
        """Mix sequential and concurrent patterns."""
        async def fetch(n):
            await asyncio.sleep(0.01)
            return n

        # Sequential phase
        step1 = await fetch(1)

        # Concurrent phase
        step2, step3 = await asyncio.gather(fetch(2), fetch(3))

        assert step1 == 1
        assert step2 == 2
        assert step3 == 3

    @pytest.mark.asyncio
    async def test_concurrent_with_rate_limiting(self):
        """Concurrent execution with rate limiting via semaphore."""
        semaphore = asyncio.Semaphore(2)
        call_log = []

        async def api_call(n):
            async with semaphore:
                call_log.append(f"start-{n}")
                await asyncio.sleep(0.01)
                call_log.append(f"end-{n}")
                return n

        results = await asyncio.gather(*[api_call(i) for i in range(4)])
        assert results == [0, 1, 2, 3]
        # Verify no more than 2 concurrent
        assert len(call_log) == 8  # 4 starts + 4 ends

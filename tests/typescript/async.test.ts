/**
 * Tests for Atom 04: Async Programming
 * =====================================
 * Tests for Promises, async/await, concurrency patterns, and error handling.
 */

import { describe, it, expect } from "vitest";

// ============================================================================
// PROMISES
// ============================================================================

describe("Promises", () => {
  it("Promise resolves with value", async () => {
    const result = await Promise.resolve(42);
    expect(result).toBe(42);
  });

  it("Promise rejects with error", async () => {
    await expect(Promise.reject(new Error("fail"))).rejects.toThrow("fail");
  });

  it("promise chaining", async () => {
    const result = await Promise.resolve(5)
      .then((n) => n * 2)
      .then((n) => n + 10);
    expect(result).toBe(20);
  });

  it("custom promise with delay", async () => {
    function delay(ms: number): Promise<void> {
      return new Promise((resolve) => setTimeout(resolve, ms));
    }

    const start = Date.now();
    await delay(50);
    const elapsed = Date.now() - start;
    expect(elapsed).toBeGreaterThanOrEqual(40);
  });
});

// ============================================================================
// ASYNC / AWAIT
// ============================================================================

describe("Async / Await", () => {
  it("async function returns promise", async () => {
    async function getValue(): Promise<number> {
      return 42;
    }
    const result = await getValue();
    expect(result).toBe(42);
  });

  it("sequential await calls", async () => {
    async function step1(): Promise<number> {
      return 10;
    }
    async function step2(n: number): Promise<number> {
      return n * 2;
    }

    const s1 = await step1();
    const s2 = await step2(s1);
    expect(s2).toBe(20);
  });

  it("async function with error", async () => {
    async function failing(): Promise<never> {
      throw new Error("async error");
    }
    await expect(failing()).rejects.toThrow("async error");
  });
});

// ============================================================================
// ERROR HANDLING
// ============================================================================

describe("Error Handling", () => {
  it("try/catch around await", async () => {
    async function riskyOperation(): Promise<string> {
      throw new Error("boom");
    }

    let result: string;
    try {
      result = await riskyOperation();
    } catch (error) {
      result = "caught: " + (error as Error).message;
    }
    expect(result).toBe("caught: boom");
  });

  it("custom error classes", async () => {
    class ValidationError extends Error {
      constructor(
        message: string,
        public field: string
      ) {
        super(message);
        this.name = "ValidationError";
      }
    }

    async function validate(name: string): Promise<void> {
      if (!name) throw new ValidationError("Name required", "name");
    }

    try {
      await validate("");
    } catch (error) {
      expect(error).toBeInstanceOf(ValidationError);
      expect((error as ValidationError).field).toBe("name");
      expect((error as ValidationError).message).toBe("Name required");
    }
  });
});

// ============================================================================
// PROMISE.ALL
// ============================================================================

describe("Promise.all", () => {
  it("resolves when all promises resolve", async () => {
    const results = await Promise.all([
      Promise.resolve(1),
      Promise.resolve(2),
      Promise.resolve(3),
    ]);
    expect(results).toEqual([1, 2, 3]);
  });

  it("rejects when any promise rejects", async () => {
    await expect(
      Promise.all([
        Promise.resolve(1),
        Promise.reject(new Error("fail")),
        Promise.resolve(3),
      ])
    ).rejects.toThrow("fail");
  });

  it("parallel execution of independent operations", async () => {
    async function fetchUser(id: number) {
      return { id, name: `User${id}` };
    }

    const users = await Promise.all([
      fetchUser(1),
      fetchUser(2),
      fetchUser(3),
    ]);
    expect(users).toHaveLength(3);
    expect(users[0].name).toBe("User1");
    expect(users[2].name).toBe("User3");
  });
});

// ============================================================================
// PROMISE.RACE AND PROMISE.ANY
// ============================================================================

describe("Promise.race and Promise.any", () => {
  it("Promise.race returns first to settle", async () => {
    const result = await Promise.race([
      new Promise((resolve) => setTimeout(() => resolve("slow"), 100)),
      Promise.resolve("fast"),
    ]);
    expect(result).toBe("fast");
  });

  it("Promise.any returns first to resolve", async () => {
    const result = await Promise.any([
      Promise.reject(new Error("fail")),
      Promise.resolve("winner"),
      Promise.resolve("second"),
    ]);
    expect(result).toBe("winner");
  });

  it("Promise.any rejects with AggregateError if all reject", async () => {
    await expect(
      Promise.any([
        Promise.reject(new Error("e1")),
        Promise.reject(new Error("e2")),
      ])
    ).rejects.toThrow();
  });

  it("timeout pattern with Promise.race", async () => {
    function timeout<T>(promise: Promise<T>, ms: number): Promise<T> {
      const timeoutPromise = new Promise<never>((_, reject) => {
        setTimeout(() => reject(new Error(`Timed out after ${ms}ms`)), ms);
      });
      return Promise.race([promise, timeoutPromise]);
    }

    // Fast operation completes before timeout
    const result = await timeout(Promise.resolve(42), 1000);
    expect(result).toBe(42);

    // Slow operation times out
    await expect(
      timeout(new Promise((r) => setTimeout(r, 200)), 50)
    ).rejects.toThrow("Timed out");
  });
});

// ============================================================================
// PROMISE.ALLSETTLED
// ============================================================================

describe("Promise.allSettled", () => {
  it("waits for all promises regardless of rejection", async () => {
    const results = await Promise.allSettled([
      Promise.resolve("ok"),
      Promise.reject(new Error("fail")),
      Promise.resolve("also ok"),
    ]);

    expect(results).toHaveLength(3);
    expect(results[0].status).toBe("fulfilled");
    if (results[0].status === "fulfilled") {
      expect(results[0].value).toBe("ok");
    }
    expect(results[1].status).toBe("rejected");
    expect(results[2].status).toBe("fulfilled");
  });

  it("processes mixed results safely", async () => {
    const results = await Promise.allSettled([
      Promise.resolve(1),
      Promise.reject(new Error("bad")),
      Promise.resolve(3),
    ]);

    const successes = results
      .filter((r): r is PromiseFulfilledResult<number> => r.status === "fulfilled")
      .map((r) => r.value);
    const failures = results
      .filter((r): r is PromiseRejectedResult => r.status === "rejected")
      .map((r) => r.reason.message);

    expect(successes).toEqual([1, 3]);
    expect(failures).toEqual(["bad"]);
  });
});

// ============================================================================
// ASYNC ITERATORS
// ============================================================================

describe("Async Iterators", () => {
  it("async generator yields values", async () => {
    async function* count(to: number): AsyncGenerator<number> {
      for (let i = 1; i <= to; i++) {
        yield i;
      }
    }

    const results: number[] = [];
    for await (const n of count(5)) {
      results.push(n);
    }
    expect(results).toEqual([1, 2, 3, 4, 5]);
  });

  it("async generator for pagination", async () => {
    async function* paginate(
      fetchPage: (page: number) => Promise<number[]>,
      pageSize: number
    ): AsyncGenerator<number> {
      let page = 0;
      while (true) {
        const items = await fetchPage(page);
        if (items.length === 0) break;
        for (const item of items) {
          yield item;
        }
        page++;
        if (items.length < pageSize) break;
      }
    }

    const fetchPage = async (page: number): Promise<number[]> => {
      if (page >= 3) return [];
      return [page * 10 + 1, page * 10 + 2, page * 10 + 3];
    };

    const results: number[] = [];
    for await (const item of paginate(fetchPage, 3)) {
      results.push(item);
    }
    expect(results).toEqual([1, 2, 3, 11, 12, 13, 21, 22, 23]);
  });
});

// ============================================================================
// CONCURRENCY PATTERNS
// ============================================================================

describe("Concurrency Patterns", () => {
  it("sequential execution", async () => {
    async function sequential<T, R>(items: T[], fn: (item: T) => Promise<R>): Promise<R[]> {
      const results: R[] = [];
      for (const item of items) {
        results.push(await fn(item));
      }
      return results;
    }

    const order: number[] = [];
    await sequential([1, 2, 3], async (n) => {
      order.push(n);
      return n * 2;
    });
    expect(order).toEqual([1, 2, 3]); // executed in order
  });

  it("concurrent with limit", async () => {
    async function concurrentLimit<T, R>(
      items: T[],
      fn: (item: T) => Promise<R>,
      limit: number
    ): Promise<R[]> {
      const results: R[] = new Array(items.length);
      let index = 0;

      async function worker() {
        while (index < items.length) {
          const currentIndex = index++;
          results[currentIndex] = await fn(items[currentIndex]);
        }
      }

      const workers = Array.from({ length: Math.min(limit, items.length) }, () => worker());
      await Promise.all(workers);
      return results;
    }

    const results = await concurrentLimit(
      [1, 2, 3, 4, 5],
      async (n) => n * 2,
      2
    );
    expect(results).toEqual([2, 4, 6, 8, 10]);
  });

  it("retry with backoff", async () => {
    async function retryWithBackoff<T>(
      fn: () => Promise<T>,
      maxRetries: number,
      baseDelay: number
    ): Promise<T> {
      let lastError: Error | undefined;
      for (let attempt = 0; attempt <= maxRetries; attempt++) {
        try {
          return await fn();
        } catch (error) {
          lastError = error as Error;
        }
      }
      throw lastError;
    }

    let attempts = 0;
    const result = await retryWithBackoff(
      async () => {
        attempts++;
        if (attempts < 3) throw new Error("not yet");
        return "success";
      },
      5,
      10 // short delay for tests
    );
    expect(result).toBe("success");
    expect(attempts).toBe(3);
  });
});

// ============================================================================
// ABORT CONTROLLER
// ============================================================================

describe("AbortController", () => {
  it("can be used to cancel operations", async () => {
    const controller = new AbortController();
    const { signal } = controller;

    async function longOperation(signal: AbortSignal): Promise<string> {
      return new Promise((resolve, reject) => {
        const timer = setTimeout(() => resolve("done"), 200);
        signal.addEventListener("abort", () => {
          clearTimeout(timer);
          reject(new DOMException("Aborted", "AbortError"));
        });
      });
    }

    // Cancel after 50ms
    setTimeout(() => controller.abort(), 50);

    await expect(longOperation(signal)).rejects.toThrow("Aborted");
  });

  it("completes if not aborted", async () => {
    const controller = new AbortController();

    async function quickOp(signal: AbortSignal): Promise<number> {
      signal.throwIfAborted();
      return 42;
    }

    const result = await quickOp(controller.signal);
    expect(result).toBe(42);
  });
});

// ============================================================================
// TYPED EVENT EMITTER
// ============================================================================

describe("Typed Event Emitter", () => {
  type EventMap = {
    data: { value: number };
    error: { message: string };
  };

  class TypedEmitter<Events extends Record<string, any>> {
    private listeners = new Map<keyof Events, Set<Function>>();

    on<K extends keyof Events>(event: K, listener: (data: Events[K]) => void): void {
      if (!this.listeners.has(event)) {
        this.listeners.set(event, new Set());
      }
      this.listeners.get(event)!.add(listener);
    }

    emit<K extends keyof Events>(event: K, data: Events[K]): void {
      const handlers = this.listeners.get(event);
      if (handlers) {
        for (const handler of handlers) {
          handler(data);
        }
      }
    }
  }

  it("emits and receives typed events", () => {
    const emitter = new TypedEmitter<EventMap>();
    const received: number[] = [];

    emitter.on("data", (d) => received.push(d.value));
    emitter.emit("data", { value: 1 });
    emitter.emit("data", { value: 2 });

    expect(received).toEqual([1, 2]);
  });

  it("multiple listeners for same event", () => {
    const emitter = new TypedEmitter<EventMap>();
    const messages: string[] = [];

    emitter.on("error", (e) => messages.push(e.message));
    emitter.on("error", (e) => messages.push(`ERR: ${e.message}`));

    emitter.emit("error", { message: "oops" });
    expect(messages).toEqual(["oops", "ERR: oops"]);
  });
});

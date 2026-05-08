/**
 * Atom 04: Async Programming in TypeScript
 * =========================================
 * Promises, async/await, concurrency patterns, and error handling.
 *
 * Architecture: JavaScript is single-threaded with an event loop. Async
 * programming is NOT parallelism -- it's concurrency via cooperative
 * multitasking. Promises represent future values; async/await is syntactic
 * sugar over Promises. TypeScript adds full type safety to all of this.
 *
 * Transferability: Python's asyncio is conceptually identical -- both use
 * an event loop, both have await, both handle concurrency (not parallelism).
 * Python's asyncio.gather maps to Promise.all, asyncio.wait to Promise.allSettled.
 *
 * Application: API calls, database queries, file I/O, WebSocket connections,
 * batch processing, rate limiting, retry logic, timeout patterns.
 */

// ============================================================================
// SECTION 1: PROMISES
// ============================================================================
// A Promise represents a value that may not be available yet.

// Creating a Promise
function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
// IO: delay(1000) => resolves after 1 second

// Promise with a result
function fetchNumber(value: number): Promise<number> {
  return new Promise((resolve, reject) => {
    if (value < 0) {
      reject(new Error("Negative value not allowed"));
    } else {
      setTimeout(() => resolve(value * 2), 100);
    }
  });
}
// IO: fetchNumber(5) => Promise that resolves to 10

// Promise chaining
fetchNumber(5)
  .then((result) => result + 1) // 11
  .then((result) => result * 3) // 33
  .then((final) => console.log(final)) // 33
  .catch((err) => console.error(err));

// ============================================================================
// SECTION 2: ASYNC / AWAIT
// ============================================================================
// Syntactic sugar over Promises. Makes async code read like sync code.

async function getUserProfile(userId: number): Promise<{ name: string; email: string }> {
  // Simulated API calls
  const user = await fetchUser(userId);
  const email = await fetchEmail(user.name);
  return { name: user.name, email };
}

async function fetchUser(id: number): Promise<{ id: number; name: string }> {
  return { id, name: "Alice" };
}

async function fetchEmail(name: string): Promise<string> {
  return `${name.toLowerCase()}@example.com`;
}

// Calling async functions
async function main() {
  const profile = await getUserProfile(1);
  console.log(profile); // { name: "Alice", email: "alice@example.com" }
}

// ============================================================================
// SECTION 3: ERROR HANDLING
// ============================================================================
// Always wrap await calls in try/catch for robust error handling.

// Basic try/catch
async function safeFetch<T>(url: string): Promise<T | null> {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return (await response.json()) as T;
  } catch (error) {
    console.error(`Failed to fetch ${url}:`, error);
    return null;
  }
}

// Error type narrowing
async function handleErrors() {
  try {
    await fetchNumber(-1);
  } catch (error) {
    if (error instanceof Error) {
      console.error(error.message); // narrowed to Error
    } else {
      console.error("Unknown error:", error);
    }
  }
}

// Custom error classes for better error handling
class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public endpoint: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

class ValidationError extends Error {
  constructor(
    message: string,
    public field: string
  ) {
    super(message);
    this.name = "ValidationError";
  }
}

async function createUserAPI(data: { name: string; email: string }): Promise<User> {
  if (!data.name) {
    throw new ValidationError("Name is required", "name");
  }
  if (!data.email.includes("@")) {
    throw new ValidationError("Invalid email format", "email");
  }
  return { id: 1, name: data.name, email: data.email, createdAt: new Date() };
}

// Catching specific error types
async function handleCreateUser() {
  try {
    await createUserAPI({ name: "", email: "test@test.com" });
  } catch (error) {
    if (error instanceof ValidationError) {
      console.error(`Validation failed on field "${error.field}": ${error.message}`);
    } else if (error instanceof ApiError) {
      console.error(`API error ${error.statusCode} at ${error.endpoint}`);
    } else {
      throw error; // Re-throw unknown errors
    }
  }
}

// ============================================================================
// SECTION 4: PROMISE.ALL -- PARALLEL EXECUTION
// ============================================================================
// Run multiple async operations concurrently and wait for ALL to complete.

interface User { id: number; name: string; email: string; createdAt: Date }

async function fetchMultipleUsers(ids: number[]): Promise<User[]> {
  const promises = ids.map((id) => fetchUser(id).then((u) => ({
    ...u,
    email: `${u.name.toLowerCase()}@example.com`,
    createdAt: new Date(),
  })));
  return Promise.all(promises);
}
// IO: fetchMultipleUsers([1, 2, 3]) => Promise<User[]> with 3 users

// Promise.all fails fast: if ANY promise rejects, the whole thing rejects.
async function failFast() {
  try {
    await Promise.all([
      fetchNumber(1),   // resolves to 2
      fetchNumber(-1),  // rejects!
      fetchNumber(3),   // may or may not execute
    ]);
  } catch (error) {
    // At least one failed. We don't know which others succeeded.
    console.error("At least one operation failed");
  }
}

// ============================================================================
// SECTION 5: PROMISE.RACE -- FIRST TO COMPLETE
// ============================================================================
// Returns the result of the first promise to settle (resolve OR reject).

function timeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  const timeoutPromise = new Promise<never>((_, reject) => {
    setTimeout(() => reject(new Error(`Timed out after ${ms}ms`)), ms);
  });
  return Promise.race([promise, timeoutPromise]);
}
// IO: timeout(fetchNumber(5), 1000) => 10 (if completes within 1s)
// IO: timeout(delay(5000), 1000) => Error: Timed out after 1000ms

// Promise.any: returns the first to RESOLVE (ignores rejections)
async function firstSuccess() {
  const result = await Promise.any([
    fetchNumber(-1),  // rejects (ignored by any)
    fetchNumber(10),  // resolves to 20
    fetchNumber(20),  // resolves to 40
  ]);
  console.log(result); // 20 (first to resolve)
}

// ============================================================================
// SECTION 6: PROMISE.ALLSETTLED -- WAIT FOR ALL
// ============================================================================
// Waits for ALL promises to settle (resolve or reject) without failing fast.

interface SettlementResult<T> {
  status: "fulfilled" | "rejected";
  value?: T;
  reason?: Error;
}

async function safeBatchFetch(ids: number[]): Promise<SettlementResult<User>[]> {
  const promises = ids.map((id) =>
    fetchUser(id).then((u) => ({
      ...u,
      email: `${u.name.toLowerCase()}@example.com`,
      createdAt: new Date(),
    }))
  );
  return Promise.allSettled(promises);
}

// Usage: process results without failing
async function processBatchResults() {
  const results = await safeBatchFetch([1, -1, 3]);

  for (const result of results) {
    if (result.status === "fulfilled") {
      console.log("Success:", result.value);
    } else {
      console.error("Failed:", result.reason);
    }
  }
}

// ============================================================================
// SECTION 7: ASYNC ITERATORS (for-await-of)
// ============================================================================
// Iterate over async data sources, like paginated APIs or streams.

// Async generator: yields values asynchronously
async function* paginate<T>(
  fetchPage: (page: number) => Promise<T[]>,
  pageSize: number
): AsyncGenerator<T> {
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

// Usage with for-await-of
async function consumePages() {
  const fetchPage = async (page: number): Promise<number[]> => {
    if (page >= 3) return [];
    return [page * 10 + 1, page * 10 + 2, page * 10 + 3];
  };

  for await (const item of paginate(fetchPage, 3)) {
    console.log(item); // 1, 2, 3, 11, 12, 13, 21, 22, 23
  }
}

// Async iterable from a stream
async function* readLines(stream: ReadableStream<string>): AsyncGenerator<string> {
  const reader = stream.getReader();
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      yield value;
    }
  } finally {
    reader.releaseLock();
  }
}

// ============================================================================
// SECTION 8: ABORTCONTROLLER
// ============================================================================
// Cancel async operations cleanly. Works with fetch, Promises, and event listeners.

async function fetchWithAbort(url: string, signal: AbortSignal): Promise<Response> {
  const response = await fetch(url, { signal });
  return response;
}

// Usage: cancel a request after timeout
async function cancellableFetch() {
  const controller = new AbortController();
  const { signal } = controller;

  // Cancel after 5 seconds
  const timeoutId = setTimeout(() => controller.abort(), 5000);

  try {
    const response = await fetchWithAbort("https://api.example.com/data", signal);
    clearTimeout(timeoutId);
    return await response.json();
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      console.log("Request was cancelled");
    } else {
      throw error;
    }
  }
}

// Passing abort signal through async functions
async function fetchUserWithCancel(userId: number, signal?: AbortSignal): Promise<User> {
  signal?.throwIfAborted();
  const user = await fetchUser(userId);
  signal?.throwIfAborted();
  const email = await fetchEmail(user.name);
  signal?.throwIfAborted();
  return { ...user, email, createdAt: new Date() };
}

// ============================================================================
// SECTION 9: CONCURRENCY PATTERNS
// ============================================================================

// Sequential execution (one at a time)
async function sequential<T, R>(
  items: T[],
  fn: (item: T) => Promise<R>
): Promise<R[]> {
  const results: R[] = [];
  for (const item of items) {
    results.push(await fn(item));
  }
  return results;
}

// Concurrent with limit (control parallelism)
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
// IO: concurrentLimit([1,2,3,4,5], fetchNumber, 2) => [2,4,6,8,10]
// Runs at most 2 fetches concurrently

// Retry with exponential backoff
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
      if (attempt < maxRetries) {
        const delayMs = baseDelay * 2 ** attempt;
        await delay(delayMs);
      }
    }
  }
  throw lastError;
}
// IO: retryWithBackoff(() => fetchNumber(5), 3, 1000)
// Retries up to 3 times with delays: 1s, 2s, 4s

// ============================================================================
// SECTION 10: TYPED EVENT EMITTER
// ============================================================================
// Type-safe async event handling.

type EventMap2 = {
  userCreated: { id: number; name: string };
  userDeleted: { id: number };
  error: { message: string; code: number };
};

class TypedEventEmitter<Events extends Record<string, any>> {
  private listeners = new Map<keyof Events, Set<Function>>();

  on<K extends keyof Events>(event: K, listener: (data: Events[K]) => void | Promise<void>): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(listener);
  }

  async emit<K extends keyof Events>(event: K, data: Events[K]): Promise<void> {
    const eventListeners = this.listeners.get(event);
    if (!eventListeners) return;
    const promises = Array.from(eventListeners).map((listener) => listener(data));
    await Promise.all(promises);
  }
}

// Usage
const emitter = new TypedEventEmitter<EventMap2>();
emitter.on("userCreated", async (data) => {
  console.log(`User created: ${data.name}`); // data is typed as { id: number; name: string }
});

// ============================================================================
// MINI-EXERCISES
// ============================================================================
// 1. Implement a `debounceAsync` function that delays execution of an async
//    function until after a specified wait time.
//
// 2. Create a `Queue` class that processes async tasks one at a time (FIFO),
//    with a configurable concurrency limit.
//
// 3. Write a `raceWithFallback` function that tries multiple async sources
//    in order and returns the first successful result.
//
// 4. Implement an async `mapLimit` function that maps over an array with
//    a concurrency limit, similar to the async library.

// ============================================================================
// KEY TAKEAWAYS
// ============================================================================
// 1. Promises represent future values; async/await makes them readable.
// 2. Promise.all fails fast; Promise.allSettled waits for all.
// 3. Promise.race returns the first to settle; Promise.any returns the first to resolve.
// 4. Always handle errors with try/catch around await calls.
// 5. AbortController provides clean cancellation for async operations.
// 6. Async generators (async function*) yield values over time.
// 7. Concurrency patterns (sequential, parallel, limited) control resource usage.
// 8. TypeScript types the resolved value: Promise<T> means the await gives you T.

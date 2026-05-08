/**
 * Tests for Atom 02: Functions & Generics
 * ========================================
 * Tests for function types, generics, overloads, and higher-order patterns.
 */

import { describe, it, expect } from "vitest";

// ============================================================================
// BASIC FUNCTION TYPES
// ============================================================================

describe("Function Types", () => {
  it("typed function parameters enforce types at compile time", () => {
    function add(a: number, b: number): number {
      return a + b;
    }
    expect(add(2, 3)).toBe(5);
    expect(add(-1, 1)).toBe(0);
  });

  it("function types as variables", () => {
    type MathOp = (a: number, b: number) => number;
    const subtract: MathOp = (a, b) => a - b;
    const multiply: MathOp = (a, b) => a * b;
    expect(subtract(10, 3)).toBe(7);
    expect(multiply(4, 5)).toBe(20);
  });

  it("function as parameter (higher-order)", () => {
    type MathOp = (a: number, b: number) => number;
    function apply(a: number, b: number, op: MathOp): number {
      return op(a, b);
    }
    expect(apply(10, 3, (a, b) => a / b)).toBeCloseTo(3.333, 2);
    expect(apply(10, 3, (a, b) => a ** b)).toBe(1000);
  });
});

// ============================================================================
// OPTIONAL AND DEFAULT PARAMETERS
// ============================================================================

describe("Optional and Default Parameters", () => {
  it("optional parameter with nullish coalescing", () => {
    function greet(name: string, greeting?: string): string {
      return `${greeting ?? "Hello"}, ${name}!`;
    }
    expect(greet("Alice")).toBe("Hello, Alice!");
    expect(greet("Alice", "Hi")).toBe("Hi, Alice!");
  });

  it("default parameter", () => {
    function createUser(name: string, role: string = "user") {
      return { name, role };
    }
    expect(createUser("Alice")).toEqual({ name: "Alice", role: "user" });
    expect(createUser("Bob", "admin")).toEqual({ name: "Bob", role: "admin" });
  });
});

// ============================================================================
// REST PARAMETERS
// ============================================================================

describe("Rest Parameters", () => {
  it("sum variadic numbers", () => {
    function sum(...numbers: number[]): number {
      return numbers.reduce((acc, n) => acc + n, 0);
    }
    expect(sum(1, 2, 3)).toBe(6);
    expect(sum(10, 20, 30, 40)).toBe(100);
    expect(sum()).toBe(0);
  });

  it("rest params with leading required param", () => {
    function log(level: string, ...messages: string[]): string {
      return `[${level}] ${messages.join(" ")}`;
    }
    expect(log("INFO", "started", "ok")).toBe("[INFO] started ok");
    expect(log("ERR")).toBe("[ERR] ");
  });
});

// ============================================================================
// GENERICS
// ============================================================================

describe("Generics", () => {
  it("identity preserves type", () => {
    function identity<T>(value: T): T {
      return value;
    }
    expect(identity("hello")).toBe("hello");
    expect(identity(42)).toBe(42);
    expect(identity(true)).toBe(true);
    expect(identity(null)).toBe(null);
  });

  it("generic with constraint (keyof)", () => {
    function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
      return obj[key];
    }
    const person = { name: "Alice", age: 30 };
    expect(getProperty(person, "name")).toBe("Alice");
    expect(getProperty(person, "age")).toBe(30);
  });

  it("multiple type parameters", () => {
    function pair<A, B>(first: A, second: B): [A, B] {
      return [first, second];
    }
    expect(pair("hello", 42)).toEqual(["hello", 42]);
    expect(pair(true, null)).toEqual([true, null]);
  });

  it("generic with default type", () => {
    function createState<T = string>(initial: T): { value: T } {
      return { value: initial };
    }
    expect(createState(42).value).toBe(42);
    expect(createState("hello").value).toBe("hello");
    expect(createState(true).value).toBe(true);
  });

  it("generic class (InMemoryRepository)", () => {
    interface Entity { id: string; name: string }

    class Repo<T extends { id: string }> {
      private store = new Map<string, T>();
      save(entity: T): T {
        this.store.set(entity.id, entity);
        return entity;
      }
      findById(id: string): T | undefined {
        return this.store.get(id);
      }
      findAll(): T[] {
        return Array.from(this.store.values());
      }
      delete(id: string): boolean {
        return this.store.delete(id);
      }
    }

    const repo = new Repo<Entity>();
    repo.save({ id: "1", name: "Alice" });
    repo.save({ id: "2", name: "Bob" });

    expect(repo.findById("1")).toEqual({ id: "1", name: "Alice" });
    expect(repo.findById("3")).toBeUndefined();
    expect(repo.findAll()).toHaveLength(2);
    expect(repo.delete("1")).toBe(true);
    expect(repo.findById("1")).toBeUndefined();
  });
});

// ============================================================================
// FUNCTION OVERLOADS
// ============================================================================

describe("Function Overloads", () => {
  it("overloaded parseInput works for string input", () => {
    function parseInput(input: string): object;
    function parseInput(input: object): string;
    function parseInput(input: string | object): string | object {
      if (typeof input === "string") return JSON.parse(input);
      return JSON.stringify(input);
    }

    const result1 = parseInput('{"a":1}');
    expect(result1).toEqual({ a: 1 });

    const result2 = parseInput({ a: 1 });
    expect(result2).toBe('{"a":1}');
  });
});

// ============================================================================
// ARROW FUNCTIONS
// ============================================================================

describe("Arrow Functions", () => {
  it("basic arrow function", () => {
    const double = (x: number): number => x * 2;
    expect(double(5)).toBe(10);
  });

  it("arrow function with map", () => {
    const numbers = [1, 2, 3, 4, 5];
    const doubled = numbers.map((n) => n * 2);
    expect(doubled).toEqual([2, 4, 6, 8, 10]);
  });

  it("arrow function with destructuring", () => {
    type Point = { x: number; y: number };
    const distance = ({ x, y }: Point): number => Math.sqrt(x * x + y * y);
    expect(distance({ x: 3, y: 4 })).toBe(5);
    expect(distance({ x: 0, y: 0 })).toBe(0);
  });

  it("generic arrow function", () => {
    const wrap = <T>(value: T): { data: T } => ({ data: value });
    expect(wrap(42)).toEqual({ data: 42 });
    expect(wrap("hi")).toEqual({ data: "hi" });
  });
});

// ============================================================================
// HIGHER-ORDER FUNCTIONS AND CURRYING
// ============================================================================

describe("Higher-Order Functions", () => {
  it("createMultiplier factory", () => {
    function createMultiplier(factor: number): (n: number) => number {
      return (n) => n * factor;
    }
    const triple = createMultiplier(3);
    const double = createMultiplier(2);
    expect(triple(10)).toBe(30);
    expect(double(10)).toBe(20);
  });

  it("curried function", () => {
    function curry<A, B, C>(fn: (a: A, b: B) => C): (a: A) => (b: B) => C {
      return (a) => (b) => fn(a, b);
    }
    const curriedAdd = curry((a: number, b: number) => a + b);
    const add5 = curriedAdd(5);
    expect(add5(3)).toBe(8);
    expect(add5(10)).toBe(15);
    expect(curriedAdd(1)(2)).toBe(3);
  });

  it("pipe composes functions", () => {
    function pipe<A, B>(ab: (a: A) => B): (a: A) => B;
    function pipe<A, B, C>(ab: (a: A) => B, bc: (b: B) => C): (a: A) => C;
    function pipe(...fns: Function[]) {
      return (input: any) => fns.reduce((acc, fn) => fn(acc), input);
    }

    const processNumber = pipe(
      (n: number) => n * 2,
      (n: number) => n + 10,
      (n: number) => `Result: ${n}`
    );
    expect(processNumber(5)).toBe("Result: 20");
    expect(processNumber(0)).toBe("Result: 10");
  });
});

// ============================================================================
// TYPE PREDICATES AND ASSERTION FUNCTIONS
// ============================================================================

describe("Type Predicates", () => {
  it("isNonNullable filters null/undefined", () => {
    function isNonNullable<T>(value: T | null | undefined): value is T {
      return value !== null && value !== undefined;
    }
    const values: (string | null | undefined)[] = ["a", null, "b", undefined, "c"];
    const nonNull = values.filter(isNonNullable);
    expect(nonNull).toEqual(["a", "b", "c"]);
  });

  it("assertDefined throws on null", () => {
    function assertDefined<T>(value: T | null | undefined, name: string): asserts value is T {
      if (value === null || value === undefined) {
        throw new Error(`Expected ${name} to be defined`);
      }
    }
    expect(() => assertDefined("hello", "input")).not.toThrow();
    expect(() => assertDefined(null, "input")).toThrow("Expected input to be defined");
    expect(() => assertDefined(undefined, "input")).toThrow("Expected input to be defined");
  });
});

// ============================================================================
// ASYNC GENERICS
// ============================================================================

describe("Async Generic Functions", () => {
  it("retry succeeds on first attempt", async () => {
    async function retry<T>(fn: () => Promise<T>, attempts: number): Promise<T> {
      let lastError: Error | undefined;
      for (let i = 0; i < attempts; i++) {
        try {
          return await fn();
        } catch (e) {
          lastError = e as Error;
        }
      }
      throw lastError;
    }

    let calls = 0;
    const result = await retry(async () => {
      calls++;
      return 42;
    }, 3);
    expect(result).toBe(42);
    expect(calls).toBe(1);
  });

  it("retry retries on failure", async () => {
    async function retry<T>(fn: () => Promise<T>, attempts: number): Promise<T> {
      let lastError: Error | undefined;
      for (let i = 0; i < attempts; i++) {
        try {
          return await fn();
        } catch (e) {
          lastError = e as Error;
        }
      }
      throw lastError;
    }

    let calls = 0;
    const result = await retry(async () => {
      calls++;
      if (calls < 3) throw new Error("fail");
      return "success";
    }, 5);
    expect(result).toBe("success");
    expect(calls).toBe(3);
  });

  it("retry throws after exhausting attempts", async () => {
    async function retry<T>(fn: () => Promise<T>, attempts: number): Promise<T> {
      let lastError: Error | undefined;
      for (let i = 0; i < attempts; i++) {
        try {
          return await fn();
        } catch (e) {
          lastError = e as Error;
        }
      }
      throw lastError;
    }

    await expect(
      retry(async () => {
        throw new Error("always fails");
      }, 3)
    ).rejects.toThrow("always fails");
  });
});

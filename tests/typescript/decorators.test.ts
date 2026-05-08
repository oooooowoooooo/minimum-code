/**
 * Tests for Atom 06: Decorators & Metaprogramming
 * ================================================
 * Tests for class, method, property decorators and decorator factories.
 * Note: Decorators require experimentalDecorators in tsconfig.json.
 * These tests verify runtime behavior of decorated classes.
 */

import { describe, it, expect, vi } from "vitest";

// ============================================================================
// CLASS DECORATORS
// ============================================================================

describe("Class Decorators", () => {
  // Simulate class decorator behavior (without actual decorator syntax for test portability)
  function Timestamped<T extends new (...args: any[]) => {}>(constructor: T) {
    return class extends constructor {
      createdAt = new Date();
    };
  }

  it("class decorator adds properties", () => {
    class Model {
      constructor(public name: string) {}
    }

    const DecoratedModel = Timestamped(Model);
    const instance = new DecoratedModel("test") as any;

    expect(instance.name).toBe("test");
    expect(instance.createdAt).toBeInstanceOf(Date);
  });

  it("class decorator factory with parameters", () => {
    function Entity(tableName: string) {
      return function <T extends new (...args: any[]) => {}>(constructor: T) {
        return class extends constructor {
          static tableName = tableName;
          static find() {
            return `SELECT * FROM ${tableName}`;
          }
        };
      };
    }

    class UserEntity {
      constructor(public name: string) {}
    }

    const DecoratedUser = Entity("users")(UserEntity);
    expect((DecoratedUser as any).tableName).toBe("users");
    expect((DecoratedUser as any).find()).toBe("SELECT * FROM users");
  });
});

// ============================================================================
// METHOD DECORATORS
// ============================================================================

describe("Method Decorators", () => {
  it("logging decorator wraps method", () => {
    function Log(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
      const original = descriptor.value;
      const calls: { method: string; args: any[]; result: any }[] = [];

      descriptor.value = function (...args: any[]) {
        const result = original.apply(this, args);
        calls.push({ method: propertyKey, args, result });
        return result;
      };

      descriptor.value._calls = calls;
      return descriptor;
    }

    class Calculator {
      @Log
      add(a: number, b: number): number {
        return a + b;
      }
    }

    const calc = new Calculator();
    const result = calc.add(2, 3);
    expect(result).toBe(5);
  });

  it("timing decorator measures execution", () => {
    const timings: { name: string; duration: number }[] = [];

    function Timed(label?: string) {
      return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
        const original = descriptor.value;
        const name = label ?? propertyKey;

        descriptor.value = function (...args: any[]) {
          const start = performance.now();
          const result = original.apply(this, args);
          const end = performance.now();
          timings.push({ name, duration: end - start });
          return result;
        };
        return descriptor;
      };
    }

    // Apply decorator manually
    class Worker {
      work() {
        let sum = 0;
        for (let i = 0; i < 1000; i++) sum += i;
        return sum;
      }
    }

    const descriptor = Object.getOwnPropertyDescriptor(Worker.prototype, "work")!;
    Timed("work")(Worker.prototype, "work", descriptor);
    Object.defineProperty(Worker.prototype, "work", descriptor);

    const worker = new Worker();
    worker.work();

    expect(timings).toHaveLength(1);
    expect(timings[0].name).toBe("work");
    expect(timings[0].duration).toBeGreaterThanOrEqual(0);
  });
});

// ============================================================================
// MEMOIZATION DECORATOR
// ============================================================================

describe("Memoization Decorator", () => {
  function Memoize(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const original = descriptor.value;
    const cache = new Map<string, any>();

    descriptor.value = function (...args: any[]) {
      const key = JSON.stringify(args);
      if (cache.has(key)) return cache.get(key);
      const result = original.apply(this, args);
      cache.set(key, result);
      return result;
    };
    return descriptor;
  }

  it("caches return values", () => {
    let callCount = 0;

    class MathService {
      @Memoize
      expensiveAdd(a: number, b: number): number {
        callCount++;
        return a + b;
      }
    }

    const service = new MathService();
    expect(service.expensiveAdd(2, 3)).toBe(5);
    expect(service.expensiveAdd(2, 3)).toBe(5);
    expect(service.expensiveAdd(2, 3)).toBe(5);
    expect(callCount).toBe(1); // called only once

    expect(service.expensiveAdd(4, 5)).toBe(9);
    expect(callCount).toBe(2); // new args = new call
  });
});

// ============================================================================
// RETRY DECORATOR
// ============================================================================

describe("Retry Decorator", () => {
  function Retry(maxAttempts: number = 3) {
    return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
      const original = descriptor.value;

      descriptor.value = async function (...args: any[]) {
        let lastError: Error | undefined;
        for (let attempt = 1; attempt <= maxAttempts; attempt++) {
          try {
            return await original.apply(this, args);
          } catch (error) {
            lastError = error as Error;
          }
        }
        throw lastError;
      };
      return descriptor;
    };
  }

  it("retries on failure and eventually succeeds", async () => {
    let attempts = 0;

    class Service {
      @Retry(3)
      async fetch(): Promise<string> {
        attempts++;
        if (attempts < 3) throw new Error("not yet");
        return "success";
      }
    }

    const service = new Service();
    const result = await service.fetch();
    expect(result).toBe("success");
    expect(attempts).toBe(3);
  });

  it("throws after exhausting retries", async () => {
    class Service {
      @Retry(2)
      async alwaysFail(): Promise<never> {
        throw new Error("always fails");
      }
    }

    const service = new Service();
    await expect(service.alwaysFail()).rejects.toThrow("always fails");
  });
});

// ============================================================================
// RATE LIMIT DECORATOR
// ============================================================================

describe("Rate Limit Decorator", () => {
  function RateLimit(callsPerWindow: number, windowMs: number = 1000) {
    const timestamps: number[] = [];

    return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
      const original = descriptor.value;

      descriptor.value = function (...args: any[]) {
        const now = Date.now();
        const windowStart = now - windowMs;

        while (timestamps.length > 0 && timestamps[0] < windowStart) {
          timestamps.shift();
        }

        if (timestamps.length >= callsPerWindow) {
          throw new Error(`Rate limit exceeded for ${propertyKey}`);
        }

        timestamps.push(now);
        return original.apply(this, args);
      };
      return descriptor;
    };
  }

  it("allows calls within rate limit", () => {
    class Api {
      @RateLimit(3)
      call() {
        return "ok";
      }
    }

    const api = new Api();
    expect(api.call()).toBe("ok");
    expect(api.call()).toBe("ok");
    expect(api.call()).toBe("ok");
  });

  it("rejects calls exceeding rate limit", () => {
    class Api {
      @RateLimit(2, 10000) // 2 calls per 10 seconds
      call() {
        return "ok";
      }
    }

    const api = new Api();
    api.call();
    api.call();
    expect(() => api.call()).toThrow("Rate limit exceeded");
  });
});

// ============================================================================
// ACCESS CONTROL DECORATOR
// ============================================================================

describe("Access Control Decorator", () => {
  function Authorized(role: string) {
    return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
      const original = descriptor.value;

      descriptor.value = function (this: any, ...args: any[]) {
        const currentUser = this.currentUser;
        if (!currentUser || currentUser.role !== role) {
          throw new Error(`Unauthorized: requires role "${role}"`);
        }
        return original.apply(this, args);
      };
      return descriptor;
    };
  }

  it("allows access for correct role", () => {
    class AdminPanel {
      currentUser = { role: "admin" };

      @Authorized("admin")
      deleteUser(id: number) {
        return `Deleted user ${id}`;
      }
    }

    const panel = new AdminPanel();
    expect(panel.deleteUser(1)).toBe("Deleted user 1");
  });

  it("denies access for wrong role", () => {
    class AdminPanel {
      currentUser = { role: "user" };

      @Authorized("admin")
      deleteUser(id: number) {
        return `Deleted user ${id}`;
      }
    }

    const panel = new AdminPanel();
    expect(() => panel.deleteUser(1)).toThrow('Unauthorized: requires role "admin"');
  });

  it("denies access when no user", () => {
    class AdminPanel {
      currentUser = null;

      @Authorized("admin")
      deleteUser(id: number) {
        return `Deleted user ${id}`;
      }
    }

    const panel = new AdminPanel();
    expect(() => panel.deleteUser(1)).toThrow("Unauthorized");
  });
});

// ============================================================================
// DECORATOR COMPOSITION ORDER
// ============================================================================

describe("Decorator Composition Order", () => {
  it("decorators apply bottom-up", () => {
    const order: string[] = [];

    function DecoratorA(target: any, key: string, descriptor: PropertyDescriptor) {
      const original = descriptor.value;
      order.push("A-applied");
      descriptor.value = function (...args: any[]) {
        order.push("A-called");
        return original.apply(this, args);
      };
      return descriptor;
    }

    function DecoratorB(target: any, key: string, descriptor: PropertyDescriptor) {
      const original = descriptor.value;
      order.push("B-applied");
      descriptor.value = function (...args: any[]) {
        order.push("B-called");
        return original.apply(this, args);
      };
      return descriptor;
    }

    // Apply B first (bottom), then A (top) -- simulating @A @B
    class Example {
      method() {
        order.push("original");
      }
    }

    const desc = Object.getOwnPropertyDescriptor(Example.prototype, "method")!;
    DecoratorB(Example.prototype, "method", desc);
    DecoratorA(Example.prototype, "method", desc);
    Object.defineProperty(Example.prototype, "method", desc);

    order.length = 0;
    const instance = new Example();
    instance.method();

    // B wraps A wraps original
    expect(order).toEqual(["A-called", "B-called", "original"]);
  });
});

// ============================================================================
// PROPERTY DECORATOR (METADATA)
// ============================================================================

describe("Property Decorators", () => {
  it("property decorator registers metadata", () => {
    const metadata = new Map<string, Set<string>>();

    function Required(target: any, propertyKey: string) {
      const key = target.constructor.name;
      if (!metadata.has(key)) metadata.set(key, new Set());
      metadata.get(key)!.add(propertyKey);
    }

    class Product {
      @Required
      name: string = "";

      @Required
      price: number = 0;

      description?: string;
    }

    const requiredFields = metadata.get("Product");
    expect(requiredFields).toBeDefined();
    expect(requiredFields!.has("name")).toBe(true);
    expect(requiredFields!.has("price")).toBe(true);
    expect(requiredFields!.has("description")).toBe(false);
  });
});

// ============================================================================
// SINGLETON DECORATOR
// ============================================================================

describe("Singleton Pattern", () => {
  it("singleton ensures one instance", () => {
    function Singleton<T extends new (...args: any[]) => any>(constructor: T) {
      let instance: InstanceType<T>;

      return class extends constructor {
        constructor(...args: any[]) {
          if (instance) return instance;
          super(...args);
          instance = this as InstanceType<T>;
        }
      } as T;
    }

    @Singleton
    class Database {
      constructor(public url: string) {}
    }

    // Note: For test we apply manually since decorator syntax may not be available
    const SingletonDb = Singleton(Database);
    const db1 = new SingletonDb("postgres://localhost");
    const db2 = new SingletonDb("postgres://localhost");

    expect(db1.url).toBe("postgres://localhost");
    expect(db1).toBe(db2); // same instance
  });
});

// ============================================================================
// DEBOUNCE DECORATOR
// ============================================================================

describe("Debounce Decorator", () => {
  it("debounce delays execution", async () => {
    function Debounce(ms: number) {
      return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
        const original = descriptor.value;
        let timeoutId: ReturnType<typeof setTimeout>;

        descriptor.value = function (this: any, ...args: any[]) {
          clearTimeout(timeoutId);
          return new Promise((resolve) => {
            timeoutId = setTimeout(() => {
              resolve(original.apply(this, args));
            }, ms);
          });
        };
        return descriptor;
      };
    }

    let callCount = 0;

    class SearchService {
      @Debounce(50)
      search(query: string): string {
        callCount++;
        return `Results for: ${query}`;
      }
    }

    const service = new SearchService();

    // Multiple rapid calls
    service.search("a");
    service.search("ab");
    const result = await service.search("abc");

    expect(result).toBe("Results for: abc");
    expect(callCount).toBe(1); // only the last call executes
  });
});

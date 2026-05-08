/**
 * Tests for Atom 01: TypeScript Type System
 * ==========================================
 * Tests validate runtime behavior of type-narrowed code patterns.
 * Note: Many type-level tests are compile-time only (the TS compiler IS the test).
 * These tests focus on runtime correctness of the patterns.
 */

import { describe, it, expect } from "vitest";

// ============================================================================
// PRIMITIVE TYPES AND BASIC OPERATIONS
// ============================================================================

describe("Primitive Types", () => {
  it("string operations work correctly", () => {
    const appName: string = "TypeScript Atom";
    expect(appName.toUpperCase()).toBe("TYPESCRIPT ATOM");
    expect(appName.length).toBe(15);
  });

  it("number operations work correctly", () => {
    const version: number = 1;
    expect(version + 0.5).toBe(1.5);
    expect(Number.isInteger(version)).toBe(true);
  });

  it("bigint works with large numbers", () => {
    const large: bigint = 100n;
    expect(large + 1n).toBe(101n);
  });
});

// ============================================================================
// UNKNOWN VS ANY
// ============================================================================

describe("Unknown type safety", () => {
  it("unknown requires narrowing before use", () => {
    const safeValue: unknown = 42;
    // After typeof check, we can use number methods
    if (typeof safeValue === "number") {
      expect(safeValue.toFixed(2)).toBe("42.00");
    } else {
      throw new Error("Expected number");
    }
  });

  it("unknown works with string narrowing", () => {
    const value: unknown = "hello";
    if (typeof value === "string") {
      expect(value.toUpperCase()).toBe("HELLO");
    } else {
      throw new Error("Expected string");
    }
  });
});

// ============================================================================
// TUPLES
// ============================================================================

describe("Tuples", () => {
  it("tuple preserves order and types", () => {
    const pair: [string, number] = ["age", 25];
    expect(pair[0]).toBe("age");
    expect(pair[1]).toBe(25);
  });

  it("tuple destructuring works", () => {
    const response: [number, string] = [200, '{"ok":true}'];
    const [status, body] = response;
    expect(status).toBe(200);
    expect(JSON.parse(body)).toEqual({ ok: true });
  });
});

// ============================================================================
// TYPE NARROWING
// ============================================================================

describe("Type Narrowing", () => {
  // Re-implement locally since imports from src/ may not resolve in test
  function processValue(value: string | number | boolean): string {
    if (typeof value === "string") return value.toUpperCase();
    if (typeof value === "number") return value.toFixed(2);
    return value ? "yes" : "no";
  }

  it("narrows string correctly", () => {
    expect(processValue("hello")).toBe("HELLO");
  });

  it("narrows number correctly", () => {
    expect(processValue(42)).toBe("42.00");
  });

  it("narrows boolean correctly", () => {
    expect(processValue(true)).toBe("yes");
    expect(processValue(false)).toBe("no");
  });

  it("instanceof narrowing for Date", () => {
    function formatDate(input: Date | string): string {
      if (input instanceof Date) return input.toISOString().split("T")[0];
      return input;
    }
    expect(formatDate("2024-01-01")).toBe("2024-01-01");
    expect(formatDate(new Date("2024-06-15T00:00:00Z"))).toBe("2024-06-15");
  });

  it("in operator narrowing", () => {
    interface Fish { swim(): void }
    interface Bird { fly(): void }

    function move(animal: Fish | Bird): string {
      if ("swim" in animal) return "swimming";
      return "flying";
    }

    const fish: Fish = { swim() {} };
    const bird: Bird = { fly() {} };
    expect(move(fish)).toBe("swimming");
    expect(move(bird)).toBe("flying");
  });
});

// ============================================================================
// CUSTOM TYPE GUARDS
// ============================================================================

describe("Custom Type Guards", () => {
  interface Fish { swim(): void; name: string }
  interface Bird { fly(): void; name: string }

  function isFish(animal: Fish | Bird): animal is Fish {
    return "swim" in animal;
  }

  it("type guard correctly identifies Fish", () => {
    const fish: Fish = { swim() {}, name: "Nemo" };
    expect(isFish(fish)).toBe(true);
  });

  it("type guard correctly rejects Bird", () => {
    const bird: Bird = { fly() {}, name: "Eagle" };
    expect(isFish(bird)).toBe(false);
  });

  it("type guard enables narrowed access", () => {
    const animals: (Fish | Bird)[] = [
      { swim() {}, name: "Nemo" },
      { fly() {}, name: "Eagle" },
      { swim() {}, name: "Dory" },
    ];
    const fishNames = animals.filter(isFish).map((f) => f.name);
    expect(fishNames).toEqual(["Nemo", "Dory"]);
  });
});

// ============================================================================
// DISCRIMINATED UNIONS
// ============================================================================

describe("Discriminated Unions", () => {
  type Shape =
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

  it("calculates circle area", () => {
    const area = calculateArea({ kind: "circle", radius: 5 });
    expect(area).toBeCloseTo(78.54, 1);
  });

  it("calculates rectangle area", () => {
    expect(calculateArea({ kind: "rectangle", width: 4, height: 6 })).toBe(24);
  });

  it("calculates triangle area", () => {
    expect(calculateArea({ kind: "triangle", base: 10, height: 5 })).toBe(25);
  });

  it("exhaustive switch handles all cases", () => {
    const shapes: Shape[] = [
      { kind: "circle", radius: 1 },
      { kind: "rectangle", width: 2, height: 3 },
      { kind: "triangle", base: 4, height: 5 },
    ];
    const areas = shapes.map(calculateArea);
    expect(areas).toHaveLength(3);
    areas.forEach((a) => expect(typeof a).toBe("number"));
  });
});

// ============================================================================
// LITERAL TYPES
// ============================================================================

describe("Literal Types", () => {
  type Direction = "north" | "south" | "east" | "west";

  function moveDirection(dir: Direction): string {
    return `Moving ${dir}`;
  }

  it("accepts valid literal values", () => {
    expect(moveDirection("north")).toBe("Moving north");
    expect(moveDirection("west")).toBe("Moving west");
  });

  it("type DiceRoll constrains values", () => {
    type DiceRoll = 1 | 2 | 3 | 4 | 5 | 6;
    function roll(): DiceRoll {
      return (Math.floor(Math.random() * 6) + 1) as DiceRoll;
    }
    const result = roll();
    expect(result).toBeGreaterThanOrEqual(1);
    expect(result).toBeLessThanOrEqual(6);
  });
});

// ============================================================================
// CONST ASSERTIONS
// ============================================================================

describe("Const Assertions", () => {
  it("as const creates readonly literal types", () => {
    const config = {
      apiUrl: "https://api.example.com",
      timeout: 5000,
    } as const;

    expect(config.apiUrl).toBe("https://api.example.com");
    expect(config.timeout).toBe(5000);
  });

  it("as const with arrays creates readonly tuples", () => {
    const coordinates = [10, 20] as const;
    expect(coordinates[0]).toBe(10);
    expect(coordinates[1]).toBe(20);
    expect(coordinates).toHaveLength(2);
  });
});

// ============================================================================
// KEYOF AND INDEXED ACCESS
// ============================================================================

describe("keyof and Indexed Access", () => {
  interface User {
    id: number;
    name: string;
    email: string;
  }

  function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
  }

  it("getProperty returns correct type and value", () => {
    const user: User = { id: 1, name: "Alice", email: "a@b.com" };
    expect(getProperty(user, "id")).toBe(1);
    expect(getProperty(user, "name")).toBe("Alice");
    expect(getProperty(user, "email")).toBe("a@b.com");
  });
});

/**
 * Tests for Atom 03: Interfaces & Type Manipulation
 * ==================================================
 * Tests for interfaces, mapped types, conditional types, and utility types.
 * Many tests are compile-time verifications. Runtime tests validate behavior.
 */

import { describe, it, expect } from "vitest";

// ============================================================================
// INTERFACES
// ============================================================================

describe("Interfaces", () => {
  it("interface defines object shape", () => {
    interface User {
      id: number;
      name: string;
      email: string;
    }

    const user: User = { id: 1, name: "Alice", email: "a@b.com" };
    expect(user.id).toBe(1);
    expect(user.name).toBe("Alice");
  });

  it("interface extension", () => {
    interface Shape { color: string }
    interface Circle extends Shape { radius: number }

    const circle: Circle = { color: "red", radius: 5 };
    expect(circle.color).toBe("red");
    expect(circle.radius).toBe(5);
  });

  it("interface with optional properties", () => {
    interface Config {
      host: string;
      port?: number;
      debug?: boolean;
    }

    const config: Config = { host: "localhost" };
    expect(config.host).toBe("localhost");
    expect(config.port).toBeUndefined();
  });

  it("interface with readonly properties", () => {
    interface Frozen {
      readonly id: number;
      name: string;
    }

    const obj: Frozen = { id: 1, name: "test" };
    expect(obj.id).toBe(1);
    obj.name = "changed"; // OK
    // obj.id = 2; // Compile error
  });
});

// ============================================================================
// UNION AND INTERSECTION TYPES
// ============================================================================

describe("Union and Intersection Types", () => {
  it("union type accepts either type", () => {
    type StringOrNumber = string | number;

    function format(value: StringOrNumber): string {
      if (typeof value === "string") return value.toUpperCase();
      return value.toFixed(2);
    }

    expect(format("hello")).toBe("HELLO");
    expect(format(42)).toBe("42.00");
  });

  it("intersection type combines all properties", () => {
    type WithId = { id: string };
    type WithTimestamps = { createdAt: Date; updatedAt: Date };
    type Entity = WithId & WithTimestamps;

    const entity: Entity = {
      id: "1",
      createdAt: new Date("2024-01-01"),
      updatedAt: new Date("2024-06-01"),
    };

    expect(entity.id).toBe("1");
    expect(entity.createdAt).toBeInstanceOf(Date);
    expect(entity.updatedAt).toBeInstanceOf(Date);
  });
});

// ============================================================================
// TYPE ALIASES
// ============================================================================

describe("Type Aliases", () => {
  it("type alias for union", () => {
    type Status = "idle" | "loading" | "success" | "error";

    function handleStatus(status: Status): string {
      switch (status) {
        case "idle": return "Waiting...";
        case "loading": return "Loading...";
        case "success": return "Done!";
        case "error": return "Failed!";
      }
    }

    expect(handleStatus("loading")).toBe("Loading...");
    expect(handleStatus("success")).toBe("Done!");
  });

  it("type alias for tuple", () => {
    type Pair<T> = [T, T];
    type Coordinate = Pair<number>;

    const point: Coordinate = [10, 20];
    expect(point[0]).toBe(10);
    expect(point[1]).toBe(20);
  });
});

// ============================================================================
// MAPPED TYPES
// ============================================================================

describe("Mapped Types", () => {
  it("Partial makes all properties optional", () => {
    interface User {
      name: string;
      email: string;
      age: number;
    }

    type PartialUser = Partial<User>;

    // Can create with no properties
    const partial: PartialUser = {};
    expect(partial.name).toBeUndefined();

    // Can create with some properties
    const partial2: PartialUser = { name: "Alice" };
    expect(partial2.name).toBe("Alice");
    expect(partial2.email).toBeUndefined();
  });

  it("Required makes all properties required", () => {
    interface Config {
      host?: string;
      port?: number;
    }

    type RequiredConfig = Required<Config>;

    const config: RequiredConfig = { host: "localhost", port: 3000 };
    expect(config.host).toBe("localhost");
    expect(config.port).toBe(3000);
  });

  it("Readonly makes all properties readonly", () => {
    interface Mutable {
      name: string;
      value: number;
    }

    type Frozen = Readonly<Mutable>;

    const frozen: Frozen = { name: "test", value: 42 };
    expect(frozen.name).toBe("test");
    // frozen.name = "other"; // Compile error
  });
});

// ============================================================================
// CONDITIONAL TYPES
// ============================================================================

describe("Conditional Types", () => {
  it("conditional type resolves correctly (compile-time)", () => {
    // These are primarily compile-time tests
    type IsString<T> = T extends string ? true : false;

    // Runtime assertion that the type system works as expected
    const isStr: IsString<string> = true;
    const isNotStr: IsString<number> = false;

    expect(isStr).toBe(true);
    expect(isNotStr).toBe(false);
  });

  it("Exclude removes types from union", () => {
    type All = string | number | boolean;
    type WithoutBool = Exclude<All, boolean>;

    const val: WithoutBool = "hello"; // OK
    expect(val).toBe("hello");

    const val2: WithoutBool = 42; // OK
    expect(val2).toBe(42);
  });

  it("Extract keeps only specified types", () => {
    type All = string | number | boolean;
    type OnlyString = Extract<All, string>;

    const val: OnlyString = "hello";
    expect(val).toBe("hello");
  });

  it("NonNullable removes null and undefined", () => {
    type MaybeString = string | null | undefined;
    type DefiniteString = NonNullable<MaybeString>;

    const val: DefiniteString = "hello";
    expect(val).toBe("hello");
  });
});

// ============================================================================
// UTILITY TYPES (Pick, Omit, Record)
// ============================================================================

describe("Utility Types", () => {
  interface User {
    id: number;
    name: string;
    email: string;
    age: number;
  }

  it("Pick selects subset of properties", () => {
    type UserPreview = Pick<User, "id" | "name">;

    const preview: UserPreview = { id: 1, name: "Alice" };
    expect(preview.id).toBe(1);
    expect(preview.name).toBe("Alice");
  });

  it("Omit excludes properties", () => {
    type UserWithoutEmail = Omit<User, "email">;

    const user: UserWithoutEmail = { id: 1, name: "Alice", age: 30 };
    expect(user.id).toBe(1);
    expect(user.name).toBe("Alice");
  });

  it("Record constructs object type", () => {
    type RolePermissions = Record<"admin" | "user" | "guest", string[]>;

    const perms: RolePermissions = {
      admin: ["read", "write", "delete"],
      user: ["read", "write"],
      guest: ["read"],
    };

    expect(perms.admin).toContain("delete");
    expect(perms.guest).toEqual(["read"]);
  });
});

// ============================================================================
// RETURNTYPE AND PARAMETERS
// ============================================================================

describe("ReturnType and Parameters", () => {
  it("ReturnType extracts function return type", () => {
    function createUser(name: string, age: number) {
      return { id: 1, name, email: `${name}@test.com`, age, createdAt: new Date() };
    }

    type UserReturn = ReturnType<typeof createUser>;
    const user: UserReturn = { id: 1, name: "Alice", email: "a@b.com", age: 30, createdAt: new Date() };
    expect(user.name).toBe("Alice");
  });

  it("Parameters extracts function parameter types", () => {
    function greet(name: string, greeting: string): string {
      return `${greeting}, ${name}!`;
    }

    type GreetParams = Parameters<typeof greet>;
    const params: GreetParams = ["Alice", "Hello"];
    expect(greet(...params)).toBe("Hello, Alice!");
  });
});

// ============================================================================
// TEMPLATE LITERAL TYPES
// ============================================================================

describe("Template Literal Types", () => {
  it("template literal type constrains string format", () => {
    type Greeting = `Hello, ${string}!`;

    const valid: Greeting = "Hello, World!";
    expect(valid).toBe("Hello, World!");
  });

  it("template literal unions generate combinations", () => {
    type Color = "red" | "blue";
    type Size = "sm" | "lg";
    type ColorSize = `${Color}-${Size}`;

    function createLabel(cs: ColorSize): string {
      return cs;
    }

    expect(createLabel("red-sm")).toBe("red-sm");
    expect(createLabel("blue-lg")).toBe("blue-lg");
  });
});

// ============================================================================
// BRANDED TYPES
// ============================================================================

describe("Branded Types", () => {
  type Brand<T, B extends string> = T & { readonly __brand: B };
  type UserId = Brand<string, "UserId">;
  type OrderId = Brand<string, "OrderId">;

  function getUser(id: UserId): string {
    return `User: ${id}`;
  }

  it("branded type works at runtime", () => {
    const userId = "user-123" as UserId;
    expect(getUser(userId)).toBe("User: user-123");
  });
});

// ============================================================================
// DEEP PARTIAL (ADVANCED)
// ============================================================================

describe("Deep Partial", () => {
  type DeepPartial<T> = {
    [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
  };

  it("deep partial allows partial nested objects", () => {
    interface Config {
      database: {
        host: string;
        port: number;
      };
      cache: {
        ttl: number;
      };
    }

    const partial: DeepPartial<Config> = {
      database: { host: "localhost" },
    };

    expect(partial.database?.host).toBe("localhost");
    expect(partial.database?.port).toBeUndefined();
    expect(partial.cache).toBeUndefined();
  });
});

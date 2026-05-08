/**
 * Atom 01: TypeScript Type System
 * ================================
 * Static typing, type narrowing, and discriminated unions for robust code.
 *
 * Architecture: TypeScript adds a structural type system on top of JavaScript's
 * dynamic nature. Types are erased at compile time -- they exist only to help
 * the developer catch bugs before runtime. This "types as documentation" model
 * means zero runtime cost with maximum developer ergonomics.
 *
 * Transferability: Python's type hints (PEP 484) mirror many TS concepts --
 * Union types, Literal types, TypeGuard. TS discriminated unions map to
 * Python's sum types / tagged unions with isinstance checks.
 *
 * Application: Every TypeScript codebase uses these. API response typing,
 * form validation, state machines, Redux reducers, protocol definitions.
 */

// ============================================================================
// SECTION 1: PRIMITIVE TYPES
// ============================================================================
// TypeScript has the same primitives as JavaScript, with explicit annotations.

// Explicit type annotation (compiler infers these anyway)
let appName: string = "TypeScript Atom";
let version: number = 1;
let isProduction: boolean = false;
let nothing: null = null;
let notDefined: undefined = undefined;
let uniqueId: symbol = Symbol("id");
let largeCount: bigint = 100n;

// The "any" type disables type checking -- avoid it.
let dangerous: any = 42;
dangerous = "now a string"; // No error -- defeats the purpose of TS

// "unknown" is the type-safe alternative to "any".
let safeValue: unknown = 42;
// safeValue.toFixed(2); // ERROR: Object is of type 'unknown'
if (typeof safeValue === "number") {
  safeValue.toFixed(2); // OK after narrowing
}

// "void" represents the absence of a return value.
function logMessage(msg: string): void {
  console.log(msg);
  // implicitly returns undefined
}

// "never" represents values that never occur.
function throwError(message: string): never {
  throw new Error(message);
}

// ============================================================================
// SECTION 2: ARRAYS AND TUPLES
// ============================================================================

// Array syntax: two equivalent forms
let numbers: number[] = [1, 2, 3];
let strings: Array<string> = ["a", "b", "c"];

// Tuples: fixed-length arrays with typed positions
let pair: [string, number] = ["age", 25];
// pair = [25, "age"]; // ERROR: type mismatch at each position

// Named tuples (TS 4.0+) improve readability
type HttpResponse = [statusCode: number, body: string, headers: Record<string, string>];
const response: HttpResponse = [200, '{"ok":true}', { "content-type": "application/json" }];

// Readonly arrays prevent mutation
const frozen: readonly number[] = [1, 2, 3];
// frozen.push(4); // ERROR: Property 'push' does not exist on type 'readonly number[]'

// ============================================================================
// SECTION 3: OBJECT TYPES & INTERFACES
// ============================================================================

// Interface: named shape of an object
interface User {
  id: number;
  name: string;
  email: string;
  age?: number;           // Optional property
  readonly createdAt: Date; // Cannot be reassigned
}

// Usage
const user: User = {
  id: 1,
  name: "Alice",
  email: "alice@example.com",
  createdAt: new Date(),
};
// user.createdAt = new Date(); // ERROR: Cannot assign to 'createdAt'

// ============================================================================
// SECTION 4: TYPE ALIASES vs INTERFACES
// ============================================================================
// Both define object shapes, but type aliases are more flexible.

// Type alias: can define unions, intersections, primitives, tuples
type ID = string | number;
type Point = { x: number; y: number };
type Nullable<T> = T | null;

// Interface: can be extended and merged (declaration merging)
interface Animal {
  name: string;
}
interface Animal {
  // This MERGES with the above -- adds to the same interface
  legs: number;
}
// Animal is now { name: string; legs: number }

// When to use which:
// - Interface: for object shapes that may need extension or merging
// - Type alias: for unions, intersections, mapped types, or when you need more power

// ============================================================================
// SECTION 5: UNION AND INTERSECTION TYPES
// ============================================================================

// Union: value can be ONE of several types (|)
type StringOrNumber = string | number;

function formatId(id: StringOrNumber): string {
  // Must narrow before using type-specific methods
  if (typeof id === "string") {
    return id.toUpperCase(); // TS knows id is string here
  }
  return id.toFixed(2); // TS knows id is number here
}

// Intersection: value must satisfy ALL types (&)
type WithTimestamp = { createdAt: Date; updatedAt: Date };
type WithId = { id: string };
type Entity = WithTimestamp & WithId;
// Entity has: id, createdAt, updatedAt

const entity: Entity = {
  id: "abc",
  createdAt: new Date(),
  updatedAt: new Date(),
};

// ============================================================================
// SECTION 6: TYPE NARROWING
// ============================================================================
// TypeScript refines types through control flow analysis.

// typeof narrowing
function processValue(value: string | number | boolean): string {
  if (typeof value === "string") {
    return value.toUpperCase(); // narrowed to string
  }
  if (typeof value === "number") {
    return value.toFixed(2); // narrowed to number
  }
  return value ? "yes" : "no"; // narrowed to boolean
}

// instanceof narrowing
function formatDate(input: Date | string): string {
  if (input instanceof Date) {
    return input.toISOString(); // narrowed to Date
  }
  return input; // narrowed to string
}

// "in" operator narrowing
interface Fish { swim(): void }
interface Bird { fly(): void }

function move(animal: Fish | Bird): void {
  if ("swim" in animal) {
    animal.swim(); // narrowed to Fish
  } else {
    animal.fly(); // narrowed to Bird
  }
}

// Custom type guards (user-defined narrowing)
function isFish(animal: Fish | Bird): animal is Fish {
  return "swim" in animal;
}

// Usage
const getAnimal = (): Fish | Bird => ({ swim() {} });
const animal = getAnimal();
if (isFish(animal)) {
  animal.swim(); // TS knows it's Fish
}

// ============================================================================
// SECTION 7: DISCRIMINATED UNIONS (TAGGED UNIONS)
// ============================================================================
// The most powerful pattern in TypeScript. A shared literal property
// ("discriminant") lets the compiler narrow the type in switch/if.

// Define a union where each member has a unique "kind" tag
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };

function calculateArea(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2; // narrowed to circle
    case "rectangle":
      return shape.width * shape.height; // narrowed to rectangle
    case "triangle":
      return 0.5 * shape.base * shape.height; // narrowed to triangle
  }
}

// Exhaustiveness check: the compiler ensures all cases are handled.
function describeShape(shape: Shape): string {
  switch (shape.kind) {
    case "circle":
      return `Circle with radius ${shape.radius}`;
    case "rectangle":
      return `Rectangle ${shape.width}x${shape.height}`;
    case "triangle":
      return `Triangle base=${shape.kind}`;
    default:
      // If a new shape is added, this line causes a compile error
      const _exhaustive: never = shape;
      return _exhaustive;
  }
}

// IO: calculateArea({ kind: "circle", radius: 5 }) => 78.539...
// IO: calculateArea({ kind: "rectangle", width: 4, height: 6 }) => 24

// ============================================================================
// SECTION 8: LITERAL TYPES
// ============================================================================

// String literal types
type Direction = "north" | "south" | "east" | "west";
function moveDirection(dir: Direction): string {
  return `Moving ${dir}`;
}
// moveDirection("up"); // ERROR: Argument of type '"up"' is not assignable

// Numeric literal types
type DiceRoll = 1 | 2 | 3 | 4 | 5 | 6;
function roll(): DiceRoll {
  return (Math.floor(Math.random() * 6) + 1) as DiceRoll;
}

// Boolean literal types
type True = true;
type False = false;

// ============================================================================
// SECTION 9: TYPE ASSERTIONS
// ============================================================================
// Sometimes you know more than the compiler. Use assertions sparingly.

// "as" syntax (preferred)
const someValue: unknown = "hello world";
const strLength: number = (someValue as string).length;

// Angle-bracket syntax (not valid in TSX/JSX)
// const strLength2: number = (<string>someValue).length;

// Non-null assertion: tells compiler value is not null/undefined
function getUser(): User | undefined {
  return undefined;
}
const maybeUser = getUser();
// const name = maybeUser.name;        // ERROR: possibly undefined
const name = maybeUser!.name; // OK: you assert it's defined (risky!)

// Const assertion: narrows to the most specific literal type
const config = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
} as const;
// typeof config: { readonly apiUrl: "https://api.example.com"; readonly timeout: 5000 }
// config.apiUrl = "other"; // ERROR: readonly

// ============================================================================
// SECTION 10: KEYOF AND INDEXED ACCESS TYPES
// ============================================================================

// keyof: extracts the keys of a type as a union
type UserKeys = keyof User; // "id" | "name" | "email" | "age" | "createdAt"

// Indexed access: access a property's type by key
type UserName = User["name"]; // string
type UserIdOrName = User["id" | "name"]; // number | string

// Nested access
interface Company {
  ceo: { name: string; age: number };
}
type CeoAge = Company["ceo"]["age"]; // number

// ============================================================================
// SECTION 11: TUPLE TYPES AND CONST ASSERTIONS
// ============================================================================

// Using const assertions to create readonly tuple types
const coordinates = [10, 20] as const;
// typeof coordinates: readonly [10, 20]
// coordinates[0] = 15; // ERROR: readonly

// Practical use: defining strict function return types
function getUserInfo() {
  return ["Alice", 30] as const;
}
// Return type: readonly [string, number]
const [userName, userAge] = getUserInfo(); // destructured with correct types

// ============================================================================
// MINI-EXERCISES
// ============================================================================
// 1. Define a discriminated union for a "Result" type that can be either
//    { status: "success"; data: T } or { status: "error"; message: string }
//    Write a function that handles both cases.
//
// 2. Create a type "ReadonlyDeep<T>" that makes all properties (including
//    nested ones) readonly using mapped types.
//
// 3. Write a type guard function "isStringArray" that narrows
//    (string | number)[] to string[].
//
// 4. Use keyof and indexed access to create a function getProperty<T, K>(obj: T, key: K)
//    that returns the correct type for any key.

// ============================================================================
// KEY TAKEAWAYS
// ============================================================================
// 1. TypeScript's type system is STRUCTURAL, not nominal -- shapes matter, not names.
// 2. "unknown" is the type-safe alternative to "any" -- prefer it always.
// 3. Discriminated unions are the most powerful pattern for type-safe branching.
// 4. Type narrowing via control flow is automatic -- write clear conditionals.
// 5. "as const" creates deeply readonly literal types at zero cost.
// 6. Types are erased at compile time -- no runtime overhead.
// 7. keyof + indexed access types let you write type-safe generic utilities.
// 8. Exhaustiveness checks (never) ensure you handle all cases in switch/if.

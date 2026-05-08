/**
 * Atom 03: Interfaces & Type Manipulation
 * ========================================
 * Advanced type-level programming: mapped types, conditional types, utility types.
 *
 * Architecture: TypeScript's type system is TURING-COMPLETE. You can compute
 * types from other types, transforming shapes, extracting subsets, and building
 * new types at compile time. This is the key differentiator from Python's
 * type system, which is much more limited in type-level computation.
 *
 * Transferability: Python's typing module has TypedDict (like interfaces),
 * but lacks mapped types and conditional types. These TS patterns have no
 * direct Python equivalent -- they are unique to TS/DTS-world.
 *
 * Application: Library type definitions (d.ts files), API client generation,
 * ORM schemas, form validation libraries (Zod, Yup), state management.
 */

// ============================================================================
// SECTION 1: INTERFACES IN DEPTH
// ============================================================================

// Extending interfaces
interface Shape {
  color: string;
  strokeWidth: number;
}

interface Circle extends Shape {
  radius: number;
}

interface Rectangle extends Shape {
  width: number;
  height: number;
}

// Multiple inheritance
interface Styled {
  className: string;
  css: Record<string, string>;
}

interface StyledCircle extends Circle, Styled {
  // Merges all properties from Circle and Styled
}
// StyledCircle has: color, strokeWidth, radius, className, css

// Declaration merging: interfaces with the same name are merged
interface Config {
  apiUrl: string;
}
interface Config {
  timeout: number;
}
// Result: Config = { apiUrl: string; timeout: number }

// ============================================================================
// SECTION 2: TYPE ALIASES IN DEPTH
// ============================================================================

// Type aliases can express things interfaces cannot

// Union types
type Status = "idle" | "loading" | "success" | "error";

// Intersection types
type WithId = { id: string };
type WithTimestamps = { createdAt: Date; updatedAt: Date };
type Entity = WithId & WithTimestamps;

// Tuple types
type Pair<T> = [T, T];
type Coordinate = Pair<number>; // [number, number]

// Conditional expressions in types
type IsString<T> = T extends string ? true : false;
type A = IsString<string>; // true
type B = IsString<number>; // false

// ============================================================================
// SECTION 3: MAPPED TYPES
// ============================================================================
// Transform every property in a type. Syntax: { [K in keyof T]: ... }

// Make all properties optional
type MyPartial<T> = { [K in keyof T]?: T[K] };

// Make all properties required
type MyRequired<T> = { [K in keyof T]-?: T[K] };

// Make all properties readonly
type MyReadonly<T> = { readonly [K in keyof T]: T[K] };

// Make all properties mutable (remove readonly)
type Mutable<T> = { -readonly [K in keyof T]: T[K] };

// Practical example: form state where all fields start optional
interface UserForm {
  name: string;
  email: string;
  age: number;
}
type PartialForm = MyPartial<UserForm>;
// { name?: string; email?: string; age?: number }

// Mapped type with key remapping (TS 4.1+)
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};
type UserGetters = Getters<User>;
// { getId: () => number; getName: () => string; getEmail: () => string; ... }

// ============================================================================
// SECTION 4: CONDITIONAL TYPES
// ============================================================================
// Types that depend on a condition. Syntax: T extends U ? X : Y

// Basic conditional type
type TypeName<T> = T extends string
  ? "string"
  : T extends number
    ? "number"
    : T extends boolean
      ? "boolean"
      : T extends Function
        ? "function"
        : "object";

type S = TypeName<string>; // "string"
type N = TypeName<number>; // "number"
type F = TypeName<() => void>; // "function"

// Distributive conditional types: distributes over unions
type ToArray<T> = T extends any ? T[] : never;
type StringOrNumberArray = ToArray<string | number>; // string[] | number[]

// Prevent distribution with tuple wrapper
type ToArrayNonDist<T> = [T] extends [any] ? T[] : never;
type Combined = ToArrayNonDist<string | number>; // (string | number)[]

// ============================================================================
// SECTION 5: INFER KEYWORD IN CONDITIONAL TYPES
// ============================================================================
// "infer" extracts a type from within another type.

// Extract the return type of a function
type MyReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
type R1 = MyReturnType<() => string>; // string
type R2 = MyReturnType<(x: number) => boolean>; // boolean

// Extract the first parameter type
type FirstParam<T> = T extends (first: infer F, ...rest: any[]) => any ? F : never;
type FP = FirstParam<(a: string, b: number) => void>; // string

// Extract array element type
type ElementOf<T> = T extends (infer E)[] ? E : never;
type El = ElementOf<string[]>; // string

// Extract Promise inner type (unwrap)
type Unwrap<T> = T extends Promise<infer U> ? U : T;
type Unwrapped = Unwrap<Promise<number>>; // number
type AlreadyPlain = Unwrap<string>; // string

// Deep unwrap: recursively unwrap Promises
type DeepUnwrap<T> = T extends Promise<infer U> ? DeepUnwrap<U> : T;
type Deep = DeepUnwrap<Promise<Promise<Promise<string>>>>; // string

// ============================================================================
// SECTION 6: TEMPLATE LITERAL TYPES
// ============================================================================
// Build strings at the type level using template literal syntax.

type Greeting = `Hello, ${string}!`;
const validGreeting: Greeting = "Hello, World!"; // OK
// const bad: Greeting = "Hi, World!"; // ERROR

// Combine with unions to generate all combinations
type Color = "red" | "blue" | "green";
type Size = "sm" | "md" | "lg";
type ColorSize = `${Color}-${Size}`;
// "red-sm" | "red-md" | "red-lg" | "blue-sm" | ... (9 combinations)

// Capitalize, Uncapitalize, Uppercase, Lowercase utilities
type EventName = "click" | "focus" | "blur";
type HandlerName = `on${Capitalize<EventName>}`;
// "onClick" | "onFocus" | "onBlur"

// Practical: type-safe event emitter
type EventMap = {
  click: { x: number; y: number };
  focus: { target: string };
  blur: { target: string };
};
type EventHandler<T extends keyof EventMap> = (event: EventMap[T]) => void;
type OnEventHandlers = {
  [K in keyof EventMap as `on${Capitalize<K>}`]: EventHandler<K>;
};
// { onClick: (e: {x: number; y: number}) => void; onFocus: ...; onBlur: ... }

// ============================================================================
// SECTION 7: UTILITY TYPES (BUILT-IN)
// ============================================================================
// TypeScript ships with many utility types in lib.es5.d.ts.

interface User {
  id: number;
  name: string;
  email: string;
  age?: number;
  readonly createdAt: Date;
}

// Pick: select a subset of properties
type UserPreview = Pick<User, "id" | "name">;
// { id: number; name: string }

// Omit: exclude properties
type UserWithoutEmail = Omit<User, "email">;
// { id: number; name: string; age?: number; readonly createdAt: Date }

// Partial: all properties optional
type UserUpdate = Partial<User>;
// { id?: number; name?: string; ... }

// Required: all properties required
type FullUser = Required<User>;
// { id: number; name: string; email: string; age: number; readonly createdAt: Date }

// Readonly: all properties readonly
type FrozenUser = Readonly<User>;

// Record: construct an object type
type RolePermissions = Record<"admin" | "user" | "guest", string[]>;
// { admin: string[]; user: string[]; guest: string[] }

// Exclude: remove types from a union
type StringOrNumber = string | number | boolean;
type WithoutBoolean = Exclude<StringOrNumber, boolean>; // string | number

// Extract: keep only specified types from a union
type OnlyStrings = Extract<StringOrNumber, string>; // string

// NonNullable: remove null and undefined
type MaybeString = string | null | undefined;
type DefiniteString = NonNullable<MaybeString>; // string

// Parameters: extract parameter types as a tuple
function createUser(name: string, age: number): User {
  return { id: 1, name, email: "", createdAt: new Date() };
}
type CreateUserParams = Parameters<typeof createUser>; // [name: string, age: number]

// ConstructorParameters: extract constructor parameter types
class Animal {
  constructor(public name: string, public legs: number) {}
}
type AnimalCtorParams = ConstructorParameters<typeof Animal>; // [name: string, legs: number]

// ReturnType: extract return type
type CreateUserReturn = ReturnType<typeof createUser>; // User

// InstanceType: extract instance type of a constructor
type AnimalInstance = InstanceType<typeof Animal>; // Animal

// Awaited: unwrap Promise type (TS 4.5+)
type AsyncUser = Awaited<Promise<Promise<User>>>; // User

// ============================================================================
// SECTION 8: ADVANCED UTILITY TYPE PATTERNS
// ============================================================================

// Deep Partial: make all nested properties optional
type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};

interface Config {
  database: {
    host: string;
    port: number;
    credentials: {
      user: string;
      password: string;
    };
  };
  cache: {
    ttl: number;
  };
}
type PartialConfig = DeepPartial<Config>;
// All properties at every level are optional

// PathKeys: extract all dot-separated paths of a nested object
type PathKeys<T, Prefix extends string = ""> = T extends object
  ? {
      [K in keyof T & string]: K | PathKeys<T[K], `${Prefix}${K}.`>;
    }[keyof T & string]
  : never;

// Type-safe pick by path
type ValueAtPath<T, Path extends string> = Path extends `${infer Key}.${infer Rest}`
  ? Key extends keyof T
    ? ValueAtPath<T[Key], Rest>
    : never
  : Path extends keyof T
    ? T[Path]
    : never;

// ============================================================================
// SECTION 9: BRANDED / OPAQUE TYPES
// ============================================================================
// TypeScript uses structural typing, so two types with the same shape are
// compatible. Sometimes you want nominal typing (e.g., UserId vs OrderId).
// Branded types solve this.

type Brand<T, B extends string> = T & { readonly __brand: B };

type UserId = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;

function getUser(id: UserId): string {
  return `User: ${id}`;
}

const userId = "user-123" as UserId;
const orderId = "order-456" as OrderId;

getUser(userId); // OK
// getUser(orderId); // ERROR: OrderId is not assignable to UserId

// ============================================================================
// MINI-EXERCISES
// ============================================================================
// 1. Create a type `Mutable<T>` that removes `readonly` from all properties.
//
// 2. Write a conditional type `IsNever<T>` that returns `true` if T is `never`.
//
// 3. Build a `DeepReadonly<T>` type that recursively makes all properties readonly.
//
// 4. Create a type `UnionToIntersection<U>` that converts a union type to
//    an intersection type (hint: use distributive conditional types with infer).
//
// 5. Implement a type-safe `pick` function using generics and `K extends keyof T`.

// ============================================================================
// KEY TAKEAWAYS
// ============================================================================
// 1. Interfaces support declaration merging and extension; type aliases are more flexible.
// 2. Mapped types transform every property: { [K in keyof T]: NewType }.
// 3. Conditional types (T extends U ? X : Y) enable type-level branching.
// 4. "infer" extracts types from within other types in conditional types.
// 5. Template literal types build string types from other string types.
// 6. Utility types (Pick, Omit, Partial, etc.) are implemented using mapped + conditional types.
// 7. Branded types add nominal typing to TypeScript's structural type system.
// 8. TypeScript's type system is Turing-complete -- you can compute anything at the type level.

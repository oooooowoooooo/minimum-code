/**
 * Atom 02: Functions & Generics in TypeScript
 * ============================================
 * Typed function signatures, generics, overloads, and higher-order patterns.
 *
 * Architecture: Functions are the primary unit of composition in TypeScript.
 * Unlike Java/C#, TypeScript does not require classes to contain functions.
 * Generics enable writing code once that works across many types, similar
 * to templates in C++ or generics in Java, but with structural typing.
 *
 * Transferability: Python's typing module provides similar constructs --
 * Callable[..., R] maps to function types, TypeVar maps to <T>,
 * @overload maps to TS function overloads. The mental model is identical.
 *
 * Application: API handlers, utility libraries, middleware chains, data
 * transformation pipelines, React hooks, event handlers, plugin systems.
 */

// ============================================================================
// SECTION 1: FUNCTION TYPE ANNOTATIONS
// ============================================================================
// Every parameter and return value can (and should) be typed.

// Basic typed function
function add(a: number, b: number): number {
  return a + b;
}
// IO: add(2, 3) => 5
// IO: add("2", 3) => compile error

// Return type inference: TS can infer the return type from the body.
// Explicit annotation is recommended for public APIs and exported functions.
function multiply(a: number, b: number) {
  return a * b; // inferred as number
}

// ============================================================================
// SECTION 2: FUNCTION TYPES (CALLABLE TYPES)
// ============================================================================
// You can describe the shape of a function with a type.

// Type alias for a function signature
type MathOperation = (a: number, b: number) => number;

const subtract: MathOperation = (a, b) => a - b;
const divide: MathOperation = (a, b) => a / b;

// Interface with a call signature
interface Formatter {
  (value: string): string;
}
const toUpperCase: Formatter = (value) => value.toUpperCase();

// Function as a parameter (higher-order function)
function applyOperation(a: number, b: number, op: MathOperation): number {
  return op(a, b);
}
// IO: applyOperation(10, 3, subtract) => 7
// IO: applyOperation(10, 3, divide) => 3.333...

// ============================================================================
// SECTION 3: OPTIONAL AND DEFAULT PARAMETERS
// ============================================================================

// Optional parameter: must come after required parameters
function greet(name: string, greeting?: string): string {
  return `${greeting ?? "Hello"}, ${name}!`;
}
// IO: greet("Alice") => "Hello, Alice!"
// IO: greet("Alice", "Hi") => "Hi, Alice!"

// Default parameter
function createUser(name: string, role: string = "user"): { name: string; role: string } {
  return { name, role };
}
// IO: createUser("Alice") => { name: "Alice", role: "user" }
// IO: createUser("Bob", "admin") => { name: "Bob", role: "admin" }

// ============================================================================
// SECTION 4: REST PARAMETERS
// ============================================================================
// Collect remaining arguments into an array.

function sum(...numbers: number[]): number {
  return numbers.reduce((acc, n) => acc + n, 0);
}
// IO: sum(1, 2, 3) => 6
// IO: sum(10, 20, 30, 40) => 100

// Rest parameters with a leading required parameter
function log(level: string, ...messages: string[]): void {
  console.log(`[${level}]`, ...messages);
}
// IO: log("INFO", "server started", "port 3000") => [INFO] server started port 3000

// ============================================================================
// SECTION 5: GENERICS
// ============================================================================
// Generics allow functions to work with any type while preserving type safety.

// Basic generic function
function identity<T>(value: T): T {
  return value;
}
// IO: identity<string>("hello") => "hello" (type: string)
// IO: identity(42) => 42 (type: number, inferred)

// Generic with constraints
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
const person = { name: "Alice", age: 30 };
// IO: getProperty(person, "name") => "Alice" (type: string)
// IO: getProperty(person, "age") => 30 (type: number)
// IO: getProperty(person, "email") => compile error: "email" not in keyof person

// Multiple type parameters
function pair<A, B>(first: A, second: B): [A, B] {
  return [first, second];
}
// IO: pair("hello", 42) => ["hello", 42] (type: [string, number])

// Generic with default type
function createState<T = string>(initial: T): { value: T; reset: () => T } {
  let state = initial;
  return {
    value: state,
    reset: () => {
      state = initial;
      return state;
    },
  };
}
// IO: createState(42).value => 42 (type: number)
// IO: createState("hello").value => "hello" (type: string)

// ============================================================================
// SECTION 6: GENERIC INTERFACES AND CLASSES
// ============================================================================

// Generic interface
interface Repository<T> {
  findById(id: string): Promise<T | undefined>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<T>;
  delete(id: string): Promise<boolean>;
}

// Generic class implementing the interface
class InMemoryRepository<T extends { id: string }> implements Repository<T> {
  private store = new Map<string, T>();

  async findById(id: string): Promise<T | undefined> {
    return this.store.get(id);
  }

  async findAll(): Promise<T[]> {
    return Array.from(this.store.values());
  }

  async save(entity: T): Promise<T> {
    this.store.set(entity.id, entity);
    return entity;
  }

  async delete(id: string): Promise<boolean> {
    return this.store.delete(id);
  }
}

// Usage
interface Product {
  id: string;
  name: string;
  price: number;
}
const productRepo = new InMemoryRepository<Product>();

// ============================================================================
// SECTION 7: FUNCTION OVERLOADS
// ============================================================================
// Overloads let a function accept different argument combinations and return
// different types based on the input. The implementation signature must be
// compatible with all overloads.

// Overload signatures (what callers see)
function parseInput(input: string): object;
function parseInput(input: object): string;
// Implementation signature (not visible to callers)
function parseInput(input: string | object): string | object {
  if (typeof input === "string") {
    return JSON.parse(input); // string => object
  }
  return JSON.stringify(input); // object => string
}
// IO: parseInput('{"a":1}') => { a: 1 }
// IO: parseInput({ a: 1 }) => '{"a":1}'

// Overloads with generics
function createElement(tag: "div"): HTMLDivElement;
function createElement(tag: "span"): HTMLSpanElement;
function createElement(tag: "input"): HTMLInputElement;
function createElement(tag: string): HTMLElement;
function createElement(tag: string): HTMLElement {
  return document.createElement(tag);
}

// ============================================================================
// SECTION 8: ARROW FUNCTIONS
// ============================================================================
// Arrow functions have concise syntax and lexically bind "this".

// Arrow function with type annotations
const double = (x: number): number => x * 2;

// Arrow function as a callback
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map((n) => n * 2);
// IO: doubled => [2, 4, 6, 8, 10]

// Arrow function with destructuring
type Point = { x: number; y: number };
const distance = ({ x, y }: Point): number => Math.sqrt(x * x + y * y);
// IO: distance({ x: 3, y: 4 }) => 5

// Arrow function in a generic context
const wrap = <T>(value: T): { data: T } => ({ data: value });
// IO: wrap(42) => { data: 42 }

// ============================================================================
// SECTION 9: HIGHER-ORDER FUNCTIONS AND CURRYING
// ============================================================================
// Functions that take or return other functions. Currying transforms a
// multi-argument function into a sequence of single-argument functions.

// Higher-order function: returns a configured function
function createMultiplier(factor: number): (n: number) => number {
  return (n) => n * factor;
}
const triple = createMultiplier(3);
// IO: triple(10) => 30

// Curried function
function curry<A, B, C>(fn: (a: A, b: B) => C): (a: A) => (b: B) => C {
  return (a) => (b) => fn(a, b);
}
const curriedAdd = curry((a: number, b: number) => a + b);
const add5 = curriedAdd(5);
// IO: add5(3) => 8

// Pipe: compose functions left to right
function pipe<A, B>(ab: (a: A) => B): (a: A) => B;
function pipe<A, B, C>(ab: (a: A) => B, bc: (b: B) => C): (a: A) => C;
function pipe<A, B, C, D>(ab: (a: A) => B, bc: (b: B) => C, cd: (c: C) => D): (a: A) => D;
function pipe(...fns: Function[]) {
  return (input: any) => fns.reduce((acc, fn) => fn(acc), input);
}
const processNumber = pipe(
  (n: number) => n * 2,
  (n: number) => n + 10,
  (n: number) => `Result: ${n}`
);
// IO: processNumber(5) => "Result: 20"

// ============================================================================
// SECTION 10: ASYNC FUNCTIONS
// ============================================================================

// Async function returns Promise<T>
async function fetchUser(id: number): Promise<{ id: number; name: string }> {
  // Simulated API call
  return { id, name: "Alice" };
}

// Async generic function
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

// ============================================================================
// SECTION 11: TYPE NARROWING IN FUNCTIONS
// ============================================================================
// Functions can narrow types using type predicates and assertion functions.

// Type predicate: returns a boolean that narrows the type
function isNonNullable<T>(value: T | null | undefined): value is T {
  return value !== null && value !== undefined;
}

const values: (string | null)[] = ["a", null, "b", null, "c"];
const nonNull = values.filter(isNonNullable);
// nonNull: string[] => ["a", "b", "c"]

// Assertion function: throws if condition is not met
function assertDefined<T>(value: T | null | undefined, name: string): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(`Expected ${name} to be defined`);
  }
}

function processMaybeNull(input: string | null): string {
  assertDefined(input, "input");
  // After assertion, TS knows input is string
  return input.toUpperCase();
}

// ============================================================================
// MINI-EXERCISES
// ============================================================================
// 1. Write a generic function `chunk<T>(arr: T[], size: number): T[][]`
//    that splits an array into chunks of the given size.
//
// 2. Implement a generic `memoize<TArgs, TResult>` function that caches
//    results of a pure function based on its arguments.
//
// 3. Create function overloads for a `format` function that accepts
//    (Date) => string and (number, string) => string (number as timestamp, format string).
//
// 4. Write a curried `debounce<T extends (...args: any[]) => any>`
//    function that delays execution.

// ============================================================================
// KEY TAKEAWAYS
// ============================================================================
// 1. TypeScript functions support full type annotations on params and return.
// 2. Generics <T> enable type-safe reusable code across different types.
// 3. Function overloads handle multiple call signatures with one implementation.
// 4. Arrow functions lexically bind "this" and are ideal for callbacks.
// 5. Higher-order functions and currying enable powerful composition patterns.
// 6. Type predicates (value is T) and assertion functions (asserts value is T)
//    let functions narrow types for callers.
// 7. async functions return Promise<T> -- the generic T captures the resolved type.
// 8. Generic constraints (K extends keyof T) restrict type parameters to valid values.

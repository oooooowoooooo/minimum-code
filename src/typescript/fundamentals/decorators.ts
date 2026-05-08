/**
 * Atom 06: Decorators & Metaprogramming
 * ======================================
 * Class, method, parameter decorators and reflect-metadata.
 *
 * Architecture: Decorators are a Stage 3 TC39 proposal (available in TS with
 * experimentalDecorators). They enable annotating and modifying classes, methods,
 * properties, and parameters at definition time. Think of them as "wrappers"
 * that add behavior (logging, validation, caching, auth) declaratively.
 *
 * Transferability: Python decorators (@decorator) are nearly identical in concept.
 * Both are higher-order functions that wrap the decorated target. Python's
 * functools.wraps preserves metadata; TypeScript uses reflect-metadata.
 *
 * Application: NestJS (dependency injection, routing, guards), Angular (components,
 * injection), TypeORM (entity definitions), class-validator, MobX.
 */

// ============================================================================
// SECTION 1: DECORATOR FUNDAMENTALS
// ============================================================================
// A decorator is a function that receives the decorated target and can modify it.
// They are applied at CLASS DEFINITION TIME, not at runtime method calls.

// ============================================================================
// SECTION 2: CLASS DECORATORS
// ============================================================================
// Receives the class constructor as the only argument.

// Simple class decorator: adds a timestamp
function Timestamped<T extends new (...args: any[]) => {}>(constructor: T) {
  return class extends constructor {
    createdAt = new Date();
    decoratedAt = new Date().toISOString();
  };
}

@Timestamped
class Model {
  constructor(public name: string) {}
}

// const m = new Model("test");
// console.log(m.createdAt); // Date object
// console.log((m as any).decoratedAt); // ISO string

// Class decorator factory (parameterized decorator)
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

@Entity("users")
class UserEntity {
  constructor(public name: string, public email: string) {}
}

// (UserEntity as any).tableName => "users"
// (UserEntity as any).find() => "SELECT * FROM users"

// ============================================================================
// SECTION 3: METHOD DECORATORS
// ============================================================================
// Receives (target, propertyKey, descriptor).
// target: the prototype (instance methods) or constructor (static methods)
// propertyKey: the method name
// propertyDescriptor: the PropertyDescriptor (value, writable, enumerable, configurable)

// Logging decorator: logs method calls and results
function Log(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;

  descriptor.value = function (...args: any[]) {
    console.log(`Calling ${propertyKey} with args:`, args);
    const result = originalMethod.apply(this, args);
    console.log(`${propertyKey} returned:`, result);
    return result;
  };

  return descriptor;
}

class Calculator {
  @Log
  add(a: number, b: number): number {
    return a + b;
  }

  @Log
  multiply(a: number, b: number): number {
    return a * a * b;
  }
}

// const calc = new Calculator();
// calc.add(2, 3);
// Output: Calling add with args: [2, 3]
// Output: add returned: 5

// ============================================================================
// SECTION 4: METHOD DECORATOR FACTORIES
// ============================================================================

// Timing decorator: measures execution time
function Timed(label?: string) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;
    const name = label ?? propertyKey;

    descriptor.value = function (...args: any[]) {
      const start = performance.now();
      const result = originalMethod.apply(this, args);
      const end = performance.now();
      console.log(`[${name}] took ${(end - start).toFixed(2)}ms`);
      return result;
    };

    return descriptor;
  };
}

// Memoization decorator: caches results based on arguments
function Memoize(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;
  const cache = new Map<string, any>();

  descriptor.value = function (...args: any[]) {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key);
    }
    const result = originalMethod.apply(this, args);
    cache.set(key, result);
    return result;
  };

  return descriptor;
}

// Retry decorator: retries on failure
function Retry(maxAttempts: number = 3) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;

    descriptor.value = async function (...args: any[]) {
      let lastError: Error | undefined;
      for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        try {
          return await originalMethod.apply(this, args);
        } catch (error) {
          lastError = error as Error;
          console.warn(`Attempt ${attempt}/${maxAttempts} failed for ${propertyKey}`);
        }
      }
      throw lastError;
    };

    return descriptor;
  };
}

// ============================================================================
// SECTION 5: PROPERTY DECORATORS
// ============================================================================
// Receives (target, propertyKey). Cannot modify the property descriptor directly.
// Used for metadata registration.

function Required(target: any, propertyKey: string) {
  // Store metadata about required fields
  const existingRequired: string[] =
    Reflect.getOwnMetadata("required", target) || [];
  existingRequired.push(propertyKey);
  Reflect.defineMetadata("required", existingRequired, target);
}

function Range(min: number, max: number) {
  return function (target: any, propertyKey: string) {
    Reflect.defineMetadata(
      "range",
      { min, max },
      target,
      propertyKey
    );
  };
}

class Product {
  @Required
  name!: string;

  @Required
  @Range(0, 10000)
  price!: number;

  description?: string;
}

// ============================================================================
// SECTION 6: PARAMETER DECORATORS
// ============================================================================
// Receives (target, propertyKey, parameterIndex).
// parameterIndex: the ordinal index of the parameter (0-based).

function Validate(target: any, propertyKey: string, parameterIndex: number) {
  const existingValidators: number[] =
    Reflect.getOwnMetadata("validators", target, propertyKey) || [];
  existingValidators.push(parameterIndex);
  Reflect.defineMetadata("validators", existingValidators, target, propertyKey);
}

function NotNull(target: any, propertyKey: string, parameterIndex: number) {
  const existingNotNull: number[] =
    Reflect.getOwnMetadata("notNull", target, propertyKey) || [];
  existingNotNull.push(parameterIndex);
  Reflect.defineMetadata("notNull", existingNotNull, target, propertyKey);
}

class UserService {
  createUser(@Validate @NotNull name: string, @NotNull email: string): void {
    // Validation metadata is registered by the decorators
  }
}

// ============================================================================
// SECTION 7: REFLECT-METADATA
// ============================================================================
// The reflect-metadata polyfill enables runtime metadata storage and retrieval.
// Install: npm install reflect-metadata
// Import once at entry point: import "reflect-metadata";

// Define and get metadata
// Reflect.defineMetadata(key, value, target);
// Reflect.defineMetadata(key, value, target, propertyKey);
// const value = Reflect.getMetadata(key, target);
// const value = Reflect.getMetadata(key, target, propertyKey);

// Metadata design types (automatic with "emitDecoratorMetadata": true)
// Reflect.getMetadata("design:type", target, propertyKey) => Property type
// Reflect.getMetadata("design:paramtypes", target, propertyKey) => Parameter types
// Reflect.getMetadata("design:returntype", target, propertyKey) => Return type

// Example: automatic type-based dependency injection
function Injectable() {
  return function <T extends new (...args: any[]) => {}>(constructor: T) {
    // Store the constructor in a service registry
    ServiceRegistry.register(constructor);
  };
}

class ServiceRegistry {
  private static services = new Map<any, any>();

  static register(constructor: any) {
    this.services.set(constructor, constructor);
  }

  static resolve<T>(constructor: new (...args: any[]) => T): T {
    const service = this.services.get(constructor);
    if (!service) {
      throw new Error(`Service ${constructor.name} not registered`);
    }
    // Get parameter types for auto-injection
    const paramTypes: any[] =
      Reflect.getMetadata("design:paramtypes", constructor) || [];
    const params = paramTypes.map((param) => this.resolve(param));
    return new constructor(...params);
  }
}

// @Injectable()
// class LoggerService {
//   log(message: string) { console.log(message); }
// }
//
// @Injectable()
// class UserService {
//   constructor(private logger: LoggerService) {}
//   createUser(name: string) { this.logger.log(`Created ${name}`); }
// }
//
// const userService = ServiceRegistry.resolve(UserService);

// ============================================================================
// SECTION 8: DECORATOR COMPOSITION AND EXECUTION ORDER
// ============================================================================
// Multiple decorators on a single target are applied BOTTOM-UP.

function First(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
  console.log("First decorator applied");
  return descriptor;
}

function Second(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
  console.log("Second decorator applied");
  return descriptor;
}

class Example {
  // Execution order: Second first, then First
  @First
  @Second
  method() {}
}
// Output: "Second decorator applied", then "First decorator applied"

// At call time, First wraps Second wraps the original method.
// So execution goes: First -> Second -> method

// ============================================================================
// SECTION 9: PRACTICAL DECORATOR PATTERNS
// ============================================================================

// Pattern 1: Rate limiting
function RateLimit(callsPerMinute: number) {
  const timestamps: number[] = [];

  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;

    descriptor.value = function (...args: any[]) {
      const now = Date.now();
      const windowStart = now - 60000;

      // Remove old timestamps
      while (timestamps.length > 0 && timestamps[0] < windowStart) {
        timestamps.shift();
      }

      if (timestamps.length >= callsPerMinute) {
        throw new Error(`Rate limit exceeded for ${propertyKey}`);
      }

      timestamps.push(now);
      return originalMethod.apply(this, args);
    };

    return descriptor;
  };
}

// Pattern 2: Debounce
function Debounce(ms: number) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;
    let timeoutId: ReturnType<typeof setTimeout>;

    descriptor.value = function (...args: any[]) {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        originalMethod.apply(this, args);
      }, ms);
    };

    return descriptor;
  };
}

// Pattern 3: Access control
function Authorized(role: string) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;

    descriptor.value = function (...args: any[]) {
      const currentUser = (this as any).currentUser;
      if (!currentUser || currentUser.role !== role) {
        throw new Error(`Unauthorized: requires role "${role}"`);
      }
      return originalMethod.apply(this, args);
    };

    return descriptor;
  };
}

// ============================================================================
// SECTION 10: LEGACY VS MODERN DECORATORS
// ============================================================================
// TypeScript supports two decorator standards:
//
// 1. Legacy (experimentalDecorators: true)
//    - Stage 2 TC39 proposal
//    - Used by NestJS, Angular, TypeORM
//    - Decorators receive (target, key, descriptor)
//
// 2. Modern (no experimentalDecorators flag in TS 5.0+)
//    - Stage 3 TC39 proposal
//    - Different signature: (value, context) => new value
//    - context has kind, name, static, private, access, addInitializer
//
// Modern decorator example:
// function logged(value, context) {
//   if (context.kind === "method") {
//     return function (...args) {
//       console.log(`Calling ${context.name}`);
//     };
//   }
// }

// ============================================================================
// MINI-EXERCISES
// ============================================================================
// 1. Write a @Sealed decorator that prevents a class from being extended.
//
// 2. Create a @Cache(ttl: number) method decorator that caches return values
//    for the specified duration (in milliseconds).
//
// 3. Implement a @ValidateArgs method decorator that checks parameter types
//    at runtime using reflect-metadata "design:paramtypes".
//
// 4. Build a @Singleton class decorator that ensures only one instance exists.

// ============================================================================
// KEY TAKEAWAYS
// ============================================================================
// 1. Decorators are higher-order functions applied at class definition time.
// 2. Class, method, property, and parameter decorators each have different signatures.
// 3. Decorator factories (functions returning decorators) enable parameterization.
// 4. Decorators compose bottom-up: @A @B method => B wraps A wraps method.
// 5. reflect-metadata enables runtime metadata storage and retrieval.
// 6. "emitDecoratorMetadata" auto-emits design:type, design:paramtypes, design:returntype.
// 7. NestJS, Angular, TypeORM all rely heavily on decorators for DI, routing, and ORM.
// 8. Modern decorators (Stage 3) differ from legacy -- choose based on your framework.

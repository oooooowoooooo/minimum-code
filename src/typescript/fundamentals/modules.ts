/**
 * Atom 05: Module System
 * ======================
 * ES Modules, CommonJS, import/export patterns, and module resolution.
 *
 * Architecture: TypeScript supports two module systems -- ES Modules (standard)
 * and CommonJS (Node.js legacy). Understanding both is critical because Node.js
 * still uses CJS under the hood for many packages. TypeScript compiles ES module
 * syntax to the target module system configured in tsconfig.json.
 *
 * Transferability: Python's import system is similar in concept -- modules are
 * files, packages are directories. Python's __init__.py parallels barrel files.
 * Python's importlib parallels dynamic import().
 *
 * Application: Every TypeScript project. Library authoring, monorepos, micro-frontends,
 * code splitting, lazy loading, plugin systems.
 */

// ============================================================================
// SECTION 1: ES MODULE BASICS
// ============================================================================
// ES Modules are the standard module system. Each file is a module.

// Named exports: export individual items
export const API_VERSION = "v1";
export const MAX_RETRIES = 3;

export function formatEndpoint(path: string): string {
  return `${API_VERSION}/${path}`;
}

export class HttpClient {
  constructor(private baseUrl: string) {}

  async get(path: string): Promise<string> {
    return `${this.baseUrl}/${formatEndpoint(path)}`;
  }
}

// Type exports
export interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
}

export type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";

// Re-exports: forward exports from other modules
// export { User } from "./types.js";
// export * from "./utils.js";
// export { default as MyComponent } from "./MyComponent.js";

// ============================================================================
// SECTION 2: DEFAULT EXPORTS
// ============================================================================
// A module can have ONE default export. Importers choose the name.

// Default class export (most common pattern)
class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  async request<T>(method: HttpMethod, path: string): Promise<ApiResponse<T>> {
    return { data: {} as T, status: 200, message: "OK" };
  }
}

export default ApiClient;

// Default function export
export default function createClient(baseUrl: string): ApiClient {
  return new ApiClient(baseUrl);
}

// Note: a file can have EITHER a default export or named exports, or both.
// But having two default exports (class + function above) is only for demonstration.
// In practice, pick one per file.

// ============================================================================
// SECTION 3: IMPORT PATTERNS
// ============================================================================

// Named imports
// import { API_VERSION, HttpClient, ApiResponse } from "./api.js";

// Import with alias
// import { HttpClient as Client } from "./api.js";

// Default import
// import ApiClient from "./api.js";

// Default + named in one statement
// import ApiClient, { API_VERSION, HttpClient } from "./api.js";

// Namespace import: import everything as an object
// import * as Api from "./api.js";
// Api.API_VERSION, Api.HttpClient, etc.

// Side-effect import: execute module without importing bindings
// import "./polyfills.js";

// Type-only import: erased at compile time, no runtime cost
// import type { ApiResponse, HttpMethod } from "./api.js";
// import { type ApiResponse, HttpClient } from "./api.js"; // mixed

// ============================================================================
// SECTION 4: DYNAMIC IMPORT
// ============================================================================
// Load modules on demand at runtime. Returns a Promise.

// Dynamic import for code splitting
async function loadChartLibrary() {
  const chartModule = await import("./chart-library.js");
  return chartModule.Chart;
}

// Conditional loading
async function loadModule(condition: boolean) {
  if (condition) {
    const { FeatureA } = await import("./feature-a.js");
    return FeatureA;
  }
  const { FeatureB } = await import("./feature-b.js");
  return FeatureB;
}

// Lazy initialization pattern
let cachedModule: typeof import("./expensive-module.js") | null = null;

async function getExpensiveModule() {
  if (!cachedModule) {
    cachedModule = await import("./expensive-module.js");
  }
  return cachedModule;
}

// ============================================================================
// SECTION 5: MODULE RESOLUTION
// ============================================================================
// How TypeScript finds imported modules. Controlled by tsconfig.json "moduleResolution".

// Classic resolution (legacy):
//   import "./foo" => looks for foo.ts, foo.d.ts

// Node resolution (most common):
//   import "./foo" => looks for:
//     1. ./foo.ts, ./foo.tsx
//     2. ./foo/index.ts, ./foo/index.tsx
//     3. ./foo/package.json (main field)
//     4. node_modules/foo/...

// Bundler resolution (modern, TS 5.0+):
//   Same as Node but also checks "exports" field in package.json

// Path mapping (tsconfig.json):
// {
//   "compilerOptions": {
//     "paths": {
//       "@utils/*": ["./src/utils/*"],
//       "@components/*": ["./src/components/*"]
//     }
//   }
// }
// import { formatDate } from "@utils/date.js";

// ============================================================================
// SECTION 6: BARREL FILES (INDEX FILES)
// ============================================================================
// A barrel file re-exports everything from a directory, providing a clean API.

// src/utils/index.ts (barrel file)
// export { formatDate, parseDate } from "./date.js";
// export { slugify, capitalize } from "./string.js";
// export { debounce, throttle } from "./timing.js";
// export type { DateOptions, StringOptions } from "./types.js";

// Consumers import from the barrel
// import { formatDate, slugify, debounce } from "./utils/index.js";
// or simply: import { formatDate, slugify, debounce } from "./utils.js";

// Pros: clean imports, encapsulates internal structure
// Cons: can increase bundle size if not using tree-shaking

// ============================================================================
// SECTION 7: COMMONJS INTEROP
// ============================================================================
// Node.js traditionally uses CommonJS (require/module.exports).
// TypeScript can compile to CJS or consume CJS modules.

// Consuming CJS from ESM (TypeScript)
// import express from "express"; // default import for CJS default export
// import { Router } from "express"; // named import for CJS named exports

// TypeScript's __esModule interop
// When a CJS module sets __esModule: true, TypeScript uses the .default property
// This is controlled by "esModuleInterop" in tsconfig.json

// Type declarations for CJS modules without types
// declare module "legacy-package" {
//   export function doSomething(x: string): number;
//   export const version: string;
// }

// ============================================================================
// SECTION 8: MODULE AUGMENTATION
// ============================================================================
// Extend existing modules with new declarations. Used for plugin systems.

// Augment the Express module
// declare module "express" {
//   interface Request {
//     userId?: string;
//     sessionId?: string;
//   }
// }
// Now req.userId is valid TypeScript

// Augment your own modules
// In file: augmentation.ts
// declare module "./api.js" {
//   interface HttpClient {
//     uploadFile(file: File): Promise<string>;
//   }
// }

// ============================================================================
// SECTION 9: GLOBAL DECLARATIONS (AMBIENT MODULES)
// ============================================================================
// Declare types for modules that don't have TypeScript definitions.

// Declare a module with no type information
// declare module "some-untyped-library" {
//   const value: any;
//   export default value;
// }

// Declare a module with full types
// declare module "image-resizer" {
//   interface ResizeOptions {
//     width: number;
//     height: number;
//     quality?: number;
//   }
//   export function resize(path: string, options: ResizeOptions): Promise<Buffer>;
//   export const version: string;
// }

// Wildcard module declaration (for file imports)
// declare module "*.css" {
//   const classes: Record<string, string>;
//   export default classes;
// }
// declare module "*.png" {
//   const url: string;
//   export default url;
// }

// ============================================================================
// SECTION 10: IMPORT ASSERTIONS / ATTRIBUTES
// ============================================================================
// TypeScript 5.0+ supports import assertions for non-JS imports.

// JSON imports with import assertions
// import config from "./config.json" assert { type: "json" };

// Import attributes (newer syntax, TS 5.3+)
// import config from "./config.json" with { type: "json" };

// In tsconfig.json, enable:
// "resolveJsonModule": true, "esModuleInterop": true

// ============================================================================
// SECTION 11: PRACTICAL MODULE PATTERNS
// ============================================================================

// Pattern 1: Facade module (simplify complex APIs)
// export class Database {
//   private connection: any;
//   async connect(): Promise<void> { /* ... */ }
//   async query<T>(sql: string): Promise<T[]> { /* ... */ }
//   async close(): Promise<void> { /* ... */ }
// }
// export function createDatabase(url: string): Database { return new Database(); }

// Pattern 2: Singleton module
// const instance = new Service();
// export default instance;

// Pattern 3: Conditional exports (dual CJS/ESM package)
// package.json:
// {
//   "exports": {
//     ".": {
//       "import": "./dist/index.mjs",
//       "require": "./dist/index.cjs"
//     }
//   }
// }

// Pattern 4: Type-only barrel (zero runtime cost)
// types/index.ts
// export type { User, Product, Order } from "./models.js";
// export type { ApiResponse, PaginatedResponse } from "./api.js";

// ============================================================================
// MINI-EXERCISES
// ============================================================================
// 1. Create a barrel file that re-exports utilities from 3 sub-modules,
//    ensuring no circular dependencies.
//
// 2. Write a module augmentation that adds a `validate()` method to
//    the Express Request object.
//
// 3. Implement a lazy-loading pattern using dynamic import() for a
//    heavy library (e.g., chart.js).
//
// 4. Create ambient module declarations for a CSS module and an image module.

// ============================================================================
// KEY TAKEAWAYS
// ============================================================================
// 1. ES Modules are the standard; use named exports for tree-shaking.
// 2. Default exports are one per file; named exports are unlimited.
// 3. Dynamic import() enables code splitting and lazy loading.
// 4. Module resolution strategies (Node, Bundler, Classic) control how imports are found.
// 5. Barrel files provide clean APIs but may affect bundle size.
// 6. Module augmentation extends existing modules without modifying them.
// 7. "import type" is erased at compile time -- zero runtime cost.
// 8. CommonJS interop requires "esModuleInterop": true in tsconfig.json.

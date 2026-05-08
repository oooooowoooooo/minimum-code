/**
 * Tests for Atom 05: Module System
 * =================================
 * Tests for import/export patterns, module resolution, and barrel files.
 * Note: Full module system tests require actual file system setup and
 * compilation. These tests validate the runtime behavior of exported values.
 */

import { describe, it, expect } from "vitest";

// ============================================================================
// SIMULATED MODULE EXPORTS (inline for test purposes)
// ============================================================================

// In a real project these would be separate files imported via ES modules.
// Here we define them inline to test the patterns in isolation.

// Named exports
const API_VERSION = "v1";
const MAX_RETRIES = 3;

function formatEndpoint(path: string): string {
  return `${API_VERSION}/${path}`;
}

interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
}

type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";

// Default export
class ApiClient {
  constructor(private baseUrl: string) {}

  async request<T>(method: HttpMethod, path: string): Promise<ApiResponse<T>> {
    return {
      data: {} as T,
      status: 200,
      message: "OK",
    };
  }
}

// ============================================================================
// NAMED EXPORTS
// ============================================================================

describe("Named Exports", () => {
  it("exported constants have correct values", () => {
    expect(API_VERSION).toBe("v1");
    expect(MAX_RETRIES).toBe(3);
  });

  it("exported functions work correctly", () => {
    expect(formatEndpoint("users")).toBe("v1/users");
    expect(formatEndpoint("products/1")).toBe("v1/products/1");
  });
});

// ============================================================================
// DEFAULT EXPORTS
// ============================================================================

describe("Default Exports", () => {
  it("default class export works", async () => {
    const client = new ApiClient("https://api.example.com");
    const response = await client.request("GET", "/users");
    expect(response.status).toBe(200);
    expect(response.message).toBe("OK");
  });
});

// ============================================================================
// RE-EXPORTS AND BARREL FILES
// ============================================================================

describe("Re-exports and Barrel Files", () => {
  // Simulate barrel file behavior
  // src/utils/date.ts
  function formatDate(date: Date): string {
    return date.toISOString().split("T")[0];
  }

  function parseDate(str: string): Date {
    return new Date(str);
  }

  // src/utils/string.ts
  function slugify(text: string): string {
    return text.toLowerCase().replace(/\s+/g, "-");
  }

  function capitalize(text: string): string {
    return text.charAt(0).toUpperCase() + text.slice(1);
  }

  // Barrel: src/utils/index.ts
  const utils = { formatDate, parseDate, slugify, capitalize };

  it("barrel provides unified access", () => {
    expect(utils.formatDate(new Date("2024-06-15"))).toBe("2024-06-15");
    expect(utils.slugify("Hello World")).toBe("hello-world");
    expect(utils.capitalize("hello")).toBe("Hello");
  });

  it("barrel preserves function behavior", () => {
    const date = utils.parseDate("2024-01-01");
    expect(date.getFullYear()).toBe(2024);
  });
});

// ============================================================================
// NAMESPACE IMPORTS
// ============================================================================

describe("Namespace Imports", () => {
  it("namespace object contains all exports", () => {
    // Simulate: import * as Api from "./api.js"
    const Api = {
      API_VERSION,
      MAX_RETRIES,
      formatEndpoint,
      ApiClient,
    };

    expect(Api.API_VERSION).toBe("v1");
    expect(Api.MAX_RETRIES).toBe(3);
    expect(Api.formatEndpoint("test")).toBe("v1/test");
  });
});

// ============================================================================
// DYNAMIC IMPORT
// ============================================================================

describe("Dynamic Import", () => {
  it("dynamic import returns module", async () => {
    // Simulate dynamic import behavior
    async function loadModule() {
      return {
        greet: (name: string) => `Hello, ${name}!`,
        version: "1.0.0",
      };
    }

    const mod = await loadModule();
    expect(mod.greet("Alice")).toBe("Hello, Alice!");
    expect(mod.version).toBe("1.0.0");
  });

  it("lazy loading pattern", async () => {
    let loadCount = 0;

    async function loadExpensiveModule() {
      loadCount++;
      return {
        compute: (x: number) => x * 2,
      };
    }

    // Simulate lazy module cache
    let cached: { compute: (x: number) => number } | null = null;

    async function getModule() {
      if (!cached) {
        cached = await loadExpensiveModule();
      }
      return cached;
    }

    const mod1 = await getModule();
    const mod2 = await getModule();

    expect(mod1.compute(5)).toBe(10);
    expect(mod2.compute(10)).toBe(20);
    expect(loadCount).toBe(1); // loaded only once
  });
});

// ============================================================================
// TYPE-ONLY IMPORTS
// ============================================================================

describe("Type-only Imports", () => {
  it("interfaces can be used for type checking", () => {
    // In real code: import type { ApiResponse } from "./api.js"
    // Type-only imports are erased at compile time, so nothing to test at runtime.
    // This test validates the type is usable.

    const response: ApiResponse<string> = {
      data: "test",
      status: 200,
      message: "OK",
    };

    expect(response.data).toBe("test");
    expect(response.status).toBe(200);
  });
});

// ============================================================================
// MODULE AUGMENTATION (CONCEPTUAL)
// ============================================================================

describe("Module Augmentation", () => {
  it("extending objects with new properties", () => {
    // Module augmentation adds properties to existing interfaces.
    // At runtime, this is just adding properties to objects.

    interface Request {
      body: string;
    }

    // Augmented interface (in real code, this is in a separate .d.ts file)
    interface AugmentedRequest extends Request {
      userId?: string;
      sessionId?: string;
    }

    const req: AugmentedRequest = {
      body: '{"data": 1}',
      userId: "user-123",
      sessionId: "sess-456",
    };

    expect(req.body).toBe('{"data": 1}');
    expect(req.userId).toBe("user-123");
    expect(req.sessionId).toBe("sess-456");
  });
});

// ============================================================================
// AMBIENT MODULE DECLARATIONS (CONCEPTUAL)
// ============================================================================

describe("Ambient Module Declarations", () => {
  it("type declarations for untyped modules", () => {
    // In real code: declare module "some-lib" { ... }
    // These provide types for JS libraries without TypeScript support.

    // Simulate: declare module "image-resizer"
    interface ResizeOptions {
      width: number;
      height: number;
      quality?: number;
    }

    function resize(path: string, options: ResizeOptions): string {
      return `Resized ${path} to ${options.width}x${options.height}`;
    }

    expect(resize("photo.jpg", { width: 100, height: 100 })).toBe(
      "Resized photo.jpg to 100x100"
    );
  });

  it("wildcard module declarations for file imports", () => {
    // In real code: declare module "*.css" { const classes: Record<string, string>; export default classes; }
    const cssClasses: Record<string, string> = {
      container: "container_abc123",
      button: "button_def456",
    };

    expect(cssClasses.container).toBe("container_abc123");
    expect(cssClasses.button).toBe("button_def456");
  });
});

// ============================================================================
// CIRCULAR DEPENDENCY PREVENTION
// ============================================================================

describe("Circular Dependency Prevention", () => {
  it("shared dependency pattern", () => {
    // Instead of: A imports B, B imports A (circular)
    // Use: A and B both import from C (shared)

    // C: shared types
    interface SharedConfig {
      apiUrl: string;
      timeout: number;
    }

    // A uses C
    function createClient(config: SharedConfig) {
      return { baseUrl: config.apiUrl };
    }

    // B uses C
    function createLogger(config: SharedConfig) {
      return { level: config.timeout > 5000 ? "verbose" : "normal" };
    }

    const config: SharedConfig = { apiUrl: "https://api.test.com", timeout: 3000 };
    expect(createClient(config).baseUrl).toBe("https://api.test.com");
    expect(createLogger(config).level).toBe("normal");
  });
});

// ============================================================================
// CONDITIONAL EXPORTS
// ============================================================================

describe("Conditional Exports", () => {
  it("dual module format pattern", () => {
    // package.json exports field:
    // { "exports": { ".": { "import": "./index.mjs", "require": "./index.cjs" } } }
    // Both files export the same API

    function createService(source: string) {
      return {
        getData: () => `Data from ${source}`,
        version: "1.0.0",
      };
    }

    const esmService = createService("esm");
    const cjsService = createService("cjs");

    expect(esmService.getData()).toBe("Data from esm");
    expect(cjsService.getData()).toBe("Data from cjs");
    expect(esmService.version).toBe(cjsService.version);
  });
});

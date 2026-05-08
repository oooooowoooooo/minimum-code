/**
 * Next.js — Atomic Code Dissection
 * =================================
 * Simplified but accurate implementations of Next.js core patterns.
 * Each section demonstrates one architectural concept.
 *
 * Run: npx tsx dissect.ts
 */

// ============================================================================
// SECTION 1: FILE-BASED ROUTING
// ============================================================================
// How Next.js maps file paths to URL routes

interface RouteDefinition {
  path: string;
  component: string;
  params: Record<string, string>;
}

class FileRouter {
  private routes: Map<string, RouteDefinition> = new Map();

  /**
   * Register a route from a file path.
   * app/blog/[slug]/page.tsx → /blog/:slug
   */
  register(filePath: string, component: string): void {
    const routePath = this.filePathToRoutePath(filePath);
    this.routes.set(routePath, { path: routePath, component, params: {} });
  }

  /**
   * Convert file system path to URL path.
   * Handles: [param], [...rest], [[...optional]]
   */
  private filePathToRoutePath(filePath: string): string {
    return filePath
      .replace(/\/page\.tsx$/, '')        // remove page.tsx
      .replace(/\/layout\.tsx$/, '')       // remove layout.tsx
      .replace(/\/\[(\w+)\]/g, '/:$1')    // [id] → :id
      .replace(/\/\[\[\.\.\.(\w+)\]\]/g, '/:$1*')  // [[...rest]] → :rest*
      .replace(/\/\[\.\.\.(\w+)\]/g, '/:$1+')      // [...rest] → :rest+
      || '/';
  }

  /**
   * Match a URL path to a registered route.
   * Returns the route definition with extracted params.
   */
  match(urlPath: string): RouteDefinition | null {
    for (const [pattern, route] of this.routes) {
      const params = this.matchPattern(pattern, urlPath);
      if (params !== null) {
        return { ...route, params };
      }
    }
    return null;
  }

  private matchPattern(pattern: string, path: string): Record<string, string> | null {
    const patternParts = pattern.split('/').filter(Boolean);
    const pathParts = path.split('/').filter(Boolean);

    if (patternParts.length !== pathParts.length) return null;

    const params: Record<string, string> = {};
    for (let i = 0; i < patternParts.length; i++) {
      const part = patternParts[i];
      if (part.startsWith(':')) {
        params[part.slice(1)] = pathParts[i];
      } else if (part !== pathParts[i]) {
        return null;
      }
    }
    return params;
  }
}

// Test
const router = new FileRouter();
router.register('app/page.tsx', 'HomePage');
router.register('app/blog/[slug]/page.tsx', 'BlogPost');
router.register('app/users/[id]/page.tsx', 'UserProfile');

console.log('=== File-Based Routing ===');
console.log(router.match('/'));                // { path: '/', component: 'HomePage', params: {} }
console.log(router.match('/blog/hello-world')); // { params: { slug: 'hello-world' } }
console.log(router.match('/users/42'));         // { params: { id: '42' } }
console.log(router.match('/nonexistent'));      // null


// ============================================================================
// SECTION 2: SERVER/CLIENT COMPONENT BOUNDARY
// ============================================================================
// How Next.js decides what runs on server vs client

type ComponentType = 'server' | 'client';

interface ComponentMeta {
  name: string;
  type: ComponentType;
  imports: string[];
}

class ComponentRegistry {
  private components: Map<string, ComponentMeta> = new Map();

  /**
   * Register a component. Type is inferred from "use client" directive.
   */
  register(name: string, source: string, imports: string[] = []): void {
    const type: ComponentType = source.startsWith('"use client"') ? 'client' : 'server';
    this.components.set(name, { name, type, imports });
  }

  /**
   * Validate the import boundary.
   * Rule: Client components cannot import server components.
   */
  validate(): string[] {
    const errors: string[] = [];
    for (const [name, meta] of this.components) {
      if (meta.type === 'client') {
        for (const importName of meta.imports) {
          const imported = this.components.get(importName);
          if (imported?.type === 'server') {
            errors.push(
              `VIOLATION: Client component "${name}" imports server component "${importName}"`
            );
          }
        }
      }
    }
    return errors;
  }
}

// Test
console.log('\n=== Server/Client Boundary ===');
const registry = new ComponentRegistry();
registry.register('UserList', '"use client"', ['UserCard']);
registry.register('UserCard', '"use client"', []);
registry.register('Dashboard', '', ['UserList']);      // server imports client = OK
registry.register('Sidebar', '"use client"', ['Dashboard']); // client imports server = VIOLATION

const errors = registry.validate();
console.log('Boundary violations:', errors.length > 0 ? errors : 'None');


// ============================================================================
// SECTION 3: MIDDLEWARE CHAIN
// ============================================================================
// How Next.js middleware intercepts and modifies requests

type MiddlewareFn = (
  request: Request,
  next: () => Response
) => Response | Promise<Response>;

class MiddlewareChain {
  private middlewares: MiddlewareFn[] = [];

  use(middleware: MiddlewareFn): this {
    this.middlewares.push(middleware);
    return this;
  }

  /**
   * Execute the middleware chain.
   * Each middleware can modify the request/response or short-circuit.
   */
  async execute(request: Request, handler: () => Response): Promise<Response> {
    let index = 0;

    const next = (): Response => {
      if (index >= this.middlewares.length) {
        return handler();
      }
      const middleware = this.middlewares[index++];
      return middleware(request, next);
    };

    return next();
  }
}

// Test
console.log('\n=== Middleware Chain ===');
const chain = new MiddlewareChain();

// Middleware 1: Add request ID
chain.use((req, next) => {
  const headers = new Headers(req.headers);
  headers.set('x-request-id', 'req-123');
  const response = next();
  response.headers.set('x-request-id', 'req-123');
  return response;
});

// Middleware 2: Auth check
chain.use((req, next) => {
  const token = req.headers.get('authorization');
  if (!token) {
    return new Response('Unauthorized', { status: 401 });
  }
  return next();
});

// Middleware 3: Logging
chain.use((req, next) => {
  console.log(`  [LOG] ${req.method} ${new URL(req.url).pathname}`);
  return next();
});

// Test with auth
const authenticatedReq = new Request('http://localhost/api/users', {
  method: 'GET',
  headers: { authorization: 'Bearer token123' },
});

chain.execute(authenticatedReq, () => new Response('OK')).then(res => {
  console.log('Authenticated:', res.status, res.statusText);
});

// Test without auth
const unauthenticatedReq = new Request('http://localhost/api/users', {
  method: 'GET',
});

chain.execute(unauthenticatedReq, () => new Response('OK')).then(res => {
  console.log('Unauthenticated:', res.status, res.statusText);
});


// ============================================================================
// SECTION 4: LAYOUT NESTING
// ============================================================================
// How layouts compose and share data

interface LayoutContext {
  params: Record<string, string>;
  parentData: Record<string, unknown>;
}

class LayoutComposer {
  private layouts: Map<string, (ctx: LayoutContext) => string> = new Map();

  register(path: string, renderer: (ctx: LayoutContext) => string): void {
    this.layouts.set(path, renderer);
  }

  /**
   * Compose layouts from root to leaf.
   * Each layout wraps its children.
   */
  compose(path: string, pageContent: string, params: Record<string, string> = {}): string {
    const layoutChain = this.getLayoutChain(path);
    let content = pageContent;

    for (const layoutPath of layoutChain.reverse()) {
      const renderer = this.layouts.get(layoutPath);
      if (renderer) {
        content = renderer({ params, parentData: {} });
        // In real Next.js, the layout renders {children} which is the next content
      }
    }

    return content;
  }

  private getLayoutChain(path: string): string[] {
    const parts = path.split('/').filter(Boolean);
    const chain: string[] = [''];  // root layout

    let current = '';
    for (const part of parts) {
      current += `/${part}`;
      if (this.layouts.has(current)) {
        chain.push(current);
      }
    }

    return chain;
  }
}

// Test
console.log('\n=== Layout Nesting ===');
const layouts = new LayoutComposer();
layouts.register('', (ctx) => `<html><body>{children}</body></html>`);
layouts.register('/dashboard', (ctx) => `<div class="sidebar">...</div><main>{children}</main>`);

console.log('Root page:', layouts.compose('/', '<h1>Home</h1>'));
console.log('Dashboard:', layouts.compose('/dashboard', '<h1>Dashboard</h1>'));


// ============================================================================
// SECTION 5: TYPE-SAFE ROUTE PARAMS
// ============================================================================
// How TypeScript enforces correct parameter usage

// Simulates Next.js's type inference for route params
type ExtractParams<T extends string> =
  T extends `${infer _Start}[${infer Param}]${infer Rest}`
    ? { [K in Param]: string } & ExtractParams<Rest>
    : {};

// Type-level test
type BlogParams = ExtractParams<'/blog/[slug]'>;
//   ^? { slug: string }

type UserPostParams = ExtractParams<'/users/[userId]/posts/[postId]'>;
//   ^? { userId: string; postId: string }

// Runtime simulation of type-safe params
function createTypedRoute<T extends string>(pattern: T) {
  return {
    match(url: string): ExtractParams<T> | null {
      const patternParts = pattern.split('/').filter(Boolean);
      const urlParts = url.split('/').filter(Boolean);

      if (patternParts.length !== urlParts.length) return null;

      const params: Record<string, string> = {};
      for (let i = 0; i < patternParts.length; i++) {
        const part = patternParts[i];
        if (part.startsWith('[') && part.endsWith(']')) {
          params[part.slice(1, -1)] = urlParts[i];
        } else if (part !== urlParts[i]) {
          return null;
        }
      }
      return params as ExtractParams<T>;
    }
  };
}

// Test
console.log('\n=== Type-Safe Route Params ===');
const blogRoute = createTypedRoute('/blog/[slug]');
console.log(blogRoute.match('/blog/hello-world'));  // { slug: 'hello-world' }
console.log(blogRoute.match('/blog'));               // null

const userPostRoute = createTypedRoute('/users/[userId]/posts/[postId]');
console.log(userPostRoute.match('/users/42/posts/7')); // { userId: '42', postId: '7' }


// ============================================================================
// SECTION 6: SERVER ACTIONS (SIMPLIFIED)
// ============================================================================
// How Next.js server actions enable mutations without API routes

class ServerActionRegistry {
  private actions: Map<string, (formData: FormData) => Promise<unknown>> = new Map();

  /**
   * Register a server action (like 'use server' directive).
   * The action runs on the server, called from client components.
   */
  register(
    name: string,
    handler: (formData: FormData) => Promise<unknown>
  ): void {
    this.actions.set(name, handler);
  }

  /**
   * Invoke a server action by name.
   * In real Next.js, this is an HTTP call from client to server.
   */
  async invoke(name: string, formData: FormData): Promise<unknown> {
    const action = this.actions.get(name);
    if (!action) {
      throw new Error(`Server action "${name}" not found`);
    }
    return action(formData);
  }
}

// Test
console.log('\n=== Server Actions ===');
const actions = new ServerActionRegistry();

actions.register('createUser', async (formData) => {
  const name = formData.get('name');
  const email = formData.get('email');
  // In real app: await db.user.create({ data: { name, email } });
  return { id: 1, name, email, created: true };
});

const form = new FormData();
form.set('name', 'Alice');
form.set('email', 'alice@example.com');

actions.invoke('createUser', form).then(result => {
  console.log('Server action result:', result);
});


// ============================================================================
// KEY TAKEAWAYS
// ============================================================================
/*
1. File-based routing maps filesystem to URL routes — zero configuration
2. Server/Client boundary controls what runs where — enforced by "use client" directive
3. Middleware chain intercepts requests before route handlers — for auth, logging, CORS
4. Layout nesting composes UI hierarchies — layouts persist across navigation
5. TypeScript types enforce framework contracts — params, metadata, props
6. Server actions enable mutations without API routes — type-safe from form to database
7. These patterns appear in every modern TypeScript framework — learn them once, use everywhere
*/

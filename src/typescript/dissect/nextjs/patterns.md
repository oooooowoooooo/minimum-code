# Next.js — Core Design Patterns

## Pattern 1: File-Based Routing

### What It Is
Instead of manually registering routes in a configuration file, the file system IS the router. Create a file at `app/users/page.tsx` and you have a `/users` route.

### Why It Works
- **Zero configuration** — no route table to maintain
- **Colocation** — route logic lives near its components
- **Discoverability** — look at the file tree, see all routes

### How It Works Internally
```
1. Build time: scan app/ directory for page.tsx files
2. Build a route tree from file paths
3. Map each route to its component chain (layout → loading → page)
4. At runtime: match incoming URL to route tree → render component chain
```

### TypeScript Angle
The framework infers route params from file names:
```typescript
// app/blog/[slug]/page.tsx
// TypeScript KNOWS that params.slug exists
export default function BlogPost({ params }: { params: { slug: string } }) {
  return <h1>{params.slug}</h1>;
}
```

---

## Pattern 2: Server/Client Component Boundary

### What It Is
Components are server-rendered by default (zero client JS). Add `"use client"` to opt into client-side interactivity.

### Why It Works
- **Performance** — server components send zero JavaScript to the client
- **Security** — server code never reaches the browser
- **Data access** — server components can directly query databases

### The Boundary Rule
```
Server Component ──can import──→ Server Component  ✓
Server Component ──can import──→ Client Component  ✓
Client Component ──can import──→ Client Component  ✓
Client Component ──can import──→ Server Component  ✗ (violation!)
```

### Why This Rule Exists
Client components run in the browser. They can't import server-side code (database connections, file system, env secrets).

---

## Pattern 3: Middleware Chain

### What It Is
Middleware runs before the route handler. It can modify the request, redirect, add headers, or short-circuit.

### Why It Works
- **Cross-cutting concerns** — auth, logging, CORS in one place
- **Edge-ready** — runs at the network edge for low latency
- **Composable** — multiple middleware functions chain together

### Real-World Usage
```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  // Auth check
  const token = request.cookies.get('auth-token');
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  // Add request ID for tracing
  const response = NextResponse.next();
  response.headers.set('x-request-id', crypto.randomUUID());
  return response;
}
```

---

## Pattern 4: Layout Nesting

### What It Is
Layouts wrap pages and persist across navigation. Nested layouts compose automatically.

### Why It Works
- **Shared UI** — header/sidebar don't re-render on navigation
- **Data sharing** — layout fetches data available to all child pages
- **Streaming** — layouts can stream content as it becomes ready

### Composition
```
app/layout.tsx          → Root layout (html, body)
├── app/dashboard/
│   └── layout.tsx      → Dashboard layout (sidebar)
│       ├── page.tsx    → Dashboard home
│       └── settings/
│           └── page.tsx → Dashboard settings
```

---

## Pattern 5: Data Fetching Patterns

### Server Components: Fetch at Render Time
```typescript
// This runs on the server — no client JS needed
export default async function UsersPage() {
  const users = await db.user.findMany();  // direct database access
  return <UserList users={users} />;
}
```

### Server Actions: Mutations from Forms
```typescript
// actions.ts
'use server'
export async function createUser(formData: FormData) {
  const name = formData.get('name') as string;
  await db.user.create({ data: { name } });
  revalidatePath('/users');
}
```

### Why This Pattern Matters
- No API layer needed for simple CRUD
- Type-safe from database to UI
- Automatic revalidation after mutations

---

## Pattern 6: TypeScript as Framework Contract

### How Types Enforce Correctness
```typescript
// The framework's types tell you exactly what's available
import type { Metadata } from 'next';

// Metadata type ensures you return valid SEO data
export const metadata: Metadata = {
  title: 'My Page',
  description: 'Page description',
};

// PageProps type ensures params match your route
type PageProps = {
  params: { id: string };
  searchParams: { [key: string]: string | string[] | undefined };
};
```

### The Lesson
TypeScript isn't just for catching bugs — it's for **designing APIs that guide the user to correctness**. Next.js's types are a masterclass in this.

---

## Key Takeaways

1. **File-based routing** eliminates configuration and improves discoverability
2. **Server/Client boundary** is the most important architectural decision — it controls what runs where
3. **Middleware** handles cross-cutting concerns at the edge
4. **Layout nesting** enables shared UI without re-rendering
5. **TypeScript types** are the framework's contract with the developer
6. **Data fetching** is colocated with the component that needs it

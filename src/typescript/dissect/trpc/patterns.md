# tRPC — Core Design Patterns

## Pattern 1: The Procedure Pattern

### What It Is
A "Procedure" is a typed function with input validation, a handler, and typed output. It replaces REST endpoints with a more developer-friendly abstraction.

### Why It's Better Than REST
```
REST:    GET /api/users/123?include=posts
tRPC:    trpc.user.getProfile.useQuery({ id: '123', include: 'posts' })
```

- **Type-safe** — the compiler catches wrong params
- **Discoverable** — IDE autocomplete shows all available procedures
- **Refactorable** — rename a procedure, all callers update automatically

### Anatomy of a Procedure
```typescript
const getProfile = publicProcedure
  .input(z.object({ id: z.string() }))    // Input validation (Zod)
  .query(({ input, ctx }) => {            // Handler
    return ctx.db.user.findUnique({
      where: { id: input.id },
      include: { posts: true },
    });
  });
// Return type is inferred from the handler
```

---

## Pattern 2: Router Composition

### What It Is
Routers group related procedures. Small routers compose into large ones.

### Why It Works
- **Organization** — related procedures live together
- **Namespacing** — `user.getProfile` vs `post.create`
- **Scalability** — each team owns their router

### Composition
```typescript
const userRouter = router({
  getProfile: getProfileProcedure,
  updateProfile: updateProfileProcedure,
});

const postRouter = router({
  create: createPostProcedure,
  list: listPostsProcedure,
});

// Compose into app router
const appRouter = router({
  user: userRouter,
  post: postRouter,
});

// Usage: trpc.user.getProfile, trpc.post.create
```

---

## Pattern 3: Context as Dependency Injection

### What It Is
Context is a dependency injection container that every procedure receives. It's created per-request and contains shared resources.

### Why It Works
- **Testable** — mock the context, test the procedure
- **Per-request** — each request gets fresh connections
- **Type-safe** — TypeScript knows what's in the context

### Implementation
```typescript
const createContext = ({ req }: CreateContextOptions) => {
  const session = getSession(req);
  return {
    db: prisma,
    session,
    user: session?.user,
  };
};

// Now every procedure has ctx.db, ctx.session, ctx.user
```

---

## Pattern 4: Middleware for Cross-Cutting Concerns

### What It Is
Middleware wraps procedures to add behavior before/after execution. Common uses: auth, logging, rate limiting.

### How It Works
```typescript
const isAuthed = middleware(({ ctx, next }) => {
  if (!ctx.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' });
  }
  return next({ ctx: { user: ctx.user } });  // narrow the context type
});

// Protected procedure
const protectedProcedure = publicProcedure.use(isAuthed);
// Now ctx.user is guaranteed to exist
```

### The Type Narrowing Trick
When middleware adds to context, `next({ ctx: { ... } })` tells TypeScript about the new context shape. Downstream procedures see the narrowed type.

---

## Pattern 5: Zod as the Validation Layer

### What It Is
Zod schemas define input shapes. tRPC uses them for both runtime validation AND type inference.

### Why This Matters
```typescript
const inputSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  age: z.number().int().positive(),
});

// This single schema provides:
// 1. Runtime validation (rejects invalid input)
// 2. TypeScript type (input: { name: string; email: string; age: number })
// 3. Error messages (Zod generates human-readable errors)
```

### The Lesson
One schema, three purposes. This is the pattern behind Pydantic (Python) and Zod (TypeScript).

---

## Pattern 6: Subscription Pattern (Real-Time)

### What It Is
tRPC supports WebSocket subscriptions for real-time data.

```typescript
const onMessage = publicProcedure
  .input(z.object({ channelId: z.string() }))
  .subscription(({ input }) => {
    return observable<string>((emit) => {
      const handler = (msg: string) => emit.next(msg);
      messageBus.subscribe(input.channelId, handler);
      return () => messageBus.unsubscribe(input.channelId, handler);
    });
  });
```

### Why Observable Over Polling
- **Push, not pull** — server sends data when available
- **Clean teardown** — unsubscribe returns a cleanup function
- **Type-safe** — the emitted values are typed

---

## Key Takeaways

1. **Procedures** replace REST endpoints with type-safe functions
2. **Router composition** organizes procedures into scalable namespaces
3. **Context** is dependency injection — type-safe and testable
4. **Middleware** narrows types while adding behavior
5. **Zod** validates input AND infers types from one schema
6. **Zero code generation** — TypeScript inference does all the work
7. The pattern: schema → type → validation → handler — all from one definition

/**
 * tRPC — Atomic Code Dissection
 * ==============================
 * Simplified but accurate implementation of tRPC's core patterns.
 * Demonstrates end-to-end type safety without code generation.
 *
 * Run: npx tsx dissect.ts
 */

// ============================================================================
// SECTION 1: ZOD-LIKE VALIDATION
// ============================================================================
// tRPC uses Zod for input validation. Here's a minimal implementation.

interface Schema<T> {
  parse(input: unknown): T;
  _type: T;  // phantom type for inference
}

function string(): Schema<string> {
  return {
    _type: '' as string,
    parse(input: unknown): string {
      if (typeof input !== 'string') throw new Error(`Expected string, got ${typeof input}`);
      return input;
    },
  };
}

function number(): Schema<number> {
  return {
    _type: 0 as number,
    parse(input: unknown): number {
      if (typeof input !== 'number') throw new Error(`Expected number, got ${typeof input}`);
      return input;
    },
  };
}

function object<T extends Record<string, Schema<any>>>(
  shape: T
): Schema<{ [K in keyof T]: T[K]['_type'] }> {
  return {
    _type: {} as any,
    parse(input: unknown): any {
      if (typeof input !== 'object' || input === null) {
        throw new Error('Expected object');
      }
      const result: Record<string, unknown> = {};
      for (const [key, schema] of Object.entries(shape)) {
        result[key] = schema.parse((input as any)[key]);
      }
      return result;
    },
  };
}

// Test
console.log('=== Zod-like Validation ===');
const userSchema = object({ name: string(), age: number() });
console.log(userSchema.parse({ name: 'Alice', age: 30 }));  // { name: 'Alice', age: 30 }
try {
  userSchema.parse({ name: 'Alice', age: 'thirty' });  // throws
} catch (e: any) {
  console.log('Validation error:', e.message);
}


// ============================================================================
// SECTION 2: THE PROCEDURE PATTERN
// ============================================================================
// A Procedure is: input schema → handler → typed output

interface ProcedureDef<TInput, TOutput> {
  _inputType: TInput;
  _outputType: TOutput;
  _handler: (input: TInput, ctx: any) => TOutput | Promise<TOutput>;
  _inputSchema: Schema<TInput> | null;
}

class ProcedureBuilder<TContext> {
  /**
   * Define input schema (like publicProcedure.input(...))
   */
  input<TInput>(schema: Schema<TInput>): ProcedureBuilderWithContext<TContext, TInput> {
    return new ProcedureBuilderWithContext<TContext, TInput>(schema);
  }

  /**
   * Define handler without input (like publicProcedure.query(...))
   */
  query<TOutput>(
    handler: (opts: { ctx: TContext }) => TOutput | Promise<TOutput>
  ): ProcedureDef<void, TOutput> {
    return {
      _inputType: undefined as void,
      _outputType: undefined as TOutput,
      _handler: (_input, ctx) => handler({ ctx }),
      _inputSchema: null,
    };
  }
}

class ProcedureBuilderWithContext<TContext, TInput> {
  constructor(private inputSchema: Schema<TInput>) {}

  /**
   * Define handler with typed input (like .query(({ input, ctx }) => ...))
   */
  query<TOutput>(
    handler: (opts: { input: TInput; ctx: TContext }) => TOutput | Promise<TOutput>
  ): ProcedureDef<TInput, TOutput> {
    return {
      _inputType: undefined as TInput,
      _outputType: undefined as TOutput,
      _handler: (input, ctx) => handler({ input, ctx }),
      _inputSchema: this.inputSchema,
    };
  }

  mutation<TOutput>(
    handler: (opts: { input: TInput; ctx: TContext }) => TOutput | Promise<TOutput>
  ): ProcedureDef<TInput, TOutput> {
    return {
      _inputType: undefined as TInput,
      _outputType: undefined as TOutput,
      _handler: (input, ctx) => handler({ input, ctx }),
      _inputSchema: this.inputSchema,
    };
  }
}

// Test
console.log('\n=== Procedure Pattern ===');
type TestContext = { db: any; user: { id: string } | null };
const proc = new ProcedureBuilder<TestContext>();

const getProfile = proc
  .input(object({ id: string() }))
  .query(({ input, ctx }) => {
    return { name: `User_${input.id}`, authenticated: ctx.user !== null };
  });

console.log('Procedure created:', typeof getProfile._handler);


// ============================================================================
// SECTION 3: ROUTER COMPOSITION
// ============================================================================
// Routers group procedures. Small routers compose into large ones.

type ProcedureMap = Record<string, ProcedureDef<any, any>>;

type RouterDef<TProcedures extends ProcedureMap> = {
  _procedures: TProcedures;
};

function router<TProcedures extends ProcedureMap>(
  procedures: TProcedures
): RouterDef<TProcedures> {
  return { _procedures: procedures };
}

// Compose routers
const userRouter = router({
  getProfile: proc
    .input(object({ id: string() }))
    .query(({ input }) => ({ name: `User_${input.id}` })),

  updateProfile: proc
    .input(object({ id: string(), name: string() }))
    .mutation(({ input }) => ({ updated: true, name: input.name })),
});

const postRouter = router({
  create: proc
    .input(object({ title: string(), body: string() }))
    .mutation(({ input }) => ({ id: '1', ...input })),

  list: proc.query(() => [
    { id: '1', title: 'First Post' },
    { id: '2', title: 'Second Post' },
  ]),
});

const appRouter = router({
  user: userRouter,
  post: postRouter,
});

// Test
console.log('\n=== Router Composition ===');
console.log('App router procedures:', Object.keys(appRouter._procedures));
console.log('User router procedures:', Object.keys(appRouter._procedures.user._procedures));
console.log('Post router procedures:', Object.keys(appRouter._procedures.post._procedures));


// ============================================================================
// SECTION 4: MIDDLEWARE WITH TYPE NARROWING
// ============================================================================
// Middleware wraps procedures, potentially narrowing the context type.

type MiddlewareFn<TContextIn, TContextOut> = (opts: {
  ctx: TContextIn;
  next: (opts: { ctx: TContextOut }) => any;
}) => any;

function middleware<TContextIn, TContextOut>(
  fn: (opts: { ctx: TContextIn; next: (opts: { ctx: TContextOut }) => any }) => any
): MiddlewareFn<TContextIn, TContextOut> {
  return fn;
}

// Auth middleware — narrows context to guarantee user exists
const isAuthed = middleware((opts: { ctx: { user: { id: string } | null } }) => {
  if (!opts.ctx.user) {
    throw new Error('UNAUTHORIZED');
  }
  return opts.next({ ctx: { user: opts.ctx.user } });
});

// Test
console.log('\n=== Middleware ===');
try {
  isAuthed({
    ctx: { user: null },
    next: ({ ctx }) => console.log('Should not reach:', ctx),
  });
} catch (e: any) {
  console.log('Auth blocked:', e.message);
}

isAuthed({
  ctx: { user: { id: '123' } },
  next: ({ ctx }) => console.log('Auth passed, user:', ctx.user),
});


// ============================================================================
// SECTION 5: PROCEDURE EXECUTION
// ============================================================================
// How tRPC actually executes a procedure: validate input → call handler

async function executeProcedure<TInput, TOutput>(
  procedure: ProcedureDef<TInput, TOutput>,
  rawInput: unknown,
  context: any
): Promise<{ success: true; data: TOutput } | { success: false; error: string }> {
  try {
    // Step 1: Validate input
    let input: TInput;
    if (procedure._inputSchema) {
      input = procedure._inputSchema.parse(rawInput);
    } else {
      input = undefined as TInput;
    }

    // Step 2: Execute handler
    const data = await procedure._handler(input, context);
    return { success: true, data };
  } catch (error: any) {
    return { success: false, error: error.message };
  }
}

// Test
console.log('\n=== Procedure Execution ===');
const context: TestContext = { db: null, user: { id: 'user-1' } };

// Successful call
executeProcedure(
  appRouter._procedures.user._procedures.getProfile,
  { id: '42' },
  context
).then(result => console.log('Success:', result));

// Failed validation
executeProcedure(
  appRouter._procedures.user._procedures.getProfile,
  { wrong: 'field' },
  context
).then(result => console.log('Validation fail:', result));

// Successful mutation
executeProcedure(
  appRouter._procedures.user._procedures.updateProfile,
  { id: '42', name: 'Alice' },
  context
).then(result => console.log('Mutation:', result));


// ============================================================================
// SECTION 6: TYPE INFERENCE (CONCEPTUAL)
// ============================================================================
// This is how tRPC infers types from server to client without code generation.

// The key insight: TypeScript's typeof operator can extract types from values.
// Since procedures ARE values with _inputType and _outputType, we can extract them.

type InferInput<T> = T extends ProcedureDef<infer I, any> ? I : never;
type InferOutput<T> = T extends ProcedureDef<any, infer O> ? O : never;

// Now we can extract types from our router:
type UserProfileInput = InferInput<typeof appRouter._procedures.user._procedures.getProfile>;
//   ^? { id: string }

type UserProfileOutput = InferOutput<typeof appRouter._procedures.user._procedures.getProfile>;
//   ^? { name: string }

// This is exactly what tRPC does — the client gets these types automatically.

// Test
console.log('\n=== Type Inference ===');
console.log('Types are extracted at compile time, not runtime.');
console.log('But the mechanism is: typeof router → typeof procedure → input/output types');


// ============================================================================
// KEY TAKEAWAYS
// ============================================================================
/*
1. Zod-like schemas provide both validation AND type inference — one definition, two purposes
2. Procedures are typed functions: input schema → handler → typed output
3. Routers compose small procedures into scalable APIs
4. Middleware narrows types while adding cross-cutting behavior
5. Context is dependency injection — type-safe and testable
6. Type inference flows from server to client through typeof — zero code generation
7. The pattern: schema → type → validation → handler — all from one definition
*/

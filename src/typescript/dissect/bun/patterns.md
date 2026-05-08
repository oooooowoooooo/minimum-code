# Bun — Core Design Patterns

## Pattern 1: Native TypeScript Execution

### What It Is
Bun runs `.ts` files directly. No `tsc`, no `ts-node`, no build step.

```bash
bun run app.ts        # Just works
bun test              # Runs .test.ts files directly
```

### Why It Matters
1. **Zero config** — no tsconfig needed for basic usage
2. **Fast iteration** — save and run, no compilation wait
3. **Type stripping** — Bun strips types, doesn't type-check (use `tsc --noEmit` for that)

---

## Pattern 2: All-in-One Toolchain

### What It Is
One binary replaces: `node`, `npm`, `npx`, `jest`, `webpack`, `esbuild`.

### Commands
```bash
bun install           # Like npm install (but 20x faster)
bun run dev           # Like npm run dev
bun test              # Like jest
bun build ./src/index.ts --outdir ./dist  # Like webpack
```

### Why It Matters
1. **One dependency** — less tooling to manage
2. **Consistent** — same binary, same behavior
3. **Fast** — Zig implementation, not JavaScript

---

## Pattern 3: Bun.file() — Lazy File API

### What It Is
`Bun.file()` returns a `Blob`-like object. The file isn't read until you call `.text()`, `.json()`, or `.arrayBuffer()`.

```typescript
const file = Bun.file("./data.json");  // No I/O yet
const data = await file.json();         // I/O happens here
```

### Why It Matters
1. **Lazy** — no unnecessary I/O
2. **Memory efficient** — streams large files
3. **Web-compatible** — same API as browser `Blob`

---

## Pattern 4: Bun.serve() — Fast HTTP Server

### What It Is
Built-in HTTP server optimized for Bun's runtime.

```typescript
Bun.serve({
  port: 3000,
  fetch(req) {
    return new Response("Hello from Bun!");
  },
});
```

### Why It Matters
1. **Fast** — handles 3x more requests than Node.js `http`
2. **Simple** — one function, no boilerplate
3. **WebSocket support** — built-in, no library needed

---

## Pattern 5: Built-in SQLite

### What It Is
Bun has a native SQLite driver. No `better-sqlite3` dependency.

```typescript
import { Database } from "bun:sqlite";
const db = new Database("app.db");
db.run("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)");
```

### Why It Matters
1. **Zero dependencies** — no native module compilation
2. **Fast** — direct SQLite binding via Zig
3. **Embedded** — perfect for local-first apps

---

## Key Takeaways

1. **Native TypeScript** — run .ts directly, no build step
2. **All-in-one** — runtime + bundler + test + package manager
3. **Bun.file()** — lazy, memory-efficient file I/O
4. **Bun.serve()** — fast HTTP server with minimal code
5. **Built-in SQLite** — embedded database without dependencies
6. **Zig implementation** — performance from systems programming

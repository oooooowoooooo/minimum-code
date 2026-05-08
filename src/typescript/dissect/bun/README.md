# Bun — The All-in-One JavaScript Runtime

> GitHub Stars: 75k+ | Language: Zig + TypeScript | Category: Runtime

## What Is Bun?

Bun is a fast all-in-one JavaScript runtime. It replaces Node.js, npm, webpack, and Jest with a single tool built on JavaScriptCore (Safari's engine) instead of V8.

## Why It Matters

1. **Speed** — 3-5x faster than Node.js for most workloads
2. **All-in-one** — runtime + bundler + test runner + package manager
3. **Node-compatible** — runs existing npm packages
4. **TypeScript-native** — runs .ts files directly, no build step

## Architecture

```
┌─────────────────────────────────────┐
│            Bun Runtime              │
├──────────┬──────────┬───────────────┤
│ Bundler  │ Test     │ Package       │
│ (esbuild)│ Runner   │ Manager       │
├──────────┴──────────┴───────────────┤
│        JavaScriptCore (WebKit)      │
├─────────────────────────────────────┤
│     Zig / C++ / FFI Layer           │
├─────────────────────────────────────┤
│     Operating System                │
└─────────────────────────────────────┘
```

## Key Patterns

| # | Pattern | What It Does |
|---|---------|-------------|
| 1 | Native TypeScript | Run .ts directly, no tsc needed |
| 2 | Built-in bundler | Bundle without webpack/vite |
| 3 | Bun.file() API | Fast file I/O with lazy reading |
| 4 | Bun.serve() | HTTP server faster than Node |
| 5 | SQLite built-in | Database without dependencies |

## Files

| File | Description |
|------|-------------|
| [patterns.md](./patterns.md) | Core design patterns |
| [dissect.ts](./dissect.ts) | Atomic code dissection |

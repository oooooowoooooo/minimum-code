/**
 * Bun — Atomic Code Dissection
 * =============================
 * Simplified implementations of Bun's core patterns.
 * Demonstrates runtime design, file I/O, and all-in-one philosophy.
 *
 * Run: npx tsx dissect.ts
 */

// ============================================================================
// SECTION 1: NATIVE TYPESCRIPT EXECUTION (CONCEPTUAL)
// ============================================================================
// How Bun can run TypeScript without a build step.

/**
 * Bun's approach: STRIP types, don't CHECK them.
 *
 * Input TypeScript:
 *   function greet(name: string): string { return `Hello, ${name}!` }
 *
 * Bun strips to JavaScript:
 *   function greet(name) { return `Hello, ${name}!` }
 *
 * This is 10-100x faster than tsc because:
 * 1. No type checking (use tsc --noEmit separately)
 * 2. No AST transformation (just regex-based stripping)
 * 3. Single pass (no multiple compilation phases)
 */

// Simulated type stripping
function stripTypes(tsCode: string): string {
  return tsCode
    .replace(/:\s*\w+(\[\])?/g, '')           // Remove type annotations
    .replace(/<[^>]+>/g, '')                    // Remove generics
    .replace(/interface\s+\w+\s*\{[^}]*\}/g, '') // Remove interfaces
    .replace(/type\s+\w+\s*=\s*[^;]+;/g, '');   // Remove type aliases
}

// Test
console.log('=== Native TypeScript Execution ===');
const tsCode = 'function greet(name: string): string { return `Hello, ${name}!`; }';
console.log('TypeScript:', tsCode);
console.log('Stripped:  ', stripTypes(tsCode));


// ============================================================================
// SECTION 2: Bun.file() — LAZY FILE API
// ============================================================================
// Files are represented as lazy Blob-like objects.

class BunFile {
  private content: string | null = null;
  private loaded = false;

  constructor(private path: string) {}

  /**
   * Returns file size without reading content.
   * In real Bun, this is a stat() call.
   */
  get size(): number {
    // Simulated — in real Bun, this queries the filesystem
    return this.content?.length ?? 0;
  }

  /**
   * Returns MIME type from extension.
   */
  get type(): string {
    const ext = this.path.split('.').pop();
    const types: Record<string, string> = {
      json: 'application/json',
      txt: 'text/plain',
      ts: 'text/typescript',
      html: 'text/html',
    };
    return types[ext ?? ''] ?? 'application/octet-stream';
  }

  /**
   * Read file as text (lazy — only reads when called).
   */
  async text(): Promise<string> {
    if (!this.loaded) {
      // Simulate file read
      this.content = `Contents of ${this.path}`;
      this.loaded = true;
    }
    return this.content!;
  }

  /**
   * Read file as JSON (lazy).
   */
  async json<T = any>(): Promise<T> {
    const text = await this.text();
    return JSON.parse(text);
  }

  /**
   * Read file as ArrayBuffer (lazy).
   */
  async arrayBuffer(): Promise<ArrayBuffer> {
    const text = await this.text();
    return new TextEncoder().encode(text).buffer;
  }
}

/**
 * Bun.file() — creates a lazy file handle.
 * No I/O happens until you call .text(), .json(), etc.
 */
function bunFile(path: string): BunFile {
  return new BunFile(path);
}

// Test
console.log('\n=== Bun.file() Lazy API ===');
const file = bunFile('./data.json');
console.log('File created (no I/O yet)');
console.log('Type:', file.type);
console.log('Size:', file.size);

file.text().then(content => {
  console.log('Content:', content);
});


// ============================================================================
// SECTION 3: Bun.serve() — FAST HTTP SERVER
// ============================================================================
// Built-in HTTP server with minimal overhead.

type FetchHandler = (request: Request) => Response | Promise<Response>;

interface ServeOptions {
  port: number;
  fetch: FetchHandler;
  hostname?: string;
}

/**
 * Simplified Bun.serve() implementation.
 * Demonstrates the server's API design.
 */
function bunServe(options: ServeOptions): { stop: () => void; url: string } {
  const { port, fetch, hostname = 'localhost' } = options;

  console.log(`  Server listening on http://${hostname}:${port}`);

  // In real Bun, this starts a native HTTP server
  // Here we simulate a request
  const testRequest = new Request(`http://${hostname}:${port}/`);
  fetch(testRequest).then(response => {
    response.text().then(body => {
      console.log(`  Response: ${body}`);
    });
  });

  return {
    stop: () => console.log('  Server stopped'),
    url: `http://${hostname}:${port}`,
  };
}

// Test
console.log('\n=== Bun.serve() ===');
const server = bunServe({
  port: 3000,
  fetch(req) {
    const url = new URL(req.url);
    if (url.pathname === '/api/hello') {
      return new Response(JSON.stringify({ message: 'Hello!' }), {
        headers: { 'Content-Type': 'application/json' },
      });
    }
    return new Response('Not Found', { status: 404 });
  },
});

// Simulate API request
const apiReq = new Request('http://localhost:3000/api/hello');
server['url']; // just accessing for demo


// ============================================================================
// SECTION 4: BUILT-IN BUNDLER (CONCEPTUAL)
// ============================================================================
// How Bun bundles code without webpack/vite.

interface BundleOptions {
  entrypoints: string[];
  outdir: string;
  target?: 'browser' | 'node' | 'bun';
  format?: 'esm' | 'cjs';
  splitting?: boolean;
  minify?: boolean;
}

/**
 * Simplified bundler showing the API design.
 * Real Bun uses esbuild internally for bundling.
 */
function bunBuild(options: BundleOptions): { outputs: string[]; logs: string[] } {
  const outputs: string[] = [];
  const logs: string[] = [];

  for (const entry of options.entrypoints) {
    const outFile = `${optionsoutdir}/${entry.split('/').pop()!.replace('.ts', '.js')}`;
    outputs.push(outFile);
    logs.push(`Bundled ${entry} → ${outFile}`);
  }

  return { outputs, logs };
}

// Test
console.log('\n=== Bun.build() Bundler ===');
const result = bunBuild({
  entrypoints: ['./src/index.ts', './src/utils.ts'],
  outdir: './dist',
  target: 'bun',
  format: 'esm',
  minify: true,
});
console.log('Outputs:', result.outputs);
console.log('Logs:', result.logs);


// ============================================================================
// SECTION 5: BUILT-IN SQLITE
// ============================================================================
// Embedded database without external dependencies.

interface SQLiteRow {
  [key: string]: string | number | null;
}

/**
 * Simplified Bun SQLite API.
 * Demonstrates the synchronous, prepared-statement interface.
 */
class BunDatabase {
  private tables: Map<string, SQLiteRow[]> = new Map();

  constructor(private path: string) {
    console.log(`  Opened database: ${path}`);
  }

  /**
   * Execute SQL (synchronous in real Bun).
   */
  run(sql: string): void {
    // Simplified: just track table creation
    const createMatch = sql.match(/CREATE TABLE IF NOT EXISTS (\w+)/);
    if (createMatch) {
      const tableName = createMatch[1];
      if (!this.tables.has(tableName)) {
        this.tables.set(tableName, []);
        console.log(`  Created table: ${tableName}`);
      }
    }
  }

  /**
   * Query with prepared statement (synchronous in real Bun).
   */
  query(sql: string): SQLiteRow[] {
    const selectMatch = sql.match(/FROM (\w+)/);
    if (selectMatch) {
      return this.tables.get(selectMatch[1]) ?? [];
    }
    return [];
  }

  /**
   * Insert a row.
   */
  insert(table: string, row: SQLiteRow): void {
    if (!this.tables.has(table)) {
      this.tables.set(table, []);
    }
    this.tables.get(table)!.push(row);
  }
}

// Test
console.log('\n=== Built-in SQLite ===');
const db = new BunDatabase('app.db');
db.run('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)');

db.insert('users', { id: 1, name: 'Alice' });
db.insert('users', { id: 2, name: 'Bob' });

const users = db.query('SELECT * FROM users');
console.log('Users:', users);


// ============================================================================
// SECTION 6: ALL-IN-ONE PHILOSOPHY
// ============================================================================
// How one binary replaces an entire toolchain.

interface ToolCommand {
  name: string;
  replaces: string[];
  description: string;
}

const bunCommands: ToolCommand[] = [
  { name: 'bun run', replaces: ['node', 'ts-node'], description: 'Execute JS/TS' },
  { name: 'bun install', replaces: ['npm install'], description: 'Install packages' },
  { name: 'bun test', replaces: ['jest', 'vitest'], description: 'Run tests' },
  { name: 'bun build', replaces: ['webpack', 'esbuild', 'vite'], description: 'Bundle code' },
  { name: 'bun create', replaces: ['npx create-*'], description: 'Scaffold projects' },
];

// Test
console.log('\n=== All-in-One Philosophy ===');
console.log('Bun replaces:');
for (const cmd of bunCommands) {
  console.log(`  ${cmd.name} → ${cmd.replaces.join(', ')} (${cmd.description})`);
}


// ============================================================================
// KEY TAKEAWAYS
// ============================================================================
/*
1. Native TypeScript — strip types, don't check them (fast!)
2. Bun.file() — lazy file handles, no I/O until needed
3. Bun.serve() — minimal HTTP server, maximum performance
4. Bun.build() — built-in bundler, no webpack/vite dependency
5. Built-in SQLite — embedded database, zero dependencies
6. All-in-one — one binary replaces node + npm + jest + webpack
7. Zig implementation — systems programming for JavaScript runtime
*/

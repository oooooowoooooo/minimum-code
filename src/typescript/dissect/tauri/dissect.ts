/**
 * Tauri — Atomic Code Dissection
 * ===============================
 * Simplified implementation of Tauri's core patterns.
 * Demonstrates IPC bridge, command pattern, and event system.
 *
 * Run: npx tsx dissect.ts
 */

// ============================================================================
// SECTION 1: THE COMMAND PATTERN
// ============================================================================
// Commands are named functions that the frontend can invoke on the backend.

type CommandHandler<TArgs, TResult> = (args: TArgs, state: AppState) => TResult | Promise<TResult>;

interface CommandDef<TArgs, TResult> {
  name: string;
  handler: CommandHandler<TArgs, TResult>;
  // In real Tauri, this would also have permission requirements
}

class CommandRegistry {
  private commands: Map<string, CommandDef<any, any>> = new Map();

  /**
   * Register a command (like Rust's #[tauri::command])
   */
  register<TArgs, TResult>(
    name: string,
    handler: CommandHandler<TArgs, TResult>
  ): void {
    this.commands.set(name, { name, handler });
  }

  /**
   * Invoke a command by name (like frontend's invoke())
   */
  async invoke<TArgs, TResult>(
    name: string,
    args: TArgs,
    state: AppState
  ): Promise<TResult> {
    const command = this.commands.get(name);
    if (!command) {
      throw new Error(`Command "${name}" not found. Available: ${[...this.commands.keys()].join(', ')}`);
    }
    return command.handler(args, state);
  }

  /**
   * List all registered commands (for debugging/documentation)
   */
  list(): string[] {
    return [...this.commands.keys()];
  }
}

// Test
console.log('=== Command Pattern ===');
const registry = new CommandRegistry();
registry.register('greet', (args: { name: string }, _state) => {
  return `Hello, ${args.name}!`;
});

registry.invoke('greet', { name: 'Alice' }, {}).then(result => {
  console.log('Command result:', result);
});

console.log('Registered commands:', registry.list());


// ============================================================================
// SECTION 2: IPC BRIDGE (SERIALIZATION)
// ============================================================================
// How data crosses the frontend ↔ backend boundary.

class IPCBridge {
  /**
   * Serialize a value for IPC transport (JS → JSON → Rust).
   * In real Tauri, this uses serde (Rust serialization library).
   */
  static serialize<T>(value: T): string {
    return JSON.stringify(value);
  }

  /**
   * Deserialize a value from IPC transport (Rust → JSON → JS).
   */
  static deserialize<T>(json: string): T {
    return JSON.parse(json);
  }

  /**
   * Simulate the full IPC roundtrip: serialize → transport → deserialize → execute
   */
  static async roundtrip<TArgs, TResult>(
    command: CommandDef<TArgs, TResult>,
    args: TArgs,
    state: AppState
  ): Promise<TResult> {
    // Step 1: Serialize args (frontend side)
    const serialized = this.serialize(args);

    // Step 2: "Transport" (in real Tauri, this goes through native IPC)
    // Step 3: Deserialize args (backend side)
    const deserialized = this.deserialize<TArgs>(serialized);

    // Step 4: Execute command
    const result = await command.handler(deserialized, state);

    // Step 5: Serialize result (backend side)
    const resultSerialized = this.serialize(result);

    // Step 6: Deserialize result (frontend side)
    return this.deserialize<TResult>(resultSerialized);
  }
}

// Test
console.log('\n=== IPC Bridge ===');
const greetCommand: CommandDef<{ name: string }, string> = {
  name: 'greet',
  handler: (args) => `Hello, ${args.name}!`,
};

IPCBridge.roundtrip(greetCommand, { name: 'Bob' }, {}).then(result => {
  console.log('IPC roundtrip result:', result);
});


// ============================================================================
// SECTION 3: STATE MANAGEMENT
// ============================================================================
// Rust backend maintains state; commands access it via dependency injection.

interface AppState {
  users: Map<string, { id: string; name: string; email: string }>;
  counter: number;
}

class StateManager {
  private state: AppState;

  constructor(initialState: Partial<AppState> = {}) {
    this.state = {
      users: new Map(),
      counter: 0,
      ...initialState,
    };
  }

  getState(): AppState {
    return this.state;
  }

  /**
   * Update state immutably (returns new state).
   * In real Tauri/Rust, this uses Mutex<state> for thread safety.
   */
  update(updater: (state: AppState) => AppState): AppState {
    this.state = updater(this.state);
    return this.state;
  }
}

// Test
console.log('\n=== State Management ===');
const stateManager = new StateManager();
const state = stateManager.getState();

// Register state-dependent commands
registry.register('create_user', (args: { name: string; email: string }, state) => {
  const id = `user-${state.users.size + 1}`;
  state.users.set(id, { id, ...args });
  return { id, created: true };
});

registry.register('list_users', (_args: {}, state) => {
  return [...state.users.values()];
});

// Create users
registry.invoke('create_user', { name: 'Alice', email: 'alice@test.com' }, state)
  .then(result => console.log('Created user:', result));

registry.invoke('create_user', { name: 'Bob', email: 'bob@test.com' }, state)
  .then(result => console.log('Created user:', result));

registry.invoke('list_users', {}, state)
  .then(users => console.log('All users:', users));


// ============================================================================
// SECTION 4: EVENT SYSTEM
// ============================================================================
// Bidirectional communication: backend can push events to frontend.

type EventHandler<T = any> = (payload: T) => void;

class EventBus {
  private listeners: Map<string, Set<EventHandler>> = new Map();

  /**
   * Listen for an event (frontend side).
   * Returns an unlisten function.
   */
  listen<T>(event: string, handler: EventHandler<T>): () => void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(handler);

    // Return unlisten function
    return () => {
      this.listeners.get(event)?.delete(handler);
    };
  }

  /**
   * Emit an event (backend side).
   */
  emit<T>(event: string, payload: T): void {
    const handlers = this.listeners.get(event);
    if (handlers) {
      for (const handler of handlers) {
        handler(payload);
      }
    }
  }

  /**
   * Listen once — auto-unlisten after first call.
   */
  once<T>(event: string, handler: EventHandler<T>): () => void {
    const wrapper: EventHandler<T> = (payload) => {
      unlisten();
      handler(payload);
    };
    const unlisten = this.listen(event, wrapper);
    return unlisten;
  }
}

// Test
console.log('\n=== Event System ===');
const eventBus = new EventBus();

// Frontend listens
const unlisten = eventBus.listen<{ file: string }>('file-changed', (payload) => {
  console.log('File changed:', payload.file);
});

// Backend emits
eventBus.emit('file-changed', { file: 'README.md' });
eventBus.emit('file-changed', { file: 'package.json' });

// Unlisten
unlisten();
eventBus.emit('file-changed', { file: 'tsconfig.json' }); // No handler, no output

// Once
eventBus.once('app-ready', () => console.log('App is ready!'));
eventBus.emit('app-ready', {});
eventBus.emit('app-ready', {}); // Second emit has no handler


// ============================================================================
// SECTION 5: PERMISSION SYSTEM
// ============================================================================
// Commands declare what permissions they need.

interface Permission {
  resource: string;
  actions: string[];
}

interface SecureCommandDef<TArgs, TResult> extends CommandDef<TArgs, TResult> {
  permissions: Permission[];
}

class SecureCommandRegistry {
  private commands: Map<string, SecureCommandDef<any, any>> = new Map();
  private grantedPermissions: Set<string> = new Set();

  register<TArgs, TResult>(
    name: string,
    handler: CommandHandler<TArgs, TResult>,
    permissions: Permission[] = []
  ): void {
    this.commands.set(name, { name, handler, permissions });
  }

  grantPermission(resource: string, action: string): void {
    this.grantedPermissions.add(`${resource}:${action}`);
  }

  async invoke<TArgs, TResult>(
    name: string,
    args: TArgs,
    state: AppState
  ): Promise<TResult> {
    const command = this.commands.get(name);
    if (!command) {
      throw new Error(`Command "${name}" not found`);
    }

    // Check permissions
    for (const perm of command.permissions) {
      for (const action of perm.actions) {
        if (!this.grantedPermissions.has(`${perm.resource}:${action}`)) {
          throw new Error(
            `Permission denied: ${perm.resource}:${action} required by "${name}"`
          );
        }
      }
    }

    return command.handler(args, state);
  }
}

// Test
console.log('\n=== Permission System ===');
const secureRegistry = new SecureCommandRegistry();

secureRegistry.register(
  'read_file',
  (args: { path: string }) => `Contents of ${args.path}`,
  [{ resource: 'fs', actions: ['read'] }]
);

secureRegistry.register(
  'write_file',
  (args: { path: string; content: string }) => `Written to ${args.path}`,
  [{ resource: 'fs', actions: ['write'] }]
);

// Grant read permission
secureRegistry.grantPermission('fs', 'read');

// Read should work
secureRegistry.invoke('read_file', { path: '/tmp/test.txt' }, {}).then(result => {
  console.log('Read:', result);
});

// Write should fail (no write permission)
secureRegistry.invoke('write_file', { path: '/tmp/test.txt', content: 'hello' }, {})
  .catch(err => console.log('Write denied:', err.message));


// ============================================================================
// SECTION 6: PLUGIN ARCHITECTURE
// ============================================================================
// Plugins extend the app with new commands, state, and lifecycle hooks.

interface Plugin {
  name: string;
  commands: Array<{ name: string; handler: CommandHandler<any, any> }>;
  onReady?: () => void;
}

class PluginManager {
  private plugins: Plugin[] = [];

  register(plugin: Plugin): void {
    this.plugins.push(plugin);
  }

  /**
   * Install all plugins into the command registry.
   */
  install(registry: CommandRegistry): void {
    for (const plugin of this.plugins) {
      console.log(`  Installing plugin: ${plugin.name}`);
      for (const command of plugin.commands) {
        registry.register(command.name, command.handler);
      }
      plugin.onReady?.();
    }
  }
}

// Test
console.log('\n=== Plugin Architecture ===');
const pluginManager = new PluginManager();
const pluginRegistry = new CommandRegistry();

const fsPlugin: Plugin = {
  name: 'fs-plugin',
  commands: [
    {
      name: 'fs:read',
      handler: (args: { path: string }) => `Reading ${args.path}`,
    },
    {
      name: 'fs:write',
      handler: (args: { path: string; content: string }) => `Written to ${args.path}`,
    },
  ],
  onReady: () => console.log('  fs-plugin ready'),
};

const dialogPlugin: Plugin = {
  name: 'dialog-plugin',
  commands: [
    {
      name: 'dialog:open',
      handler: () => '/selected/file.txt',
    },
  ],
  onReady: () => console.log('  dialog-plugin ready'),
};

pluginManager.register(fsPlugin);
pluginManager.register(dialogPlugin);
pluginManager.install(pluginRegistry);

console.log('Available commands:', pluginRegistry.list());


// ============================================================================
// KEY TAKEAWAYS
// ============================================================================
/*
1. Command pattern: discrete, named functions replace open API surfaces
2. IPC bridge: serialize → transport → deserialize — type-safe on both sides
3. State management: backend owns state, commands access via dependency injection
4. Event system: bidirectional push communication with clean teardown
5. Permission system: explicit capability declarations enforce least privilege
6. Plugin architecture: modular extensions follow the same patterns as core
7. The key insight: LIMIT what the frontend can access, don't expose everything
*/

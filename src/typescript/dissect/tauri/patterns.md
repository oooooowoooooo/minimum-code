# Tauri — Core Design Patterns

## Pattern 1: The Command Pattern

### What It Is
Instead of exposing a full API surface, Tauri uses discrete "commands" — named functions with typed arguments that the frontend can invoke.

### Why It's Secure
- Only explicitly declared commands are callable
- Each command has typed inputs (validated at the IPC boundary)
- Commands can require permissions

### Frontend → Backend Flow
```typescript
// Frontend (TypeScript)
const result = await invoke('greet', { name: 'Alice' });
```
```rust
// Backend (Rust)
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}
```

### The Lesson
**Explicit is better than implicit.** Don't expose your entire backend — expose only what the frontend needs.

---

## Pattern 2: IPC Bridge Design

### What It Is
The IPC bridge serializes data between JavaScript (frontend) and Rust (backend). It handles:
- Serialization (JS object → JSON → Rust struct)
- Deserialization (Rust struct → JSON → JS object)
- Error propagation (Rust errors → JS exceptions)

### Why It Works
- **Type-safe on both sides** — TypeScript types match Rust types
- **Language-agnostic** — JSON is the lingua franca
- **Error handling** — errors cross the boundary cleanly

### Serialization Contract
```typescript
// Frontend sends:
invoke('create_user', { name: 'Alice', age: 30 });
// Serialized as: {"name": "Alice", "age": 30}

// Backend receives:
#[derive(Deserialize)]
struct CreateUserArgs {
    name: String,
    age: u32,
}
```

---

## Pattern 3: State Management Across Boundaries

### What It Is
The Rust backend maintains state that commands can access. State is managed by Tauri's state system, similar to dependency injection.

### Why It Works
- **Single source of truth** — state lives in Rust, not in the WebView
- **Thread-safe** — Rust's ownership model prevents data races
- **Accessible** — any command can request state via function parameters

```rust
#[tauri::command]
fn get_users(state: State<AppState>) -> Vec<User> {
    state.users.lock().unwrap().clone()
}
```

---

## Pattern 4: Event System (Bidirectional)

### What It Is
Events allow the backend to push data to the frontend (not just request-response).

### Frontend Listens
```typescript
import { listen } from '@tauri-apps/api/event';
const unlisten = await listen('file-changed', (event) => {
  console.log('File changed:', event.payload);
});
```

### Backend Emits
```rust
app.emit_all("file-changed", payload).unwrap();
```

### Why This Pattern Matters
- **Push, not poll** — backend notifies frontend when something changes
- **Decoupled** — emitter doesn't know about listeners
- **Clean teardown** — `unlisten()` removes the listener

---

## Pattern 5: Permission System

### What It Is
Tauri has a capability system that controls what commands can access. Commands must declare their required permissions.

### Why It's Important
- **Principle of least privilege** — commands only get what they need
- **Auditability** — you can see exactly what each command accesses
- **User trust** — users can review what the app can do

```json
// tauri.conf.json
{
  "capabilities": [{
    "identifier": "main-capability",
    "windows": ["main"],
    "permissions": [
      "fs:read",
      "dialog:open"
    ]
  }]
}
```

---

## Pattern 6: Plugin Architecture

### What It Is
Tauri's functionality is extensible through plugins. Each plugin can register commands, manage state, and hook into the app lifecycle.

### Why It Works
- **Modularity** — install only what you need
- **Community** — third-party plugins extend functionality
- **Consistency** — plugins follow the same patterns as core

---

## Key Takeaways

1. **Command pattern** — discrete, typed functions replace open APIs
2. **IPC bridge** — JSON serialization with type safety on both sides
3. **State management** — Rust owns state, commands access it via DI
4. **Event system** — bidirectional push communication
5. **Permission system** — explicit capability declarations
6. **Plugin architecture** — extensible, modular, community-driven
7. The pattern: declare commands → serialize args → execute → return result

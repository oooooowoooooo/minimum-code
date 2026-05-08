# Observer

## What It Is

The Observer pattern defines a one-to-many dependency between objects. When one object (the subject)
changes state, all its dependents (observers) are notified and updated automatically. The subject
does not know who the observers are -- it just broadcasts events. Observers subscribe and unsubscribe
dynamically.

## Why It Matters in the AI Era

AI systems are event-driven by nature: a streaming LLM response emits tokens, a training loop emits
metrics, a pipeline stage completes and triggers the next one. The Observer pattern decouples the
event producer from consumers. You can add logging, progress bars, alerting, or dashboard updates
without modifying the core logic.

Streaming responses are the killer use case. The LLM does not know or care whether tokens go to a
terminal, a web socket, or a database -- it just emits them.

## Python Example

```python
from typing import Protocol, Any
from dataclasses import dataclass, field


class Observer(Protocol):
    def update(self, event: str, data: Any) -> None: ...


@dataclass
class EventEmitter:
    """Subject that broadcasts events to registered observers."""
    _observers: dict[str, list[Observer]] = field(default_factory=dict)

    def on(self, event: str, observer: Observer) -> None:
        if event not in self._observers:
            self._observers[event] = []
        self._observers[event].append(observer)

    def off(self, event: str, observer: Observer) -> None:
        if event in self._observers:
            self._observers[event].remove(observer)

    def emit(self, event: str, data: Any = None) -> None:
        for observer in self._observers.get(event, []):
            observer.update(event, data)


# Concrete observers
class TokenLogger:
    def __init__(self):
        self.tokens: list[str] = []

    def update(self, event: str, data: Any) -> None:
        if event == "token":
            self.tokens.append(data)
            print(f"[LOG] Token: {data}")


class TokenCounter:
    def __init__(self):
        self.count = 0

    def update(self, event: str, data: Any) -> None:
        if event == "token":
            self.count += 1

    def total(self) -> int:
        return self.count


# Simulated streaming LLM
class StreamingLLM(EventEmitter):
    def generate(self, prompt: str) -> None:
        # Simulate token-by-token output
        response = "Hello world this is a test".split()
        for token in response:
            self.emit("token", token)
        self.emit("done", {"total_tokens": len(response)})


# Wiring
llm = StreamingLLM()
logger = TokenLogger()
counter = TokenCounter()

llm.on("token", logger)
llm.on("token", counter)
llm.on("done", lambda event, data: print(f"[DONE] {data}"))

llm.generate("Say hello")

print(f"Total tokens: {counter.total()}")
print(f"All tokens: {logger.tokens}")
```

## TypeScript Example

```typescript
type EventHandler = (data: unknown) => void;

class EventEmitter {
  private listeners = new Map<string, EventHandler[]>();

  on(event: string, handler: EventHandler): void {
    const handlers = this.listeners.get(event) ?? [];
    handlers.push(handler);
    this.listeners.set(event, handlers);
  }

  off(event: string, handler: EventHandler): void {
    const handlers = this.listeners.get(event) ?? [];
    this.listeners.set(
      event,
      handlers.filter((h) => h !== handler),
    );
  }

  emit(event: string, data?: unknown): void {
    for (const handler of this.listeners.get(event) ?? []) {
      handler(data);
    }
  }
}

// Token logger
class TokenLogger {
  tokens: string[] = [];

  handle = (data: unknown): void => {
    const token = data as string;
    this.tokens.push(token);
    console.log(`[LOG] Token: ${token}`);
  };
}

// Token counter
class TokenCounter {
  count = 0;

  handle = (): void => {
    this.count++;
  };
}

// Simulated streaming LLM
class StreamingLLM extends EventEmitter {
  async generate(prompt: string): Promise<void> {
    const tokens = "Hello world this is a test".split(" ");
    for (const token of tokens) {
      this.emit("token", token);
      await new Promise((r) => setTimeout(r, 100)); // simulate delay
    }
    this.emit("done", { totalTokens: tokens.length });
  }
}

// Wiring
const llm = new StreamingLLM();
const logger = new TokenLogger();
const counter = new TokenCounter();

llm.on("token", logger.handle);
llm.on("token", counter.handle);
llm.on("done", (data) => console.log("[DONE]", data));

await llm.generate("Say hello");
console.log(`Total tokens: ${counter.count}`);
```

## Where You'll See It

| Project | How Observer Appears |
|---------|---------------------|
| **OpenAI SDK** | Streaming responses use event-based callbacks for `on_message`, `on_token`, etc. |
| **React** | State management (Redux, Zustand) uses observer pattern for re-rendering on state change. |
| **Node.js `EventEmitter`** | The foundation of Node's async I/O model. Streams, HTTP servers, and sockets all emit events. |
| **TensorBoard** | Training loops emit metrics; TensorBoard observes and visualizes them in real time. |
| **LangChain callbacks** | `CallbackHandler` observes chain execution events (start, end, error, token). |

## Mini-Exercises

1. **Unsubscribe**: Add an `unsubscribe` mechanism. When `llm.off("token", logger.handle)` is called,
   the logger should stop receiving tokens. Verify it works mid-stream.

2. **Once listener**: Implement `once(event, handler)` that automatically unsubscribes after the first
   event. This is useful for "done" or "error" events.

3. **Async observers**: Modify the Python `EventEmitter` so observers can be `async def`. The `emit`
   method should `await` each observer. How does error handling change?

## Key Takeaways

- Observer decouples event producers from consumers -- neither needs to know about the other.
- Observers can be added or removed at runtime, enabling dynamic behavior composition.
- Streaming LLM responses are a natural fit: tokens are events, UI/logging/monitoring are observers.
- The pattern is ubiquitous in JavaScript (EventEmitter, DOM events, RxJS) and increasingly in Python async.
- Beware of observer loops (A notifies B, B notifies A) and memory leaks (forgotten subscriptions).

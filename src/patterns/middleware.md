# Middleware

## What It Is

Middleware is a chain of processing units that sit between a request and a response. Each middleware
can inspect, modify, or short-circuit a request before passing it to the next handler. The pattern
follows a "Russian doll" model: request flows inward through each layer, the core handler processes it,
then the response flows back outward through the same layers in reverse.

## Why It Matters in the AI Era

AI applications need cross-cutting concerns that are orthogonal to core logic: authentication, rate limiting,
token counting, prompt injection detection, content filtering, logging, and cost tracking. Middleware lets
you add all of these without touching the LLM call itself. A new requirement like "log every prompt longer
than 1000 tokens" becomes adding one middleware, not rewriting every endpoint.

## Python Example

```python
from typing import Callable, Any
from dataclasses import dataclass, field
import time


@dataclass
class Request:
    prompt: str
    metadata: dict = field(default_factory=dict)


@dataclass
class Response:
    text: str
    metadata: dict = field(default_factory=dict)


# Type alias for a handler function
Handler = Callable[[Request], Response]
Middleware = Callable[[Request, Handler], Response]


def logging_middleware(request: Request, next_handler: Handler) -> Response:
    print(f"[LOG] Processing prompt: {request.prompt[:50]}...")
    start = time.time()
    response = next_handler(request)
    elapsed = time.time() - start
    print(f"[LOG] Completed in {elapsed:.2f}s")
    return response


def auth_middleware(request: Request, next_handler: Handler) -> Response:
    api_key = request.metadata.get("api_key")
    if not api_key:
        return Response(text="Unauthorized", metadata={"status": 401})
    return next_handler(request)


def token_limit_middleware(request: Request, next_handler: Handler) -> Response:
    if len(request.prompt) > 10_000:
        return Response(text="Prompt too long", metadata={"status": 413})
    return next_handler(request)


def build_chain(middlewares: list[Middleware], final_handler: Handler) -> Handler:
    """Compose middlewares into a single handler."""
    handler = final_handler
    for mw in reversed(middlewares):
        handler = lambda req, h=handler, m=mw: m(req, h)
    return handler


# Core handler
def llm_handler(request: Request) -> Response:
    return Response(text=f"AI response to: {request.prompt}")


# Assemble and use
chain = build_chain(
    [logging_middleware, auth_middleware, token_limit_middleware],
    llm_handler,
)

result = chain(
    Request(prompt="Explain quantum computing", metadata={"api_key": "abc123"})
)
print(result.text)
```

## TypeScript Example

```typescript
interface Request {
  prompt: string;
  metadata: Record<string, unknown>;
}

interface Response {
  text: string;
  metadata: Record<string, unknown>;
}

type Handler = (req: Request) => Promise<Response>;
type Middleware = (req: Request, next: Handler) => Promise<Response>;

const loggingMiddleware: Middleware = async (req, next) => {
  console.log(`[LOG] Processing prompt: ${req.prompt.slice(0, 50)}...`);
  const start = Date.now();
  const response = await next(req);
  const elapsed = Date.now() - start;
  console.log(`[LOG] Completed in ${elapsed}ms`);
  return response;
};

const authMiddleware: Middleware = async (req, next) => {
  if (!req.metadata.api_key) {
    return { text: "Unauthorized", metadata: { status: 401 } };
  }
  return next(req);
};

const tokenLimitMiddleware: Middleware = async (req, next) => {
  if (req.prompt.length > 10_000) {
    return { text: "Prompt too long", metadata: { status: 413 } };
  }
  return next(req);
};

function buildChain(middlewares: Middleware[], handler: Handler): Handler {
  let chain = handler;
  for (const mw of [...middlewares].reverse()) {
    const prev = chain;
    chain = (req) => mw(req, prev);
  }
  return chain;
}

// Core handler
async function llmHandler(req: Request): Promise<Response> {
  return { text: `AI response to: ${req.prompt}`, metadata: {} };
}

// Assemble and use
const chain = buildChain(
  [loggingMiddleware, authMiddleware, tokenLimitMiddleware],
  llmHandler,
);

const result = await chain({
  prompt: "Explain quantum computing",
  metadata: { api_key: "abc123" },
});
console.log(result.text);
```

## Where You'll See It

| Project | How Middleware Appears |
|---------|----------------------|
| **Express.js / Fastify** | `app.use(middleware)` -- the canonical middleware chain for HTTP servers. |
| **FastAPI / Starlette** | `BaseHTTPMiddleware` classes and `Depends()` for per-route middleware. |
| **Koa** | Pioneered the async middleware model with `await next()`. |
| **tRPC** | Procedures compose with `.use()` to add middleware layers to routers. |
| **LangChain** | Callback handlers act as middleware around LLM calls. |

## Mini-Exercises

1. **Add rate limiting**: Write a middleware that tracks requests per API key using a dictionary.
   If a key exceeds 100 requests per minute, return a "Too Many Requests" response.

2. **Middleware ordering**: What happens if you put `auth_middleware` after `logging_middleware`?
   Will unauthenticated requests still get logged? Rewrite the chain to log everything but
   only process authenticated requests.

3. **Async middleware**: Rewrite the Python example to use `async def` handlers and `await next_handler(request)`.
   How does the `build_chain` function need to change?

## Key Takeaways

- Middleware decomposes cross-cutting concerns (logging, auth, rate limiting) into independent, composable units.
- Each middleware decides: handle the request, pass it along, or short-circuit.
- Order matters: the sequence of middleware determines which checks run first.
- The pattern is identical across languages -- once you learn it in Express, you understand it in FastAPI, Koa, or tRPC.
- In AI apps, middleware is the natural place for prompt validation, cost tracking, and content filtering.

# Dependency Injection

## What It Is

Dependency Injection (DI) is a technique where an object receives its dependencies from an external source
rather than creating them itself. Instead of a class instantiating what it needs, something outside hands
those pieces in. This inverts the control of dependency creation.

## Why It Matters in the AI Era

Modern AI applications compose many services: LLM clients, vector databases, embedding models, caching layers,
and observability tools. DI lets you swap any of these without rewriting core logic. When a new model drops
or you need to switch providers, you change one wiring point, not every file.

Testability is the other half. With DI, you can inject mock LLMs that return fixed responses, letting you
write deterministic tests against non-deterministic systems.

## Python Example

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass


class LLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str: ...


class OpenAIClient(LLMClient):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate(self, prompt: str) -> str:
        # Real API call would go here
        return f"OpenAI response to: {prompt}"


class MockLLMClient(LLMClient):
    def __init__(self, fixed_response: str = "mock response"):
        self.fixed_response = fixed_response

    def generate(self, prompt: str) -> str:
        return self.fixed_response


@dataclass
class ChatbotService:
    llm: LLMClient  # injected dependency

    def chat(self, user_input: str) -> str:
        return self.llm.generate(user_input)


# Wiring: external code decides which implementation to use
service = ChatbotService(llm=OpenAIClient(api_key="sk-..."))
print(service.chat("Hello"))

# Testing: swap in mock
test_service = ChatbotService(llm=MockLLMClient("expected"))
assert test_service.chat("anything") == "expected"
```

## TypeScript Example

```typescript
interface LLMClient {
  generate(prompt: string): Promise<string>;
}

class OpenAIClient implements LLMClient {
  constructor(private apiKey: string) {}

  async generate(prompt: string): Promise<string> {
    // Real API call would go here
    return `OpenAI response to: ${prompt}`;
  }
}

class MockLLMClient implements LLMClient {
  constructor(private fixedResponse = "mock response") {}

  async generate(prompt: string): Promise<string> {
    return this.fixedResponse;
  }
}

class ChatbotService {
  constructor(private llm: LLMClient) {} // injected dependency

  async chat(input: string): Promise<string> {
    return this.llm.generate(input);
  }
}

// Wiring
const service = new ChatbotService(new OpenAIClient("sk-..."));
const result = await service.chat("Hello");

// Testing
const testService = new ChatbotService(new MockLLMClient("expected"));
const testResult = await testService.chat("anything");
console.assert(testResult === "expected");
```

## Where You'll See It

| Project | How DI Appears |
|---------|---------------|
| **FastAPI** | Path operation functions declare dependencies via `Depends()`. FastAPI resolves and injects them at runtime. |
| **tRPC** | Context objects carry injected services through middleware chains to procedures. |
| **LangChain** | LLM, embeddings, and vector store instances are injected into chains and agents. |
| **NestJS** | Constructor-based DI is the core architecture. Modules declare providers that get injected. |
| **Spring Boot** | The classic DI container. `@Autowired` and `@Inject` annotations wire beans together. |

## Mini-Exercises

1. **Refactor for testability**: Take this function and refactor it to use DI so you can test the email
   sending without a real SMTP server:
   ```python
   def send_welcome_email(user_email: str):
       import smtplib
       server = smtplib.SMTP("smtp.example.com")
       server.sendmail("bot@example.com", user_email, "Welcome!")
       server.quit()
   ```

2. **Implement a provider**: Create a `CacheProvider` interface with `get(key)` and `set(key, value)` methods.
   Implement `RedisCache` and `InMemoryCache`. Inject the provider into a `UserService`.

3. **Constructor vs method injection**: Rewrite the `ChatbotService` example to use method injection
   (pass the dependency to each method call instead of the constructor). Discuss trade-offs.

## Key Takeaways

- DI separates "what to use" from "how to use it" -- classes declare what they need, external code decides the implementation.
- It makes testing trivial: swap real implementations for mocks or fakes.
- Frameworks like FastAPI and NestJS automate DI, but the principle works without any framework.
- In AI applications, DI is essential for swapping LLM providers, embedding models, and storage backends.
- The cost is indirection: tracing where a dependency comes from requires following the wiring code.

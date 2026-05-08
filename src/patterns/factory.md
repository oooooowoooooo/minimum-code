# Factory

## What It Is

The Factory pattern provides an interface for creating objects without specifying their exact class.
A factory function or method decides which concrete class to instantiate based on input parameters.
The caller receives a common interface and does not need to know which implementation was created.

There are two main variants:
- **Factory Function**: A standalone function that returns an instance.
- **Factory Method**: A method on a class that subclasses can override.

## Why It Matters in the AI Era

AI applications juggle multiple model providers, embedding backends, and data sources -- each with
different APIs, authentication, and behavior. A factory centralizes the creation logic so callers
ask for "an LLM client" or "a vector store" by name, and the factory returns the right implementation.
When you add a new provider, you add one class and one branch in the factory. Nothing else changes.

## Python Example

```python
from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, text: str) -> list[float]: ...

    @abstractmethod
    def dimensions(self) -> int: ...


class OpenAIEmbeddings(EmbeddingProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def embed(self, text: str) -> list[float]:
        # Real API call here
        return [0.1, 0.2, 0.3]  # simplified

    def dimensions(self) -> int:
        return 1536


class CohereEmbeddings(EmbeddingProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def embed(self, text: str) -> list[float]:
        return [0.4, 0.5, 0.6]

    def dimensions(self) -> int:
        return 1024


class LocalEmbeddings(EmbeddingProvider):
    def __init__(self, model_path: str):
        self.model_path = model_path

    def embed(self, text: str) -> list[float]:
        return [0.7, 0.8, 0.9]

    def dimensions(self) -> int:
        return 768


# Factory function: single creation point
def create_embedding_provider(
    provider: str,
    api_key: str = "",
    model_path: str = "",
) -> EmbeddingProvider:
    providers = {
        "openai": lambda: OpenAIEmbeddings(api_key),
        "cohere": lambda: CohereEmbeddings(api_key),
        "local": lambda: LocalEmbeddings(model_path),
    }

    if provider not in providers:
        available = ", ".join(providers)
        raise ValueError(f"Unknown provider '{provider}'. Choose from: {available}")

    return providers[provider]()


# Usage: caller doesn't know which class was created
embedder = create_embedding_provider("openai", api_key="sk-...")
vector = embedder.embed("Hello world")
print(f"Dimensions: {embedder.dimensions()}")
```

## TypeScript Example

```typescript
interface EmbeddingProvider {
  embed(text: string): Promise<number[]>;
  dimensions(): number;
}

class OpenAIEmbeddings implements EmbeddingProvider {
  constructor(private apiKey: string) {}

  async embed(text: string): Promise<number[]> {
    return [0.1, 0.2, 0.3];
  }

  dimensions(): number {
    return 1536;
  }
}

class CohereEmbeddings implements EmbeddingProvider {
  constructor(private apiKey: string) {}

  async embed(text: string): Promise<number[]> {
    return [0.4, 0.5, 0.6];
  }

  dimensions(): number {
    return 1024;
  }
}

class LocalEmbeddings implements EmbeddingProvider {
  constructor(private modelPath: string) {}

  async embed(text: string): Promise<number[]> {
    return [0.7, 0.8, 0.9];
  }

  dimensions(): number {
    return 768;
  }
}

// Factory function
interface EmbeddingConfig {
  provider: "openai" | "cohere" | "local";
  apiKey?: string;
  modelPath?: string;
}

function createEmbeddingProvider(config: EmbeddingConfig): EmbeddingProvider {
  switch (config.provider) {
    case "openai":
      if (!config.apiKey) throw new Error("apiKey required for OpenAI");
      return new OpenAIEmbeddings(config.apiKey);
    case "cohere":
      if (!config.apiKey) throw new Error("apiKey required for Cohere");
      return new CohereEmbeddings(config.apiKey);
    case "local":
      if (!config.modelPath) throw new Error("modelPath required for local");
      return new LocalEmbeddings(config.modelPath);
    default:
      throw new Error(`Unknown provider: ${config.provider}`);
  }
}

// Usage
const embedder = createEmbeddingProvider({
  provider: "openai",
  apiKey: "sk-...",
});
const vector = await embedder.embed("Hello world");
console.log(`Dimensions: ${embedder.dimensions()}`);
```

## Where You'll See It

| Project | How Factory Appears |
|---------|-------------------|
| **Django ORM** | `Model.objects.create()` is a factory that builds model instances from database rows. |
| **React** | `React.createElement()` is a factory that creates virtual DOM elements. |
| **PyTorch** | `torch.optim.Adam(model.parameters())` is a factory for optimizer instances. |
| **Vitest / Jest** | `describe()` and `it()` are factories that create test suite and test case objects. |
| **LangChain** | `ChatOpenAI.from_model("gpt-4")` and similar class methods are factory methods. |

## Mini-Exercises

1. **Registry factory**: Instead of an `if/elif` chain, use a dictionary registry. Add a
   `register(name, class)` function so new providers can register themselves at import time.

2. **Config-driven factory**: Read a JSON config file and pass its contents to the factory. The config
   specifies `provider`, `api_key`, and optional `model_path`. Validate required fields before creation.

3. **Factory with defaults**: Modify the factory so that if no provider is specified, it picks a
   sensible default based on which API keys are available in environment variables.

## Key Takeaways

- Factories centralize object creation logic, so adding new implementations requires changes in one place.
- The caller programs against an interface and does not need to know which concrete class was created.
- Factory functions are preferred over complex class hierarchies in modern Python and TypeScript.
- In AI applications, factories handle provider selection (OpenAI vs Anthropic vs local) cleanly.
- Use factories when creation logic involves validation, configuration, or conditional branching.

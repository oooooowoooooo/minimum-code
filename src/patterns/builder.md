# Builder

## What It Is

The Builder pattern separates the construction of a complex object from its representation. Instead of
a constructor with dozens of parameters, you use a step-by-step builder that lets you set only what you
need, with sensible defaults for the rest. The builder validates the final state and produces the
finished object.

## Why It Matters in the AI Era

AI API calls have many optional parameters: model, temperature, max_tokens, top_p, stop sequences,
response format, tools, and more. Builders handle this complexity elegantly. They also make code
self-documenting -- `builder.withTemperature(0.7).withMaxTokens(1000)` reads like English.

Configuration objects for ML pipelines (data preprocessing, feature engineering, model selection) benefit
the same way: each step has its own builder that validates constraints before producing a pipeline.

## Python Example

```python
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class LLMConfig:
    model: str
    temperature: float = 0.7
    max_tokens: int = 1024
    top_p: float = 1.0
    stop: tuple[str, ...] = ()
    response_format: Optional[str] = None


class LLMConfigBuilder:
    def __init__(self, model: str):
        self._model = model
        self._temperature = 0.7
        self._max_tokens = 1024
        self._top_p = 1.0
        self._stop: list[str] = []
        self._response_format: Optional[str] = None

    def with_temperature(self, temp: float) -> "LLMConfigBuilder":
        if not 0.0 <= temp <= 2.0:
            raise ValueError(f"Temperature must be 0-2, got {temp}")
        self._temperature = temp
        return self

    def with_max_tokens(self, tokens: int) -> "LLMConfigBuilder":
        if tokens < 1:
            raise ValueError(f"Max tokens must be positive, got {tokens}")
        self._max_tokens = tokens
        return self

    def with_top_p(self, top_p: float) -> "LLMConfigBuilder":
        if not 0.0 <= top_p <= 1.0:
            raise ValueError(f"Top-p must be 0-1, got {top_p}")
        self._top_p = top_p
        return self

    def with_stop(self, *sequences: str) -> "LLMConfigBuilder":
        self._stop.extend(sequences)
        return self

    def with_json_response(self) -> "LLMConfigBuilder":
        self._response_format = "json_object"
        return self

    def build(self) -> LLMConfig:
        return LLMConfig(
            model=self._model,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
            top_p=self._top_p,
            stop=tuple(self._stop),
            response_format=self._response_format,
        )


# Usage: readable, chainable, validated
config = (
    LLMConfigBuilder("gpt-4")
    .with_temperature(0.3)
    .with_max_tokens(2000)
    .with_stop("\n\n", "END")
    .with_json_response()
    .build()
)

print(config)  # LLMConfig(model='gpt-4', temperature=0.3, ...)
```

## TypeScript Example

```typescript
interface LLMConfig {
  readonly model: string;
  readonly temperature: number;
  readonly maxTokens: number;
  readonly topP: number;
  readonly stop: string[];
  readonly responseFormat?: "json_object" | "text";
}

class LLMConfigBuilder {
  private temperature = 0.7;
  private maxTokens = 1024;
  private topP = 1.0;
  private stop: string[] = [];
  private responseFormat?: "json_object" | "text";

  constructor(private model: string) {}

  withTemperature(temp: number): this {
    if (temp < 0 || temp > 2) {
      throw new Error(`Temperature must be 0-2, got ${temp}`);
    }
    this.temperature = temp;
    return this;
  }

  withMaxTokens(tokens: number): this {
    if (tokens < 1) throw new Error(`Max tokens must be positive, got ${tokens}`);
    this.maxTokens = tokens;
    return this;
  }

  withTopP(topP: number): this {
    if (topP < 0 || topP > 1) throw new Error(`Top-p must be 0-1, got ${topP}`);
    this.topP = topP;
    return this;
  }

  withStop(...sequences: string[]): this {
    this.stop.push(...sequences);
    return this;
  }

  withJsonResponse(): this {
    this.responseFormat = "json_object";
    return this;
  }

  build(): LLMConfig {
    if (!this.model) throw new Error("Model is required");
    return Object.freeze({
      model: this.model,
      temperature: this.temperature,
      maxTokens: this.maxTokens,
      topP: this.topP,
      stop: [...this.stop],
      responseFormat: this.responseFormat,
    });
  }
}

// Usage
const config = new LLMConfigBuilder("gpt-4")
  .withTemperature(0.3)
  .withMaxTokens(2000)
  .withStop("\n\n", "END")
  .withJsonResponse()
  .build();

console.log(config);
```

## Where You'll See It

| Project | How Builder Appears |
|---------|-------------------|
| **OpenAI SDK** | Client and request builders for configuring API calls with many optional parameters. |
| **Elasticsearch clients** | Query builders that construct complex search DSL step by step. |
| **SQLAlchemy** | The query builder pattern constructs SQL from chained method calls. |
| **React Testing Library** | `render()` options are built incrementally for complex test setups. |
| **Docker / Kubernetes** | Dockerfile multi-stage builds and Kubernetes manifest generation tools use builder patterns. |

## Mini-Exercises

1. **Pipeline builder**: Create a `DataPipelineBuilder` with methods like `withSource()`, `withTransform()`,
   `withSink()`, and `withBatchSize()`. The `build()` method should validate that source and sink are set.

2. **Fluent validation**: Add a `validate()` method to `LLMConfigBuilder` that checks for invalid combinations
   (e.g., `temperature=0` with `top_p < 1.0` is redundant). Should validation happen in `build()` or `validate()`?

3. **Immutable builder**: The Python example uses `frozen=True` dataclass. Why? What happens if `LLMConfig`
   is mutable and two API calls share the same config?

## Key Takeaways

- Builders turn "constructor with 15 parameters" into readable, chainable method calls.
- Validation logic lives in the builder, not scattered across constructors or callers.
- The fluent interface (`return self`) enables method chaining that reads top-to-bottom.
- Builders are especially valuable for API wrappers, configuration objects, and pipeline definitions.
- In AI applications, builders handle the explosion of LLM parameters and pipeline configurations.

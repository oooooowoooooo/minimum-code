# Strategy

## What It Is

The Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable.
The context (the object that uses the algorithm) holds a reference to a strategy interface and delegates
the work to whichever concrete strategy is plugged in. The context does not know or care which strategy
it is using.

## Why It Matters in the AI Era

AI systems face constant model churn: GPT-4 today, Claude tomorrow, an open-source model next week.
The Strategy pattern lets you swap the inference backend without changing the application logic.
Similarly, different tasks need different strategies: summarization, classification, and extraction
each require distinct prompting approaches, but the surrounding pipeline stays the same.

## Python Example

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass


class PricingStrategy(ABC):
    """Calculate the cost of an API call based on token usage."""

    @abstractmethod
    def calculate(self, input_tokens: int, output_tokens: int) -> float: ...


class OpenAIPricing(PricingStrategy):
    def __init__(self, input_per_1k: float = 0.005, output_per_1k: float = 0.015):
        self.input_per_1k = input_per_1k
        self.output_per_1k = output_per_1k

    def calculate(self, input_tokens: int, output_tokens: int) -> float:
        return (input_tokens / 1000 * self.input_per_1k
                + output_tokens / 1000 * self.output_per_1k)


class AnthropicPricing(PricingStrategy):
    def __init__(self, input_per_1k: float = 0.008, output_per_1k: float = 0.024):
        self.input_per_1k = input_per_1k
        self.output_per_1k = output_per_1k

    def calculate(self, input_tokens: int, output_tokens: int) -> float:
        return (input_tokens / 1000 * self.input_per_1k
                + output_tokens / 1000 * self.output_per_1k)


class FreeTierPricing(PricingStrategy):
    def calculate(self, input_tokens: int, output_tokens: int) -> float:
        return 0.0


@dataclass
class CostTracker:
    strategy: PricingStrategy  # pluggable strategy
    total_cost: float = 0.0

    def record_call(self, input_tokens: int, output_tokens: int) -> float:
        cost = self.strategy.calculate(input_tokens, output_tokens)
        self.total_cost += cost
        return cost


# Switch strategies at runtime
tracker = CostTracker(strategy=OpenAIPricing())
print(tracker.record_call(500, 200))  # OpenAI rate

tracker.strategy = AnthropicPricing()
print(tracker.record_call(500, 200))  # Anthropic rate

tracker.strategy = FreeTierPricing()
print(tracker.record_call(500, 200))  # $0.00
```

## TypeScript Example

```typescript
interface PricingStrategy {
  calculate(inputTokens: number, outputTokens: number): number;
}

class OpenAIPricing implements PricingStrategy {
  constructor(
    private inputPer1k = 0.005,
    private outputPer1k = 0.015,
  ) {}

  calculate(inputTokens: number, outputTokens: number): number {
    return (
      (inputTokens / 1000) * this.inputPer1k +
      (outputTokens / 1000) * this.outputPer1k
    );
  }
}

class AnthropicPricing implements PricingStrategy {
  constructor(
    private inputPer1k = 0.008,
    private outputPer1k = 0.024,
  ) {}

  calculate(inputTokens: number, outputTokens: number): number {
    return (
      (inputTokens / 1000) * this.inputPer1k +
      (outputTokens / 1000) * this.outputPer1k
    );
  }
}

class FreeTierPricing implements PricingStrategy {
  calculate(): number {
    return 0;
  }
}

class CostTracker {
  private totalCost = 0;
  constructor(public strategy: PricingStrategy) {}

  recordCall(inputTokens: number, outputTokens: number): number {
    const cost = this.strategy.calculate(inputTokens, outputTokens);
    this.totalCost += cost;
    return cost;
  }

  getTotal(): number {
    return this.totalCost;
  }
}

// Switch strategies at runtime
const tracker = new CostTracker(new OpenAIPricing());
console.log(tracker.recordCall(500, 200));

tracker.strategy = new AnthropicPricing();
console.log(tracker.recordCall(500, 200));
```

## Where You'll See It

| Project | How Strategy Appears |
|---------|---------------------|
| **LangChain** | `ChatModel`, `Embeddings`, `VectorStore` are all strategy interfaces with many implementations. |
| **Passport.js** | Authentication strategies (local, JWT, OAuth) are interchangeable via the strategy interface. |
| **Python `sorted()`** | The `key` parameter is a strategy for comparison -- you pass a function, not subclass anything. |
| **Kubernetes schedulers** | Scheduling strategies (round-robin, least-loaded, bin-packing) are pluggable. |
| **TensorFlow / PyTorch** | Optimizers (SGD, Adam, RMSProp) are strategies plugged into the training loop. |

## Mini-Exercises

1. **Retry strategy**: Define a `RetryStrategy` interface with `shouldRetry(attempt: int, error: Exception) -> bool`
   and `delay(attempt: int) -> float`. Implement `ExponentialBackoff`, `FixedDelay`, and `NoRetry`.

2. **Prompt strategy**: Create a `PromptStrategy` interface for different LLM tasks (summarize, translate, extract).
   Each strategy takes raw text and returns a formatted prompt. Build a `TaskRunner` that accepts any strategy.

3. **Runtime selection**: How would you let users select a strategy via a config file or CLI flag? Implement
   a strategy registry that maps string names to strategy instances.

## Key Takeaways

- Strategy encapsulates "what varies" behind a stable interface, so the caller does not change.
- It eliminates long `if/elif/else` chains for algorithm selection.
- Strategies can be swapped at runtime based on config, user input, or A/B test assignments.
- In AI systems, strategy handles model selection, pricing, retry logic, and prompt formatting.
- The pattern is so common in Python that it often uses plain functions instead of classes.

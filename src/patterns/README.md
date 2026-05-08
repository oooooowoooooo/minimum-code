# Industrial Design Patterns

Eight design patterns that appear across all top GitHub projects. Each pattern solves a specific
structural problem that arises repeatedly in production codebases. This module covers them with
working examples in both Python and TypeScript.

## Patterns Overview

| Pattern | One-Line Summary |
|---------|-----------------|
| [Dependency Injection](dependency_injection.md) | Receive dependencies from outside, don't create them yourself |
| [Middleware](middleware.md) | Chain processing units between request and response |
| [Builder](builder.md) | Construct complex objects step by step with a fluent interface |
| [Strategy](strategy.md) | Swap interchangeable algorithms behind a common interface |
| [Observer](observer.md) | Broadcast events to dynamically registered listeners |
| [Factory](factory.md) | Create objects without specifying the exact class |
| [Repository](repository.md) | Abstract data access behind a collection-like interface |
| [Pipeline](pipeline.md) | Chain processing stages where output feeds the next input |

## Where Each Pattern Appears

This table shows which major open-source projects and frameworks use each pattern:

| Pattern | Express | FastAPI | LangChain | React | NestJS | Django | Next.js | tRPC | Spring | Prisma |
|---------|:-------:|:-------:|:---------:|:-----:|:------:|:------:|:-------:|:----:|:------:|:------:|
| Dependency Injection | | x | x | | x | | | x | x | |
| Middleware | x | x | | | x | x | x | x | x | |
| Builder | | | x | | | x | | | x | x |
| Strategy | x | x | x | | x | | | | x | |
| Observer | x | | x | x | | | | | | |
| Factory | | x | x | x | x | x | x | | x | x |
| Repository | | | x | | x | x | | | x | x |
| Pipeline | | | x | | | | | | | |

## How to Use This Module

Each pattern file follows the same structure:

1. **What It Is** -- A clear, concise definition
2. **Why It Matters in the AI Era** -- Relevance to modern AI/ML applications
3. **Python Example** -- Working code you can run
4. **TypeScript Example** -- Working code you can run
5. **Where You'll See It** -- Real projects that use the pattern
6. **Mini-Exercises** -- Practice problems to deepen understanding
7. **Key Takeaways** -- The essential points to remember

## Suggested Reading Order

For beginners, read in this order (simplest to most complex):

1. **Factory** -- simplest creation pattern, easy to grasp
2. **Strategy** -- introduces polymorphism in a practical way
3. **Observer** -- introduces event-driven thinking
4. **Middleware** -- builds on the chain concept
5. **Builder** -- fluent interfaces and construction validation
6. **Pipeline** -- sequential processing composition
7. **Repository** -- data access abstraction
8. **Dependency Injection** -- ties many patterns together

## Patterns in Combination

Real codebases rarely use one pattern in isolation. Common combinations:

- **DI + Repository**: Inject different repository implementations for testing vs production
- **Middleware + Pipeline**: Middleware for cross-cutting concerns, pipeline for core processing
- **Factory + Strategy**: Factory creates the right strategy based on configuration
- **Observer + Pipeline**: Pipeline stages emit events that observers track for monitoring
- **Builder + Factory**: Builder constructs complex configuration, factory creates the service from it

## Key Insight

These patterns are not academic exercises. They are the structural vocabulary of every major
open-source project. When you read the source code of FastAPI, LangChain, or Next.js, you will
see these patterns everywhere. Learning them is learning to read production code.

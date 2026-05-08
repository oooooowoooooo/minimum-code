# Pipeline

## What It Is

The Pipeline pattern chains a sequence of processing stages where each stage's output becomes the next
stage's input. Each stage is a self-contained unit that performs one transformation. Pipelines can be
linear (A -> B -> C), branching (A -> [B, C]), or fan-out/fan-in (A -> [B, C, D] -> E). The pattern
promotes single-responsibility and composability.

## Why It Matters in the AI Era

AI workflows are inherently sequential: preprocess input -> build prompt -> call LLM -> parse response ->
validate output -> format result. Each step is a distinct concern that might need replacement, testing,
or reuse. Pipelines make these steps explicit, testable, and rearrangeable.

RAG (Retrieval-Augmented Generation) is a textbook pipeline: embed query -> search vector store ->
retrieve documents -> construct prompt -> call LLM -> return answer. Each stage can be swapped or
configured independently.

## Python Example

```python
from typing import Any, Callable, TypeVar
from dataclasses import dataclass, field

T = TypeVar("T")


@dataclass
class PipelineContext:
    """Shared state that flows through the pipeline."""
    query: str
    documents: list[str] = field(default_factory=list)
    prompt: str = ""
    response: str = ""
    metadata: dict = field(default_factory=dict)


class PipelineStage:
    """A single processing step."""
    def __init__(self, name: str, fn: Callable[[PipelineContext], PipelineContext]):
        self.name = name
        self.fn = fn

    def execute(self, context: PipelineContext) -> PipelineContext:
        return self.fn(context)


class Pipeline:
    def __init__(self, name: str = "pipeline"):
        self.name = name
        self.stages: list[PipelineStage] = []

    def add_stage(self, name: str, fn: Callable[[PipelineContext], PipelineContext]) -> "Pipeline":
        self.stages.append(PipelineStage(name, fn))
        return self  # fluent interface

    def execute(self, context: PipelineContext) -> PipelineContext:
        for stage in self.stages:
            context = stage.execute(context)
        return context


# Concrete stages for a RAG pipeline
def normalize_query(ctx: PipelineContext) -> PipelineContext:
    ctx.query = ctx.query.strip().lower()
    ctx.metadata["normalized"] = True
    return ctx


def retrieve_documents(ctx: PipelineContext) -> PipelineContext:
    # Simulate vector search
    ctx.documents = [
        f"Document 1 related to '{ctx.query}'",
        f"Document 2 related to '{ctx.query}'",
    ]
    return ctx


def build_prompt(ctx: PipelineContext) -> PipelineContext:
    context_text = "\n".join(ctx.documents)
    ctx.prompt = (
        f"Context:\n{context_text}\n\n"
        f"Question: {ctx.query}\n"
        f"Answer based on the context above:"
    )
    return ctx


def call_llm(ctx: PipelineContext) -> PipelineContext:
    # Simulate LLM call
    ctx.response = f"Answer to '{ctx.query}' based on {len(ctx.documents)} documents."
    return ctx


# Assemble and run
rag_pipeline = (
    Pipeline("RAG")
    .add_stage("normalize", normalize_query)
    .add_stage("retrieve", retrieve_documents)
    .add_stage("build_prompt", build_prompt)
    .add_stage("llm_call", call_llm)
)

result = rag_pipeline.execute(PipelineContext(query="  What is dependency injection?  "))
print(f"Prompt: {result.prompt}")
print(f"Response: {result.response}")
print(f"Metadata: {result.metadata}")
```

## TypeScript Example

```typescript
interface PipelineContext {
  query: string;
  documents: string[];
  prompt: string;
  response: string;
  metadata: Record<string, unknown>;
}

type StageFn = (ctx: PipelineContext) => Promise<PipelineContext> | PipelineContext;

interface Stage {
  name: string;
  execute: StageFn;
}

class Pipeline {
  private stages: Stage[] = [];

  constructor(private name = "pipeline") {}

  addStage(name: string, fn: StageFn): this {
    this.stages.push({ name, execute: fn });
    return this;
  }

  async execute(context: PipelineContext): Promise<PipelineContext> {
    let ctx = context;
    for (const stage of this.stages) {
      ctx = await stage.execute(ctx);
    }
    return ctx;
  }
}

// Concrete stages for a RAG pipeline
function normalizeQuery(ctx: PipelineContext): PipelineContext {
  return { ...ctx, query: ctx.query.trim().toLowerCase(), metadata: { ...ctx.metadata, normalized: true } };
}

async function retrieveDocuments(ctx: PipelineContext): Promise<PipelineContext> {
  const documents = [
    `Document 1 related to '${ctx.query}'`,
    `Document 2 related to '${ctx.query}'`,
  ];
  return { ...ctx, documents };
}

function buildPrompt(ctx: PipelineContext): PipelineContext {
  const contextText = ctx.documents.join("\n");
  return {
    ...ctx,
    prompt: `Context:\n${contextText}\n\nQuestion: ${ctx.query}\nAnswer based on the context above:`,
  };
}

async function callLLM(ctx: PipelineContext): Promise<PipelineContext> {
  return {
    ...ctx,
    response: `Answer to '${ctx.query}' based on ${ctx.documents.length} documents.`,
  };
}

// Assemble and run
const ragPipeline = new Pipeline("RAG")
  .addStage("normalize", normalizeQuery)
  .addStage("retrieve", retrieveDocuments)
  .addStage("build_prompt", buildPrompt)
  .addStage("llm_call", callLLM);

const result = await ragPipeline.execute({
  query: "  What is dependency injection?  ",
  documents: [],
  prompt: "",
  response: "",
  metadata: {},
});

console.log(`Prompt: ${result.prompt}`);
console.log(`Response: ${result.response}`);
```

## Where You'll See It

| Project | How Pipeline Appears |
|---------|---------------------|
| **LangChain** | Chains and LCEL (LangChain Expression Language) are pipelines: `chain = prompt | llm | parser`. |
| **GitHub Actions** | CI/CD pipelines chain steps: build -> test -> deploy. |
| **RxJS / xstream** | Reactive pipelines chain operators: `source.pipe(filter(), map(), reduce())`. |
| **ETL frameworks** | Apache Beam, Luigi, and Prefect orchestrate data pipelines. |
| **Unix pipes** | The original pipeline: `cat file | grep error | sort | uniq -c`. |

## Mini-Exercises

1. **Branching pipeline**: Modify the `Pipeline` class to support branching. Given a predicate function,
   route the context to different stage chains based on a condition (e.g., short queries go to one LLM,
   long queries go to another).

2. **Error handling**: Add `on_error` callbacks to each stage. If a stage raises an exception, the
   callback decides whether to retry, skip, or abort the pipeline.

3. **Pipeline composition**: Create a `ComposePipeline` that takes two pipelines and chains them:
   the output context of the first becomes the input of the second. This lets you build pipelines
   from smaller pipelines.

## Key Takeaways

- Pipelines decompose complex workflows into sequential, single-responsibility stages.
- Each stage is independently testable, replaceable, and reusable.
- The pattern maps directly to AI workflows: preprocess -> prompt -> LLM -> parse -> validate.
- RAG, summarization, and multi-step reasoning are all natural pipelines.
- Unlike middleware (which wraps a central handler), pipelines are the central flow -- stages transform data in sequence.

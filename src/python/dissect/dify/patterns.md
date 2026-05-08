# Dify Core Design Patterns

## Pattern 1: Workflow Engine (DAG Execution)

**Intent:** Execute a directed acyclic graph of processing nodes where each
node runs when its inputs are ready.

**Structure:**
```
Workflow
  nodes: list[Node]           -- processing units
  edges: list[Edge]           -- connections between nodes
  variables: dict             -- global variable store
  execute() -> dict           -- run the workflow, return outputs
```

**Execution algorithm:**
```
1. Build adjacency list from edges
2. Compute in-degree for each node
3. Initialize queue with nodes that have in-degree 0
4. While queue is not empty:
   a. Dequeue a node
   b. Resolve its input variables from upstream outputs
   c. Execute the node
   d. Store node output in the variable store
   e. Decrement in-degree of downstream nodes
   f. If a downstream node's in-degree reaches 0, enqueue it
5. Return outputs from terminal nodes (out-degree 0)
```

**Why it matters:** DAG execution is the backbone of workflow systems. It
enables parallelism (independent branches), determinism (fixed execution order),
and composability (nodes are self-contained units).

**Key insight:** The DAG is data, not code. It can be serialized as JSON,
stored in a database, versioned, and shared. This is what makes visual
editors possible -- the UI writes a JSON graph, the engine executes it.

---

## Pattern 2: Node Pattern (Workflow Building Block)

**Intent:** Define a self-contained processing unit with typed inputs, typed
outputs, and a clear execution contract.

**Structure:**
```
Node
  id: str                     -- unique identifier
  type: str                   -- "llm", "http", "code", "if_else", etc.
  config: dict                -- node-specific configuration
  input_ports: list[Port]     -- what this node expects
  output_ports: list[Port]    -- what this node produces
  execute(inputs) -> outputs  -- run the node
```

**Why it matters:** Nodes are the atoms of the workflow. Each node type
encapsulates a specific capability:
- `LLMNode` -- send a prompt to a model, get a response
- `HTTPNode` -- make an HTTP request
- `CodeNode` -- run arbitrary Python/JavaScript
- `IfElseNode` -- conditional branching
- `VariableNode` -- assign or transform variables
- `RetrievalNode` -- query a knowledge base

**Design rule:** Nodes should be stateless. All state lives in the variable
store. This makes nodes testable in isolation and reusable across workflows.

---

## Pattern 3: Variable System (Data Flow Between Nodes)

**Intent:** Enable data to flow between nodes through a centralized variable
store with template-based resolution.

**Mechanism:**
```
1. Node A executes and produces output: {"result": "hello world"}
2. This is stored as: variables["node_a.result"] = "hello world"
3. Node B has a config: prompt = "Summarize: {{node_a.result}}"
4. Before Node B executes, the resolver replaces {{node_a.result}} with "hello world"
5. Node B receives: prompt = "Summarize: hello world"
```

**Template syntax:**
```
{{node_id.field}}          -- access a specific output field
{{node_id.field | upper}}  -- apply a filter (pipe syntax)
{{#if node_id.flag}}...{{/if}}  -- conditional rendering
```

**Why it matters:** The variable system is the glue that connects nodes. Without
it, nodes would need direct references to each other, creating tight coupling.
Template strings are human-readable, debuggable, and support lazy resolution.

**Key insight:** Variable resolution happens at runtime, not at graph-build time.
This means the same workflow template can work with different data inputs.

---

## Pattern 4: Plugin System (Extensibility)

**Intent:** Allow third-party extensions to add capabilities to the platform
without modifying core code.

**Structure:**
```
Plugin
  name: str                   -- "web_search"
  version: str                -- "1.0.0"
  type: str                   -- "model" | "tool" | "extension"
  interface: dict             -- declared input/output schema
  install() -> None           -- register with the platform
  execute(inputs) -> outputs  -- plugin logic
```

**Plugin lifecycle:**
```
1. Platform discovers plugins (scan directory, registry, or manifest)
2. Platform loads plugin metadata (name, type, interface)
3. Platform registers plugin in the appropriate registry
4. When a workflow node references a plugin, platform instantiates it
5. Plugin executes with the node's inputs
6. Plugin output is stored in the variable store
```

**Why it matters:** A platform without plugins is a walled garden. Plugins
allow:
- New LLM providers (Ollama, vLLM, custom endpoints)
- New tools (databases, APIs, file systems)
- Custom logic (business rules, data transformations)

**Design rule:** Plugins must declare their interface upfront. The platform
validates inputs against the interface before execution. This prevents
runtime errors from propagating through the workflow.

---

## Pattern 5: App Pattern (Application Types)

**Intent:** Specialize the generic workflow engine into distinct application
types with tailored UI and execution behavior.

**App types and their specializations:**

| Type | Input | Output | State | UI |
|------|-------|--------|-------|-----|
| Chatbot | User message | Bot response | Conversation history | Chat interface |
| Agent | User message | Final answer + tool traces | Conversation + tool state | Chat interface |
| Workflow | JSON payload | JSON result | None (stateless) | Trigger button |
| Text Generation | Prompt text | Generated text | None | Text area |
| Chatflow | User message | Bot response | Conversation history | Chat interface |

**Why it matters:** Users think in terms of "I want a chatbot" or "I want an
agent," not "I want a workflow with these nodes." The App Pattern maps user
intent to the underlying workflow engine.

**Key insight:** All app types are workflows underneath. A chatbot is a workflow
with a memory-management node and a chat-input node. An agent is a workflow
with a tool-calling loop. The App Pattern is a UX abstraction, not a
fundamentally different execution model.

---

## Pattern 6: Provider Abstraction Pattern

**Intent:** Abstract away differences between LLM providers behind a common
interface.

**Structure:**
```
LLMProvider
  name: str                   -- "openai", "anthropic", "ollama"
  models: list[str]           -- available model IDs
  chat(messages, config)      -- send a chat completion request
  stream(messages, config)    -- stream a chat completion response
  embed(texts)                -- generate embeddings
```

**Why it matters:** Users should not be locked into one LLM provider. The
provider abstraction allows:
- Switching providers by changing config, not code
- Comparing providers on the same workflow
- Using local models (Ollama) and cloud models (OpenAI) interchangeably

---

## Pattern 7: Retrieval-Augmented Generation Pattern

**Intent:** Augment LLM responses with relevant context from a knowledge base.

**Flow:**
```
1. User asks a question
2. Question is embedded into a vector
3. Vector is used to search the knowledge base
4. Top-K relevant chunks are retrieved
5. Chunks are injected into the LLM prompt as context
6. LLM generates a response grounded in the retrieved context
```

**Why it matters:** LLMs hallucinate. RAG grounds responses in real data. This
pattern is the foundation of most production LLM applications.

---

## Summary Table

| Pattern | Purpose | Key Insight |
|---------|---------|-------------|
| Workflow Engine | DAG execution | Graphs are data, not code |
| Node | Processing unit | Stateless, typed, testable |
| Variable System | Data flow | Template strings enable loose coupling |
| Plugin System | Extensibility | Declare interface, validate at runtime |
| App Pattern | UX abstraction | All apps are workflows underneath |
| Provider Abstraction | LLM portability | Switch providers via config |
| RAG | Grounded generation | Retrieve before generate |

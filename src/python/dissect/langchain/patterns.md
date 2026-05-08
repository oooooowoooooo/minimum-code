# LangChain Design Patterns

## Pattern 1: Chain Pattern (Sequential Composition via LCEL)

### What It Is

A Chain is a sequence of processing steps connected via the pipe operator (`|`). Each step receives the output of the previous step as its input. This is LangChain's core composition model, called LCEL (LangChain Expression Language).

### Why LangChain Uses It

- **Composability**: Combine simple building blocks into complex pipelines
- **Uniform interface**: Every component implements the same `Runnable` protocol
- **Streaming**: Data flows through the chain step by step, enabling streaming
- **Parallelism**: Steps that don't depend on each other can run in parallel
- **Batch processing**: The same chain works on single inputs or batches

### How It Works Internally

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template("Q: {question}\nA:")
llm = ChatOpenAI()
chain = prompt | llm  # pipe operator creates a RunnableSequence
result = chain.invoke({"question": "What is Python?"})
```

The `|` operator creates a `RunnableSequence` object that stores references to both components. When `invoke()` is called:

1. The first component (`prompt`) processes the input dict
2. Its output is passed to the second component (`llm`)
3. The final output is returned

### The Runnable Protocol

Every LangChain component implements:

```python
class Runnable:
    def invoke(self, input) -> output           # Single input
    def batch(self, inputs) -> list[output]     # Multiple inputs
    def stream(self, input) -> Iterator[output] # Streaming
    def ainvoke(self, input) -> output          # Async single
```

This uniform interface is what makes the `|` operator work. Any two Runnables can be composed.

### Internal Flow

```
chain = A | B | C

chain.invoke(input)
    |
    v
A.invoke(input) -> output_A
    |
    v
B.invoke(output_A) -> output_B
    |
    v
C.invoke(output_B) -> final_output
```

### Design Insight

LCEL is inspired by Unix pipes (`|`) and Elixir's pipe operator. The key insight is: **if every component has the same interface, composition becomes trivial**. This is the same insight behind monads in functional programming.

---

## Pattern 2: Agent Pattern (LLM-Driven Tool Selection)

### What It Is

An Agent is a loop where the LLM decides what action to take. Unlike a Chain (fixed sequence), an Agent's behavior is dynamic -- the LLM chooses which tool to call based on the current state.

### Why LangChain Uses It

- **Flexibility**: The same agent can handle different types of questions by choosing different tools
- **Reasoning**: The LLM can break down complex questions into sub-steps
- **Adaptability**: Add new tools without changing the agent logic

### How It Works Internally

The Agent loop:

```
1. Receive user question
2. Format prompt with question + available tools
3. Call LLM to get a response
4. Parse the response:
   a. If the LLM chose a tool -> execute the tool, add result to context, go to step 3
   b. If the LLM gave a final answer -> return it
5. Repeat until answer or max iterations reached
```

### Tool Selection via Structured Output

The LLM receives a prompt like:

```
You have access to the following tools:
- search(query): Search the web
- calculator(expression): Calculate math expressions

Question: What is the population of France squared?

Thought: I need to find the population first, then calculate.
Action: search
Action Input: population of France
```

The framework parses the `Action:` and `Action Input:` lines, executes the tool, and feeds the result back:

```
Observation: France has a population of approximately 67 million.
Thought: Now I need to calculate 67000000^2.
Action: calculator
Action Input: 67000000**2
```

### Internal Flow

```
User Question
    |
    v
+-> Format Prompt (question + tools + history)
|       |
|       v
|   Call LLM
|       |
|       v
|   Parse Response
|       |
|       +---> Has tool call? --Yes--> Execute Tool --> Add to History --+
|       |                                                               |
|       +---> Has final answer? --Yes--> Return Answer                  |
|                                                                       |
+<----------------------------------------------------------------------+
(max iterations reached -> force return)
```

### Design Decision: ReAct Pattern

LangChain agents use the **ReAct** (Reasoning + Acting) pattern:
- The LLM first **reasons** about what to do (Thought:)
- Then **acts** by choosing a tool (Action:)
- Observes the result (Observation:)
- Repeats until it has enough information to answer

This interleaving of reasoning and action produces more accurate results than either reasoning alone or acting alone.

---

## Pattern 3: RAG Pattern (Retrieval-Augmented Generation)

### What It Is

RAG solves the problem of LLMs not knowing about your specific data. Instead of fine-tuning the model, you retrieve relevant documents at query time and include them in the prompt.

### Why LangChain Uses It

- **No fine-tuning needed**: Works with any LLM out of the box
- **Always up-to-date**: The retrieval index can be updated independently
- **Citable**: You can show the user which documents informed the answer
- **Cost-effective**: No expensive fine-tuning runs

### How It Works Internally

The RAG pipeline has three phases:

#### Phase 1: Indexing (offline, done once)

```
Documents (PDFs, web pages, etc.)
    |
    v
Text Splitter (chunk into ~500 token pieces)
    |
    v
Embedding Model (text -> vector of 1536 numbers)
    |
    v
Vector Store (index vectors for fast similarity search)
```

#### Phase 2: Retrieval (online, per query)

```
User Question
    |
    v
Embedding Model (question -> vector)
    |
    v
Vector Store (find K most similar document vectors)
    |
    v
Return K documents
```

#### Phase 3: Generation (online, per query)

```
Prompt Template:
"You are a helpful assistant. Use the following context to answer.

Context:
{retrieved_documents}

Question: {user_question}

Answer:"
    |
    v
LLM (generates answer grounded in context)
```

### Why Embeddings?

Embeddings capture **semantic meaning**. Documents about "machine learning" will have vectors close to documents about "neural networks" even if they share few words. This is how RAG finds relevant context without keyword matching.

### Key Design Decisions

1. **Chunking strategy matters**: Too small = lost context; too large = irrelevant noise. ~500 tokens is a common sweet spot.
2. **Top-K retrieval**: Return the K most similar chunks (typically K=3 to K=5). More context is not always better.
3. **Relevance threshold**: Sometimes no document is relevant enough. The system should detect this and fall back to the LLM's general knowledge.

---

## Pattern 4: Memory Pattern (Conversation State)

### What It Is

Memory stores conversation history so the LLM can maintain context across multiple turns. Without memory, each message is independent.

### Why LangChain Uses It

- **Multi-turn conversations**: Users expect the bot to remember what was said
- **Pluggable strategies**: Different use cases need different memory approaches
- **Decoupled from LLM**: Memory is a separate component, not baked into the model

### Memory Strategies

| Strategy | How It Works | When to Use |
|----------|-------------|-------------|
| **Buffer** | Store all messages in full | Short conversations (< 10 turns) |
| **Window** | Keep last K messages | Medium conversations (bounded context) |
| **Summary** | Summarize old messages, keep recent in full | Long conversations (compress history) |
| **Entity** | Track named entities mentioned | Information retrieval tasks |

### How Buffer Memory Works Internally

```
Turn 1: User: "What is Python?"
    Memory: [User: "What is Python?"]
    Prompt: {memory} + "What is Python?"
    Response: "Python is a programming language."
    Memory: [User: "What is Python?", AI: "Python is a programming language."]

Turn 2: User: "Who created it?"
    Memory: [User: "What is Python?", AI: "Python is a programming language.",
             User: "Who created it?"]
    Prompt: {memory} + "Who created it?"
    Response: "Python was created by Guido van Rossum."
    Memory: [... + AI: "Python was created by Guido van Rossum."]
```

### How Summary Memory Works

```
After 10 turns:
    Old messages (turns 1-8) -> LLM summarizes:
        "User asked about Python. I explained it's a programming language
         created by Guido van Rossum, first released in 1991."

    Recent messages (turns 9-10) -> kept in full

    Memory: [summary] + [turn 9, turn 10]
```

### Design Decision

LangChain keeps memory as a **separate component** rather than building it into the LLM wrapper. This means:
- You can swap memory strategies without changing the chain
- The same chain can work with or without memory
- Memory can be persisted to a database for long-running applications

---

## Pattern 5: Tool Pattern (Extensible Capabilities)

### What It Is

A Tool is a function that an Agent can call. It wraps any external capability (web search, calculator, database query, API call) behind a uniform interface.

### Why LangChain Uses It

- **Extensibility**: Add new capabilities by defining new tools
- **Safety**: Tools can have validation, rate limiting, and error handling
- **Discoverability**: Each tool has a name and description that the LLM uses to decide when to call it

### Tool Interface

```python
class Tool:
    name: str           # "search"
    description: str    # "Search the web for information"
    func: Callable      # The actual function to call

    def run(self, input: str) -> str:
        return self.func(input)
```

### How Tools Are Selected

The LLM does NOT see the tool's source code. It only sees:

1. The tool's **name** (short identifier)
2. The tool's **description** (what it does, when to use it)
3. The tool's **input schema** (what arguments it expects)

Based on this information and the user's question, the LLM decides which tool to call.

### Design Decision: Tool Descriptions Matter

The quality of the tool description directly affects the agent's ability to use it correctly. A bad description leads to wrong tool selection.

```
# Bad: Vague
"search(query)": "Does stuff with queries"

# Good: Specific
"search(query)": "Search the web for current information. Use this when you need
  facts about recent events, statistics, or information not in your training data."
```

---

## Pattern Summary

| Pattern | Core Mechanism | Key Insight |
|---------|---------------|-------------|
| Chain (LCEL) | `Runnable` protocol + `\|` operator | Uniform interface enables trivial composition |
| Agent | LLM-driven tool selection loop | LLM as the decision-maker, not just the generator |
| RAG | Embed -> Retrieve -> Generate | Ground LLM answers in external data |
| Memory | Conversation history management | State is separate from the model |
| Tool | Callable with name + description | LLM selects tools by reading descriptions |

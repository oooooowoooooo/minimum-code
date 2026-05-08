# LangChain Internals Dissection

## What Is LangChain?

LangChain is a framework for building applications powered by large language models (LLMs). Created by Harrison Chase in October 2022, it has grown to **100,000+ GitHub stars** and has become the most widely used LLM application framework.

Why it matters:

- **Composability**: Build complex LLM workflows by chaining simple components
- **Ecosystem**: Integrations with 100+ LLM providers, vector stores, and tools
- **Abstractions**: Provides patterns (Chains, Agents, RAG) that solve common LLM problems
- **Production-ready**: Streaming, callbacks, retry logic, and observability built in

## Architecture Overview

```
+------------------------------------------------------------------+
|                      LangChain Application                       |
+------------------------------------------------------------------+
           |
           v
+------------------------------------------------------------------+
|                        Core Primitives                           |
|                                                                  |
|  +--------------------+    +----------------------------------+  |
|  |   LLM / ChatModel  |    |          Prompts                 |  |
|  |  (OpenAI, Anthropic)|    |  (Templates, Few-shot, etc.)    |  |
|  +--------------------+    +----------------------------------+  |
|           |                          |                          |
|           v                          v                          |
|  +------------------------------------------------------------+ |
|  |                     Chains (LCEL)                          | |
|  |  prompt | llm | output_parser  (pipe operator composition) | |
|  +------------------------------------------------------------+ |
|                              |                                   |
|           +------------------+------------------+                |
|           v                  v                  v                |
|  +----------------+  +----------------+  +----------------+     |
|  |    Agents      |  |      RAG       |  |     Memory     |     |
|  | (tool-calling) |  | (retrieval)    |  | (conversation) |     |
|  +----------------+  +----------------+  +----------------+     |
|           |                  |                  |                |
|           v                  v                  v                |
|  +----------------+  +----------------+  +----------------+     |
|  |     Tools      |  | Vector Store   |  |  Chat History  |     |
|  | (search, code) |  | (embeddings)   |  |  (buffer, etc.)|     |
|  +----------------+  +----------------+  +----------------+     |
+------------------------------------------------------------------+
```

## Key Design Decisions

### 1. LCEL (LangChain Expression Language) -- Pipe Operator Composition

LangChain's core abstraction is the **Runnable** protocol. Every component (prompt, LLM, parser) implements `Runnable`, and they compose with the `|` operator:

```python
chain = prompt | llm | output_parser
result = chain.invoke({"question": "What is Python?"})
```

This is a functional pipeline. Each step transforms the output of the previous step.

### 2. Agents Decide What To Do

Unlike Chains (which follow a fixed sequence), **Agents** use the LLM itself to decide which tool to call next. The LLM sees available tools, reasons about which one to use, and the framework executes the tool and feeds the result back.

### 3. RAG Grounds LLMs in Data

Retrieval-Augmented Generation solves hallucination by:
1. Converting a question to an embedding (vector)
2. Searching a vector store for relevant documents
3. Injecting those documents into the prompt as context
4. Having the LLM answer based on the retrieved context

### 4. Memory Is Pluggable

Conversation memory is not built into the LLM -- it is a separate component that manages chat history. This allows different memory strategies (buffer, summary, window) without changing the LLM or chain.

## Learning Objectives

After completing this dissection, you will understand:

1. How the Runnable protocol enables composition via `|`
2. How Agents use LLM reasoning to select tools
3. How RAG pipelines retrieve and inject context
4. How memory manages conversation state across turns
5. How the Tool abstraction enables extensible capabilities

## Prerequisites

- Python 3.10+ (type hints, `match` statement helpful)
- Understanding of what LLMs are (text in, text out)
- Basic knowledge of embeddings (text -> vector of numbers)
- Familiarity with the concept of APIs (LLM providers like OpenAI)

## How to Use This Module

1. Read `README.md` for the big picture
2. Study `patterns.md` for design pattern analysis
3. Run and modify `dissect.py` for hands-on understanding

```bash
cd src/python/dissect/langchain
python dissect.py
```

## When NOT to Use LangChain

LangChain is powerful but adds complexity. For simple use cases (one LLM call, no tools, no retrieval), a direct API call is simpler and more transparent. Use LangChain when you need:

- Multi-step workflows (chains)
- Tool-using agents
- RAG with vector stores
- Conversation memory management

"""
LangChain Internals: Atomic Code Dissection

This file rebuilds the core mechanisms of LangChain from scratch.
Each section is self-contained with detailed comments and inline tests.

All LLM calls are simulated (no API keys needed).
Run: python dissect.py
"""

import math
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Iterator
from abc import ABC, abstractmethod


# =============================================================================
# SECTION 1: Runnable Protocol and LCEL (Pipe Operator Composition)
# =============================================================================
#
# LangChain's core abstraction is the Runnable protocol. Every component
# (prompt, LLM, parser) implements Runnable, and they compose with |.
#
# The key insight: if every component has the same interface (input -> output),
# composition becomes trivial. This is the same insight behind Unix pipes.
# =============================================================================


class Runnable(ABC):
    """
    The Runnable protocol -- LangChain's universal interface.

    Every LangChain component implements this protocol. This is what makes
    the pipe operator (|) work: any two Runnables can be composed.

    Design decision: Using an abstract base class (ABC) rather than a
    Protocol/duck-typing because we want:
    1. Explicit interface contract
    2. Default implementations for batch/stream
    3. The ability to add shared methods (like pipe)
    """

    @abstractmethod
    def invoke(self, input: Any) -> Any:
        """Process a single input and return the output."""
        ...

    def batch(self, inputs: list[Any]) -> list[Any]:
        """Process multiple inputs. Default: sequential invoke()."""
        return [self.invoke(inp) for inp in inputs]

    def stream(self, input: Any) -> Iterator[Any]:
        """Stream output chunks. Default: yield the full result."""
        yield self.invoke(input)

    def __or__(self, other: "Runnable") -> "RunnableSequence":
        """
        The pipe operator: chain1 | chain2 creates a RunnableSequence.

        This is the heart of LCEL. It allows:
            prompt | llm | parser
        which creates:
            RunnableSequence([prompt, llm, parser])

        Design decision: __or__ returns RunnableSequence, not a generic
        Runnable, because we need to know the sequence of steps for
        optimization (batching, parallel execution).
        """
        if isinstance(other, RunnableSequence):
            # Flatten: A | (B | C) -> [A, B, C]
            return RunnableSequence(list(self.runnables) + other.runnables)
        return RunnableSequence([self, other])

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class RunnableSequence(Runnable):
    """
    A sequence of Runnables connected in series.

    This is what the pipe operator (|) creates. It stores the list of
    steps and invokes them in order, piping each output to the next input.

    Design decisions:
    - Stores steps as a flat list (not nested pairs) for efficiency
    - The first step can receive any input type
    - Subsequent steps receive the output of the previous step
    - Supports streaming by streaming through each step
    """

    def __init__(self, runnables: list[Runnable]):
        self.runnables = runnables

    def invoke(self, input: Any) -> Any:
        """
        Execute the chain: A(input) -> B(result) -> C(result) -> final

        This is a simple left-fold (reduce) over the runnables list.
        """
        result = input
        for runnable in self.runnables:
            result = runnable.invoke(result)
        return result

    def stream(self, input: Any) -> Iterator[Any]:
        """
        Stream through the chain.

        For a sequence of [A, B, C], we:
        1. Get the full result from A (prompts are not streamable)
        2. Stream from B (LLMs are streamable)
        3. Pass each chunk through C (parsers may be streamable)
        """
        result = input
        for i, runnable in enumerate(self.runnables):
            if i < len(self.runnables) - 1:
                # Non-final steps: get full result
                result = runnable.invoke(result)
            else:
                # Final step: stream
                yield from runnable.stream(result)

    def __repr__(self):
        steps = " | ".join(repr(r) for r in self.runnables)
        return f"RunnableSequence({steps})"


class RunnableLambda(Runnable):
    """
    Wraps a plain function as a Runnable.

    This is how you use arbitrary functions in LCEL chains:
        chain = prompt | llm | RunnableLambda(lambda x: x.upper())
    """

    def __init__(self, func: Callable):
        self.func = func

    def invoke(self, input: Any) -> Any:
        return self.func(input)

    def __repr__(self):
        return f"RunnableLambda({self.func.__name__})"


def test_runnable_and_lcel():
    """Test: Runnable protocol and pipe operator composition."""

    # Simple Runnables that transform data
    class DoubleIt(Runnable):
        def invoke(self, input: int) -> int:
            return input * 2

    class AddTen(Runnable):
        def invoke(self, input: int) -> int:
            return input + 10

    class ToString(Runnable):
        def invoke(self, input: int) -> str:
            return f"Result: {input}"

    # Compose with pipe operator
    chain = DoubleIt() | AddTen() | ToString()

    result = chain.invoke(5)
    assert result == "Result: 20", f"Expected 'Result: 20', got '{result}'"

    # Test that pipe creates RunnableSequence
    assert isinstance(chain, RunnableSequence)
    assert len(chain.runnables) == 3

    # Test RunnableLambda
    chain2 = DoubleIt() | RunnableLambda(lambda x: x + 1)
    assert chain2.invoke(5) == 11

    # Test flattening: A | (B | C) -> [A, B, C] not [A, [B, C]]
    a, b, c = DoubleIt(), AddTen(), ToString()
    nested = a | (b | c)
    assert isinstance(nested, RunnableSequence)
    assert len(nested.runnables) == 3

    print("[PASS] Runnable Protocol & LCEL: pipe composition, flattening")


# =============================================================================
# SECTION 2: Prompt Template
# =============================================================================
#
# Prompt templates are Runnables that format a template string with variables.
# They are the first step in most chains: take a dict of variables, produce
# a formatted string for the LLM.
# =============================================================================


class PromptTemplate(Runnable):
    """
    Formats a template string with input variables.

    Design decisions:
    - Uses Python's str.format() syntax ({variable_name})
    - Validates that all required variables are provided
    - Implements Runnable so it composes with | into chains

    This is a simplified version of LangChain's ChatPromptTemplate.
    """

    def __init__(self, template: str):
        self.template = template
        # Extract variable names from {name} patterns
        self.input_variables = re.findall(r"\{(\w+)\}", template)

    def invoke(self, input: dict[str, Any]) -> str:
        """
        Format the template with the input variables.

        Args:
            input: Dict mapping variable names to values

        Returns:
            The formatted prompt string
        """
        missing = set(self.input_variables) - set(input.keys())
        if missing:
            raise ValueError(f"Missing variables: {missing}")
        return self.template.format(**input)

    def __repr__(self):
        return f"PromptTemplate(variables={self.input_variables})"


def test_prompt_template():
    """Test: Prompt template formatting and validation."""

    prompt = PromptTemplate(
        "You are a helpful assistant.\n\n"
        "Context: {context}\n\n"
        "Question: {question}\n\n"
        "Answer:"
    )

    result = prompt.invoke({
        "context": "Python is a programming language.",
        "question": "What is Python?"
    })

    assert "Python is a programming language." in result
    assert "What is Python?" in result

    # Test missing variable
    try:
        prompt.invoke({"question": "What?"})
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Missing" in str(e)

    print("[PASS] Prompt Template: formatting, variable extraction, validation")


# =============================================================================
# SECTION 3: Simulated LLM
# =============================================================================
#
# Since we can't make real API calls, this section implements a simulated
# LLM that mimics the behavior of a real LLM (like GPT-4 or Claude).
# It supports both simple completion and tool-calling patterns.
# =============================================================================


class ChatMessage:
    """Represents a message in a conversation."""

    def __init__(self, role: str, content: str, tool_calls: list[dict] | None = None):
        self.role = role
        self.content = content
        self.tool_calls = tool_calls or []

    def __repr__(self):
        return f"ChatMessage(role={self.role!r}, content={self.content[:50]!r})"


class SimulatedLLM(Runnable):
    """
    A simulated LLM that returns predefined responses.

    In a real application, this would call OpenAI/Anthropic/etc.
    Here it returns canned responses for testing purposes.

    Design decisions:
    - Accepts both string and ChatMessage inputs (like real LLMs)
    - Supports a "knowledge base" for RAG simulation
    - Supports tool-call simulation for Agent testing
    """

    def __init__(self, responses: dict[str, str] | None = None):
        self.responses = responses or {}
        self.default_response = "I don't know the answer to that."

    def invoke(self, input: Any) -> ChatMessage:
        """Generate a response based on the input."""
        if isinstance(input, str):
            prompt = input
        elif isinstance(input, ChatMessage):
            prompt = input.content
        elif isinstance(input, dict):
            # For prompt template output
            prompt = str(input)
        else:
            prompt = str(input)

        # Check for tool-calling patterns (Agent mode)
        if "Action:" in prompt:
            return self._handle_tool_call(prompt)

        # Check knowledge base for RAG
        for key, response in self.responses.items():
            if key.lower() in prompt.lower():
                return ChatMessage(role="assistant", content=response)

        return ChatMessage(role="assistant", content=self.default_response)

    def _handle_tool_call(self, prompt: str) -> ChatMessage:
        """Simulate tool-calling behavior for agents."""
        # Parse the action from the prompt
        action_match = re.search(r"Action:\s*(\w+)", prompt)
        input_match = re.search(r"Action Input:\s*(.+?)(?:\n|$)", prompt)

        if action_match:
            tool_name = action_match.group(1)
            tool_input = input_match.group(1).strip() if input_match else ""

            # Simulate tool execution result
            response = (
                f"Thought: I now know the answer.\n"
                f"Final Answer: Based on the tool '{tool_name}' with input '{tool_input}', "
                f"here is the result."
            )
            return ChatMessage(role="assistant", content=response)

        return ChatMessage(role="assistant", content=self.default_response)


def test_simulated_llm():
    """Test: Simulated LLM response generation."""

    llm = SimulatedLLM({
        "python": "Python is a high-level programming language created by Guido van Rossum.",
        "javascript": "JavaScript is the language of the web, created by Brendan Eich.",
    })

    # Test knowledge lookup
    msg = llm.invoke("Tell me about Python")
    assert "Guido van Rossum" in msg.content

    msg = llm.invoke("What is JavaScript?")
    assert "Brendan Eich" in msg.content

    # Test unknown topic
    msg = llm.invoke("Tell me about Go")
    assert "don't know" in msg.content

    print("[PASS] Simulated LLM: knowledge lookup, default response")


# =============================================================================
# SECTION 4: Output Parser
# =============================================================================
#
# Output parsers transform LLM output into structured data.
# They are the final step in most chains.
# =============================================================================


class StrOutputParser(Runnable):
    """
    Extracts the text content from a ChatMessage.

    This is the most common parser: it just returns the message content
    as a plain string, stripping any metadata.
    """

    def invoke(self, input: ChatMessage) -> str:
        if isinstance(input, ChatMessage):
            return input.content
        return str(input)


class JsonOutputParser(Runnable):
    """
    Parses JSON from the LLM's text output.

    The LLM returns text that looks like JSON. This parser extracts
    and validates the JSON structure.
    """

    def invoke(self, input: ChatMessage | str) -> dict:
        import json
        text = input.content if isinstance(input, ChatMessage) else str(input)

        # Try to find JSON in the text
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        return {"raw": text}


def test_output_parsers():
    """Test: Output parsers extract structured data from LLM output."""

    str_parser = StrOutputParser()
    json_parser = JsonOutputParser()

    msg = ChatMessage(role="assistant", content='{"name": "Alice", "age": 30}')

    # String parser
    assert str_parser.invoke(msg) == '{"name": "Alice", "age": 30}'

    # JSON parser
    result = json_parser.invoke(msg)
    assert result == {"name": "Alice", "age": 30}

    # JSON parser with surrounding text
    msg2 = ChatMessage(role="assistant", content='Here is the result: {"status": "ok"} done.')
    result2 = json_parser.invoke(msg2)
    assert result2 == {"status": "ok"}

    print("[PASS] Output Parsers: string extraction, JSON parsing")


# =============================================================================
# SECTION 5: Agent (LLM-Driven Tool Selection)
# =============================================================================
#
# An Agent uses the LLM to decide which tool to call. The LLM sees the
# available tools, the user's question, and any previous observations,
# then decides: use a tool, or give a final answer.
#
# This implements the ReAct (Reasoning + Acting) pattern.
# =============================================================================


@dataclass
class Tool:
    """
    A tool that an Agent can call.

    Design decisions:
    - name + description are shown to the LLM (tool selection)
    - func is the actual implementation (never shown to LLM)
    - The LLM chooses tools by reading descriptions, not code
    """
    name: str
    description: str
    func: Callable[[str], str]

    def run(self, input: str) -> str:
        """Execute the tool."""
        return self.func(input)


class Agent:
    """
    Simplified ReAct Agent.

    The agent loop:
    1. Format prompt with question + available tools + history
    2. Call LLM
    3. Parse response:
       - If "Final Answer:" -> return the answer
       - If "Action:" -> execute the tool, add observation to history, loop
    4. Repeat until answer or max iterations

    Design decisions:
    - Uses ReAct prompt format (Thought/Action/Action Input/Observation)
    - Max iterations prevents infinite loops
    - Tool descriptions are injected into the prompt (not the tools themselves)
    """

    def __init__(self, llm: SimulatedLLM, tools: list[Tool], max_iterations: int = 5):
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.max_iterations = max_iterations

    def _format_tools_description(self) -> str:
        """Format tool descriptions for the prompt."""
        lines = []
        for tool in self.tools.values():
            lines.append(f"- {tool.name}: {tool.description}")
        return "\n".join(lines)

    def _build_prompt(self, question: str, history: list[str]) -> str:
        """Build the ReAct prompt with tools and history."""
        tools_desc = self._format_tools_description()
        history_text = "\n".join(history) if history else ""

        return (
            f"You are a helpful assistant with access to these tools:\n"
            f"{tools_desc}\n\n"
            f"To use a tool, respond with:\n"
            f"Thought: <your reasoning>\n"
            f"Action: <tool_name>\n"
            f"Action Input: <input>\n\n"
            f"If you know the answer, respond with:\n"
            f"Thought: <your reasoning>\n"
            f"Final Answer: <your answer>\n\n"
            f"Question: {question}\n"
            f"{history_text}"
        )

    def _parse_response(self, response: str) -> tuple[str | None, str | None, str | None]:
        """
        Parse the LLM's response to extract thought, action, or final answer.

        Returns:
            (thought, action_name, action_input) or (thought, None, final_answer)
        """
        thought_match = re.search(r"Thought:\s*(.+?)(?:\n|$)", response)
        thought = thought_match.group(1).strip() if thought_match else ""

        # Check for final answer
        final_match = re.search(r"Final Answer:\s*(.+?)(?:\n|$)", response)
        if final_match:
            return thought, None, final_match.group(1).strip()

        # Check for tool action
        action_match = re.search(r"Action:\s*(\w+)", response)
        input_match = re.search(r"Action Input:\s*(.+?)(?:\n|$)", response)

        if action_match:
            action_name = action_match.group(1)
            action_input = input_match.group(1).strip() if input_match else ""
            return thought, action_name, action_input

        return thought, None, response

    def run(self, question: str) -> str:
        """
        Execute the agent loop.

        This is the main entry point. It runs the ReAct loop until
        the LLM produces a Final Answer or we hit max iterations.
        """
        history: list[str] = []

        for iteration in range(self.max_iterations):
            # Step 1: Build prompt with history
            prompt = self._build_prompt(question, history)

            # Step 2: Call LLM
            response = self.llm.invoke(prompt)
            response_text = response.content

            # Step 3: Parse response
            thought, action_name, action_input = self._parse_response(response_text)

            if thought:
                history.append(f"Thought: {thought}")

            if action_name is None:
                # Final answer
                return action_input or response_text

            if action_name in self.tools:
                # Execute the tool
                observation = self.tools[action_name].run(action_input)
                history.append(f"Action: {action_name}")
                history.append(f"Action Input: {action_input}")
                history.append(f"Observation: {observation}")
            else:
                history.append(f"Error: Tool '{action_name}' not found")

        return "Agent reached max iterations without a final answer."


def test_agent():
    """Test: Agent uses tools based on LLM reasoning."""

    # Define tools
    def search(query: str) -> str:
        results = {
            "python": "Python is a programming language created by Guido van Rossum in 1991.",
            "population": "The world population is approximately 8 billion people.",
        }
        for key, value in results.items():
            if key in query.lower():
                return value
        return "No results found."

    def calculator(expression: str) -> str:
        try:
            result = eval(expression, {"__builtins__": {}}, {"math": math})
            return str(result)
        except Exception as e:
            return f"Error: {e}"

    tools = [
        Tool("search", "Search for information on any topic", search),
        Tool("calculator", "Calculate mathematical expressions", calculator),
    ]

    # LLM that responds to tool-use patterns
    llm = SimulatedLLM()

    agent = Agent(llm=llm, tools=tools)

    # Test: Agent processes a question (the simulated LLM will use tool pattern)
    result = agent.run("What is Python?")
    # The agent should produce some response (even with simulated LLM)
    assert isinstance(result, str)
    assert len(result) > 0

    # Test: Tool execution works
    assert search("python") == "Python is a programming language created by Guido van Rossum in 1991."
    assert calculator("2 + 2") == "4"
    assert calculator("math.sqrt(16)") == "4.0"

    print("[PASS] Agent: tool selection, ReAct loop, tool execution")


# =============================================================================
# SECTION 6: RAG Pipeline (Retrieval-Augmented Generation)
# =============================================================================
#
# RAG = Retrieve relevant documents + Generate answer from them.
#
# This section implements:
# 1. A simple embedding model (text -> vector)
# 2. An in-memory vector store with cosine similarity search
# 3. A complete RAG pipeline: embed -> retrieve -> generate
# =============================================================================


def simple_embedding(text: str, dimensions: int = 10) -> list[float]:
    """
    A simplified embedding function.

    Real embeddings (OpenAI, Sentence Transformers) produce 768-3072 dimensional
    vectors that capture semantic meaning. This is a toy version that produces
    a deterministic vector based on character frequencies.

    In production, you would use:
    - OpenAI's text-embedding-3-small (1536 dimensions)
    - Sentence Transformers (768 dimensions)
    - Cohere embed (1024 dimensions)

    Design decision: Even this toy version demonstrates the key property
    of embeddings: similar texts produce similar vectors.
    """
    # Create a simple hash-based vector
    vector = [0.0] * dimensions
    for i, char in enumerate(text.lower()):
        vector[i % dimensions] += ord(char) / 128.0

    # Normalize to unit vector (required for cosine similarity)
    magnitude = math.sqrt(sum(v * v for v in vector))
    if magnitude > 0:
        vector = [v / magnitude for v in vector]

    return vector


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """
    Compute cosine similarity between two vectors.

    Cosine similarity measures the angle between vectors, giving a value
    from -1 (opposite) to 1 (identical). For normalized vectors, it's
    just the dot product.

    This is the standard similarity metric for text embeddings.
    """
    dot_product = sum(x * y for x, y in zip(a, b))
    magnitude_a = math.sqrt(sum(x * x for x in a))
    magnitude_b = math.sqrt(sum(x * x for x in b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


class VectorStore:
    """
    In-memory vector store with similarity search.

    Design decisions:
    - Stores documents and their embeddings as parallel lists
    - Search uses cosine similarity (standard for text embeddings)
    - Returns top-K results sorted by similarity

    In production, you would use:
    - Pinecone (managed vector database)
    - Weaviate (open-source vector database)
    - ChromaDB (local, lightweight)
    - FAISS (Facebook's similarity search library)
    """

    def __init__(self, embedding_func: Callable = simple_embedding):
        self.embedding_func = embedding_func
        self.documents: list[str] = []
        self.embeddings: list[list[float]] = []

    def add_documents(self, documents: list[str]):
        """Index documents by computing their embeddings."""
        for doc in documents:
            self.documents.append(doc)
            self.embeddings.append(self.embedding_func(doc))

    def search(self, query: str, k: int = 3) -> list[tuple[str, float]]:
        """
        Find the K most similar documents to the query.

        Returns:
            List of (document, similarity_score) tuples, sorted by similarity.
        """
        if not self.documents:
            return []

        query_embedding = self.embedding_func(query)

        # Compute similarity with all documents
        scores = []
        for i, doc_embedding in enumerate(self.embeddings):
            score = cosine_similarity(query_embedding, doc_embedding)
            scores.append((i, score))

        # Sort by similarity (highest first) and return top K
        scores.sort(key=lambda x: x[1], reverse=True)

        results = []
        for i, score in scores[:k]:
            results.append((self.documents[i], score))

        return results


class RAGPipeline:
    """
    Complete RAG pipeline: Retrieve + Generate.

    The pipeline:
    1. Takes a user question
    2. Searches the vector store for relevant documents
    3. Formats a prompt with the retrieved context
    4. Calls the LLM to generate an answer

    Design decisions:
    - Prompt template includes a clear instruction to use the context
    - Top-K retrieval (configurable)
    - The LLM is the last step, so the pipeline is a Runnable chain
    """

    def __init__(self, vector_store: VectorStore, llm: SimulatedLLM,
                 prompt_template: PromptTemplate | None = None, k: int = 3):
        self.vector_store = vector_store
        self.llm = llm
        self.k = k

        self.prompt_template = prompt_template or PromptTemplate(
            "Use the following context to answer the question.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n\n"
            "Answer based on the context above:"
        )

    def run(self, question: str) -> str:
        """
        Execute the full RAG pipeline.

        Steps:
        1. Retrieve relevant documents
        2. Format them into the prompt context
        3. Call the LLM with the augmented prompt
        4. Extract and return the answer
        """
        # Step 1: Retrieve
        results = self.vector_store.search(question, k=self.k)
        context = "\n\n".join(doc for doc, score in results)

        # Step 2: Format prompt
        prompt = self.prompt_template.invoke({
            "context": context,
            "question": question,
        })

        # Step 3: Generate
        response = self.llm.invoke(prompt)

        # Step 4: Extract answer
        return response.content


def test_rag_pipeline():
    """Test: Complete RAG pipeline with retrieval and generation."""

    # Knowledge base
    documents = [
        "Python is a high-level programming language created by Guido van Rossum. "
        "It was first released in 1991.",
        "JavaScript is the programming language of the web. It was created by "
        "Brendan Eich at Netscape in 1995.",
        "Rust is a systems programming language focused on safety and performance. "
        "It was developed by Mozilla Research.",
        "Go (Golang) is a programming language designed at Google by Rob Pike, "
        "Ken Thompson, and Robert Griesemer.",
        "TypeScript is a typed superset of JavaScript developed by Microsoft. "
        "It adds static typing to JavaScript.",
    ]

    # Create vector store and index documents
    store = VectorStore(embedding_func=simple_embedding)
    store.add_documents(documents)

    # Test vector search
    results = store.search("Python programming", k=2)
    assert len(results) == 2
    # Python document should be most similar to "Python programming"
    assert "Python" in results[0][0]
    assert results[0][1] > 0  # Has positive similarity

    # Create RAG pipeline with LLM that knows about the topics
    llm = SimulatedLLM({
        "python": "Based on the context, Python is a high-level programming language created by Guido van Rossum in 1991.",
        "javascript": "Based on the context, JavaScript is the language of the web, created by Brendan Eich in 1995.",
    })

    rag = RAGPipeline(vector_store=store, llm=llm)

    # Test: Question about Python
    answer = rag.run("What is Python?")
    assert "Python" in answer

    # Test: Question about JavaScript
    answer = rag.run("Tell me about JavaScript")
    assert "JavaScript" in answer

    print("[PASS] RAG Pipeline: embedding, vector search, context-augmented generation")


# =============================================================================
# SECTION 7: Memory (Conversation State Management)
# =============================================================================
#
# Memory stores conversation history so the LLM can maintain context.
# This section implements three memory strategies:
# 1. Buffer Memory: stores all messages
# 2. Window Memory: keeps last K messages
# 3. Summary Memory: summarizes old messages
# =============================================================================


class ConversationMemory(ABC):
    """
    Abstract base class for conversation memory.

    Design decision: Memory is separate from the LLM and chain.
    This means you can swap memory strategies without changing anything else.
    """

    @abstractmethod
    def add_message(self, role: str, content: str):
        """Add a message to the conversation history."""
        ...

    @abstractmethod
    def get_messages(self) -> list[ChatMessage]:
        """Get all messages (possibly summarized/windowed)."""
        ...

    @abstractmethod
    def clear(self):
        """Clear the conversation history."""
        ...


class BufferMemory(ConversationMemory):
    """
    Stores all messages in full.

    Simplest strategy: no information loss, but grows unboundedly.
    Best for short conversations (< 10 turns).
    """

    def __init__(self):
        self.messages: list[ChatMessage] = []

    def add_message(self, role: str, content: str):
        self.messages.append(ChatMessage(role=role, content=content))

    def get_messages(self) -> list[ChatMessage]:
        return list(self.messages)

    def clear(self):
        self.messages.clear()


class WindowMemory(ConversationMemory):
    """
    Keeps only the last K messages.

    Prevents context window overflow by dropping old messages.
    Best for medium-length conversations where recent context matters most.
    """

    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.messages: list[ChatMessage] = []

    def add_message(self, role: str, content: str):
        self.messages.append(ChatMessage(role=role, content=content))
        # Trim to window size
        if len(self.messages) > self.window_size:
            self.messages = self.messages[-self.window_size:]

    def get_messages(self) -> list[ChatMessage]:
        return list(self.messages)

    def clear(self):
        self.messages.clear()


class SummaryMemory(ConversationMemory):
    """
    Summarizes old messages, keeps recent in full.

    Strategy:
    - Messages older than the threshold are replaced with a summary
    - Recent messages are kept in full
    - The summary is updated incrementally as new messages arrive

    Best for long conversations where you need to preserve key information
    but can't fit all messages in the context window.
    """

    def __init__(self, max_recent: int = 4):
        self.max_recent = max_recent
        self.messages: list[ChatMessage] = []
        self.summary: str = ""

    def add_message(self, role: str, content: str):
        self.messages.append(ChatMessage(role=role, content=content))

        # When we have too many messages, summarize the old ones
        if len(self.messages) > self.max_recent + 2:  # +2 for the summary exchange
            old_messages = self.messages[:len(self.messages) - self.max_recent]
            self._update_summary(old_messages)
            self.messages = self.messages[len(self.messages) - self.max_recent:]

    def _update_summary(self, old_messages: list[ChatMessage]):
        """Create/update the summary from old messages."""
        # In production, this would call an LLM to summarize.
        # Here we do a simple concatenation.
        new_text = " ".join(f"{m.role}: {m.content}" for m in old_messages)
        if self.summary:
            self.summary += " " + new_text
        else:
            self.summary = new_text

        # Keep summary manageable (truncate if too long)
        if len(self.summary) > 500:
            self.summary = self.summary[-500:]

    def get_messages(self) -> list[ChatMessage]:
        messages = []
        if self.summary:
            messages.append(ChatMessage(
                role="system",
                content=f"Previous conversation summary: {self.summary}"
            ))
        messages.extend(self.messages)
        return messages

    def clear(self):
        self.messages.clear()
        self.summary = ""


def test_memory():
    """Test: All three memory strategies."""

    # --- Buffer Memory ---
    buffer = BufferMemory()
    buffer.add_message("user", "Hello")
    buffer.add_message("assistant", "Hi there!")
    buffer.add_message("user", "How are you?")

    messages = buffer.get_messages()
    assert len(messages) == 3
    assert messages[0].content == "Hello"
    assert messages[2].content == "How are you?"

    # --- Window Memory ---
    window = WindowMemory(window_size=3)
    for i in range(5):
        window.add_message("user", f"Message {i}")

    messages = window.get_messages()
    assert len(messages) == 3
    assert messages[0].content == "Message 2"  # Oldest kept
    assert messages[2].content == "Message 4"  # Newest

    # --- Summary Memory ---
    summary_mem = SummaryMemory(max_recent=2)

    # Add many messages
    for i in range(6):
        summary_mem.add_message("user", f"Question {i}")
        summary_mem.add_message("assistant", f"Answer {i}")

    messages = summary_mem.get_messages()
    # Should have summary + recent messages
    assert messages[0].role == "system"  # Summary
    assert "summary" in messages[0].content.lower()
    # Recent messages should be preserved in full
    assert any("Question 5" in m.content for m in messages)

    print("[PASS] Memory: buffer, window, summary strategies")


# =============================================================================
# SECTION 8: Chain with Memory (Conversational Chain)
# =============================================================================
#
# This section combines Chain + Memory into a conversational chain
# that maintains context across multiple turns.
# =============================================================================


class ConversationalChain:
    """
    A chain that includes memory for multi-turn conversations.

    Flow for each turn:
    1. Get conversation history from memory
    2. Format history + new question into a prompt
    3. Call LLM
    4. Store the exchange in memory
    5. Return the response

    Design decisions:
    - Memory is injected, not hardcoded (swap strategies easily)
    - History is formatted as a simple text block (not structured messages)
    - The prompt template includes a {history} variable
    """

    def __init__(self, llm: SimulatedLLM, memory: ConversationMemory,
                 prompt_template: PromptTemplate | None = None):
        self.llm = llm
        self.memory = memory
        self.prompt_template = prompt_template or PromptTemplate(
            "You are a helpful assistant.\n\n"
            "Conversation history:\n{history}\n\n"
            "Human: {question}\n"
            "Assistant:"
        )

    def _format_history(self) -> str:
        """Format conversation history as text."""
        messages = self.memory.get_messages()
        lines = []
        for msg in messages:
            if msg.role == "system":
                lines.append(f"[System: {msg.content}]")
            elif msg.role == "user":
                lines.append(f"Human: {msg.content}")
            elif msg.role == "assistant":
                lines.append(f"Assistant: {msg.content}")
        return "\n".join(lines)

    def run(self, question: str) -> str:
        """Process one conversational turn."""
        # Get history
        history = self._format_history()

        # Format prompt
        prompt = self.prompt_template.invoke({
            "history": history,
            "question": question,
        })

        # Call LLM
        response = self.llm.invoke(prompt)
        answer = response.content

        # Store in memory
        self.memory.add_message("user", question)
        self.memory.add_message("assistant", answer)

        return answer


def test_conversational_chain():
    """Test: Conversational chain with memory across turns."""

    llm = SimulatedLLM({
        "python": "Python is a programming language.",
        "who created": "Python was created by Guido van Rossum.",
    })

    memory = BufferMemory()
    chain = ConversationalChain(llm=llm, memory=memory)

    # Turn 1
    response1 = chain.run("What is Python?")
    assert "Python" in response1

    # Verify memory was updated
    messages = memory.get_messages()
    assert len(messages) == 2
    assert messages[0].role == "user"
    assert messages[1].role == "assistant"

    # Turn 2 (memory should carry context)
    response2 = chain.run("Who created it?")
    assert len(response2) > 0

    # Memory should now have 4 messages
    messages = memory.get_messages()
    assert len(messages) == 4

    print("[PASS] Conversational Chain: multi-turn with memory")


# =============================================================================
# MAIN: Run all tests
# =============================================================================


if __name__ == "__main__":
    print("=" * 60)
    print("LangChain Internals Dissection")
    print("=" * 60)
    print()

    test_runnable_and_lcel()
    test_prompt_template()
    test_simulated_llm()
    test_output_parsers()
    test_agent()
    test_rag_pipeline()
    test_memory()
    test_conversational_chain()

    print()
    print("=" * 60)
    print("All tests passed. Read the source code for detailed")
    print("explanations of each mechanism.")
    print("=" * 60)

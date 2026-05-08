"""
Dify Dissection -- Simplified Workflow Engine

This module reimplements Dify's core workflow engine from scratch.
The goal is understanding: how does a DAG-based workflow engine work?
How do nodes, variables, and execution fit together?

Run: python dissect.py
"""

from __future__ import annotations

import re
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any, Callable


# =============================================================================
# Variable Store -- Centralized Data Flow
# =============================================================================

class VariableStore:
    """
    Centralized store for workflow variables.

    In Dify, all node outputs are stored here. Nodes read from the store
    using template strings like {{node_id.field}}.

    This is the glue that connects nodes without direct coupling.
    """

    def __init__(self):
        self._store: dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        """Store a variable value."""
        self._store[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a variable value."""
        return self._store.get(key, default)

    def resolve_template(self, template: str) -> str:
        """
        Resolve {{variable}} references in a template string.

        Example: "Summarize: {{node_a.result}}" -> "Summarize: hello world"
        """
        def replacer(match: re.Match) -> str:
            var_path = match.group(1).strip()
            value = self._store.get(var_path, match.group(0))
            return str(value)

        return re.sub(r"\{\{(.+?)\}\}", replacer, template)

    def resolve_dict(self, data: dict[str, Any]) -> dict[str, Any]:
        """Resolve templates in all string values of a dictionary."""
        resolved = {}
        for key, value in data.items():
            if isinstance(value, str):
                resolved[key] = self.resolve_template(value)
            elif isinstance(value, dict):
                resolved[key] = self.resolve_dict(value)
            else:
                resolved[key] = value
        return resolved

    def __repr__(self) -> str:
        return f"VariableStore({len(self._store)} variables)"


# =============================================================================
# Node -- The Workflow Building Block
# =============================================================================

class Node:
    """
    Base class for workflow nodes.

    Each node has:
    - id: unique identifier
    - type: what kind of node this is
    - config: node-specific configuration
    - execute(): the actual logic

    Nodes are stateless. All state lives in the VariableStore.
    """

    def __init__(self, node_id: str, node_type: str, config: dict[str, Any] | None = None):
        self.id = node_id
        self.type = node_type
        self.config = config or {}

    def execute(self, inputs: dict[str, Any], variables: VariableStore) -> dict[str, Any]:
        """
        Execute this node and return its outputs.

        Override in subclasses. The base implementation is a no-op.
        """
        raise NotImplementedError(f"Node type '{self.type}' does not implement execute()")

    def __repr__(self) -> str:
        return f"Node(id='{self.id}', type='{self.type}')"


class LLMNode(Node):
    """
    Sends a prompt to a language model and returns the response.

    In Dify, LLM nodes are the most common. They:
    1. Resolve template variables in the prompt
    2. Call the configured LLM provider
    3. Return the response text

    Here we simulate the LLM call.
    """

    def __init__(self, node_id: str, prompt: str, model: str = "gpt-4"):
        super().__init__(node_id, "llm", {"prompt": prompt, "model": model})
        self.prompt = prompt
        self.model = model

    def execute(self, inputs: dict[str, Any], variables: VariableStore) -> dict[str, Any]:
        """Resolve prompt templates and simulate LLM response."""
        # Resolve {{variable}} references in the prompt
        resolved_prompt = variables.resolve_template(self.prompt)

        # In real Dify, this calls the LLM API
        # Here we simulate a response
        simulated_response = f"[LLM:{self.model}] Response to: {resolved_prompt[:80]}..."

        return {"text": simulated_response, "prompt_used": resolved_prompt}


class HTTPNode(Node):
    """
    Makes an HTTP request and returns the response.

    In Dify, HTTP nodes are used for API calls, webhooks, etc.
    """

    def __init__(self, node_id: str, url: str, method: str = "GET"):
        super().__init__(node_id, "http", {"url": url, "method": method})
        self.url = url
        self.method = method

    def execute(self, inputs: dict[str, Any], variables: VariableStore) -> dict[str, Any]:
        """Resolve URL templates and simulate HTTP request."""
        resolved_url = variables.resolve_template(self.url)
        # Simulate HTTP response
        return {"status": 200, "body": f"Response from {resolved_url}"}


class CodeNode(Node):
    """
    Executes arbitrary Python code.

    In Dify, code nodes allow custom logic. They receive inputs
    and must return outputs as a dictionary.

    Security note: real Dify sandboxes code execution. We do not.
    """

    def __init__(self, node_id: str, code: str):
        super().__init__(node_id, "code", {"code": code})
        self.code = code

    def execute(self, inputs: dict[str, Any], variables: VariableStore) -> dict[str, Any]:
        """Execute the code with inputs available as local variables."""
        # Resolve templates in the code
        resolved_code = variables.resolve_template(self.code)

        # Create a safe execution environment
        local_vars = {"inputs": inputs, "result": None}
        try:
            exec(resolved_code, {"__builtins__": {}}, local_vars)
            return {"result": local_vars.get("result", "No result")}
        except Exception as e:
            return {"error": str(e)}


class IfElseNode(Node):
    """
    Conditional branching node.

    Evaluates a condition and routes execution accordingly.
    In Dify, this is how workflows branch based on data.

    Condition format: "{{node_id.field}} == 'value'"
    """

    def __init__(self, node_id: str, condition: str):
        super().__init__(node_id, "if_else", {"condition": condition})
        self.condition = condition

    def execute(self, inputs: dict[str, Any], variables: VariableStore) -> dict[str, Any]:
        """Evaluate the condition and return the branch result."""
        resolved_condition = variables.resolve_template(self.condition)

        # Simple condition evaluation
        # Supports: ==, !=, >, <, contains
        try:
            if "==" in resolved_condition:
                left, right = resolved_condition.split("==", 1)
                result = left.strip().strip("'\"") == right.strip().strip("'\"')
            elif "!=" in resolved_condition:
                left, right = resolved_condition.split("!=", 1)
                result = left.strip().strip("'\"") != right.strip().strip("'\"")
            elif "contains" in resolved_condition:
                left, right = resolved_condition.split("contains", 1)
                result = right.strip().strip("'\"") in left.strip().strip("'\"")
            else:
                result = bool(eval(resolved_condition))
        except Exception:
            result = False

        return {"condition": resolved_condition, "result": result, "branch": "true" if result else "false"}


class VariableNode(Node):
    """
    Assigns or transforms variables.

    Used for data transformation between nodes.
    """

    def __init__(self, node_id: str, assignments: dict[str, str]):
        super().__init__(node_id, "variable", {"assignments": assignments})
        self.assignments = assignments

    def execute(self, inputs: dict[str, Any], variables: VariableStore) -> dict[str, Any]:
        """Resolve and assign variables."""
        resolved = {}
        for key, template in self.assignments.items():
            resolved[key] = variables.resolve_template(template)
        return resolved


# =============================================================================
# Edge -- Connection Between Nodes
# =============================================================================

@dataclass
class Edge:
    """
    A directed edge from source node to target node.

    Edges define the execution order. The workflow engine uses edges
    to build the adjacency list and compute topological order.
    """
    source_id: str
    target_id: str


# =============================================================================
# Plugin Interface -- Extensibility
# =============================================================================

class Plugin:
    """
    Base class for Dify plugins.

    Plugins extend the platform with new capabilities:
    - Model plugins: new LLM providers
    - Tool plugins: new node types
    - Extension plugins: custom logic

    Each plugin declares its interface so the platform can validate
    inputs before execution.
    """

    def __init__(self, name: str, version: str, plugin_type: str):
        self.name = name
        self.version = version
        self.type = plugin_type

    def get_interface(self) -> dict[str, Any]:
        """Return the plugin's declared interface (input/output schema)."""
        return {"inputs": {}, "outputs": {}}

    def execute(self, inputs: dict[str, Any]) -> dict[str, Any]:
        """Execute the plugin logic. Override in subclasses."""
        raise NotImplementedError


class WebSearchPlugin(Plugin):
    """Example tool plugin: web search."""

    def __init__(self):
        super().__init__("web_search", "1.0.0", "tool")

    def get_interface(self) -> dict[str, Any]:
        return {
            "inputs": {"query": "string"},
            "outputs": {"results": "list[string]"},
        }

    def execute(self, inputs: dict[str, Any]) -> dict[str, Any]:
        query = inputs.get("query", "")
        return {"results": [f"Result 1 for '{query}'", f"Result 2 for '{query}'"]}


# =============================================================================
# Workflow -- The DAG Orchestrator
# =============================================================================

class Workflow:
    """
    A directed acyclic graph of nodes that executes in topological order.

    This is the core of Dify. The workflow:
    1. Takes a set of nodes and edges
    2. Validates the graph (no cycles, all edges reference valid nodes)
    3. Executes nodes in topological order
    4. Passes data between nodes via the VariableStore
    5. Returns outputs from terminal nodes
    """

    def __init__(self, nodes: list[Node], edges: list[Edge]):
        self.nodes = {n.id: n for n in nodes}
        self.edges = edges
        self.variables = VariableStore()

        # Build adjacency list and in-degree map
        self.adjacency: dict[str, list[str]] = defaultdict(list)
        self.in_degree: dict[str, int] = {n.id: 0 for n in nodes}

        for edge in edges:
            self.adjacency[edge.source_id].append(edge.target_id)
            self.in_degree[edge.target_id] = self.in_degree.get(edge.target_id, 0) + 1

    def validate(self) -> list[str]:
        """
        Validate the workflow graph.

        Checks:
        1. All edges reference existing nodes
        2. No cycles (topological sort succeeds)
        3. At least one node exists

        Returns a list of error messages (empty if valid).
        """
        errors = []

        # Check edge references
        for edge in self.edges:
            if edge.source_id not in self.nodes:
                errors.append(f"Edge references unknown source node: {edge.source_id}")
            if edge.target_id not in self.nodes:
                errors.append(f"Edge references unknown target node: {edge.target_id}")

        # Check for cycles using Kahn's algorithm
        if not errors:
            temp_in_degree = dict(self.in_degree)
            queue = deque([nid for nid, deg in temp_in_degree.items() if deg == 0])
            visited = 0

            while queue:
                node_id = queue.popleft()
                visited += 1
                for neighbor in self.adjacency[node_id]:
                    temp_in_degree[neighbor] -= 1
                    if temp_in_degree[neighbor] == 0:
                        queue.append(neighbor)

            if visited != len(self.nodes):
                errors.append("Workflow contains a cycle")

        return errors

    def execute(self, initial_variables: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Execute the workflow.

        Algorithm: topological sort via Kahn's algorithm.
        Nodes execute when all their upstream dependencies are complete.

        Returns: outputs from all terminal nodes (nodes with no downstream edges).
        """
        # Validate first
        errors = self.validate()
        if errors:
            raise ValueError(f"Invalid workflow: {'; '.join(errors)}")

        # Set initial variables
        if initial_variables:
            for key, value in initial_variables.items():
                self.variables.set(key, value)

        # Topological execution
        temp_in_degree = dict(self.in_degree)
        queue = deque([nid for nid, deg in temp_in_degree.items() if deg == 0])
        execution_order = []
        node_outputs: dict[str, dict[str, Any]] = {}

        print(f"  Workflow starting with {len(self.nodes)} nodes")

        while queue:
            node_id = queue.popleft()
            node = self.nodes[node_id]
            execution_order.append(node_id)

            # Gather inputs from upstream nodes
            inputs = {}
            for edge in self.edges:
                if edge.target_id == node_id and edge.source_id in node_outputs:
                    inputs[edge.source_id] = node_outputs[edge.source_id]

            # Execute the node
            print(f"    Executing: {node}")
            try:
                output = node.execute(inputs, self.variables)
            except Exception as e:
                output = {"error": str(e)}
                print(f"    ERROR in {node_id}: {e}")

            # Store output in variable store and local map
            for key, value in output.items():
                self.variables.set(f"{node_id}.{key}", value)
            node_outputs[node_id] = output

            # Update in-degree and enqueue downstream nodes
            for neighbor in self.adjacency[node_id]:
                temp_in_degree[neighbor] -= 1
                if temp_in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Collect outputs from terminal nodes
        terminal_nodes = [
            nid for nid in self.nodes
            if len(self.adjacency[nid]) == 0
        ]

        result = {}
        for nid in terminal_nodes:
            result[nid] = node_outputs.get(nid, {})

        print(f"  Execution order: {execution_order}")
        print(f"  Terminal outputs: {list(result.keys())}")

        return result


# =============================================================================
# Inline Tests & Demo
# =============================================================================

def test_variable_store():
    """Test the VariableStore's template resolution."""
    print("--- Test: VariableStore ---")

    store = VariableStore()
    store.set("node_a.result", "hello world")
    store.set("node_b.count", 42)

    # Basic template resolution
    result = store.resolve_template("Summarize: {{node_a.result}}")
    assert result == "Summarize: hello world", f"Got: {result}"
    print(f"  resolve_template -> {result}")

    # Multiple variables in one template
    result = store.resolve_template("Result: {{node_a.result}}, Count: {{node_b.count}}")
    assert "hello world" in result and "42" in result
    print(f"  multi-variable resolve -> {result}")

    # Unresolved variable keeps the template
    result = store.resolve_template("{{missing.var}}")
    assert "{{missing.var}}" in result
    print(f"  unresolved -> {result}")

    print("  PASS\n")


def test_llm_node():
    """Test the LLMNode."""
    print("--- Test: LLMNode ---")

    store = VariableStore()
    store.set("input.question", "What is Python?")

    node = LLMNode("llm_1", prompt="Answer: {{input.question}}", model="gpt-4")
    output = node.execute({}, store)

    assert "text" in output
    assert "What is Python?" in output["prompt_used"]
    print(f"  prompt_used -> {output['prompt_used']}")
    print(f"  text -> {output['text'][:60]}...")
    print("  PASS\n")


def test_if_else_node():
    """Test conditional branching."""
    print("--- Test: IfElseNode ---")

    store = VariableStore()
    store.set("input.language", "python")

    node = IfElseNode("branch_1", "{{input.language}} == 'python'")
    output = node.execute({}, store)

    assert output["result"] is True
    assert output["branch"] == "true"
    print(f"  condition: {output['condition']} -> {output['branch']}")

    # Test false branch
    store.set("input.language", "javascript")
    output = node.execute({}, store)
    assert output["result"] is False
    assert output["branch"] == "false"
    print(f"  condition: {{input.language}} == 'python' -> {output['branch']}")

    print("  PASS\n")


def test_code_node():
    """Test the CodeNode."""
    print("--- Test: CodeNode ---")

    store = VariableStore()
    store.set("input.numbers", "[1, 2, 3, 4, 5]")

    code = "result = sum({{input.numbers}})"
    node = CodeNode("code_1", code=code)
    output = node.execute({}, store)

    assert output.get("result") == 15, f"Expected 15, got: {output}"
    print(f"  code result -> {output['result']}")

    print("  PASS\n")


def test_plugin():
    """Test the plugin system."""
    print("--- Test: Plugin ---")

    plugin = WebSearchPlugin()
    print(f"  Plugin: {plugin.name} v{plugin.version} (type: {plugin.type})")

    interface = plugin.get_interface()
    print(f"  Interface: {interface}")

    result = plugin.execute({"query": "Python tutorials"})
    assert "results" in result
    assert len(result["results"]) == 2
    print(f"  Execute result: {result}")

    print("  PASS\n")


def test_workflow_simple():
    """Test a simple two-node workflow."""
    print("--- Test: Workflow (Simple) ---")

    node_a = LLMNode("node_a", prompt="What is AI?", model="gpt-4")
    node_b = LLMNode("node_b", prompt="Summarize: {{node_a.text}}", model="gpt-4")

    edge = Edge("node_a", "node_b")

    workflow = Workflow([node_a, node_b], [edge])

    # Validate
    errors = workflow.validate()
    assert len(errors) == 0, f"Validation errors: {errors}"
    print(f"  Validation: OK")

    # Execute
    result = workflow.execute()
    assert "node_b" in result  # node_b is the terminal node
    print(f"  Result keys: {list(result.keys())}")
    print(f"  Result preview: {list(result.values())[0]['text'][:80]}...")
    print("  PASS\n")


def test_workflow_diamond():
    """Test a diamond-shaped workflow (A -> B, A -> C, B -> D, C -> D)."""
    print("--- Test: Workflow (Diamond) ---")

    node_a = LLMNode("start", prompt="Analyze the topic: AI")
    node_b = CodeNode("branch_1", code="result = 'Branch 1 processed'")
    node_c = CodeNode("branch_2", code="result = 'Branch 2 processed'")
    node_d = LLMNode("merge", prompt="Combine: {{branch_1.result}} and {{branch_2.result}}")

    edges = [
        Edge("start", "branch_1"),
        Edge("start", "branch_2"),
        Edge("branch_1", "merge"),
        Edge("branch_2", "merge"),
    ]

    workflow = Workflow([node_a, node_b, node_c, node_d], edges)

    errors = workflow.validate()
    assert len(errors) == 0, f"Validation errors: {errors}"
    print(f"  Validation: OK")

    result = workflow.execute()
    assert "merge" in result
    print(f"  Result keys: {list(result.keys())}")
    print(f"  Merge output: {result['merge']['text'][:80]}...")
    print("  PASS\n")


def test_workflow_with_initial_variables():
    """Test workflow with externally provided variables."""
    print("--- Test: Workflow (Initial Variables) ---")

    node = LLMNode("ask", prompt="Tell me about {{topic}}")
    workflow = Workflow([node], [])

    result = workflow.execute(initial_variables={"topic": "machine learning"})
    assert "ask" in result
    assert "machine learning" in result["ask"]["prompt_used"]
    print(f"  Resolved prompt: {result['ask']['prompt_used']}")
    print("  PASS\n")


def test_workflow_cycle_detection():
    """Test that cycles are detected."""
    print("--- Test: Workflow (Cycle Detection) ---")

    node_a = LLMNode("a", prompt="step 1")
    node_b = LLMNode("b", prompt="step 2")

    # Create a cycle: a -> b -> a
    edges = [Edge("a", "b"), Edge("b", "a")]
    workflow = Workflow([node_a, node_b], edges)

    errors = workflow.validate()
    assert len(errors) > 0, "Should detect cycle"
    assert any("cycle" in e.lower() for e in errors)
    print(f"  Detected errors: {errors}")
    print("  PASS\n")


# =============================================================================
# Main -- Run all tests
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Dify Dissection -- Running Tests")
    print("=" * 60)
    print()

    test_variable_store()
    test_llm_node()
    test_if_else_node()
    test_code_node()
    test_plugin()
    test_workflow_simple()
    test_workflow_diamond()
    test_workflow_with_initial_variables()
    test_workflow_cycle_detection()

    print("=" * 60)
    print("All tests passed.")
    print("=" * 60)

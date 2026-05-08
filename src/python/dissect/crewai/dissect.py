"""
CrewAI Dissection -- Simplified Multi-Agent Framework

This module reimplements CrewAI's core from scratch. The goal is not
production readiness but understanding. Every class maps to a real
CrewAI concept. Every method reveals the design decisions underneath.

Run: python dissect.py
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


# =============================================================================
# Tool -- The Capability Interface
# =============================================================================

class Tool:
    """
    A capability that an agent can invoke during reasoning.

    In real CrewAI, tools wrap LangChain tools or custom functions.
    Here we use plain callables with metadata.

    Key insight: the description is critical. The LLM reads it to decide
    WHEN and HOW to use the tool. A bad description = a useless tool.
    """

    def __init__(self, name: str, description: str, func: Callable[..., str]):
        self.name = name
        self.description = description
        self.func = func

    def run(self, *args: Any, **kwargs: Any) -> str:
        """Execute the tool and return its output as a string."""
        result = self.func(*args, **kwargs)
        return str(result)

    def __repr__(self) -> str:
        return f"Tool(name='{self.name}')"


# --- Example tools for demonstration ---

def _search_impl(query: str) -> str:
    """Simulated web search. In production, this calls a search API."""
    fake_results = {
        "python": "Python is a high-level programming language created by Guido van Rossum.",
        "crewai": "CrewAI is a multi-agent framework with 25k+ GitHub stars.",
    }
    for key, val in fake_results.items():
        if key in query.lower():
            return val
    return f"No results found for: {query}"


def _calculate_impl(expression: str) -> str:
    """Safe calculator. Only evaluates arithmetic expressions."""
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return f"Error: invalid characters in expression: {expression}"
    try:
        return str(eval(expression))  # Safe here: only digits and operators
    except Exception as e:
        return f"Error: {e}"


search_tool = Tool(
    name="search",
    description="Search the internet for factual information. Input: a search query string.",
    func=_search_impl,
)

calculate_tool = Tool(
    name="calculate",
    description="Evaluate a mathematical expression. Input: arithmetic expression like '2 + 3 * 4'.",
    func=_calculate_impl,
)


# =============================================================================
# Agent -- The Autonomous Decision-Maker
# =============================================================================

class Agent:
    """
    An AI entity with a role, goal, and the ability to use tools.

    In real CrewAI, agents call an LLM (GPT-4, Claude, etc.) and the LLM
    decides which tools to use in a ReAct loop. Here we simulate the
    decision-making with simple heuristics to show the structure.

    Design decisions:
    - role: defines WHO the agent is (displayed in logs)
    - goal: defines WHAT the agent wants to achieve (injected into prompts)
    - backstory: behavioral context that shapes output style
    - tools: capabilities the agent can invoke
    - allow_delegation: whether this agent can hand off work to others
    """

    def __init__(
        self,
        role: str,
        goal: str,
        backstory: str,
        tools: list[Tool] | None = None,
        allow_delegation: bool = False,
    ):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools or []
        self.allow_delegation = allow_delegation

    def execute_task(self, task: Task, context: str = "") -> str:
        """
        Execute a task and return the result.

        In real CrewAI, this is a ReAct loop:
        1. Agent receives task + context
        2. Agent reasons about what to do
        3. Agent selects a tool (or writes directly)
        4. Agent observes the tool output
        5. Repeat until done

        Here we simulate this with keyword-based tool selection.
        """
        print(f"  [{self.role}] Working on: {task.description[:60]}...")

        # Build the prompt (in real CrewAI, this goes to the LLM)
        prompt = self._build_prompt(task, context)

        # Simulate tool use: if the task mentions "search", use search tool
        tool_output = ""
        for tool in self.tools:
            if tool.name in task.description.lower() or "search" in task.description.lower():
                if tool.name == "search":
                    # Extract a search query from the task description
                    query = task.description.split("about")[-1].strip() if "about" in task.description else task.description
                    tool_output += f"[{tool.name}] {tool.run(query)}\n"

        # Compose the final output
        # In real CrewAI, the LLM generates this. Here we simulate.
        result = self._simulate_llm_output(task, context, tool_output)
        return result

    def delegate_work(self, task: Task, agent: Agent, context: str = "") -> str:
        """
        Delegate a sub-task to another agent.

        This is the Delegation Pattern in action. An agent recognizes that
        another agent is better suited for a sub-task and hands it off.
        """
        if not self.allow_delegation:
            return f"Error: {self.role} is not allowed to delegate."

        print(f"  [{self.role}] Delegating to [{agent.role}]: {task.description[:40]}...")
        return agent.execute_task(task, context)

    def _build_prompt(self, task: Task, context: str) -> str:
        """Build the LLM prompt from agent attributes and task details."""
        prompt_parts = [
            f"You are: {self.role}",
            f"Your goal: {self.goal}",
            f"Background: {self.backstory}",
            "",
            f"Task: {task.description}",
            f"Expected output: {task.expected_output}",
        ]
        if context:
            prompt_parts.append(f"\nContext from prior tasks:\n{context}")
        if self.tools:
            tool_descs = "\n".join(f"- {t.name}: {t.description}" for t in self.tools)
            prompt_parts.append(f"\nAvailable tools:\n{tool_descs}")
        return "\n".join(prompt_parts)

    def _simulate_llm_output(self, task: Task, context: str, tool_output: str) -> str:
        """
        Simulate LLM output. In production, this is a real API call.
        Here we return a structured placeholder that shows the pattern.
        """
        parts = [f"## {task.description}"]
        if tool_output:
            parts.append(f"\n### Tool Results\n{tool_output}")
        if context:
            parts.append(f"\n### Based on Context\n{context[:200]}...")
        parts.append(f"\n### Output\nSimulated output for: {task.expected_output}")
        return "\n".join(parts)

    def __repr__(self) -> str:
        return f"Agent(role='{self.role}', tools={[t.name for t in self.tools]})"


# =============================================================================
# Task -- The Unit of Work
# =============================================================================

class Task:
    """
    A discrete unit of work assigned to an agent.

    Key fields:
    - description: what needs to be done (read by the agent)
    - expected_output: success criteria (also read by the agent)
    - agent: who is responsible
    - context: outputs from prior tasks (fed as background)

    The expected_output field is the most important. It acts as a
    self-evaluation criterion. "500-word analysis with bullet points" is
    far better than "Analyze X."
    """

    def __init__(
        self,
        description: str,
        expected_output: str,
        agent: Agent,
        context: list[Task] | None = None,
    ):
        self.description = description
        self.expected_output = expected_output
        self.agent = agent
        self.context = context or []
        self.output: str | None = None  # Set after execution

    def execute(self) -> str:
        """
        Execute this task.

        Steps:
        1. Gather context from upstream tasks
        2. Pass context + task to the assigned agent
        3. Store the result in self.output
        """
        # Collect context from upstream tasks
        context_text = ""
        if self.context:
            ctx_parts = []
            for upstream_task in self.context:
                if upstream_task.output:
                    ctx_parts.append(
                        f"[From task '{upstream_task.description[:40]}...']\n"
                        f"{upstream_task.output}"
                    )
            context_text = "\n\n".join(ctx_parts)

        # Execute via the assigned agent
        self.output = self.agent.execute_task(self, context_text)
        return self.output

    def __repr__(self) -> str:
        return f"Task(description='{self.description[:40]}...', agent='{self.agent.role}')"


# =============================================================================
# Process -- Execution Strategy Enum
# =============================================================================

class Process(Enum):
    """
    Determines how the Crew executes tasks.

    SEQUENTIAL: tasks run in list order. Each task receives output from
    all prior tasks as context. Simple, predictable, deterministic.

    HIERARCHICAL: a manager agent dynamically decides execution order.
    The manager can delegate to worker agents. Flexible but less predictable.
    """
    SEQUENTIAL = "sequential"
    HIERARCHICAL = "hierarchical"


# =============================================================================
# Crew -- The Orchestrator
# =============================================================================

class Crew:
    """
    The top-level orchestrator that coordinates agents and tasks.

    Usage:
        crew = Crew(agents=[researcher, writer], tasks=[research, write], process=Process.SEQUENTIAL)
        result = crew.kickoff()

    Execution flow:
    1. Validate that every task has an agent
    2. Execute tasks according to the chosen process
    3. Collect and return final output
    """

    def __init__(
        self,
        agents: list[Agent],
        tasks: list[Task],
        process: Process = Process.SEQUENTIAL,
        verbose: bool = False,
    ):
        self.agents = agents
        self.tasks = tasks
        self.process = process
        self.verbose = verbose

    def kickoff(self) -> str:
        """
        Start the crew's execution.

        Returns the output of the last task.
        """
        print(f"\n{'='*60}")
        print(f"Crew starting | Process: {self.process.value}")
        print(f"Agents: {[a.role for a in self.agents]}")
        print(f"Tasks:  {[t.description[:40] for t in self.tasks]}")
        print(f"{'='*60}\n")

        if self.process == Process.SEQUENTIAL:
            return self._run_sequential()
        elif self.process == Process.HIERARCHICAL:
            return self._run_hierarchical()
        else:
            raise ValueError(f"Unknown process: {self.process}")

    def _run_sequential(self) -> str:
        """
        Execute tasks in list order.

        Each task automatically receives output from all prior tasks
        as context (via the Task.context mechanism).
        """
        final_output = ""
        for i, task in enumerate(self.tasks):
            print(f"Step {i+1}/{len(self.tasks)}: {task.description[:50]}...")
            output = task.execute()
            final_output = output
            if self.verbose:
                print(f"  -> Output length: {len(output)} chars\n")
        return final_output

    def _run_hierarchical(self) -> str:
        """
        Execute tasks with a manager agent overseeing the process.

        In real CrewAI, the manager uses an LLM to decide which agent
        should handle which task, and can delegate dynamically.

        Here we simplify: the first agent is the manager. It delegates
        each task to the most appropriate agent based on role matching.
        """
        if not self.agents:
            return "Error: no agents in crew."

        manager = self.agents[0]
        workers = self.agents[1:] if len(self.agents) > 1 else self.agents

        print(f"  Manager: {manager.role}")
        print(f"  Workers: {[w.role for w in workers]}\n")

        final_output = ""
        for i, task in enumerate(self.tasks):
            print(f"Step {i+1}/{len(self.tasks)}: {task.description[:50]}...")

            # Manager delegates to the best worker
            best_worker = self._pick_best_agent(task, workers)
            if manager.allow_delegation and best_worker != manager:
                output = manager.delegate_work(task, best_worker)
            else:
                output = task.execute()

            task.output = output
            final_output = output

        return final_output

    def _pick_best_agent(self, task: Task, agents: list[Agent]) -> Agent:
        """
        Simple heuristic: pick the agent whose role keywords best match
        the task description.

        In real CrewAI, the manager LLM makes this decision.
        """
        task_lower = task.description.lower()
        best_score = -1
        best_agent = agents[0]

        for agent in agents:
            # Score by keyword overlap between role and task
            role_words = set(agent.role.lower().split())
            task_words = set(task_lower.split())
            score = len(role_words & task_words)
            if score > best_score:
                best_score = score
                best_agent = agent

        return best_agent


# =============================================================================
# Inline Tests & Demo
# =============================================================================

def test_tool():
    """Test the Tool interface."""
    print("--- Test: Tool ---")

    # Test search tool
    result = search_tool.run("python programming")
    assert "Python" in result, f"Expected 'Python' in result, got: {result}"
    print(f"  search('python') -> {result}")

    # Test calculate tool
    result = calculate_tool.run("2 + 3 * 4")
    assert result == "14", f"Expected '14', got: {result}"
    print(f"  calculate('2 + 3 * 4') -> {result}")

    # Test invalid input
    result = calculate_tool.run("import os")
    assert "Error" in result, f"Expected error for invalid input, got: {result}"
    print(f"  calculate('import os') -> {result}")

    print("  PASS\n")


def test_agent():
    """Test Agent creation and task execution."""
    print("--- Test: Agent ---")

    researcher = Agent(
        role="Researcher",
        goal="Find accurate information",
        backstory="You are a senior researcher with expertise in technology.",
        tools=[search_tool],
    )

    task = Task(
        description="Search for information about python",
        expected_output="A summary of Python's key features",
        agent=researcher,
    )

    result = researcher.execute_task(task)
    assert "## Search for information" in result
    print(f"  Agent output preview: {result[:100]}...")
    print("  PASS\n")


def test_task_context_propagation():
    """Test that task outputs flow as context to downstream tasks."""
    print("--- Test: Task Context Propagation ---")

    agent = Agent(
        role="Analyst",
        goal="Analyze data",
        backstory="Expert data analyst.",
    )

    # Task A produces output
    task_a = Task(
        description="Analyze market trends",
        expected_output="Market analysis summary",
        agent=agent,
    )
    task_a.execute()
    assert task_a.output is not None
    print(f"  Task A output length: {len(task_a.output)} chars")

    # Task B receives Task A's output as context
    task_b = Task(
        description="Write a report based on market analysis",
        expected_output="Executive summary",
        agent=agent,
        context=[task_a],
    )
    task_b.execute()
    assert task_b.output is not None
    assert "Based on Context" in task_b.output, "Context should appear in output"
    print(f"  Task B received context from Task A: YES")
    print("  PASS\n")


def test_crew_sequential():
    """Test Crew with sequential execution."""
    print("--- Test: Crew (Sequential) ---")

    researcher = Agent(
        role="Researcher",
        goal="Find information",
        backstory="Expert researcher.",
        tools=[search_tool],
    )
    writer = Agent(
        role="Writer",
        goal="Write clear prose",
        backstory="Professional writer.",
    )

    research_task = Task(
        description="Search for information about crewai",
        expected_output="Research findings",
        agent=researcher,
    )
    write_task = Task(
        description="Write a summary of the research",
        expected_output="200-word summary",
        agent=writer,
        context=[research_task],
    )

    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        process=Process.SEQUENTIAL,
        verbose=True,
    )

    result = crew.kickoff()
    assert result is not None
    assert len(result) > 0
    print(f"\n  Final output preview: {result[:120]}...")
    print("  PASS\n")


def test_crew_hierarchical():
    """Test Crew with hierarchical (manager-delegation) execution."""
    print("--- Test: Crew (Hierarchical) ---")

    manager = Agent(
        role="Manager",
        goal="Coordinate the team",
        backstory="Experienced project manager.",
        allow_delegation=True,
    )
    researcher = Agent(
        role="Researcher",
        goal="Find information",
        backstory="Expert researcher.",
        tools=[search_tool],
    )
    writer = Agent(
        role="Writer",
        goal="Write clear prose",
        backstory="Professional writer.",
    )

    task1 = Task(
        description="Research about python",
        expected_output="Research findings",
        agent=researcher,
    )
    task2 = Task(
        description="Write about crewai framework",
        expected_output="Written summary",
        agent=writer,
    )

    crew = Crew(
        agents=[manager, researcher, writer],
        tasks=[task1, task2],
        process=Process.HIERARCHICAL,
        verbose=True,
    )

    result = crew.kickoff()
    assert result is not None
    print(f"\n  Final output preview: {result[:120]}...")
    print("  PASS\n")


def test_delegation():
    """Test agent-to-agent delegation."""
    print("--- Test: Delegation ---")

    agent_a = Agent(
        role="Lead",
        goal="Complete the project",
        backstory="Team lead.",
        allow_delegation=True,
    )
    agent_b = Agent(
        role="Specialist",
        goal="Handle technical tasks",
        backstory="Technical specialist.",
        tools=[search_tool],
    )

    task = Task(
        description="Search for information about AI",
        expected_output="Technical findings",
        agent=agent_b,
    )

    # Agent A delegates to Agent B
    result = agent_a.delegate_work(task, agent_b)
    assert "## Search for information" in result
    print(f"  Delegation result preview: {result[:100]}...")
    print("  PASS\n")


# =============================================================================
# Main -- Run all tests
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("CrewAI Dissection -- Running Tests")
    print("=" * 60)
    print()

    test_tool()
    test_agent()
    test_task_context_propagation()
    test_delegation()
    test_crew_sequential()
    test_crew_hierarchical()

    print("=" * 60)
    print("All tests passed.")
    print("=" * 60)

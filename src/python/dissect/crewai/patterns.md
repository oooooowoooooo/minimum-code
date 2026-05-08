# CrewAI Core Design Patterns

## Pattern 1: Agent Pattern (Autonomous Decision-Maker)

**Intent:** Encapsulate an AI entity with a role, goal, and the ability to
reason and act autonomously.

**Structure:**
```
Agent
  role: str          -- "Senior Researcher"
  goal: str          -- "Find the most relevant information"
  backstory: str     -- "You are a veteran researcher with 20 years..."
  tools: list[Tool]  -- capabilities the agent can invoke
  llm: LLM           -- the language model powering this agent
```

**Why it matters:** Without a clear role and goal, LLMs produce generic output.
The Agent pattern forces you to define WHO is doing the work and WHY. The
backstory provides behavioral context that shapes output style and quality.

**Anti-pattern:** Creating one "do everything" agent. Agents should be
specialized. A researcher agent does not need code execution tools. A coder
agent does not need web search.

---

## Pattern 2: Task Pattern (Unit of Work)

**Intent:** Define a discrete, assignable unit of work with clear inputs,
outputs, and success criteria.

**Structure:**
```
Task
  description: str           -- what needs to be done
  expected_output: str       -- what success looks like
  agent: Agent               -- who is responsible
  context: list[Task]        -- inputs from prior tasks
  output_file: str?          -- optional file to write results
```

**Why it matters:** Vague instructions produce vague results. The Task pattern
forces explicit specification of:
- WHAT to do (description)
- WHAT success looks like (expected_output)
- WHO does it (agent)
- WHAT prior context is available (context from other tasks)

**Key insight:** The `expected_output` field is the most important. It acts as
a self-evaluation criterion for the agent. "Write a 500-word analysis comparing
X and Y with bullet points" is far better than "Analyze X and Y."

---

## Pattern 3: Crew Pattern (Orchestrator)

**Intent:** Coordinate multiple agents working on multiple tasks in a defined
execution order.

**Structure:**
```
Crew
  agents: list[Agent]        -- the team
  tasks: list[Task]          -- the work
  process: Process           -- SEQUENTIAL or HIERARCHICAL
  verbose: bool              -- debug logging
```

**Two execution modes:**

1. **Sequential** -- tasks execute in list order. Task 2 receives Task 1's
   output as context. Simple, predictable.

2. **Hierarchical** -- a manager agent delegates tasks to worker agents. The
   manager decides execution order dynamically. More flexible, less predictable.

**Why it matters:** The Crew is the entry point. `crew.kickoff()` triggers the
entire workflow. It manages context propagation, tool invocation, and result
collection.

---

## Pattern 4: Delegation Pattern (Agent-to-Agent)

**Intent:** Allow an agent to delegate sub-tasks to other agents when it
recognizes the work is outside its expertise.

**Mechanism:**
```
1. Agent A receives Task X
2. Agent A reasons: "This requires web search, which Agent B has"
3. Agent A calls: delegate_work(task, agent=B)
4. Agent B executes the sub-task
5. Agent B returns result to Agent A
6. Agent A incorporates result into its own output
```

**Why it matters:** Delegation is what makes multi-agent systems truly
collaborative. Without it, agents are just parallel workers with no interaction.
With delegation, agents form dynamic teams at runtime.

**When to enable:** Hierarchical process mode. The manager agent has
`allow_delegation=True` and can route work to the best-suited agent.

**When to disable:** Sequential mode where task boundaries are pre-defined.
Random delegation in sequential mode creates chaos.

---

## Pattern 5: Memory Pattern (Shared Context)

**Intent:** Provide agents with persistent memory across task executions so
they can learn from prior interactions.

**Memory types:**
```
Short-term Memory  -- current task context (task outputs)
Long-term Memory   -- persisted across crew executions (stored externally)
Entity Memory      -- tracks entities mentioned in conversations (people, places)
```

**Why it matters:** Without memory, each crew execution starts from scratch.
Memory enables:
- Learning from past mistakes
- Maintaining consistency across runs
- Building knowledge over time

**Implementation:** Memory is typically backed by a vector store (e.g.,
ChromaDB). Each memory entry is embedded and stored. On retrieval, relevant
memories are fetched by similarity search.

---

## Pattern 6: Tool Pattern (Capability Interface)

**Intent:** Define a clean interface for agent capabilities that agents can
discover and invoke during reasoning.

**Structure:**
```
Tool
  name: str           -- "search_web"
  description: str    -- "Search the internet for information"
  func: Callable      -- the actual implementation
  args_schema: dict   -- input validation schema
```

**Why it matters:** Tools turn agents from "text generators" into "actors."
An agent with a search tool can find real information. An agent with a code
execution tool can write and run Python.

**Key design rule:** Tool descriptions matter enormously. The agent reads the
description to decide WHEN and HOW to use the tool. A poorly described tool
will be ignored or misused.

---

## Pattern 7: Context Propagation Pattern

**Intent:** Pass outputs from upstream tasks as inputs to downstream tasks,
forming a dependency chain.

**Flow:**
```
Task A (agent: researcher) -> output: "Research findings..."
Task B (agent: writer, context: [Task A]) -> uses A's output as background
Task C (agent: reviewer, context: [Task B]) -> reviews B's output
```

**Why it matters:** This is how multi-step workflows actually work. The
researcher's findings inform the writer. The writer's draft is reviewed by the
reviewer. Context propagation is the glue that binds tasks into a pipeline.

---

## Summary Table

| Pattern | Purpose | Key Insight |
|---------|---------|-------------|
| Agent | Autonomous decision-maker | Specialization beats generalization |
| Task | Unit of work | Expected output > vague description |
| Crew | Orchestrator | Sequential or hierarchical execution |
| Delegation | Agent-to-agent help | Dynamic team formation at runtime |
| Memory | Shared context | Learn from past executions |
| Tool | Capability interface | Descriptions drive agent tool selection |
| Context Propagation | Data flow | Upstream outputs become downstream inputs |

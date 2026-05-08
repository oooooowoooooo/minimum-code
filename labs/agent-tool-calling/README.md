# Lab 5: Agent Tool Calling

## Objective

Build a simple agent framework with tool registration, keyword-based planning, tool execution with error handling, and conversation history tracking.

## Skills Practiced

- Dataclass-based agent design
- Tool registry pattern
- Keyword-based intent routing
- Error handling and custom exceptions
- Conversation state management

## Getting Started

```bash
pip install pytest
```

1. Open `starter.py`
2. Implement `register_tool`, `plan`, `execute`, and `chat`
3. Run tests: `pytest test_agent.py -v`

## Architecture

```
User Input
    |
    v
[Plan] -- keyword matching --> tool_name
    |
    v
[Execute] -- lookup + run --> result
    |
    v
[History] -- store user + assistant messages
```

## Planning Rules

| Keywords | Tool |
|---|---|
| "weather" | `get_weather` |
| "calculate", +, -, *, / | `calculate` |
| "time", "date" | `get_time` |
| (anything else) | `chat` |

## Solution

See `solution.py` when you're ready to check your work.

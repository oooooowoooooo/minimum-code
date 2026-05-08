"""Agent Tool Calling Lab
Goal: Build an agent with tool registry, planner, executor, and conversation
"""
from dataclasses import dataclass, field
from typing import Callable, Any, Dict, List


class ToolNotFoundError(Exception):
    """Raised when agent tries to use an unregistered tool."""
    pass


class ToolExecutionError(Exception):
    """Raised when a tool fails during execution."""
    pass


@dataclass
class Tool:
    name: str
    description: str
    func: Callable


@dataclass
class Agent:
    tools: Dict[str, Tool] = field(default_factory=dict)
    history: List[dict] = field(default_factory=list)

    def register_tool(self, tool: Tool):
        """Register a tool for the agent to use."""
        # TODO: implement
        pass

    def plan(self, user_input: str) -> str:
        """Select the best tool for the user's request.

        Simple keyword matching:
        - If input contains "weather" -> return "get_weather"
        - If input contains "calculate" or math operators -> return "calculate"
        - If input contains "time" or "date" -> return "get_time"
        - Otherwise -> return "chat"
        """
        # TODO: implement
        pass

    def execute(self, tool_name: str, **kwargs) -> Any:
        """Execute a tool by name.

        - If tool not found, raise ToolNotFoundError
        - If tool execution fails, raise ToolExecutionError
        - Otherwise return the tool's result
        """
        # TODO: implement
        pass

    def chat(self, user_input: str) -> str:
        """Main conversation loop.

        1. Add user message to history
        2. Plan which tool to use
        3. Execute the tool
        4. Add assistant response to history
        5. Return the result as a string
        """
        # TODO: implement
        pass

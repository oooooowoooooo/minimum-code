from dataclasses import dataclass, field
from typing import Callable, Any, Dict, List

class ToolNotFoundError(Exception): pass
class ToolExecutionError(Exception): pass

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
        self.tools[tool.name] = tool

    def plan(self, user_input: str) -> str:
        lower = user_input.lower()
        if "weather" in lower:
            return "get_weather"
        if "calculate" in lower or any(op in lower for op in ["+", "-", "*", "/"]):
            return "calculate"
        if "time" in lower or "date" in lower:
            return "get_time"
        return "chat"

    def execute(self, tool_name: str, **kwargs) -> Any:
        if tool_name not in self.tools:
            raise ToolNotFoundError(f"Tool '{tool_name}' not found")
        try:
            return self.tools[tool_name].func(**kwargs)
        except Exception as e:
            raise ToolExecutionError(f"Tool '{tool_name}' failed: {e}")

    def chat(self, user_input: str) -> str:
        self.history.append({"role": "user", "content": user_input})
        tool_name = self.plan(user_input)
        result = self.execute(tool_name)
        response = str(result)
        self.history.append({"role": "assistant", "content": response})
        return response

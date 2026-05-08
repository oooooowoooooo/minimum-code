import pytest
from starter import Agent, Tool, ToolNotFoundError, ToolExecutionError


def make_test_tools():
    """Create a set of test tools."""
    weather = Tool(
        name="get_weather",
        description="Get weather for a location",
        func=lambda location="NYC": f"Sunny, 72°F in {location}"
    )
    calc = Tool(
        name="calculate",
        description="Evaluate a math expression",
        func=lambda expression="1+1": str(eval(expression))
    )
    time_tool = Tool(
        name="get_time",
        description="Get current time",
        func=lambda: "2024-01-01 12:00:00"
    )
    chat = Tool(
        name="chat",
        description="General chat response",
        func=lambda message="hello": f"I received: {message}"
    )
    return [weather, calc, time_tool, chat]


@pytest.fixture
def agent():
    a = Agent()
    for tool in make_test_tools():
        a.register_tool(tool)
    return a


def test_register_tool(agent):
    """Tools should be registered and accessible."""
    assert "get_weather" in agent.tools
    assert "calculate" in agent.tools
    assert len(agent.tools) == 4


def test_plan_weather(agent):
    """Should select get_weather for weather queries."""
    assert agent.plan("what's the weather") == "get_weather"
    assert agent.plan("weather in Tokyo") == "get_weather"


def test_plan_calculate(agent):
    """Should select calculate for math queries."""
    assert agent.plan("calculate 2+2") == "calculate"
    assert agent.plan("what is 5 * 3") == "calculate"


def test_plan_time(agent):
    """Should select get_time for time queries."""
    assert agent.plan("what time is it") == "get_time"
    assert agent.plan("current date") == "get_time"


def test_plan_default(agent):
    """Should default to chat for unrecognized input."""
    assert agent.plan("hello there") == "chat"
    assert agent.plan("tell me a joke") == "chat"


def test_execute_existing_tool(agent):
    """Should execute tool and return result."""
    result = agent.execute("get_weather", location="Tokyo")
    assert "Tokyo" in result


def test_execute_not_found(agent):
    """Should raise ToolNotFoundError for unknown tool."""
    with pytest.raises(ToolNotFoundError):
        agent.execute("nonexistent_tool")


def test_execute_error():
    """Should raise ToolExecutionError when tool fails."""
    bad_tool = Tool(name="bad", description="fails", func=lambda: 1/0)
    agent = Agent()
    agent.register_tool(bad_tool)
    with pytest.raises(ToolExecutionError):
        agent.execute("bad")


def test_chat_integration(agent):
    """Full chat flow: plan -> execute -> return."""
    result = agent.chat("what's the weather in London")
    assert isinstance(result, str)
    assert len(result) > 0


def test_chat_history(agent):
    """Chat should maintain conversation history."""
    agent.chat("hello")
    agent.chat("what time is it")
    assert len(agent.history) == 4  # 2 user + 2 assistant

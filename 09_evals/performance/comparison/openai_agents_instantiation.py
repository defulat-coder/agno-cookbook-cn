"""
OpenAI Agents 实例化性能评估
==================================================

演示使用 OpenAI Agents SDK 进行 Agent 实例化基准测试。
"""

from typing import Literal

from agno.eval.performance import PerformanceEval

try:
    from agents import Agent, function_tool
except ImportError:
    raise ImportError(
        "OpenAI agents not installed. Please install it using `uv pip install openai-agents`."
    )


# ---------------------------------------------------------------------------
# 创建基准测试工具
# ---------------------------------------------------------------------------
def get_weather(city: Literal["nyc", "sf"]):
    """使用此工具获取天气信息。"""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")


# ---------------------------------------------------------------------------
# 创建基准测试函数
# ---------------------------------------------------------------------------
def instantiate_agent():
    return Agent(
        name="Haiku agent",
        instructions="Always respond in haiku form",
        model="o3-mini",
        tools=[function_tool(get_weather)],
    )


# ---------------------------------------------------------------------------
# 创建评估
# ---------------------------------------------------------------------------
openai_agents_instantiation = PerformanceEval(
    func=instantiate_agent, num_iterations=1000
)

# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    openai_agents_instantiation.run(print_results=True, print_summary=True)

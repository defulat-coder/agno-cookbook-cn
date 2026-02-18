"""
CrewAI 实例化性能评估
===========================================

演示使用 CrewAI 进行 Agent 实例化基准测试。
"""

from typing import Literal

from agno.eval.performance import PerformanceEval
from crewai.agent import Agent
from crewai.tools import tool


# ---------------------------------------------------------------------------
# 创建基准测试工具
# ---------------------------------------------------------------------------
@tool("Tool Name")
def get_weather(city: Literal["nyc", "sf"]):
    """使用此工具获取天气信息。"""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")


tools = [get_weather]


# ---------------------------------------------------------------------------
# 创建基准测试函数
# ---------------------------------------------------------------------------
def instantiate_agent():
    return Agent(
        llm="gpt-4o",
        role="Test Agent",
        goal="Be concise, reply with one sentence.",
        tools=tools,
        backstory="Test",
    )


# ---------------------------------------------------------------------------
# 创建评估
# ---------------------------------------------------------------------------
crew_instantiation = PerformanceEval(func=instantiate_agent, num_iterations=1000)

# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    crew_instantiation.run(print_results=True, print_summary=True)

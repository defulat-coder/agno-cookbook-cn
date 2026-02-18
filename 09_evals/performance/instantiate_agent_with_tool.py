"""
带工具的 Agent 实例化性能评估
====================================================

演示如何测量带工具的 Agent 实例化性能。
"""

from typing import Literal

from agno.agent import Agent
from agno.eval.performance import PerformanceEval
from agno.models.openai import OpenAIChat


# ---------------------------------------------------------------------------
# 创建基准测试工具
# ---------------------------------------------------------------------------
def get_weather(city: Literal["nyc", "sf"]):
    """使用此工具获取天气信息。"""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"


tools = [get_weather]


# ---------------------------------------------------------------------------
# 创建基准测试函数
# ---------------------------------------------------------------------------
def instantiate_agent():
    return Agent(model=OpenAIChat(id="gpt-4o"), tools=tools)  # type: ignore


# ---------------------------------------------------------------------------
# 创建评估
# ---------------------------------------------------------------------------
instantiation_perf = PerformanceEval(
    name="Agent Instantiation", func=instantiate_agent, num_iterations=1000
)

# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    instantiation_perf.run(print_results=True, print_summary=True)

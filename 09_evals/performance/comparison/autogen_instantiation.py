"""
AutoGen 实例化性能评估
============================================

演示使用 AutoGen 进行 Agent 实例化基准测试。
"""

from typing import Literal

from agno.eval.performance import PerformanceEval
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient


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


tools = [get_weather]


# ---------------------------------------------------------------------------
# 创建基准测试函数
# ---------------------------------------------------------------------------
def instantiate_agent():
    return AssistantAgent(
        name="assistant",
        model_client=OpenAIChatCompletionClient(
            model="gpt-4o",
            model_info={
                "vision": False,
                "function_calling": True,
                "json_output": False,
                "family": "gpt-4o",
                "structured_output": True,
            },
        ),
        tools=tools,
    )


# ---------------------------------------------------------------------------
# 创建评估
# ---------------------------------------------------------------------------
autogen_instantiation = PerformanceEval(func=instantiate_agent, num_iterations=1000)

# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    autogen_instantiation.run(print_results=True, print_summary=True)

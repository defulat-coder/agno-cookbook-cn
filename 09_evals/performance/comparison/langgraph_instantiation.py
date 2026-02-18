"""
LangGraph 实例化性能评估
==============================================

演示使用 LangGraph 进行 Agent 实例化基准测试。
"""

from typing import Literal

from agno.eval.performance import PerformanceEval
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent


# ---------------------------------------------------------------------------
# 创建基准测试工具
# ---------------------------------------------------------------------------
@tool
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
    return create_react_agent(model=ChatOpenAI(model="gpt-4o"), tools=tools)


# ---------------------------------------------------------------------------
# 创建评估
# ---------------------------------------------------------------------------
langgraph_instantiation = PerformanceEval(func=instantiate_agent, num_iterations=1000)

# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    langgraph_instantiation.run(print_results=True, print_summary=True)

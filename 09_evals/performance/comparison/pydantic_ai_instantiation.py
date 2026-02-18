"""
PydanticAI 实例化性能评估
===============================================

演示使用 PydanticAI 进行 Agent 实例化基准测试。
"""

from typing import Literal

from agno.eval.performance import PerformanceEval
from pydantic_ai import Agent


# ---------------------------------------------------------------------------
# 创建基准测试函数
# ---------------------------------------------------------------------------
def instantiate_agent():
    agent = Agent("openai:gpt-4o", system_prompt="Be concise, reply with one sentence.")

    # 工具定义的作用域故意限定在 Agent 构建阶段。
    @agent.tool_plain
    def get_weather(city: Literal["nyc", "sf"]):
        """使用此工具获取天气信息。"""
        if city == "nyc":
            return "It might be cloudy in nyc"
        elif city == "sf":
            return "It's always sunny in sf"
        else:
            raise AssertionError("Unknown city")

    return agent


# ---------------------------------------------------------------------------
# 创建评估
# ---------------------------------------------------------------------------
pydantic_instantiation = PerformanceEval(func=instantiate_agent, num_iterations=1000)

# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    pydantic_instantiation.run(print_results=True, print_summary=True)

"""
基础推理
=============================

基础推理示例。
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
reasoning_agent = Agent(
    name="Reasoning Agent",
    model=OpenAIResponses(id="gpt-5.2"),
    reasoning=True,
    reasoning_min_steps=2,
    reasoning_max_steps=6,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    reasoning_agent.print_response(
        "一个球拍和一个球总共花费 1.10 美元。球拍比球贵 1.00 美元。"
        "球的价格是多少？",
        stream=True,
        show_full_reasoning=True,
    )

"""
推理力度（Reasoning Effort）
================

演示推理 Cookbook 示例。
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.websearch import WebSearchTools


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    agent = Agent(
        model=OpenAIChat(id="o3-mini", reasoning_effort="high"),
        tools=[WebSearchTools(enable_news=False)],
        instructions="使用表格展示数据。",
        markdown=True,
    )

    agent.print_response("撰写一份对比 NVDA 与 TSLA 的报告", stream=True)


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()

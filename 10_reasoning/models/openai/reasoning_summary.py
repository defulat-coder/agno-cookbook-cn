"""
推理摘要
=================

演示推理 Cookbook 示例。
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.websearch import WebSearchTools


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    # 设置推理 Agent
    agent = Agent(
        model=OpenAIResponses(
            id="o4-mini",
            reasoning_summary="auto",  # 请求推理摘要
        ),
        tools=[WebSearchTools(enable_news=False)],
        instructions="使用表格展示分析结果",
        markdown=True,
    )

    agent.print_response(
        "撰写一份简短的对比 NVDA 与 TSLA 的报告",
        stream=True,
    )


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()

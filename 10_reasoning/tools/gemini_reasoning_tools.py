"""
Gemini 推理工具
======================

演示推理 Cookbook 示例。
"""

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    reasoning_agent = Agent(
        model=Gemini(id="gemini-2.5-pro"),
        tools=[
            ReasoningTools(
                enable_think=True,
                enable_analyze=True,
            ),
            YFinanceTools(),
        ],
        instructions="尽可能使用表格",
        stream_events=True,
        markdown=True,
    )
    reasoning_agent.print_response(
        "撰写一份对比 NVDA 与 TSLA 的报告。", show_full_reasoning=True
    )


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()

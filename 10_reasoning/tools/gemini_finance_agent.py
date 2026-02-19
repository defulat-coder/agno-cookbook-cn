"""
Gemini 金融 Agent
====================

演示推理 Cookbook 示例。
"""
# ! pip install -U agno

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    thinking_agent = Agent(
        model=Gemini(id="gemini-3-flash-preview"),
        tools=[
            ReasoningTools(add_instructions=True),
            YFinanceTools(),
        ],
        instructions="尽可能使用表格",
        markdown=True,
        stream_events=True,
    )
    thinking_agent.print_response(
        "撰写一份详细对比 NVDA 与 TSLA 的报告",
        stream=True,
        show_reasoning=True,
    )


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()

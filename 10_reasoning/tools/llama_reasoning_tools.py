"""
Llama 推理工具
=====================

演示推理 Cookbook 示例。
"""

from agno.agent import Agent
from agno.models.meta import Llama
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    reasoning_agent = Agent(
        model=Llama(id="Llama-4-Maverick-17B-128E-Instruct-FP8"),
        tools=[
            ReasoningTools(
                enable_think=True,
                enable_analyze=True,
                add_instructions=True,
            ),
            YFinanceTools(),
        ],
        instructions="尽可能使用表格",
        markdown=True,
    )
    reasoning_agent.print_response(
        "NVDA 的股价是多少？请撰写一份报告",
        show_full_reasoning=True,
    )


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()

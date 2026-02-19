"""
推理力度（xAI）
================

演示推理 Cookbook 示例。
"""

from agno.agent import Agent
from agno.models.xai import xAI
from agno.tools.yfinance import YFinanceTools


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    agent = Agent(
        model=xAI(id="grok-3-mini-fast", reasoning_effort="high"),
        tools=[YFinanceTools()],
        instructions="使用表格展示数据。",
        markdown=True,
    )
    agent.print_response("撰写一份对比 NVDA 与 TSLA 的报告", stream=True)


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()

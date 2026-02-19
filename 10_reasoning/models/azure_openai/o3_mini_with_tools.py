"""
O3 Mini（带工具，Azure OpenAI）
==================

演示推理 Cookbook 示例。
"""

from agno.agent import Agent
from agno.models.azure.openai_chat import AzureOpenAI
from agno.tools.yfinance import YFinanceTools


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    agent = Agent(
        model=AzureOpenAI(id="o3-mini"),
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

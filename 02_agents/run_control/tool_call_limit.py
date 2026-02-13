"""
工具调用限制
=============================

本示例展示如何使用工具调用限制来控制 agent 可以进行的工具调用次数。
"""

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.yfinance import YFinanceTools

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=Claude(id="claude-3-5-haiku-20241022"),
    tools=[YFinanceTools()],
    tool_call_limit=1,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 它应该只调用第一个工具，而无法调用第二个工具。
    agent.print_response(
        "Find me the current price of TSLA, then after that find me the latest news about Tesla.",
        stream=True,
    )

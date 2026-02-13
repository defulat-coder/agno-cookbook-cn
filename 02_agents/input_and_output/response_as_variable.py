"""
响应存储为变量
=============================

演示如何将 Agent 的响应捕获到变量中以便进一步处理。
"""

from typing import Iterator  # noqa
from rich.pretty import pprint
from agno.agent import Agent, RunOutput
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[YFinanceTools()],
    instructions=["尽可能使用表格"],
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_response: RunOutput = agent.run("What is the stock price of NVDA")
    pprint(run_response)

    # run_response_strem: Iterator[RunOutputEvent] = agent.run("What is the stock price of NVDA", stream=True)
    # for response in run_response_strem:
    #     pprint(response)

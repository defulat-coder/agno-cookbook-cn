"""
团队流式传输
==============

演示团队的同步和异步流式响应。
"""

import asyncio

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.yfinance import YFinanceTools
from agno.utils.pprint import apprint_run_response

# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
stock_searcher = Agent(
    name="Stock Searcher",
    model=OpenAIChat("o3-mini"),
    role="在网络上搜索股票信息。",
    tools=[
        YFinanceTools(
            include_tools=["get_current_stock_price", "get_analyst_recommendations"],
        )
    ],
)

company_info_agent = Agent(
    name="Company Info Searcher",
    model=OpenAIChat("o3-mini"),
    role="在网络上搜索公司信息。",
    tools=[
        YFinanceTools(
            include_tools=["get_company_info", "get_company_news"],
        )
    ],
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
team = Team(
    name="Stock Research Team",
    model=OpenAIChat("o3-mini"),
    members=[stock_searcher, company_info_agent],
    markdown=True,
    show_members_responses=True,
)


# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
async def streaming_with_arun() -> None:
    await apprint_run_response(
        team.arun(input="What is the current stock price of NVDA?", stream=True)
    )


async def streaming_with_aprint_response() -> None:
    await team.aprint_response("What is the current stock price of NVDA?", stream=True)


if __name__ == "__main__":
    # 同步流式传输
    team.print_response(
        "What is the current stock price of NVDA?",
        stream=True,
    )

    team.print_response(
        "What is the latest news for TSLA?",
        stream=True,
        show_member_responses=False,
    )

    # 异步流式传输
    asyncio.run(streaming_with_arun())
    # asyncio.run(streaming_with_aprint_response())

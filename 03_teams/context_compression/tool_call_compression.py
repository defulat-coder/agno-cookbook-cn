"""
工具调用压缩
=============================

演示同步和异步工作流中的团队级工具结果压缩。
"""

import asyncio
from textwrap import dedent

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.aws import AwsBedrock
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
sync_tech_researcher = Agent(
    name="Alex",
    role="技术研究员",
    model=AwsBedrock(id="us.anthropic.claude-sonnet-4-20250514-v1:0"),
    instructions=dedent("""
        你专注于技术和 AI 研究。
        - 关注最新发展、趋势和突破
        - 提供简洁、数据驱动的见解
        - 引用你的来源
    """).strip(),
)

sync_business_analyst = Agent(
    name="Sarah",
    role="商业分析师",
    model=AwsBedrock(id="us.anthropic.claude-sonnet-4-20250514-v1:0"),
    instructions=dedent("""
        你专注于商业和市场分析。
        - 关注公司、市场和经济趋势
        - 提供可操作的商业见解
        - 包括相关数据和统计信息
    """).strip(),
)

async_tech_specialist = Agent(
    name="Tech Specialist",
    role="技术研究员",
    model=OpenAIChat(id="gpt-5.2"),
    instructions=dedent("""
        你专注于技术和 AI 研究。
        - 关注最新发展、趋势和突破
        - 提供简洁、数据驱动的见解
        - 引用你的来源
    """).strip(),
)

async_business_analyst = Agent(
    name="Sarah",
    role="商业分析师",
    model=OpenAIChat(id="gpt-4.1"),
    instructions=dedent("""
        你专注于商业和市场分析。
        - 关注公司、市场和经济趋势
        - 提供可操作的商业见解
        - 包括相关数据和统计信息
    """).strip(),
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
sync_research_team = Team(
    name="Research Team",
    model=AwsBedrock(id="us.anthropic.claude-sonnet-4-20250514-v1:0"),
    members=[sync_tech_researcher, sync_business_analyst],
    tools=[WebSearchTools()],  # 团队使用 DuckDuckGo 进行研究
    description="调查主题并提供分析的研究团队。",
    instructions=dedent("""
        你是一个全面调查主题的研究协调员。

        你的流程：
        1. 使用 DuckDuckGo 搜索大量关于主题的信息。
        2. 将详细分析委托给合适的专家
        3. 将研究发现与专家见解综合

        指南：
        - 始终使用你的 DuckDuckGo 工具开始网络研究。尽可能获取更多信息。
        - 根据主题（技术 vs 商业）选择合适的专家
        - 将你的研究与专家分析结合
        - 提供全面、有据可查的响应
    """).strip(),
    db=SqliteDb(db_file="tmp/research_team.db"),
    compress_tool_results=True,
    show_members_responses=True,
)

async_research_team = Team(
    name="Research Team",
    model=OpenAIChat(id="gpt-5.2"),
    members=[async_tech_specialist, async_business_analyst],
    tools=[WebSearchTools()],  # 团队使用 DuckDuckGo 进行研究
    description="调查主题并提供分析的研究团队。",
    instructions=dedent("""
        你是一个全面调查主题的研究协调员。

        你的流程：
        1. 使用 DuckDuckGo 搜索大量关于主题的信息。
        2. 将详细分析委托给合适的专家
        3. 将研究发现与专家见解综合

        指南：
        - 始终使用你的 DuckDuckGo 工具开始网络研究。尽可能获取更多信息。
        - 根据主题（技术 vs 商业）选择合适的专家进行分析
        - 将你的研究与专家分析结合
        - 提供全面、有据可查的响应
    """).strip(),
    db=SqliteDb(db_file="tmp/research_team2.db"),
    markdown=True,
    show_members_responses=True,
    compress_tool_results=True,
)


async def run_async_tool_compression() -> None:
    await async_research_team.aprint_response(
        "What are the latest developments in AI agents? Which companies dominate the market? Find the latest news and reports on the companies.",
        stream=True,
    )


# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # --- 同步 ---
    sync_research_team.print_response(
        "What are the latest developments in AI agents? Which companies dominate the market? Find the latest news and reports on the companies.",
        stream=True,
    )

    # --- 异步 ---
    asyncio.run(run_async_tool_compression())

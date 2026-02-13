"""
从历史记录中过滤工具调用
==============================

演示限制团队上下文中的历史工具调用结果。
"""

from textwrap import dedent

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
tech_researcher = Agent(
    name="Alex",
    role="技术研究员",
    instructions=dedent("""
        你专注于技术和 AI 研究。
        - 关注最新发展、趋势和突破
        - 提供简洁、数据驱动的见解
        - 引用你的来源
    """).strip(),
)

business_analyst = Agent(
    name="Sarah",
    role="商业分析师",
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
research_team = Team(
    name="Research Team",
    model=OpenAIChat("gpt-4o"),
    members=[tech_researcher, business_analyst],
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
    session_id="research_session",
    add_history_to_context=True,
    num_history_runs=6,
    max_tool_calls_from_history=3,
    markdown=True,
    show_members_responses=True,
)

# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    research_team.print_response(
        "What are the latest developments in AI agents? Which companies dominate the market? Find the latest news and reports on the companies.",
        stream=True,
    )
    research_team.print_response(
        "How is the tech market performing this quarter? How about last year? Find the latest news and reports on Mag 7.",
        stream=True,
    )
    research_team.print_response(
        "What are the trends in LLM applications for enterprises? Find the latest news and reports on the trends.",
        stream=True,
    )
    research_team.print_response(
        "What companies are leading in AI infrastructure? Find reports on the companies and their products.",
        stream=True,
    )

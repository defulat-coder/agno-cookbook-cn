"""
金融团队思维链（Chain Of Thought）
=============================

演示推理 Cookbook 示例。
"""

import asyncio
from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team.team import Team
from agno.tools.websearch import WebSearchTools


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    web_agent = Agent(
        name="Web Search Agent",
        role="Handle web search requests",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[WebSearchTools()],
        instructions="始终注明信息来源",
        add_datetime_to_context=True,
    )

    finance_agent = Agent(
        name="Finance Agent",
        role="Handle financial data requests",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[WebSearchTools(enable_news=False)],
        instructions=[
            "你是一位金融数据专家，请提供简洁准确的数据。",
            "使用表格展示股价、基本面数据（市盈率、市值）和分析师建议。",
            "清晰注明公司名称和股票代码。",
            "如有最新公司相关新闻，请简要摘要。",
            "专注于清晰呈现所请求的金融数据点。",
        ],
        add_datetime_to_context=True,
    )

    team_leader = Team(
        name="Reasoning Finance Team Leader",
        members=[
            web_agent,
            finance_agent,
        ],
        instructions=[
            "只输出最终答案，不要其他文字。",
            "使用表格展示数据",
        ],
        markdown=True,
        reasoning=True,
        show_members_responses=True,
    )

    async def run_team(task: str):
        await team_leader.aprint_response(
            task,
            stream=True,
            show_full_reasoning=True,
        )

    if __name__ == "__main__":
        asyncio.run(
            run_team(
                dedent("""\
        分析近期美国关税对以下关键行业市场表现的影响：
        - 钢铁与铝材：(X, NUE, AA)
        - 科技硬件：(AAPL, DELL, HPQ)
        - 农产品：(ADM, BG, INGR)
        - 汽车：(F, GM, TSLA)

        对于每个行业：
        1. 比较关税实施前后的股价表现
        2. 识别供应链中断情况和成本影响百分比
        3. 分析企业的战略应对措施（回流、价格调整、供应商多元化）
        4. 评估直接归因于关税政策的分析师展望变化
        """)
            )
        )


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()

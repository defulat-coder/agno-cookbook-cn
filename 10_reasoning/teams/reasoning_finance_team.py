"""
推理金融团队
======================

演示推理 Cookbook 示例。
"""

from textwrap import dedent

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.models.openai import OpenAIChat
from agno.team.team import Team
from agno.tools.reasoning import ReasoningTools
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
        model=Claude(id="claude-sonnet-4-5"),
        members=[
            web_agent,
            finance_agent,
        ],
        tools=[ReasoningTools(add_instructions=True)],
        instructions=[
            "只输出最终答案，不要其他文字。",
            "使用表格展示数据",
        ],
        markdown=True,
        show_members_responses=True,
        add_datetime_to_context=True,
    )

    def run_team(task: str):
        team_leader.print_response(
            task,
            stream=True,
            show_full_reasoning=True,
        )

    if __name__ == "__main__":
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

        # run_team(dedent("""\
        # 评估近期半导体出口管制对以下方面的影响：
        # - 美国芯片设计商 (Nvidia, AMD, Intel)
        # - 亚洲制造商 (TSMC, Samsung)
        # - 设备制造商 (ASML, Applied Materials)
        # 包括对研发投资、供应链重组和市场份额变化的影响。"""))

        # run_team(dedent("""\
        # 比较零售行业对消费品关税的应对：
        # - 大型零售商 (Walmart, Target, Amazon)
        # - 消费品牌 (Nike, Apple, Hasbro)
        # - 折扣零售商 (Dollar General, Five Below)
        # 包括定价策略变化、库存管理和消费者行为影响。"""))

        # run_team(dedent("""\
        # 分析半导体市场表现，重点关注：
        # - 英伟达 (NVDA)
        # - AMD (AMD)
        # - 英特尔 (INTC)
        # - 台积电 (TSM)
        # 比较它们的市场地位、增长指标和未来展望。"""))

        # run_team(dedent("""\
        # 评估汽车行业当前状况：
        # - 特斯拉 (TSLA)
        # - 福特 (F)
        # - 通用汽车 (GM)
        # - 丰田 (TM)
        # 包括电动车转型进展和传统汽车指标。"""))

        # run_team(dedent("""\
        # 比较苹果 (AAPL) 和谷歌 (GOOGL) 的财务指标：
        # - 市值
        # - 市盈率
        # - 收入增长
        # - 利润率"""))

        # run_team(dedent("""\
        # 分析近期中国太阳能电池板关税对以下方面的影响：
        # - 美国太阳能制造商 (First Solar, SunPower)
        # - 中国出口商 (JinkoSolar, Trina Solar)
        # - 美国安装公司 (Sunrun, SunPower)
        # 包括对定价、供应链和安装率的影响。"""))


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()

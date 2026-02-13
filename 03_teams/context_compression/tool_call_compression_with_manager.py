"""
使用 Manager 的工具调用压缩
==================================

演示使用 CompressionManager 进行自定义工具结果压缩。
"""

from textwrap import dedent

from agno.agent import Agent
from agno.compression.manager import CompressionManager
from agno.db.sqlite import SqliteDb
from agno.models.aws import AwsBedrock
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
compression_prompt = """
    你是一名压缩专家。你的目标是为竞争情报分析师压缩网络搜索结果。

    你的目标：仅提取可操作的竞争见解，同时极其简洁。

    必须保留：
    - 竞争对手名称和具体行动（产品发布、合作伙伴关系、收购、定价变更）
    - 确切数字（收入、市场份额、增长率、定价、员工人数）
    - 精确日期（公告日期、发布日期、交易日期）
    - 高管或官方声明的直接引用
    - 融资轮次和估值

    必须删除：
    - 公司历史和背景信息
    - 一般行业趋势（除非特定于竞争对手）
    - 分析师意见和推测（仅保留事实）
    - 详细产品描述（仅保留关键差异化因素和定价）
    - 营销宣传和促销语言

    输出格式：
    返回一个要点列表，其中每一行遵循此格式：
    "[公司名称] - [日期]: [行动/事件] ([关键数字/详情])"

    总共保持在 200 字以下。要极其简洁。仅事实。

    示例：
    - Acme Corp - Mar 15, 2024: 以 $99/用户/月推出 AcmeGPT，针对企业市场
    - TechCo - Feb 10, 2024: 以 $150M 收购 DataStart，获得 500 家企业客户
"""

compression_manager = CompressionManager(
    model=OpenAIChat(id="gpt-4o"),
    compress_tool_results_limit=2,  # 仅保留最后 2 个工具调用结果未压缩
    compress_tool_call_instructions=compression_prompt,
)

# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
tech_researcher = Agent(
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

business_analyst = Agent(
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

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
research_team = Team(
    name="Research Team",
    model=AwsBedrock(id="us.anthropic.claude-sonnet-4-20250514-v1:0"),
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
    show_members_responses=True,
    compression_manager=compression_manager,
)

# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    research_team.print_response(
        "What are the latest developments in AI agents? Which companies dominate the market? Find the latest news and reports on the companies.",
        stream=True,
    )

"""
知识库工具团队
===================

演示推理 Cookbook 示例。
"""

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.team.team import Team
from agno.tools.knowledge import KnowledgeTools
from agno.tools.websearch import WebSearchTools
from agno.vectordb.lancedb import LanceDb, SearchType


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    agno_docs = Knowledge(
        # 使用 LanceDB 作为向量数据库，将嵌入向量存储在 `agno_docs` 表中
        vector_db=LanceDb(
            uri="tmp/lancedb",
            table_name="agno_docs",
            search_type=SearchType.hybrid,
        ),
    )
    # 向知识库添加内容
    agno_docs.insert(url="https://www.paulgraham.com/read.html")

    knowledge_tools = KnowledgeTools(
        knowledge=agno_docs,
        enable_think=True,
        enable_search=True,
        enable_analyze=True,
        add_few_shot=True,
    )

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
        add_datetime_to_context=True,
    )

    team_leader = Team(
        name="Reasoning Finance Team",
        model=OpenAIChat(id="gpt-4o"),
        members=[
            web_agent,
            finance_agent,
        ],
        tools=[knowledge_tools],
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
        run_team("保罗·格雷厄姆在这篇文章中谈到了阅读的必要性，他说了什么？")


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()

"""
Session 摘要
=============================

演示 session 摘要创建、上下文重用和异步摘要检索。
"""

import asyncio

from agno.agent import Agent
from agno.db.postgres import AsyncPostgresDb, PostgresDb
from agno.models.openai import OpenAIChat
from agno.team import Team

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
sync_db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
sync_db = PostgresDb(db_url=sync_db_url, session_table="sessions")

async_db_url = "postgresql+psycopg_async://ai:ai@localhost:5532/ai"
async_db = AsyncPostgresDb(db_url=async_db_url, session_table="sessions")

# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
sync_agent = Agent(model=OpenAIChat(id="o3-mini"))
async_agent = Agent(model=OpenAIChat(id="gpt-5.2"))

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
summary_team = Team(
    model=OpenAIChat(id="o3-mini"),
    members=[sync_agent],
    db=sync_db,
    enable_session_summaries=True,
)

context_summary_team = Team(
    model=OpenAIChat(id="o3-mini"),
    db=sync_db,
    session_id="session_summary",
    add_session_summary_to_context=True,
    members=[sync_agent],
)

async_summary_team = Team(
    model=OpenAIChat(id="gpt-5.2"),
    members=[async_agent],
    db=async_db,
    session_id="async_team_session_summary",
    enable_session_summaries=True,
)


# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
async def run_async_summary_demo() -> None:
    print("运行第一次交互...")
    await async_summary_team.aprint_response(
        "Hi my name is Jane and I work as a software engineer"
    )

    print("\n运行第二次交互...")
    await async_summary_team.aprint_response(
        "I enjoy coding in Python and building AI applications"
    )

    print("\n异步检索 session 摘要...")
    summary = await async_summary_team.aget_session_summary(
        session_id="async_team_session_summary"
    )

    if summary:
        print(f"\nSession 摘要: {summary.summary}")
        if summary.topics:
            print(f"主题: {', '.join(summary.topics)}")
    else:
        print("未找到 session 摘要")


if __name__ == "__main__":
    summary_team.print_response("Hi my name is John and I live in New York")
    summary_team.print_response("I like to play basketball and hike in the mountains")

    summary_team.print_response(
        "My name is John Doe and I like to hike in the mountains on weekends.",
    )

    context_summary_team.print_response("I also like to play basketball.")

    asyncio.run(run_async_summary_demo())

"""
持久化 Session 存储
==================

演示如何使用 PostgresDb 为团队提供持久化 session 存储功能。
"""

from agno.agent.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat
from agno.team.team import Team

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
db = PostgresDb(db_url=db_url, session_table="sessions")

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
agent = Agent(name="test_agent", model=OpenAIChat(id="gpt-5.2"))
team = Team(
    members=[agent],
    db=db,
    session_id="team_session_storage",
    add_history_to_context=True,
)

# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    team.print_response("Tell me a new interesting fact about space")

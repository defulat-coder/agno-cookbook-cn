"""
持久化 Session
==================

演示持久化团队 session 以及可选的历史记录注入。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat
from agno.team import Team

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
db = PostgresDb(db_url=db_url, session_table="sessions")

# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
agent = Agent(model=OpenAIChat(id="o3-mini"))

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
basic_team = Team(
    model=OpenAIChat(id="o3-mini"),
    members=[agent],
    db=db,
)

history_team = Team(
    model=OpenAIChat(id="o3-mini"),
    members=[agent],
    db=db,
    add_history_to_context=True,
    num_history_runs=3,
)

# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    basic_team.print_response("Tell me a new interesting fact about space")

    history_team.print_response("Tell me a new interesting fact about space")
    history_team.print_response("Tell me a new interesting fact about oceans")
    history_team.print_response("What have we been talking about?")

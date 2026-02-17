"""
Session 摘要
============

演示如何使用 PostgresDb 为 Agent 配置 session 摘要功能。
"""

from agno.agent.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat
from agno.session.summary import SessionSummaryManager  # noqa: F401

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
db = PostgresDb(db_url=db_url, session_table="sessions")

# 方法 1：将 enable_session_summaries 设置为 True
#
# agent = Agent(
#     model=OpenAIChat(id="gpt-5.2"),
#     db=db,
#     enable_session_summaries=True,
#     session_id="session_summary",
#     add_session_summary_to_context=True,
# )
#
# agent.print_response("Hi my name is John and I live in New York")
# agent.print_response("I like to play basketball and hike in the mountains")

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
# 方法 2：设置 session_summary_manager
session_summary_manager = SessionSummaryManager(model=OpenAIChat(id="gpt-5.2"))
agent = Agent(
    model=OpenAIChat(id="gpt-5.2"),
    db=db,
    session_id="session_summary",
    session_summary_manager=session_summary_manager,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response("Hi my name is John and I live in New York")
    agent.print_response("I like to play basketball and hike in the mountains")

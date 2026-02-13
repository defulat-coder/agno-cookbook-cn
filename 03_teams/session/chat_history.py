"""
聊天历史记录
=============================

演示检索聊天历史记录并限制包含的历史记录消息数量。
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
history_team = Team(
    model=OpenAIChat(id="o3-mini"),
    members=[agent],
    db=db,
)

limited_history_team = Team(
    model=OpenAIChat(id="gpt-5.2"),
    members=[Agent(model=OpenAIChat(id="gpt-5.2"))],
    db=db,
    add_history_to_context=True,
    num_history_messages=1,
)

# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    history_team.print_response("Tell me a new interesting fact about space")
    print(history_team.get_chat_history())

    history_team.print_response("Tell me a new interesting fact about oceans")
    print(history_team.get_chat_history())

    limited_history_team.print_response("Tell me a new interesting fact about space")
    limited_history_team.print_response(
        "Repeat the last message, but make it much more concise"
    )

"""
聊天历史
========

演示如何从存储在 PostgresDb 中的 Agent session 获取聊天历史。
"""

from agno.agent.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
db = PostgresDb(db_url=db_url, session_table="sessions")

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-5.2"),
    db=db,
    session_id="chat_history",
    instructions="你是一个能够回答关于太空和海洋问题的助手。",
    add_history_to_context=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response("Tell me a new interesting fact about space")
    print(agent.get_chat_history())

    agent.print_response("Tell me a new interesting fact about oceans")
    print(agent.get_chat_history())

"""
Agent 之间共享记忆和历史记录
============================

本示例展示两个 Agent 通过共享数据库、用户 ID 和 Session ID，
实现对话历史和用户记忆的共享。
"""

from uuid import uuid4

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai.chat import OpenAIChat

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
db = SqliteDb(db_file="tmp/agent_sessions.db")

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent_1 = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你非常友好且乐于助人。",
    db=db,
    add_history_to_context=True,
    update_memory_on_run=True,
)

agent_2 = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你脾气暴躁，说话很刻薄。",
    db=db,
    add_history_to_context=True,
    update_memory_on_run=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    session_id = str(uuid4())
    user_id = "john_doe@example.com"

    agent_1.print_response(
        "你好！我叫 John Doe。", session_id=session_id, user_id=user_id
    )

    agent_2.print_response("我叫什么名字？", session_id=session_id, user_id=user_id)

    agent_2.print_response(
        "我喜欢周末去山里徒步。",
        session_id=session_id,
        user_id=user_id,
    )

    agent_1.print_response(
        "我有什么爱好？", session_id=session_id, user_id=user_id
    )

    agent_1.print_response(
        "我们之前聊了什么？请列出要点。",
        session_id=session_id,
        user_id=user_id,
    )

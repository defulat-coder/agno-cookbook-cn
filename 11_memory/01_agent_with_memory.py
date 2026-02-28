"""
带持久化记忆的 Agent
====================

本示例展示如何为 Agent 配置持久化记忆。
每次运行后，用户记忆会自动创建或更新。
"""

import asyncio
from uuid import uuid4

from agno.agent.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat
from rich.pretty import pprint

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
db = PostgresDb(db_url=db_url)

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    db=db,
    update_memory_on_run=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    db.clear_memories()

    session_id = str(uuid4())
    john_doe_id = "john_doe@example.com"

    asyncio.run(
        agent.aprint_response(
            "我叫 John Doe，我喜欢周末去山里徒步。",
            stream=True,
            user_id=john_doe_id,
            session_id=session_id,
        )
    )

    agent.print_response(
        "我有什么爱好？", stream=True, user_id=john_doe_id, session_id=session_id
    )

    memories = agent.get_user_memories(user_id=john_doe_id)
    print("John Doe 的记忆：")
    pprint(memories)

    agent.print_response(
        "我不再喜欢徒步了，我现在喜欢踢足球。",
        stream=True,
        user_id=john_doe_id,
        session_id=session_id,
    )

    memories = agent.get_user_memories(user_id=john_doe_id)
    print("John Doe 的记忆：")
    pprint(memories)

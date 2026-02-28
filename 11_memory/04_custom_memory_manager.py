"""
自定义记忆管理器配置
====================

本示例展示如何独立于 Agent 配置 MemoryManager，
并应用自定义的记忆捕获指令。
"""

from agno.agent.agent import Agent
from agno.db.postgres import PostgresDb
from agno.memory import MemoryManager
from agno.models.openai import OpenAIChat
from rich.pretty import pprint

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
db = PostgresDb(db_url=db_url)

# ---------------------------------------------------------------------------
# 创建记忆管理器
# ---------------------------------------------------------------------------
memory_manager = MemoryManager(
    model=OpenAIChat(id="gpt-4o"),
    additional_instructions="""
    重要：不要存储任何关于用户姓名的记忆。用"该用户"来代替用户的姓名。
    """,
    db=db,
)

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    db=db,
    memory_manager=memory_manager,
    update_memory_on_run=True,
    user_id="john_doe@example.com",
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    john_doe_id = "john_doe@example.com"

    agent.print_response(
        "我叫 John Doe，我喜欢游泳和踢足球。", stream=True
    )

    agent.print_response("我不喜欢游泳了", stream=True)

    memories = agent.get_user_memories(user_id=john_doe_id)
    print("John Doe 的记忆：")
    pprint(memories)

"""
搜索用户记忆
============

本示例展示如何使用不同的检索方式搜索用户记忆，
包括 last_n、first_n 和 agentic 检索。
"""

from agno.db.postgres import PostgresDb
from agno.memory import MemoryManager, UserMemory
from agno.models.openai import OpenAIChat
from rich.pretty import pprint

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
memory_db = PostgresDb(db_url=db_url)

# ---------------------------------------------------------------------------
# 创建记忆管理器
# ---------------------------------------------------------------------------
memory = MemoryManager(model=OpenAIChat(id="gpt-4o"), db=memory_db)

# ---------------------------------------------------------------------------
# 运行记忆搜索
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    john_doe_id = "john_doe@example.com"
    memory.add_user_memory(
        memory=UserMemory(memory="The user enjoys hiking in the mountains on weekends"),
        user_id=john_doe_id,
    )
    memory.add_user_memory(
        memory=UserMemory(
            memory="The user enjoys reading science fiction novels before bed"
        ),
        user_id=john_doe_id,
    )
    print("John Doe 的记忆：")
    pprint(memory.get_user_memories(user_id=john_doe_id))

    memories = memory.search_user_memories(
        user_id=john_doe_id, limit=1, retrieval_method="last_n"
    )
    print("\nJohn Doe 的 last_n 记忆：")
    pprint(memories)

    memories = memory.search_user_memories(
        user_id=john_doe_id, limit=1, retrieval_method="first_n"
    )
    print("\nJohn Doe 的 first_n 记忆：")
    pprint(memories)

    memories = memory.search_user_memories(
        user_id=john_doe_id,
        query="用户周末喜欢做什么？",
        retrieval_method="agentic",
    )
    print("\nJohn Doe 与查询相似的记忆（agentic 检索）：")
    pprint(memories)

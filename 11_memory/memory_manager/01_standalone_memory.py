"""
独立记忆管理器 CRUD 操作
========================

本示例展示如何手动添加、获取、删除和替换用户记忆。
"""

from agno.db.postgres import PostgresDb
from agno.memory import MemoryManager, UserMemory
from rich.pretty import pprint

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# ---------------------------------------------------------------------------
# 创建记忆管理器
# ---------------------------------------------------------------------------
memory = MemoryManager(db=PostgresDb(db_url=db_url))

# ---------------------------------------------------------------------------
# 运行记忆管理器
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    memory.add_user_memory(
        memory=UserMemory(memory="The user's name is John Doe", topics=["name"]),
    )
    print("记忆：")
    pprint(memory.get_user_memories())

    jane_doe_id = "jane_doe@example.com"
    print(f"\nUser: {jane_doe_id}")
    memory_id_1 = memory.add_user_memory(
        memory=UserMemory(memory="The user's name is Jane Doe", topics=["name"]),
        user_id=jane_doe_id,
    )
    memory_id_2 = memory.add_user_memory(
        memory=UserMemory(memory="She likes to play tennis", topics=["hobbies"]),
        user_id=jane_doe_id,
    )
    memories = memory.get_user_memories(user_id=jane_doe_id)
    print("记忆：")
    pprint(memories)

    print("\n删除记忆")
    assert memory_id_2 is not None
    memory.delete_user_memory(user_id=jane_doe_id, memory_id=memory_id_2)
    print("记忆已删除\n")
    memories = memory.get_user_memories(user_id=jane_doe_id)
    print("记忆：")
    pprint(memories)

    print("\n替换记忆")
    assert memory_id_1 is not None
    memory.replace_user_memory(
        memory_id=memory_id_1,
        memory=UserMemory(memory="The user's name is Jane Mary Doe", topics=["name"]),
        user_id=jane_doe_id,
    )
    print("记忆已替换")
    memories = memory.get_user_memories(user_id=jane_doe_id)
    print("记忆：")
    pprint(memories)

"""
从文本和消息历史创建记忆
========================

本示例展示如何使用 MemoryManager 从直接文本和消息列表创建用户记忆。
"""

from agno.db.postgres import PostgresDb
from agno.memory import MemoryManager, UserMemory
from agno.models.message import Message
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
# 运行记忆管理器
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    john_doe_id = "john_doe@example.com"
    memory.add_user_memory(
        memory=UserMemory(
            memory="""
我喜欢周末去山里徒步，
睡前阅读科幻小说，
尝试不同文化的新菜谱，
和朋友下棋，
有机会就去看现场音乐会。
摄影是我最近的爱好，尤其喜欢拍风景和街景。
我还喜欢早上冥想和练瑜伽来保持内心平静。
"""
        ),
        user_id=john_doe_id,
    )

    memories = memory.get_user_memories(user_id=john_doe_id)
    print("John Doe 的记忆：")
    pprint(memories)

    jane_doe_id = "jane_doe@example.com"
    memory.create_user_memories(
        messages=[
            Message(role="user", content="我叫 Jane Doe"),
            Message(role="assistant", content="很好！"),
            Message(role="user", content="我喜欢下棋"),
            Message(role="assistant", content="很好！"),
        ],
        user_id=jane_doe_id,
    )

    memories = memory.get_user_memories(user_id=jane_doe_id)
    print("Jane Doe 的记忆：")
    pprint(memories)

"""
自定义记忆捕获指令
==================

本示例展示如何自定义记忆捕获指令，并将结果与默认记忆管理器进行对比。
"""

from agno.db.postgres import PostgresDb
from agno.memory import MemoryManager
from agno.models.anthropic.claude import Claude
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
memory = MemoryManager(
    model=OpenAIChat(id="gpt-4o"),
    memory_capture_instructions="""\
                    记忆应仅包含用户学术兴趣的相关细节。
                    只记录他们感兴趣的学科。
                    忽略姓名、爱好和个人兴趣。
                    """,
    db=memory_db,
)

# ---------------------------------------------------------------------------
# 运行记忆管理器
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    john_doe_id = "john_doe@example.com"
    memory.create_user_memories(
        message="""\
我叫 John Doe。

我喜欢周末去山里徒步，
睡前阅读科幻小说，
尝试不同文化的新菜谱，
和朋友下棋。

我对宇宙的历史和其他天文学话题很感兴趣。
""",
        user_id=john_doe_id,
    )

    memories = memory.get_user_memories(user_id=john_doe_id)
    print("John Doe 的记忆：")
    pprint(memories)

    memory = MemoryManager(model=Claude(id="claude-3-5-sonnet-latest"), db=memory_db)
    jane_doe_id = "jane_doe@example.com"

    memory.create_user_memories(
        messages=[
            Message(role="user", content="你好，你好吗？"),
            Message(role="assistant", content="我很好，谢谢！"),
            Message(role="user", content="你能做什么？"),
            Message(
                role="assistant",
                content="我可以帮你做作业，回答关于宇宙的问题。",
            ),
            Message(role="user", content="我叫 Jane Doe"),
            Message(role="user", content="我喜欢下棋"),
            Message(
                role="user",
                content="算了，忘掉我喜欢下棋这件事。我更喜欢玩桌游，比如龙与地下城",
            ),
            Message(
                role="user",
                content="我还对宇宙的历史和其他天文学话题很感兴趣。",
            ),
            Message(role="assistant", content="很好！"),
            Message(
                role="user",
                content="我对物理学非常感兴趣。能给我讲讲量子力学吗？",
            ),
        ],
        user_id=jane_doe_id,
    )

    memories = memory.get_user_memories(user_id=jane_doe_id)
    print("Jane Doe 的记忆：")
    pprint(memories)

"""
控制记忆数据库工具
==================

本示例演示如何通过数据库工具标志来控制 AI 模型可用的记忆数据库操作。
"""

from agno.agent.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.memory.manager import MemoryManager
from agno.models.openai import OpenAIChat
from rich.pretty import pprint

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
memory_db = SqliteDb(db_file="tmp/memory_control_demo.db")
john_doe_id = "john_doe@example.com"

# ---------------------------------------------------------------------------
# 创建记忆管理器和 Agent
# ---------------------------------------------------------------------------
memory_manager_full = MemoryManager(
    model=OpenAIChat(id="gpt-4o"),
    db=memory_db,
    add_memories=True,
    update_memories=True,
)

agent_full = Agent(
    model=OpenAIChat(id="gpt-4o"),
    memory_manager=memory_manager_full,
    enable_agentic_memory=True,
    db=memory_db,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent_full.print_response(
        "我叫 John Doe，我喜欢周末去山里徒步。我还喜欢摄影。",
        stream=True,
        user_id=john_doe_id,
    )

    agent_full.print_response("我有什么爱好？", stream=True, user_id=john_doe_id)

    agent_full.print_response(
        "我不再喜欢摄影了。我现在改玩攀岩了。",
        stream=True,
        user_id=john_doe_id,
    )

    print("\n更新后的记忆：")
    memories = memory_manager_full.get_user_memories(user_id=john_doe_id)
    pprint([m.memory for m in memories] if memories else [])

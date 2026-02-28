"""
Agent 自主记忆管理
==================

本示例展示如何为 Agent 启用自主记忆功能。
在每次运行过程中，Agent 可以自主创建、更新和删除用户记忆。
"""

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
    enable_agentic_memory=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    john_doe_id = "john_doe@example.com"

    agent.print_response(
        "我叫 John Doe，我喜欢周末去山里徒步。",
        stream=True,
        user_id=john_doe_id,
    )

    agent.print_response("我有什么爱好？", stream=True, user_id=john_doe_id)

    memories = agent.get_user_memories(user_id=john_doe_id)
    print("关于 John Doe 的记忆：")
    pprint(memories)

    agent.print_response(
        "删除所有关于我的记忆。",
        stream=True,
        user_id=john_doe_id,
    )

    memories = agent.get_user_memories(user_id=john_doe_id)
    print("关于 John Doe 的记忆：")
    pprint(memories)

    agent.print_response(
        "我叫 John Doe，我喜欢画画。", stream=True, user_id=john_doe_id
    )

    memories = agent.get_user_memories(user_id=john_doe_id)
    print("关于 John Doe 的记忆：")
    pprint(memories)

    agent.print_response(
        "我不再画画了，我现在改画素描了。", stream=True, user_id=john_doe_id
    )

    memories = agent.get_user_memories(user_id=john_doe_id)
    print("关于 John Doe 的记忆：")
    pprint(memories)

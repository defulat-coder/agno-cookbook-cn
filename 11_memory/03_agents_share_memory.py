"""
多个 Agent 共享记忆
===================

本示例展示两个 Agent 共享同一用户记忆的用法。
"""

from agno.agent.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat
from agno.tools.websearch import WebSearchTools
from rich.pretty import pprint

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
db = PostgresDb(db_url=db_url)

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
chat_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description="你是一个可以与用户聊天的助手",
    db=db,
    update_memory_on_run=True,
)

research_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description="你是一个可以帮助用户解答研究问题的研究助手",
    tools=[WebSearchTools()],
    db=db,
    update_memory_on_run=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    john_doe_id = "john_doe@example.com"

    chat_agent.print_response(
        "我叫 John Doe，我喜欢周末去山里徒步。",
        stream=True,
        user_id=john_doe_id,
    )

    chat_agent.print_response("我有什么爱好？", stream=True, user_id=john_doe_id)

    research_agent.print_response(
        "我喜欢研究量子计算方面的问题。量子计算的最新进展是什么？",
        stream=True,
        user_id=john_doe_id,
    )

    memories = research_agent.get_user_memories(user_id=john_doe_id)
    print("关于 John Doe 的记忆：")
    pprint(memories)

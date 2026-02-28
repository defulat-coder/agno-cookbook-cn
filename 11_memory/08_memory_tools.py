"""
记忆工具与网页搜索
==================

本示例展示如何将 MemoryTools 与 WebSearchTools 配合使用，
让 Agent 在规划旅行的同时存储和使用用户记忆。
"""

import asyncio

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.tools.memory import MemoryTools
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
db = SqliteDb(db_file="tmp/memory.db")
john_doe_id = "john_doe@example.com"

memory_tools = MemoryTools(
    db=db,
)

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[memory_tools, WebSearchTools()],
    instructions=[
        "你是一个旅行规划机器人，帮助用户规划旅行。",
        "你应该使用 WebSearchTools 获取目的地和活动的信息。",
        "你应该使用 MemoryTools 存储用户信息以便将来参考。",
        "不要向用户询问更多信息，不知道的内容自行补充。",
    ],
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(
        agent.aprint_response(
            "我叫 John Doe，我喜欢周末去山里徒步。"
            "我喜欢去新的地方旅行，体验不同的文化。"
            "我计划十二月去非洲旅行。",
            stream=True,
            user_id=john_doe_id,
        )
    )

    asyncio.run(
        agent.aprint_response(
            "帮我制定一份旅行计划，建议我应该去哪里、预算多少等。",
            stream=True,
            user_id=john_doe_id,
        )
    )

"""使用 Postgres 作为 Agent 的数据库。

运行 `uv pip install openai ddgs sqlalchemy psycopg` 安装依赖。"""

import asyncio

from agno.agent import Agent
from agno.db.postgres import AsyncPostgresDb
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
db_url = "postgresql+psycopg_async://ai:ai@localhost:5532/ai"
db = AsyncPostgresDb(db_url=db_url)

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    db=db,
    tools=[WebSearchTools()],
    add_history_to_context=True,
    add_datetime_to_context=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(agent.aprint_response("How many people live in Canada?"))
    asyncio.run(agent.aprint_response("What is their national anthem called?"))

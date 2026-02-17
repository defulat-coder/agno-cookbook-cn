"""使用 SQLite 作为 Agent 的数据库。

运行 `uv pip install ddgs sqlalchemy openai` 安装依赖。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
db = SqliteDb(db_file="tmp/data.db")

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
    # Agent 的 session 和运行记录现在将存储在 SQLite 中
    agent.print_response("How many people live in Canada?")
    agent.print_response("What is their national anthem?")
    agent.print_response("List my messages one by one")

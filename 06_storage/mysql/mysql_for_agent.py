"""使用 MySQL 作为 Agent 的数据库。

运行 `uv pip install openai` 安装依赖。"""

from agno.agent import Agent
from agno.db.mysql import MySQLDb

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
db_url = "mysql+pymysql://ai:ai@localhost:3306/ai"
db = MySQLDb(db_url=db_url)

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    db=db,
    add_history_to_context=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response("How many people live in Canada?")
    agent.print_response("What is their national anthem called?")

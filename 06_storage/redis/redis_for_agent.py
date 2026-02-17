"""
演示如何使用 Redis 作为 Agent 的数据库的示例。

运行 `uv pip install redis ddgs openai` 安装依赖。

我们可以使用 docker 在本地启动 Redis：
1. 启动 Redis 容器
docker run --name my-redis -p 6379:6379 -d redis

2. 验证容器正在运行
docker ps
"""

from agno.agent import Agent
from agno.db.base import SessionType
from agno.db.redis import RedisDb
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
db = RedisDb(db_url="redis://localhost:6379")

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    db=db,
    tools=[WebSearchTools()],
    add_history_to_context=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response("How many people live in Canada?")
    agent.print_response("What is their national anthem called?")

    # 验证数据库内容
    print("\nVerifying db contents...")
    all_sessions = db.get_sessions(session_type=SessionType.AGENT)
    print(f"Total sessions in Redis: {len(all_sessions)}")

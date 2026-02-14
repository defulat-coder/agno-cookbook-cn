"""
AgentOS 追踪
要求：
    pip install agno opentelemetry-api opentelemetry-sdk openinference-instrumentation-agno
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from agno.tracing.setup import setup_tracing

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# 设置数据库 - 每个 agent 都有自己的 db
db1 = SqliteDb(db_file="tmp/db1.db", id="db1")
db2 = SqliteDb(db_file="tmp/db2.db", id="db2")

# 专用追踪数据库
tracing_db = SqliteDb(db_file="tmp/traces.db", id="traces")

setup_tracing(
    db=tracing_db, batch_processing=True, max_queue_size=1024, max_export_batch_size=256
)

agent = Agent(
    name="HackerNews Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[HackerNewsTools()],
    instructions="你是一个 hacker news agent。简洁地回答问题。",
    markdown=True,
    db=db1,
)

agent2 = Agent(
    name="Web Search Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[WebSearchTools()],
    instructions="你是一个网络搜索 agent。简洁地回答问题。",
    markdown=True,
    db=db2,
)

# 使用专用 db 设置我们的 AgentOS 应用
# 这确保追踪被写入和读取自同一数据库
agent_os = AgentOS(
    description="用于追踪 HackerNews 的示例应用",
    agents=[agent, agent2],
    db=tracing_db,  # AgentOS 的默认数据库（用于追踪）
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="06_tracing_with_multi_db_scenario:app", reload=True)

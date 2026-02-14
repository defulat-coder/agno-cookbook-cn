"""
AgentOS 追踪
要求：
    uv pip install agno opentelemetry-api opentelemetry-sdk openinference-instrumentation-agno
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.tools.hackernews import HackerNewsTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# 设置数据库
db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

agent = Agent(
    name="HackerNews Agent",
    model=OpenAIChat(id="gpt-5.2"),
    tools=[HackerNewsTools()],
    instructions="你是一个 hacker news agent。简洁地回答问题。",
    markdown=True,
    db=db,
)

# 设置我们的 AgentOS 应用
agent_os = AgentOS(
    description="用于追踪 HackerNews 的示例应用",
    agents=[agent],
    tracing=True,
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="basic_agent_with_postgresdb:app", reload=True)

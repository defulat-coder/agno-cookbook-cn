"""
AgentOS 演示

设置 OS_SECURITY_KEY 环境变量为你的 OS 安全密钥以启用身份验证。

前置条件：
uv pip install -U fastapi uvicorn sqlalchemy pgvector psycopg openai ddgs yfinance
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.team import Team
from agno.tools.mcp import MCPTools
from agno.tools.websearch import WebSearchTools
from agno.vectordb.pgvector import PgVector

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# 数据库连接
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# 创建 Postgres 支持的记忆存储
db = PostgresDb(db_url=db_url)

# 创建 Postgres 支持的向量存储
vector_db = PgVector(
    db_url=db_url,
    table_name="agno_docs",
)
knowledge = Knowledge(
    name="Agno Docs",
    contents_db=db,
    vector_db=vector_db,
)

# 创建你的 agent
agno_agent = Agent(
    name="Agno Agent",
    model=OpenAIChat(id="gpt-4.1"),
    tools=[MCPTools(transport="streamable-http", url="https://docs.agno.com/mcp")],
    db=db,
    update_memory_on_run=True,
    knowledge=knowledge,
    markdown=True,
)

simple_agent = Agent(
    name="Simple Agent",
    role="Simple agent",
    id="simple_agent",
    model=OpenAIChat(id="gpt-5.2"),
    instructions=["你是一个简单的 agent"],
    db=db,
    update_memory_on_run=True,
)

research_agent = Agent(
    name="Research Agent",
    role="Research agent",
    id="research_agent",
    model=OpenAIChat(id="gpt-5.2"),
    instructions=["你是一个研究 agent"],
    tools=[WebSearchTools()],
    db=db,
    update_memory_on_run=True,
)

# 创建一个团队
research_team = Team(
    name="Research Team",
    description="A team of agents that research the web",
    members=[research_agent, simple_agent],
    model=OpenAIChat(id="gpt-4.1"),
    id="research_team",
    instructions=[
        "你是一个研究团队的首席研究员。",
    ],
    db=db,
    update_memory_on_run=True,
    add_datetime_to_context=True,
    markdown=True,
)

# 创建 AgentOS
agent_os = AgentOS(
    id="agentos-demo",
    agents=[agno_agent],
    teams=[research_team],
)
app = agent_os.get_app()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="demo:app", port=7777, reload=True)

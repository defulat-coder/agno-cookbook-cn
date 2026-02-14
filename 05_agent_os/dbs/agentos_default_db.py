"""
AgentOS 演示

设置 OS_SECURITY_KEY 环境变量为你的 OS 安全密钥以启用身份验证。

前置条件：
pip install -U fastapi uvicorn sqlalchemy pgvector psycopg openai ddgs yfinance
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.tools.mcp import MCPTools
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
    knowledge=knowledge,
    markdown=True,
)

# 创建 AgentOS
agent_os = AgentOS(
    id="agentos-demo",
    agents=[agno_agent],
    db=db,  # 这是 AgentOS 的默认数据库，agno_agent 将使用它
)
app = agent_os.get_app()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="agentos_default_db:app", port=7777, reload=True)

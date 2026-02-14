"""展示如何在 AgentOS 中使用 SurrealDB 作为数据库的示例"""

from agno.agent import Agent
from agno.db.surrealdb import SurrealDb
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.team.team import Team
from agno.vectordb.pgvector import PgVector

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# 设置 SurrealDB 数据库
SURREALDB_URL = "ws://localhost:8000"
SURREALDB_USER = "root"
SURREALDB_PASSWORD = "root"
SURREALDB_NAMESPACE = "agno"
SURREALDB_DATABASE = "agent_os_demo"

creds = {"username": SURREALDB_USER, "password": SURREALDB_PASSWORD}
db = SurrealDb(None, SURREALDB_URL, creds, SURREALDB_NAMESPACE, SURREALDB_DATABASE)

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
vector_db = PgVector(table_name="agent_os_knowledge", db_url=db_url)

knowledge = Knowledge(
    contents_db=db,
    vector_db=vector_db,
    name="Agent OS Knowledge",
    description="Agent OS 演示的知识库",
)

# Agent 设置
agent = Agent(
    db=db,
    name="Basic Agent",
    id="basic-agent",
    model=OpenAIChat(id="gpt-4o"),
    add_history_to_context=True,
    num_history_runs=3,
    knowledge=knowledge,
)

# 团队设置
team = Team(
    db=db,
    id="basic-team",
    name="Team Agent",
    model=OpenAIChat(id="gpt-4o"),
    members=[agent],
    add_history_to_context=True,
    num_history_runs=3,
)

# AgentOS 设置
agent_os = AgentOS(
    description="示例 OS 设置",
    agents=[agent],
    teams=[team],
)

# 获取应用
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # 服务应用
    agent_os.serve(app="surreal:app", reload=True)

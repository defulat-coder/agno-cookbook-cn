"""
从生命周期更新
====================

演示从生命周期更新。
"""

from contextlib import asynccontextmanager

from agno.agent.agent import Agent
from agno.db.postgres.postgres import PostgresDb
from agno.os import AgentOS
from agno.tools.mcp import MCPTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

db = PostgresDb(id="basic-db", db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

# 第一个 agent。我们将在初始化时将其添加到 AgentOS。
agent1 = Agent(
    name="First Agent",
    markdown=True,
)

# 第二个 agent。我们将在 lifespan 函数中将其添加到 AgentOS。
agent2 = Agent(
    id="second-agent",
    name="Second Agent",
    tools=[MCPTools(transport="streamable-http", url="https://docs.agno.com/mcp")],
    markdown=True,
    db=db,
)


# 接收 AgentOS 实例作为参数的 Lifespan 函数。
@asynccontextmanager
async def lifespan(app, agent_os):
    # 添加新的 Agent
    agent_os.agents.append(agent2)

    # 重新同步 AgentOS
    agent_os.resync(app=app)

    yield


# 使用 lifespan 函数和第一个 agent 设置我们的 AgentOS。
agent_os = AgentOS(
    lifespan=lifespan,
    agents=[agent1],
    enable_mcp_server=True,
)

# 获取我们的应用。
app = agent_os.get_app()

# 服务应用。
# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="update_from_lifespan:app", reload=True)

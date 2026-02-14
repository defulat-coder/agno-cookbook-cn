"""
Agent 具有自定义生命周期的 AgentOS 示例应用。
"""

from contextlib import asynccontextmanager

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.anthropic import Claude
from agno.os import AgentOS
from agno.utils.log import log_info

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# 设置数据库
db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

# 设置基础 agent、团队和工作流
agno_support_agent = Agent(
    id="example-agent",
    name="Example Agent",
    model=Claude(id="claude-sonnet-4-0"),
    db=db,
    markdown=True,
)


@asynccontextmanager
async def lifespan(app):
    log_info("Starting My FastAPI App")
    yield
    log_info("Stopping My FastAPI App")


agent_os = AgentOS(
    description="Example app with custom lifespan",
    agents=[agno_support_agent],
    lifespan=lifespan,
)


app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """运行你的 AgentOS。

    你可以在此处测试你的 AgentOS：
    http://localhost:7777/docs

    """
    # 不要在这里使用 reload=True，这可能会导致生命周期问题
    agent_os.serve(app="custom_lifespan:app")

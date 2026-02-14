"""
Postgres 数据库后端
=========================

演示使用同步和异步设置的 PostgreSQL 存储的 AgentOS。
"""

from agno.agent import Agent
from agno.db.postgres import AsyncPostgresDb, PostgresDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.team.team import Team
from agno.workflow.step import Step
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
sync_db = PostgresDb(
    db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
)

async_db = AsyncPostgresDb(db_url="postgresql+psycopg_async://ai:ai@localhost:5532/ai")

# ---------------------------------------------------------------------------
# 创建同步 Agent、团队和 AgentOS
# ---------------------------------------------------------------------------
sync_agent = Agent(
    db=sync_db,
    name="Basic Agent",
    id="basic-agent",
    model=OpenAIChat(id="gpt-4o"),
    add_history_to_context=True,
    num_history_runs=3,
)

sync_team = Team(
    db=sync_db,
    id="basic-team",
    name="Team Agent",
    model=OpenAIChat(id="gpt-4o"),
    members=[sync_agent],
    add_history_to_context=True,
    num_history_runs=3,
)

sync_agent_os = AgentOS(
    description="Example OS setup",
    agents=[sync_agent],
    teams=[sync_team],
)

# ---------------------------------------------------------------------------
# 创建异步 Agent、团队、工作流和 AgentOS
# ---------------------------------------------------------------------------
async_agent = Agent(
    name="Basic Agent",
    id="basic-agent",
    model=OpenAIChat(id="gpt-4o"),
    db=async_db,
    update_memory_on_run=True,
    enable_session_summaries=True,
    add_history_to_context=True,
    num_history_runs=3,
    add_datetime_to_context=True,
    markdown=True,
)

async_team = Team(
    id="basic-team",
    name="Team Agent",
    model=OpenAIChat(id="gpt-4o"),
    db=async_db,
    update_memory_on_run=True,
    members=[async_agent],
)

async_workflow = Workflow(
    id="basic-workflow",
    name="Basic Workflow",
    description="Just a simple workflow",
    db=async_db,
    steps=[
        Step(
            name="step1",
            description="Just a simple step",
            agent=async_agent,
        )
    ],
)

async_agent_os = AgentOS(
    description="Example OS setup",
    agents=[async_agent],
    teams=[async_team],
    workflows=[async_workflow],
)

# ---------------------------------------------------------------------------
# 创建 AgentOS 应用
# ---------------------------------------------------------------------------
# 默认使用同步设置。切换到 async_agent_os 以运行异步变体。
agent_os = sync_agent_os
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent_os.serve(app="postgres:app", reload=True)

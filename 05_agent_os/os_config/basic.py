"""
基础
=====

演示基础功能。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.os.config import (
    AgentOSConfig,
    ChatConfig,
    DatabaseConfig,
    MemoryConfig,
    MemoryDomainConfig,
)
from agno.team import Team
from agno.workflow.step import Step
from agno.workflow.workflow import Workflow

# 设置数据库
db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai", id="db-0001")
db2 = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai2", id="db-0002")

# ---------------------------------------------------------------------------
# 创建 Agent、团队和工作流
# ---------------------------------------------------------------------------
basic_agent = Agent(
    name="Marketing Agent",
    db=db,
    enable_session_summaries=True,
    update_memory_on_run=True,
    add_history_to_context=True,
    num_history_runs=3,
    add_datetime_to_context=True,
    markdown=True,
)
basic_team = Team(
    id="basic-team",
    name="Basic Team",
    model=OpenAIChat(id="gpt-4o"),
    db=db,
    members=[basic_agent],
    update_memory_on_run=True,
)
basic_workflow = Workflow(
    id="basic-workflow",
    name="Basic Workflow",
    description="Just a simple workflow",
    db=db2,
    steps=[
        Step(
            name="step1",
            description="Just a simple step",
            agent=basic_agent,
        )
    ],
)

# 设置我们的 AgentOS 应用
agent_os = AgentOS(
    description="Your AgentOS",
    id="basic-os",
    agents=[basic_agent],
    teams=[basic_team],
    workflows=[basic_workflow],
    # AgentOS 的配置
    config=AgentOSConfig(
        chat=ChatConfig(
            quick_prompts={
                "marketing-agent": [
                    "What can you do?",
                    "How is our latest post working?",
                    "Tell me about our active marketing campaigns",
                ],
            },
        ),
        memory=MemoryConfig(
            dbs=[
                DatabaseConfig(
                    db_id=db.id,
                    domain_config=MemoryDomainConfig(
                        display_name="Main app user memories",
                    ),
                )
            ],
        ),
    ),
)
app = agent_os.get_app()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """运行你的 AgentOS。

    你可以在以下地址查看配置和可用端点：
    http://localhost:7777/config
    """
    agent_os.serve(app="basic:app", reload=True)

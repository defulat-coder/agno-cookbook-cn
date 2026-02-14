"""
Yaml 配置
===========

演示 yaml 配置。
"""

from pathlib import Path

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.os.interfaces.slack import Slack
from agno.os.interfaces.whatsapp import Whatsapp
from agno.team import Team
from agno.workflow.step import Step
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

cwd = Path(__file__).parent
os_config_path = str(cwd.joinpath("config.yaml"))

# 设置数据库
db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai", id="db-0001")

# 设置基础 agent、团队和工作流
basic_agent = Agent(
    id="basic-agent",
    name="Basic Agent",
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
    db=db,
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
    description="Example AgentOS",
    id="basic-os",
    agents=[basic_agent],
    teams=[basic_team],
    workflows=[basic_workflow],
    interfaces=[Whatsapp(agent=basic_agent), Slack(agent=basic_agent)],
    # AgentOS 的配置
    config=os_config_path,
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
    agent_os.serve(app="yaml_config:app", reload=True)

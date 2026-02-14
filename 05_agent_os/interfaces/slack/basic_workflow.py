"""
基础工作流
==============

演示基础工作流。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.os.interfaces.slack import Slack
from agno.tools.websearch import WebSearchTools
from agno.workflow.step import Step
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# 为工作流定义 agent
researcher_agent = Agent(
    name="Research Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[WebSearchTools()],
    role="搜索网络并收集有关给定主题的全面研究",
    instructions=[
        "搜索最新和最相关的信息",
        "关注可信来源和关键见解",
        "清晰简洁地总结发现",
    ],
)

writer_agent = Agent(
    name="Content Writer",
    model=OpenAIChat(id="gpt-4o-mini"),
    role="根据研究发现创建引人入胜的内容",
    instructions=[
        "以清晰、引人入胜和专业的语气写作",
        "用适当的标题和项目符号组织内容",
        "包含研究中的关键见解",
        "保持内容信息丰富但易于理解",
    ],
)

# 创建工作流步骤
research_step = Step(
    name="Research Step",
    agent=researcher_agent,
)

writing_step = Step(
    name="Writing Step",
    agent=writer_agent,
)

# 创建工作流
content_workflow = Workflow(
    name="Content Creation Workflow",
    description="通过 Slack 研究和创建任何主题的内容",
    db=PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai"),
    steps=[research_step, writing_step],
    session_id="slack_workflow_session",
)

# 创建带有 Slack 接口的 AgentOS 用于工作流
agent_os = AgentOS(
    workflows=[content_workflow],
    interfaces=[Slack(workflow=content_workflow)],
)

app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="basic_workflow:app", reload=True)

"""
带 Session 指标的工作流
=============================

演示在执行后收集和打印工作流 session 指标。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from agno.utils.pprint import pprint_run_response
from agno.workflow.step import Step
from agno.workflow.workflow import Workflow
from rich.pretty import pprint

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
hackernews_agent = Agent(
    name="Hackernews Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[HackerNewsTools()],
    role="从 Hackernews 帖子中提取关键见解和内容",
)

web_agent = Agent(
    name="Web Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[WebSearchTools()],
    role="搜索网络获取最新新闻和趋势",
)

content_planner = Agent(
    name="Content Planner",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "为提供的主题和研究内容规划 4 周的内容发布计划",
        "确保每周有 3 篇文章",
    ],
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
research_team = Team(
    name="Research Team",
    members=[hackernews_agent, web_agent],
    instructions="从 Hackernews 和网络研究技术主题",
)

# ---------------------------------------------------------------------------
# 定义步骤
# ---------------------------------------------------------------------------
research_step = Step(
    name="Research Step",
    team=research_team,
)

content_planning_step = Step(
    name="Content Planning Step",
    agent=content_planner,
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
content_creation_workflow = Workflow(
    name="Content Creation Workflow",
    description="从博客文章到社交媒体的自动化内容创作",
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/workflow_session_metrics.db",
    ),
    steps=[research_step, content_planning_step],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    response = content_creation_workflow.run(
        input="AI trends in 2024",
    )

    print("=" * 50)
    print("WORKFLOW RESPONSE")
    print("=" * 50)
    pprint_run_response(response, markdown=True)

    print("\n" + "=" * 50)
    print("SESSION METRICS")
    print("=" * 50)

    session_metrics = content_creation_workflow.get_session_metrics()
    pprint(session_metrics)

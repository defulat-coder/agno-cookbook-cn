"""
运行: `pip install openai ddgs sqlalchemy aiosqlite` 安装依赖
运行: `python cookbook/db/async_sqlite/async_sqlite_for_workflow.py` 运行工作流
"""

import asyncio

from agno.agent import Agent
from agno.db.sqlite import AsyncSqliteDb
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from agno.workflow.step import Step
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
db = AsyncSqliteDb(db_file="workflow_storage.db")

# ---------------------------------------------------------------------------
# 创建工作流
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
    role="在网上搜索最新的新闻和趋势",
)
content_planner = Agent(
    name="Content Planner",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "为提供的主题和研究内容计划 4 周的内容时间表",
        "确保每周有 3 篇帖子",
    ],
)

research_team = Team(
    name="Research Team",
    members=[hackernews_agent, web_agent],
    instructions="从 Hackernews 和网络研究科技话题",
)

research_step = Step(
    name="Research Step",
    team=research_team,
)
content_planning_step = Step(
    name="Content Planning Step",
    agent=content_planner,
)
content_creation_workflow = Workflow(
    name="Content Creation Workflow",
    description="从博客文章到社交媒体的自动化内容创建",
    db=db,
    steps=[research_step, content_planning_step],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(
        content_creation_workflow.aprint_response(
            input="AI trends in 2024",
            markdown=True,
        )
    )

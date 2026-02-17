"""
使用 JSON 文件作为工作流的数据库。
适用于性能不是关键的简单演示。

运行 `pip install ddgs openai` 安装依赖。
"""

from agno.agent import Agent
from agno.db.in_memory import InMemoryDb
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from agno.workflow.step import Step
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
db = InMemoryDb()

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

# 定义用于复杂分析的研究团队
research_team = Team(
    name="Research Team",
    members=[hackernews_agent, web_agent],
    instructions="从 Hackernews 和网络研究科技话题",
)

content_planner = Agent(
    name="Content Planner",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "为提供的主题和研究内容计划 4 周的内容时间表",
        "确保每周有 3 篇帖子",
    ],
)

# 定义步骤
research_step = Step(
    name="Research Step",
    team=research_team,
)

content_planning_step = Step(
    name="Content Planning Step",
    agent=content_planner,
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    content_creation_workflow = Workflow(
        name="Content Creation Workflow",
        description="从博客文章到社交媒体的自动化内容创建",
        db=db,
        steps=[research_step, content_planning_step],
    )
    content_creation_workflow.print_response(
        input="AI trends in 2024",
        markdown=True,
    )

"""
带路由的工作流
====================

演示带路由的工作流。
"""

from typing import List

from agno.agent.agent import Agent
from agno.db.sqlite import SqliteDb

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
# 导入工作流
from agno.os import AgentOS
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from agno.workflow.router import Router
from agno.workflow.step import Step
from agno.workflow.types import StepInput
from agno.workflow.workflow import Workflow

# 定义研究 agent
hackernews_agent = Agent(
    name="HackerNews Researcher",
    instructions="你是一位专门从 Hacker News 查找最新技术新闻和讨论的研究员。关注创业趋势、编程主题和科技行业见解。",
    tools=[HackerNewsTools()],
)

web_agent = Agent(
    name="Web Researcher",
    instructions="你是一位全面的网络研究员。搜索包括新闻网站、博客和官方文档在内的多个来源以收集详细信息。",
    tools=[WebSearchTools()],
)

content_agent = Agent(
    name="Content Publisher",
    instructions="你是一位内容创作者，利用研究数据创建引人入胜、结构良好的文章。使用适当的标题、要点和清晰的结论格式化内容。",
)

# 创建研究步骤
research_hackernews = Step(
    name="research_hackernews",
    agent=hackernews_agent,
    description="Research latest tech trends from Hacker News",
)

research_web = Step(
    name="research_web",
    agent=web_agent,
    description="Comprehensive web research on the topic",
)

publish_content = Step(
    name="publish_content",
    agent=content_agent,
    description="Create and format final content for publication",
)


# 现在返回要执行的 Step(s)
def research_router(step_input: StepInput) -> List[Step]:
    """
    根据输入主题决定使用哪种研究方法。
    返回一个包含要执行的步骤的列表。
    """
    # 如果这是第一步，则使用原始工作流消息
    topic = step_input.previous_step_content or step_input.input or ""
    topic = topic.lower()

    # 检查主题是否与技术/创业相关 - 使用 HackerNews
    tech_keywords = [
        "startup",
        "programming",
        "ai",
        "machine learning",
        "software",
        "developer",
        "coding",
        "tech",
        "silicon valley",
        "venture capital",
        "cryptocurrency",
        "blockchain",
        "open source",
        "github",
    ]

    if any(keyword in topic for keyword in tech_keywords):
        print(f"Tech topic detected: Using HackerNews research for '{topic}'")
        return [research_hackernews]
    else:
        print(f"General topic detected: Using web research for '{topic}'")
        return [research_web]


workflow = Workflow(
    name="intelligent-research-workflow",
    description="Automatically selects the best research method based on topic, then publishes content",
    steps=[
        Router(
            name="research_strategy_router",
            selector=research_router,
            choices=[research_hackernews, research_web],
            description="Intelligently selects research method based on topic",
        ),
        publish_content,
    ],
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/workflow.db",
    ),
)

# 使用工作流初始化 AgentOS
agent_os = AgentOS(
    description="Example OS setup",
    workflows=[workflow],
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="workflow_with_router:app", reload=True)

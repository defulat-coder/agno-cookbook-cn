"""
带嵌套步骤的工作流
==========================

演示带嵌套步骤的工作流。
"""

from typing import List

from agno.agent.agent import Agent
from agno.db.postgres import PostgresDb

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
# 导入工作流
from agno.os import AgentOS
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from agno.workflow.loop import Loop
from agno.workflow.router import Router
from agno.workflow.step import Step
from agno.workflow.types import StepInput, StepOutput
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

# 循环的结束条件函数


def research_quality_check(outputs: List[StepOutput]) -> bool:
    """
    评估研究结果是否充分
    返回 True 以中断循环，返回 False 以继续
    """
    if not outputs:
        return False

    # 检查任何输出是否包含大量内容
    for output in outputs:
        if output.content and len(output.content) > 300:
            print(
                f"[OK] Research quality check passed - found substantial content ({len(output.content)} chars)"
            )
            return True

    print("[FAIL] Research quality check failed - need more substantial research")
    return False


# 为深度技术研究创建循环步骤
deep_tech_research_loop = Loop(
    name="Deep Tech Research Loop",
    steps=[research_hackernews],
    end_condition=research_quality_check,
    max_iterations=3,
    description="Perform iterative deep research on tech topics",
)

# 路由函数，在简单网络研究或深度技术研究循环之间选择


def research_strategy_router(step_input: StepInput) -> List[Step]:
    """
    根据输入主题在简单网络研究或深度技术研究循环之间决定。
    返回单个网络研究步骤或技术研究循环。
    """
    return [deep_tech_research_loop]


workflow = Workflow(
    name="Adaptive Research Workflow",
    description="Intelligently selects between simple web research or deep iterative tech research based on topic complexity",
    steps=[
        Router(
            name="research_strategy_router",
            selector=research_strategy_router,
            choices=[research_web, deep_tech_research_loop],
            description="Chooses between simple web research or deep tech research loop",
        ),
        publish_content,
    ],
    db=PostgresDb(
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
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
    agent_os.serve(app="workflow_with_nested_steps:app", reload=True)

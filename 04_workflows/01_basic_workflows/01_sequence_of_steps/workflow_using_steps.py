"""
使用 Steps 的工作流
====================

演示如何使用 `Steps` 序列组合包含研究、写作和编辑步骤的工作流。
"""

import asyncio

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.websearch import WebSearchTools
from agno.workflow.step import Step
from agno.workflow.steps import Steps
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
researcher = Agent(
    name="Research Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[WebSearchTools()],
    instructions="研究给定主题并提供关键事实和见解。",
)

writer = Agent(
    name="Writing Agent",
    model=OpenAIChat(id="gpt-4o"),
    instructions="根据提供的研究撰写一篇全面的文章。使其引人入胜且结构清晰。",
)

editor = Agent(
    name="Editor Agent",
    model=OpenAIChat(id="gpt-4o"),
    instructions="审查和编辑文章的清晰度、语法和流畅性。提供精修的最终版本。",
)

# ---------------------------------------------------------------------------
# 定义步骤
# ---------------------------------------------------------------------------
research_step = Step(
    name="research",
    agent=researcher,
    description="研究主题并收集信息",
)

writing_step = Step(
    name="writing",
    agent=writer,
    description="根据研究撰写文章",
)

editing_step = Step(
    name="editing",
    agent=editor,
    description="编辑和润色文章",
)

article_creation_sequence = Steps(
    name="article_creation",
    description="从研究到最终编辑的完整文章创作工作流",
    steps=[research_step, writing_step, editing_step],
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
article_workflow = Workflow(
    name="Article Creation Workflow",
    description="从研究到发布的自动化文章创作",
    steps=[article_creation_sequence],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 同步运行
    article_workflow.print_response(
        input="Write an article about the benefits of renewable energy",
        markdown=True,
    )

    # 异步运行
    asyncio.run(
        article_workflow.aprint_response(
            input="Write an article about the benefits of renewable energy",
            markdown=True,
        )
    )

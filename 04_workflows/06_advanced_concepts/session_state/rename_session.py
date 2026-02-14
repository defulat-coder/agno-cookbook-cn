"""
重命名会话
==============

演示在运行后自动生成工作流会话名称。
"""

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
    instructions="根据提供的研究撰写一篇全面的文章。使其引人入胜且结构良好。",
)

# ---------------------------------------------------------------------------
# Define Steps
# ---------------------------------------------------------------------------
research_step = Step(
    name="research",
    agent=researcher,
    description="Research the topic and gather information",
)

writing_step = Step(
    name="writing",
    agent=writer,
    description="Write an article based on the research",
)

article_creation_sequence = Steps(
    name="article_creation",
    description="Complete article creation workflow from research to writing",
    steps=[research_step, writing_step],
)

# ---------------------------------------------------------------------------
# Run Workflow
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    article_workflow = Workflow(
        description="Automated article creation from research to writing",
        steps=[article_creation_sequence],
        debug_mode=True,
    )

    article_workflow.print_response(
        input="Write an article about the benefits of renewable energy",
        markdown=True,
    )

    article_workflow.set_session_name(autogenerate=True)
    print(f"New session name: {article_workflow.session_name}")

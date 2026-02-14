"""
带文件输入的工作流
========================

演示通过工作流步骤传递文件输入以进行阅读和摘要。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.media import File
from agno.models.anthropic import Claude
from agno.models.openai import OpenAIChat
from agno.workflow.step import Step
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
read_agent = Agent(
    name="Agent",
    model=Claude(id="claude-sonnet-4-20250514"),
    role="阅读附加文件的内容。",
)

summarize_agent = Agent(
    name="Summarize Agent",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "总结附加文件的内容。",
    ],
)

# ---------------------------------------------------------------------------
# 定义步骤
# ---------------------------------------------------------------------------
read_step = Step(
    name="Read Step",
    agent=read_agent,
)

summarize_step = Step(
    name="Summarize Step",
    agent=summarize_agent,
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
content_creation_workflow = Workflow(
    name="Content Creation Workflow",
    description="从博客文章到社交媒体的自动化内容创作",
    db=SqliteDb(
        session_table="workflow",
        db_file="tmp/workflow.db",
    ),
    steps=[read_step, summarize_step],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    content_creation_workflow.print_response(
        input="Summarize the contents of the attached file.",
        files=[
            File(url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf")
        ],
        markdown=True,
    )

"""使用 Async MySQL 作为工作流的数据库。
运行 `uv pip install openai duckduckgo-search sqlalchemy asyncmy agno` 安装依赖。
"""

import asyncio
import uuid
from typing import List

from agno.agent import Agent
from agno.db.base import SessionType
from agno.db.mysql import AsyncMySQLDb
from agno.tools.websearch import WebSearchTools
from agno.workflow.types import WorkflowExecutionInput
from agno.workflow.workflow import Workflow
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
db_url = "mysql+asyncmy://ai:ai@localhost:3306/ai"
db = AsyncMySQLDb(db_url=db_url)


# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
class ResearchTopic(BaseModel):
    topic: str
    key_points: List[str]
    summary: str


# 创建研究者 Agent
researcher = Agent(
    name="Researcher",
    tools=[WebSearchTools()],
    instructions="深入研究给定的主题并提供关键见解",
    output_schema=ResearchTopic,
)

# 创建写作者 Agent
writer = Agent(
    name="Writer",
    instructions="根据提供的研究撰写结构良好的博客文章",
)


# 定义工作流
async def blog_workflow(workflow: Workflow, execution_input: WorkflowExecutionInput):
    """
    一个研究主题并撰写博客文章的工作流。
    """
    topic = execution_input.input

    # 步骤 1：研究主题
    research_result = await researcher.arun(f"Research this topic: {topic}")

    # 步骤 2：撰写博客文章
    if research_result and research_result.content:
        blog_result = await writer.arun(
            f"Write a blog post about {topic}. Use this research: {research_result.content.model_dump_json()}"
        )
        return blog_result.content

    return "Failed to complete workflow"


workflow = Workflow(
    name="Blog Generator",
    steps=blog_workflow,
    db=db,
)


# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
async def main():
    """使用示例主题运行工作流"""
    session_id = str(uuid.uuid4())

    await workflow.aprint_response(
        input="The future of artificial intelligence",
        session_id=session_id,
        markdown=True,
    )
    session_data = await db.get_session(
        session_id=session_id, session_type=SessionType.WORKFLOW
    )
    print("\n=== SESSION DATA ===")
    print(session_data.to_dict())


if __name__ == "__main__":
    asyncio.run(main())

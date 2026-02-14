"""
顺序执行步骤
=================

演示使用同步、异步、流式和事件流式运行模式的顺序工作流执行。
"""

import asyncio
from textwrap import dedent
from typing import AsyncIterator

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.run.workflow import WorkflowRunEvent, WorkflowRunOutputEvent
from agno.team import Team
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from agno.workflow.step import Step
from agno.workflow.types import StepInput, StepOutput
from agno.workflow.workflow import Workflow

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

writer_agent = Agent(
    name="Writer Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="撰写关于该主题的博客文章",
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


async def prepare_input_for_web_search(
    step_input: StepInput,
) -> AsyncIterator[StepOutput]:
    topic = step_input.input
    content = dedent(
        f"""\
        I'm writing a blog post on the topic
        <topic>
        {topic}
        </topic>

        Search the web for atleast 10 articles\
        """
    )
    yield StepOutput(content=content)


async def prepare_input_for_writer(step_input: StepInput) -> AsyncIterator[StepOutput]:
    topic = step_input.input
    research_team_output = step_input.previous_step_content
    content = dedent(
        f"""\
        I'm writing a blog post on the topic:
        <topic>
        {topic}
        </topic>

        Here is information from the web:
        <research_results>
        {research_team_output}
        </research_results>\
        """
    )
    yield StepOutput(content=content)


# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
content_creation_workflow = Workflow(
    name="Content Creation Workflow",
    description="从博客文章到社交媒体的自动化内容创作",
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/workflow.db",
    ),
    steps=[research_step, content_planning_step],
)

blog_post_workflow = Workflow(
    name="Blog Post Workflow",
    description="从 Hackernews 和网络自动创建博客文章",
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/workflow.db",
    ),
    steps=[
        prepare_input_for_web_search,
        research_team,
        prepare_input_for_writer,
        writer_agent,
    ],
)


async def stream_run_events() -> None:
    events: AsyncIterator[WorkflowRunOutputEvent] = blog_post_workflow.arun(
        input="AI trends in 2024",
        markdown=True,
        stream=True,
        stream_events=True,
    )
    async for event in events:
        if event.event == WorkflowRunEvent.condition_execution_started.value:
            print(event)
            print()
        elif event.event == WorkflowRunEvent.condition_execution_completed.value:
            print(event)
            print()
        elif event.event == WorkflowRunEvent.workflow_started.value:
            print(event)
            print()
        elif event.event == WorkflowRunEvent.step_started.value:
            print(event)
            print()
        elif event.event == WorkflowRunEvent.step_completed.value:
            print(event)
            print()
        elif event.event == WorkflowRunEvent.workflow_completed.value:
            print(event)
            print()


# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 同步运行
    content_creation_workflow.print_response(
        input="AI trends in 2024",
        markdown=True,
    )

    # 同步流式运行
    content_creation_workflow.print_response(
        input="AI trends in 2024",
        markdown=True,
        stream=True,
    )

    # 异步运行
    asyncio.run(
        content_creation_workflow.aprint_response(
            input="AI agent frameworks 2025",
            markdown=True,
        )
    )

    # 异步流式运行
    asyncio.run(
        content_creation_workflow.aprint_response(
            input="AI agent frameworks 2025",
            markdown=True,
            stream=True,
        )
    )

    # 异步流式事件运行
    asyncio.run(stream_run_events())

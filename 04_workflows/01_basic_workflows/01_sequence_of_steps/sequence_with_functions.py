"""
函数序列
=======================

演示函数步骤和 Agent/团队步骤的顺序执行，包括同步、异步和流式运行。
"""

import asyncio
from textwrap import dedent
from typing import AsyncIterator, Iterator

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from agno.workflow.types import StepInput, StepOutput
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
web_agent = Agent(
    name="Web Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[WebSearchTools()],
    role="搜索网络获取最新新闻和趋势",
)

hackernews_agent = Agent(
    name="Hackernews Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[HackerNewsTools()],
    role="从 Hackernews 帖子中提取关键见解和内容",
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
# 定义函数步骤
# ---------------------------------------------------------------------------
def prepare_input_for_web_search_sync(step_input: StepInput) -> StepOutput:
    topic = step_input.input
    return StepOutput(
        content=dedent(
            f"""\
            I'm writing a blog post on the topic
            <topic>
            {topic}
            </topic>

            Search the web for atleast 10 articles\
            """
        )
    )


def prepare_input_for_writer_sync(step_input: StepInput) -> StepOutput:
    topic = step_input.input
    research_team_output = step_input.previous_step_content
    return StepOutput(
        content=dedent(
            f"""\
            I'm writing a blog post on the topic:
            <topic>
            {topic}
            </topic>

            Here is information from the web:
            <research_results>
            {research_team_output}
            <research_results>\
            """
        )
    )


def prepare_input_for_web_search_sync_stream(
    step_input: StepInput,
) -> Iterator[StepOutput]:
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


def prepare_input_for_writer_sync_stream(step_input: StepInput) -> Iterator[StepOutput]:
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


async def prepare_input_for_web_search_async(step_input: StepInput) -> StepOutput:
    topic = step_input.input
    return StepOutput(
        content=dedent(
            f"""\
            I'm writing a blog post on the topic
            <topic>
            {topic}
            </topic>

            Search the web for atleast 10 articles\
            """
        )
    )


async def prepare_input_for_writer_async(step_input: StepInput) -> StepOutput:
    topic = step_input.input
    research_team_output = step_input.previous_step_content
    return StepOutput(
        content=dedent(
            f"""\
            I'm writing a blog post on the topic:
            <topic>
            {topic}
            </topic>

            Here is information from the web:
            <research_results>
            {research_team_output}
            <research_results>\
            """
        )
    )


async def prepare_input_for_web_search_async_stream(
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


async def prepare_input_for_writer_async_stream(
    step_input: StepInput,
) -> AsyncIterator[StepOutput]:
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
sync_workflow = Workflow(
    name="Blog Post Workflow",
    description="从 Hackernews 和网络自动创建博客文章",
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/workflow.db",
    ),
    steps=[
        prepare_input_for_web_search_sync,
        research_team,
        prepare_input_for_writer_sync,
        writer_agent,
    ],
)

sync_stream_workflow = Workflow(
    name="Blog Post Workflow",
    description="从 Hackernews 和网络自动创建博客文章",
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/workflow.db",
    ),
    steps=[
        prepare_input_for_web_search_sync_stream,
        research_team,
        prepare_input_for_writer_sync_stream,
        writer_agent,
    ],
)

async_workflow = Workflow(
    name="Blog Post Workflow",
    description="从 Hackernews 和网络自动创建博客文章",
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/workflow.db",
    ),
    steps=[
        prepare_input_for_web_search_async,
        research_team,
        prepare_input_for_writer_async,
        writer_agent,
    ],
)

async_stream_workflow = Workflow(
    name="Blog Post Workflow",
    description="从 Hackernews 和网络自动创建博客文章",
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/workflow.db",
    ),
    steps=[
        prepare_input_for_web_search_async_stream,
        research_team,
        prepare_input_for_writer_async_stream,
        writer_agent,
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 同步运行
    sync_workflow.print_response(
        input="AI trends in 2024",
        markdown=True,
    )

    # 同步流式运行
    sync_stream_workflow.print_response(
        input="AI trends in 2024",
        markdown=True,
        stream=True,
    )

    # 异步运行
    asyncio.run(
        async_workflow.aprint_response(
            input="AI trends in 2024",
            markdown=True,
        )
    )

    # 异步流式运行
    asyncio.run(
        async_stream_workflow.aprint_response(
            input="AI trends in 2024",
            markdown=True,
            stream=True,
        )
    )

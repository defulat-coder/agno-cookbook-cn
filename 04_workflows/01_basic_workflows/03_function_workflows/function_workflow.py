"""
函数工作流
=================

演示在同步和异步运行模式中使用单个执行函数代替显式步骤列表。
"""

import asyncio
from typing import AsyncIterator, Iterator

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from agno.workflow.types import WorkflowExecutionInput
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

streaming_hackernews_agent = Agent(
    name="Hackernews Agent",
    model=OpenAIChat(id="gpt-5.2"),
    tools=[HackerNewsTools()],
    role="从 Hackernews 帖子中研究关键见解和内容",
)

content_planner = Agent(
    name="Content Planner",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "为提供的主题和研究内容规划 4 周的内容发布计划",
        "确保每周有 3 篇文章",
    ],
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
# 定义执行函数
# ---------------------------------------------------------------------------
def custom_execution_function(
    workflow: Workflow,
    execution_input: WorkflowExecutionInput,
) -> str:
    print(f"执行工作流：{workflow.name}")
    run_response = research_team.run(execution_input.input)
    research_content = run_response.content
    planning_prompt = f"""
        战略内容规划请求：

        核心主题：{execution_input.input}

        研究结果：{research_content[:500]}

        规划要求：
        1. 基于研究创建全面的内容策略
        2. 有效利用研究发现
        3. 确定内容格式和渠道
        4. 提供时间表和优先级建议
        5. 包含参与度和分发策略

        请创建详细的、可执行的内容计划。
    """
    content_plan = content_planner.run(planning_prompt)
    return content_plan.content


def custom_execution_function_stream(
    workflow: Workflow,
    execution_input: WorkflowExecutionInput,
) -> Iterator:
    print(f"执行工作流：{workflow.name}")
    research_content = ""
    for response in streaming_hackernews_agent.run(
        execution_input.input,
        stream=True,
        stream_events=True,
    ):
        if hasattr(response, "content") and response.content:
            research_content += str(response.content)

    planning_prompt = f"""
        战略内容规划请求：

        核心主题：{execution_input.input}

        研究结果：{research_content[:500]}

        规划要求：
        1. 基于研究创建全面的内容策略
        2. 有效利用研究发现
        3. 确定内容格式和渠道
        4. 提供时间表和优先级建议
        5. 包含参与度和分发策略

        请创建详细的、可执行的内容计划。
    """
    yield from content_planner.run(
        planning_prompt,
        stream=True,
        stream_events=True,
    )


async def custom_execution_function_async(
    workflow: Workflow,
    execution_input: WorkflowExecutionInput,
) -> str:
    print(f"执行工作流：{workflow.name}")
    run_response = research_team.run(execution_input.input)
    research_content = run_response.content
    planning_prompt = f"""
        战略内容规划请求：

        核心主题：{execution_input.input}

        研究结果：{research_content[:500]}

        规划要求：
        1. 基于研究创建全面的内容策略
        2. 有效利用研究发现
        3. 确定内容格式和渠道
        4. 提供时间表和优先级建议
        5. 包含参与度和分发策略

        请创建详细的、可执行的内容计划。
    """
    content_plan = await content_planner.arun(planning_prompt)
    return content_plan.content


async def custom_execution_function_async_stream(
    workflow: Workflow,
    execution_input: WorkflowExecutionInput,
) -> AsyncIterator:
    print(f"执行工作流：{workflow.name}")
    research_content = ""
    async for response in streaming_hackernews_agent.arun(
        execution_input.input,
        stream=True,
        stream_events=True,
    ):
        if hasattr(response, "content") and response.content:
            research_content += str(response.content)

    planning_prompt = f"""
        战略内容规划请求：

        核心主题：{execution_input.input}

        研究结果：{research_content[:500]}

        规划要求：
        1. 基于研究创建全面的内容策略
        2. 有效利用研究发现
        3. 确定内容格式和渠道
        4. 提供时间表和优先级建议
        5. 包含参与度和分发策略

        请创建详细的、可执行的内容计划。
    """

    async for response in content_planner.arun(
        planning_prompt,
        stream=True,
        stream_events=True,
    ):
        yield response


# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
sync_workflow = Workflow(
    name="Content Creation Workflow",
    description="从博客文章到社交媒体的自动化内容创作",
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/workflow.db",
    ),
    steps=custom_execution_function,
)

sync_stream_workflow = Workflow(
    name="Content Creation Workflow",
    description="从博客文章到社交媒体的自动化内容创作",
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/workflow.db",
    ),
    steps=custom_execution_function_stream,
)

async_workflow = Workflow(
    name="Content Creation Workflow",
    description="从博客文章到社交媒体的自动化内容创作",
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/workflow.db",
    ),
    steps=custom_execution_function_async,
)

async_stream_workflow = Workflow(
    name="Content Creation Workflow",
    description="从博客文章到社交媒体的自动化内容创作",
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/workflow.db",
    ),
    steps=custom_execution_function_async_stream,
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 同步运行
    sync_workflow.print_response(
        input="AI trends in 2024",
    )

    # 同步流式运行
    sync_stream_workflow.print_response(
        input="AI trends in 2024",
        stream=True,
    )

    # 异步运行
    asyncio.run(
        async_workflow.aprint_response(
            input="AI trends in 2024",
        )
    )

    # 异步流式运行
    asyncio.run(
        async_stream_workflow.aprint_response(
            input="AI trends in 2024",
            stream=True,
        )
    )

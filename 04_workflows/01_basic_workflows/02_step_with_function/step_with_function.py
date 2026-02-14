"""
带函数的步骤
==================

演示在基于步骤的工作流中使用自定义函数执行器，包括同步、同步流式和异步流式运行。
"""

import asyncio
from typing import AsyncIterator, Iterator, Union

from agno.agent import Agent
from agno.db.in_memory import InMemoryDb
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.run.workflow import WorkflowRunOutputEvent
from agno.team import Team
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from agno.workflow.step import Step, StepInput, StepOutput
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
hackernews_agent = Agent(
    name="Hackernews Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[HackerNewsTools()],
    instructions="从 Hackernews 帖子中提取关键见解和内容",
)

web_agent = Agent(
    name="Web Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[WebSearchTools()],
    instructions="搜索网络获取最新新闻和趋势",
)

content_planner = Agent(
    name="Content Planner",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "为提供的主题和研究内容规划 4 周的内容发布计划",
        "确保每周有 3 篇文章",
    ],
)

streaming_content_planner = Agent(
    name="Content Planner",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "为提供的主题和研究内容规划 4 周的内容发布计划",
        "确保每周有 3 篇文章",
    ],
    db=InMemoryDb(),
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
research_team = Team(
    name="Research Team",
    members=[hackernews_agent, web_agent],
    instructions="分析内容并创建全面的社交媒体策略",
)


# ---------------------------------------------------------------------------
# 定义函数执行器
# ---------------------------------------------------------------------------
def custom_content_planning_function(step_input: StepInput) -> StepOutput:
    message = step_input.input
    previous_step_content = step_input.previous_step_content
    planning_prompt = f"""
        战略内容规划请求：

        核心主题：{message}

        研究结果：{previous_step_content[:500] if previous_step_content else "无研究结果"}

        规划要求：
        1. 基于研究创建全面的内容策略
        2. 有效利用研究发现
        3. 确定内容格式和渠道
        4. 提供时间表和优先级建议
        5. 包含参与度和分发策略

        请创建详细的、可执行的内容计划。
    """

    try:
        response = content_planner.run(planning_prompt)
        enhanced_content = f"""
            ## 战略内容计划

            **规划主题：** {message}

            **研究整合：** {"✓ 基于研究" if previous_step_content else "✗ 无研究基础"}

            **内容策略：**
            {response.content}

            **自定义规划增强：**
            - 研究整合：{"高" if previous_step_content else "基准"}
            - 战略对齐：针对多渠道分发进行优化
            - 执行就绪：包含详细行动项
        """.strip()
        return StepOutput(content=enhanced_content)
    except Exception as e:
            return StepOutput(
                content=f"自定义内容规划失败：{str(e)}",
                success=False,
            )


def custom_content_planning_function_stream(
    step_input: StepInput,
) -> Iterator[Union[WorkflowRunOutputEvent, StepOutput]]:
    message = step_input.input
    previous_step_content = step_input.previous_step_content
    planning_prompt = f"""
        战略内容规划请求：

        核心主题：{message}

        研究结果：{previous_step_content[:500] if previous_step_content else "无研究结果"}

        规划要求：
        1. 基于研究创建全面的内容策略
        2. 有效利用研究发现
        3. 确定内容格式和渠道
        4. 提供时间表和优先级建议
        5. 包含参与度和分发策略

        请创建详细的、可执行的内容计划。
    """

    try:
        response_iterator = streaming_content_planner.run(
            planning_prompt,
            stream=True,
            stream_events=True,
        )
        for event in response_iterator:
            yield event

        response = streaming_content_planner.get_last_run_output()
        enhanced_content = f"""
            ## Strategic Content Plan

            **Planning Topic:** {message}

            **Research Integration:** {"✓ Research-based" if previous_step_content else "✗ No research foundation"}

            **Content Strategy:**
            {response.content}

            **Custom Planning Enhancements:**
            - Research Integration: {"High" if previous_step_content else "Baseline"}
            - Strategic Alignment: Optimized for multi-channel distribution
            - Execution Ready: Detailed action items included
        """.strip()
        yield StepOutput(content=enhanced_content)
    except Exception as e:
        yield StepOutput(
            content=f"Custom content planning failed: {str(e)}",
            success=False,
        )


async def custom_content_planning_function_async_stream(
    step_input: StepInput,
) -> AsyncIterator[Union[WorkflowRunOutputEvent, StepOutput]]:
    message = step_input.input
    previous_step_content = step_input.previous_step_content
    planning_prompt = f"""
        战略内容规划请求：

        核心主题：{message}

        研究结果：{previous_step_content[:500] if previous_step_content else "无研究结果"}

        规划要求：
        1. 基于研究创建全面的内容策略
        2. 有效利用研究发现
        3. 确定内容格式和渠道
        4. 提供时间表和优先级建议
        5. 包含参与度和分发策略

        请创建详细的、可执行的内容计划。
    """

    try:
        response_iterator = streaming_content_planner.arun(
            planning_prompt,
            stream=True,
            stream_events=True,
        )
        async for event in response_iterator:
            yield event

        response = streaming_content_planner.get_last_run_output()
        enhanced_content = f"""
            ## Strategic Content Plan

            **Planning Topic:** {message}

            **Research Integration:** {"✓ Research-based" if previous_step_content else "✗ No research foundation"}

            **Content Strategy:**
            {response.content}

            **Custom Planning Enhancements:**
            - Research Integration: {"High" if previous_step_content else "Baseline"}
            - Strategic Alignment: Optimized for multi-channel distribution
            - Execution Ready: Detailed action items included
        """.strip()
        yield StepOutput(content=enhanced_content)
    except Exception as e:
        yield StepOutput(
            content=f"Custom content planning failed: {str(e)}",
            success=False,
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
    executor=custom_content_planning_function,
)

streaming_content_planning_step = Step(
    name="Content Planning Step",
    executor=custom_content_planning_function_stream,
)

async_streaming_content_planning_step = Step(
    name="Content Planning Step",
    executor=custom_content_planning_function_async_stream,
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
content_creation_workflow = Workflow(
    name="Content Creation Workflow",
    description="带自定义执行选项的自动化内容创作",
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/workflow.db",
    ),
    steps=[research_step, content_planning_step],
)

streaming_content_workflow = Workflow(
    name="Streaming Content Creation Workflow",
    description="带流式自定义执行函数的自动化内容创作",
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/workflow.db",
    ),
    steps=[research_step, streaming_content_planning_step],
)

async_content_workflow = Workflow(
    name="Content Creation Workflow",
    description="带自定义执行选项的自动化内容创作",
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/workflow.db",
    ),
    steps=[research_step, async_streaming_content_planning_step],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 同步运行
    content_creation_workflow.print_response(
        input="AI trends in 2024",
        markdown=True,
    )

    print("\n" + "=" * 60 + "\n")

    # 同步流式运行
    streaming_content_workflow.print_response(
        input="AI trends in 2024",
        markdown=True,
        stream=True,
    )

    # 异步流式运行
    asyncio.run(
        async_content_workflow.aprint_response(
            input="AI agent frameworks 2025",
            markdown=True,
            stream=True,
        )
    )

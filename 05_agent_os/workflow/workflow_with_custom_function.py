"""
带自定义函数执行器的工作流
=======================================

演示使用同步和流式自定义函数步骤的 AgentOS 工作流。
"""

from typing import AsyncIterator, Union

from agno.agent import Agent
from agno.db.in_memory import InMemoryDb
from agno.db.postgres import PostgresDb
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.team import Team
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from agno.workflow.step import Step, StepInput, StepOutput, WorkflowRunOutputEvent
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
USE_STREAMING_WORKFLOW = False

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# ---------------------------------------------------------------------------
# Create Agents And Team
# ---------------------------------------------------------------------------
hackernews_agent = Agent(
    name="Hackernews Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[HackerNewsTools()],
    instructions="从 Hackernews 文章中提取关键见解和内容",
)

web_agent = Agent(
    name="Web Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[WebSearchTools()],
    instructions="搜索网络以获取最新新闻和趋势",
)

research_team = Team(
    name="Research Team",
    members=[hackernews_agent, web_agent],
    instructions="分析内容并创建全面的社交媒体策略",
)

sync_content_planner = Agent(
    name="Content Planner",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "为提供的主题和研究内容规划 4 周的内容安排",
        "确保每周有 3 篇文章",
    ],
)

streaming_content_planner = Agent(
    name="Content Planner",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "为提供的主题和研究内容规划 4 周的内容安排",
        "确保每周有 3 篇文章",
    ],
    db=InMemoryDb(),
)


# ---------------------------------------------------------------------------
# Create Custom Functions
# ---------------------------------------------------------------------------
def custom_content_planning_function(step_input: StepInput) -> StepOutput:
    """使用之前的工作流上下文创建内容计划。"""
    message = step_input.input
    previous_step_content = step_input.previous_step_content

    planning_prompt = f"""
        战略内容规划请求：

        核心主题：{message}

        研究结果：{previous_step_content[:500] if previous_step_content else "没有研究结果"}

        规划要求：
        1. 根据研究创建全面的内容策略
        2. 有效利用研究发现
        3. 识别内容格式和渠道
        4. 提供时间表和优先级建议
        5. 包括参与和分发策略

        请创建详细、可执行的内容计划。
    """

    try:
        response = sync_content_planner.run(planning_prompt)
        enhanced_content = f"""
            ## 战略内容计划

            **规划主题：** {message}

            **研究整合：** {"基于研究" if previous_step_content else "无研究基础"}

            **内容策略：**
            {response.content}

            **自定义规划增强：**
            - 研究整合：{"高" if previous_step_content else "基线"}
            - 战略对齐：针对多渠道分发进行优化
            - 执行就绪：包含详细行动项
        """.strip()
        return StepOutput(content=enhanced_content)
    except Exception as exc:
        return StepOutput(
            content=f"自定义内容规划失败：{str(exc)}", success=False
        )


async def streaming_custom_content_planning_function(
    step_input: StepInput,
) -> AsyncIterator[Union[WorkflowRunOutputEvent, StepOutput]]:
    """Create a content plan with streamed planner output events."""
    message = step_input.input
    previous_step_content = step_input.previous_step_content

    planning_prompt = f"""
        STRATEGIC CONTENT PLANNING REQUEST:

        Core Topic: {message}

        Research Results: {previous_step_content[:500] if previous_step_content else "No research results"}

        Planning Requirements:
        1. Create a comprehensive content strategy based on the research
        2. Leverage the research findings effectively
        3. Identify content formats and channels
        4. Provide timeline and priority recommendations
        5. Include engagement and distribution strategies

        Please create a detailed, actionable content plan.
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

            **Research Integration:** {"Research-based" if previous_step_content else "No research foundation"}

            **Content Strategy:**
            {response.content}

            **Custom Planning Enhancements:**
            - Research Integration: {"High" if previous_step_content else "Baseline"}
            - Strategic Alignment: Optimized for multi-channel distribution
            - Execution Ready: Detailed action items included
        """.strip()
        yield StepOutput(content=enhanced_content)
    except Exception as exc:
        yield StepOutput(
            content=f"Custom content planning failed: {str(exc)}", success=False
        )


# ---------------------------------------------------------------------------
# Create Workflows
# ---------------------------------------------------------------------------
sync_content_creation_workflow = Workflow(
    name="Content Creation Workflow",
    description="Automated content creation with custom execution options",
    db=PostgresDb(
        session_table="workflow_session",
        db_url=db_url,
    ),
    steps=[
        Step(
            name="Research Step",
            team=research_team,
        ),
        Step(
            name="Content Planning Step",
            executor=custom_content_planning_function,
        ),
    ],
)

streaming_content_creation_workflow = Workflow(
    name="Streaming Content Creation Workflow",
    description="Automated content creation with streaming custom execution functions",
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/workflow.db",
    ),
    steps=[
        Step(
            name="Research Step",
            team=research_team,
        ),
        Step(
            name="Content Planning Step",
            executor=streaming_custom_content_planning_function,
        ),
    ],
)

# ---------------------------------------------------------------------------
# Create AgentOS
# ---------------------------------------------------------------------------
agent_os = AgentOS(
    description="带 playground 功能的基础 agent 示例应用",
    workflows=[
        streaming_content_creation_workflow
        if USE_STREAMING_WORKFLOW
        else sync_content_creation_workflow
    ],
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent_os.serve(app="workflow_with_custom_function:app", reload=True)

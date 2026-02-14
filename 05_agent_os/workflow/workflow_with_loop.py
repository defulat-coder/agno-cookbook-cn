"""
带循环的工作流
==================

演示带循环的工作流。
"""

from typing import List

from agno.agent.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai.chat import OpenAIChat

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
# 导入工作流
from agno.os import AgentOS
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from agno.workflow.loop import Loop
from agno.workflow.step import Step
from agno.workflow.types import StepOutput
from agno.workflow.workflow import Workflow

research_agent = Agent(
    name="Research Agent",
    role="Research specialist",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[HackerNewsTools(), WebSearchTools()],
    instructions="你是一位研究专家。彻底研究给定的主题。",
    markdown=True,
)

content_agent = Agent(
    name="Content Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    role="Content creator",
    instructions="你是一位内容创作者。根据研究创建引人入胜的内容。",
    markdown=True,
)

# 创建研究步骤
research_hackernews_step = Step(
    name="Research HackerNews",
    agent=research_agent,
    description="Research trending topics on HackerNews",
)

research_web_step = Step(
    name="Research Web",
    agent=research_agent,
    description="Research additional information from web sources",
)

content_step = Step(
    name="Create Content",
    agent=content_agent,
    description="Create content based on research findings",
)

# 结束条件函数


def research_evaluator(outputs: List[StepOutput]) -> bool:
    """
    评估研究结果是否充分
    返回 True 以中断循环，返回 False 以继续
    """
    # 检查是否有良好的研究结果
    if not outputs:
        return False

    # 简单检查 - 如果任何输出包含大量内容，我们就满意了
    for output in outputs:
        if output.content and len(output.content) > 200:
            print(
                f"✅ Research evaluation passed - found substantial content ({len(output.content)} chars)"
            )
            return True

    print("❌ Research evaluation failed - need more substantial research")
    return False


# 创建带循环的工作流
workflow = Workflow(
    name="research-and-content-workflow",
    description="Research topics in a loop until conditions are met, then create content",
    steps=[
        Loop(
            name="Research Loop",
            steps=[research_hackernews_step, research_web_step],
            end_condition=research_evaluator,
            max_iterations=3,  # 最多 3 次迭代
        ),
        content_step,
    ],
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/workflow.db",
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
    agent_os.serve(app="workflow_with_loop:app", reload=True)

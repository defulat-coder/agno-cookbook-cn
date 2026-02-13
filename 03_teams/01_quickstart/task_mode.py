"""
任务模式
=============================

演示使用 TeamMode.tasks 进行自主任务分解和执行。
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.team import Team, TeamMode

# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
researcher = Agent(
    name="Researcher",
    model=OpenAIResponses(id="gpt-5.2"),
    role="研究需求并收集参考资料",
)

architect = Agent(
    name="Architect",
    model=OpenAIResponses(id="gpt-5.2"),
    role="设计执行计划和任务依赖关系",
)

writer = Agent(
    name="Writer",
    model=OpenAIResponses(id="gpt-5.2"),
    role="编写简洁的交付摘要",
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
tasks_team = Team(
    name="Task Execution Team",
    members=[researcher, architect, writer],
    model=OpenAIResponses(id="gpt-5.2"),
    mode=TeamMode.tasks,
    instructions=[
        "在开始之前将目标分解为具有依赖关系的清晰任务。",
        "将每个任务分配给最合适的成员。",
        "跟踪任务完成情况并明确显示阻塞因素。",
        "提供包含已完成任务的最终综合摘要。",
    ],
    markdown=True,
    show_members_responses=True,
)

# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    tasks_team.print_response(
        "Plan a launch checklist for a new AI feature, including engineering, QA, and rollout tasks.",
        stream=True,
    )

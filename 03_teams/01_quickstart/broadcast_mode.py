"""
广播模式
=============================

演示使用 TeamMode.broadcast 将相同任务委托给所有成员。
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.team import Team, TeamMode

# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
product_manager = Agent(
    name="Product Manager",
    model=OpenAIResponses(id="gpt-5.2"),
    role="评估用户和业务影响",
)

engineer = Agent(
    name="Engineer",
    model=OpenAIResponses(id="gpt-5.2"),
    role="评估技术可行性和风险",
)

designer = Agent(
    name="Designer",
    model=OpenAIResponses(id="gpt-5.2"),
    role="评估用户体验影响和可用性",
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
broadcast_team = Team(
    name="Broadcast Review Team",
    members=[product_manager, engineer, designer],
    model=OpenAIResponses(id="gpt-5.2"),
    mode=TeamMode.broadcast,
    instructions=[
        "每个成员必须独立评估相同的请求。",
        "从你的专业角度提供简洁的建议。",
        "清楚地突出权衡和开放风险。",
    ],
    markdown=True,
    show_members_responses=True,
)

# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    broadcast_team.print_response(
        "Should we ship a beta autopilot feature next month? Provide your recommendation and risks.",
        stream=True,
    )

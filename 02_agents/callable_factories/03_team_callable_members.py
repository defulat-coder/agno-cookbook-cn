"""
Team 可调用成员
=====================
将函数作为 `members` 传递给 Team。团队组成
根据 session_state 在运行时决定。
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team import Team

# ---------------------------------------------------------------------------
# 创建团队成员
# ---------------------------------------------------------------------------

writer = Agent(
    name="Writer",
    role="Content writer",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=["编写清晰、简洁的内容。"],
)

researcher = Agent(
    name="Researcher",
    role="Research analyst",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=["研究主题并总结发现。"],
)


def pick_members(session_state: dict):
    """仅在需要时包含 researcher。"""
    needs_research = session_state.get("needs_research", False)
    print(f"--> needs_research={needs_research}")

    if needs_research:
        return [researcher, writer]
    return [writer]


# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------

team = Team(
    name="Content Team",
    model=OpenAIChat(id="gpt-4o-mini"),
    members=pick_members,
    cache_callables=False,
    instructions=["协调团队完成任务。"],
)


# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Writer only ===")
    team.print_response(
        "Write a haiku about Python",
        session_state={"needs_research": False},
        stream=True,
    )

    print("\n=== Researcher + Writer ===")
    team.print_response(
        "Research the history of Python and write a short summary",
        session_state={"needs_research": True},
        stream=True,
    )

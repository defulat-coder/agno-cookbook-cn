"""
团队学习：Session 规划
================================
团队可以在启用规划模式的情况下使用 SessionContext 跟踪 session 目标和进度。

规划模式捕获：
- 当前目标和子任务
- 具有完成状态的计划步骤
- 跨轮次的进度标记

这对于处理多步骤任务的团队很有用，如
部署管道、项目规划或入职流程。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.learn import (
    LearningMachine,
    LearningMode,
    SessionContextConfig,
    UserProfileConfig,
)
from agno.models.openai import OpenAIChat
from agno.team import Team

db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

devops_engineer = Agent(
    name="DevOps Engineer",
    model=OpenAIChat(id="gpt-4o"),
    role="Handle infrastructure, CI/CD, and deployment tasks.",
)

security_reviewer = Agent(
    name="Security Reviewer",
    model=OpenAIChat(id="gpt-4o"),
    role="Review security considerations and compliance requirements.",
)

team = Team(
    name="Release Team",
    model=OpenAIChat(id="gpt-4o"),
    members=[devops_engineer, security_reviewer],
    db=db,
    learning=LearningMachine(
        user_profile=UserProfileConfig(
            mode=LearningMode.ALWAYS,
        ),
        session_context=SessionContextConfig(
            enable_planning=True,
        ),
    ),
    markdown=True,
    show_members_responses=True,
)

if __name__ == "__main__":
    user_id = "diana@example.com"
    session_id = "release_v2"

    # Turn 1: Define the release goal
    print("\n" + "=" * 60)
    print("TURN 1: Define release goal")
    print("=" * 60 + "\n")

    team.print_response(
        "I'm Diana, release manager. We need to deploy v2.0 to production. "
        "Give me a 3-step release checklist covering infra, security, and rollout.",
        user_id=user_id,
        session_id=session_id,
        stream=True,
    )

    lm = team.learning_machine
    print("\n--- Session Context ---")
    lm.session_context_store.print(session_id=session_id)

    # Turn 2: Complete first step
    print("\n" + "=" * 60)
    print("TURN 2: Infrastructure ready")
    print("=" * 60 + "\n")

    team.print_response(
        "Infrastructure is ready - staging tests passed. "
        "What security checks should we run before proceeding?",
        user_id=user_id,
        session_id=session_id,
        stream=True,
    )

    print("\n--- Updated Session Context ---")
    lm.session_context_store.print(session_id=session_id)

    # Turn 3: Final step
    print("\n" + "=" * 60)
    print("TURN 3: Security cleared, ready for rollout")
    print("=" * 60 + "\n")

    team.print_response(
        "Security review passed. What's the recommended rollout strategy?",
        user_id=user_id,
        session_id=session_id,
        stream=True,
    )

    print("\n--- Final Session Context ---")
    lm.session_context_store.print(session_id=session_id)

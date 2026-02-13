"""
运行时更改 State
===================

演示针对不同用户/session 的每次运行 session state 覆盖。
"""

from agno.db.in_memory import InMemoryDb
from agno.models.openai import OpenAIChat
from agno.team import Team

# ---------------------------------------------------------------------------
# Create Team
# ---------------------------------------------------------------------------
team = Team(
    db=InMemoryDb(),
    model=OpenAIChat(id="gpt-5.2"),
    members=[],
    instructions="Users name is {user_name} and age is {age}",
)

# ---------------------------------------------------------------------------
# Run Team
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    team.print_response(
        "What is my name?",
        session_id="user_1_session_1",
        user_id="user_1",
        session_state={"user_name": "John", "age": 30},
    )

    team.print_response(
        "How old am I?",
        session_id="user_1_session_1",
        user_id="user_1",
    )

    team.print_response(
        "What is my name?",
        session_id="user_2_session_1",
        user_id="user_2",
        session_state={"user_name": "Jane", "age": 25},
    )

    team.print_response(
        "How old am I?",
        session_id="user_2_session_1",
        user_id="user_2",
    )

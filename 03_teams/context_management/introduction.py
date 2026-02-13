"""
团队介绍
=============================

演示为 session 设置可重用的团队介绍消息。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.team import Team

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
db = SqliteDb(db_file="tmp/teams.db", session_table="team_sessions")
INTRODUCTION = (
    "你好，我是你的个人助手。我只能帮助你解决与"
    "登山相关的问题。"
)

# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(),
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
team = Team(
    model=OpenAIChat(),
    db=db,
    members=[agent],
    introduction=INTRODUCTION,
    session_id="introduction_session_mountain_climbing",
    add_history_to_context=True,
)

# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    team.print_response("Easiest 14er in USA?")
    team.print_response("Is K2 harder to climb than Everest?")

"""
02 基础团队追踪
=====================

演示 02 基础团队追踪。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.team import Team
from agno.tools.hackernews import HackerNewsTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# 设置数据库
db = SqliteDb(db_file="tmp/traces.db")

# 创建 agent - 无需在每个上设置追踪！
agent = Agent(
    name="HackerNews Agent",
    model=OpenAIChat(id="gpt-5.2"),
    tools=[HackerNewsTools()],
    instructions="你是一个 hacker news agent。简洁地回答问题。",
    markdown=True,
)

team = Team(
    name="HackerNews Team",
    model=OpenAIChat(id="gpt-5.2"),
    members=[agent],
    instructions="你是一个 hacker news 团队。使用 HackerNews Agent 成员简洁地回答问题",
    db=db,
)

# 使用 tracing=True 设置 AgentOS
# 这会自动为所有 agent 和团队启用追踪！
agent_os = AgentOS(
    description="用于追踪 HackerNews 的示例应用",
    teams=[team],
    tracing=True,
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="02_basic_team_tracing:app", reload=True)

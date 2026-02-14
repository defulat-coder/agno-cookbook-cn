"""
支持团队
============

演示支持团队。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.os.app import AgentOS
from agno.os.interfaces.slack import Slack
from agno.team import Team
from agno.tools.slack import SlackTools
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

team_db = SqliteDb(session_table="team_sessions", db_file="tmp/support_team.db")

# 技术支持 Agent
tech_support = Agent(
    name="Technical Support",
    role="代码和技术故障排除",
    model=OpenAIChat(id="gpt-4o"),
    tools=[WebSearchTools()],
    instructions=[
        "你处理有关代码、API 和实现的技术问题。",
        "在有帮助时提供代码示例。",
        "搜索当前文档和最佳实践。",
    ],
    markdown=True,
)

# 文档 Agent
docs_agent = Agent(
    name="Documentation Specialist",
    role="查找和解释文档",
    model=OpenAIChat(id="gpt-4o"),
    tools=[
        SlackTools(
            enable_search_messages=True,
            enable_get_thread=True,
        ),
        WebSearchTools(),
    ],
    instructions=[
        "你查找相关文档和过去的讨论。",
        "在 Slack 中搜索类似问题的先前答案。",
        "在网络上搜索官方文档。",
        "用简单的术语解释文档。",
    ],
    markdown=True,
)

# 带有协调员的团队
support_team = Team(
    name="Support Team",
    model=OpenAIChat(id="gpt-4o"),
    members=[tech_support, docs_agent],
    description="一个将问题路由到正确专家的支持团队。",
    instructions=[
        "你协调支持请求。",
        "将技术/代码问题路由到技术支持。",
        "将'如何做'或'在哪里'问题路由到文档专家。",
        "对于复杂问题，咨询两个 agent。",
    ],
    db=team_db,
    add_history_to_context=True,
    num_history_runs=3,
    markdown=True,
)

agent_os = AgentOS(
    teams=[support_team],
    interfaces=[
        Slack(
            team=support_team,
            reply_to_mentions_only=True,
        )
    ],
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="support_team:app", reload=True)

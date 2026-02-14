"""
示例：AgentOS 中团队的后台钩子

此示例演示如何在团队中使用后台钩子。
后台钩子在 API 响应发送后执行，使其非阻塞。
"""

import asyncio

from agno.agent import Agent
from agno.db.sqlite import AsyncSqliteDb
from agno.hooks.decorator import hook
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.run.team import TeamRunOutput
from agno.team import Team

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------


@hook(run_in_background=True)
async def log_team_result(run_output: TeamRunOutput, team: Team) -> None:
    """
    记录团队执行结果的后台 post-hook。
    在响应发送给用户后运行。
    """
    print(f"[Background Hook] Team '{team.name}' completed run: {run_output.run_id}")
    print(f"[Background Hook] Content length: {len(str(run_output.content))} chars")

    # 模拟异步工作（例如，存储指标）
    await asyncio.sleep(2)
    print("[Background Hook] Team metrics logged successfully!")


# 创建团队成员
researcher = Agent(
    name="Researcher",
    model=OpenAIChat(id="gpt-5.2"),
    instructions="你研究主题并提供事实信息。",
)

writer = Agent(
    name="Writer",
    model=OpenAIChat(id="gpt-5.2"),
    instructions="你根据研究撰写清晰、引人入胜的内容。",
)

# 创建带有后台钩子的团队
content_team = Team(
    id="content-team",
    name="ContentTeam",
    model=OpenAIChat(id="gpt-5.2"),
    members=[researcher, writer],
    instructions="协调研究员和作者之间的工作以创建内容。",
    db=AsyncSqliteDb(db_file="tmp/team.db"),
    post_hooks=[log_team_result],
    markdown=True,
)

# 创建启用后台钩子的 AgentOS
agent_os = AgentOS(
    teams=[content_team],
    run_hooks_in_background=True,
)

app = agent_os.get_app()

# 示例请求：
# curl -X POST http://localhost:7777/teams/content-team/runs \
#   -F "message=Write a short paragraph about Python" \
#   -F "stream=false"

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="background_hooks_team:app", port=7777, reload=True)

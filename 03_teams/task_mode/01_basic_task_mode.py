"""
基础任务模式示例

演示 `mode=tasks` 模式下的团队，团队领导者自主地：
1. 将用户目标分解为离散任务
2. 将任务分配给最合适的成员 agent
3. 通过委托给成员来执行任务
4. 收集结果并提供最终摘要

运行: .venvs/demo/bin/python cookbook/03_teams/task_mode/01_basic_task_mode.py
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team.mode import TeamMode
from agno.team.team import Team

# -- 成员 agent -----------------------------------------------------------

researcher = Agent(
    name="Researcher",
    role="研究专家，寻找主题相关信息",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=[
        "你是一名研究专家。",
        "当给定一个主题时，提供清晰简洁的关键事实摘要。",
        "始终引用你所知道的内容，并对局限性保持诚实。",
    ],
)

writer = Agent(
    name="Writer",
    role="内容作者，创建结构良好的文本",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=[
        "你是一名熟练的内容作者。",
        "获取提供的信息并将其制作成精美、引人入胜的文本。",
        "在适当的时候使用清晰的结构，包括标题和要点。",
    ],
)

critic = Agent(
    name="Critic",
    role="质量审核者，提供建设性反馈",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=[
        "你是一名建设性的评论家。",
        "审查内容的准确性、清晰度和完整性。",
        "提供具体、可操作的反馈。",
    ],
)

# -- 任务模式团队 ----------------------------------------------------------

content_team = Team(
    name="Content Creation Team",
    mode=TeamMode.tasks,
    model=OpenAIChat(id="gpt-4o"),
    members=[researcher, writer, critic],
    instructions=[
        "你是一个内容创建团队领导者。",
        "将用户的请求分解为研究、写作和审查任务。",
        "将每个任务分配给最合适的团队成员。",
        "在所有任务完成后，将结果综合为最终响应。",
    ],
    show_members_responses=True,
    markdown=True,
    max_iterations=10,
    debug_mode=True,
)

# -- 运行 ---------------------------------------------------------------------

if __name__ == "__main__":
    content_team.print_response(
        "Write a short briefing on the current state of quantum computing, "
        "covering recent breakthroughs, key challenges, and potential near-term applications."
    )

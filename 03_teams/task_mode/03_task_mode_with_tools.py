"""
带工具的任务模式 Agent

演示成员 agent 拥有实际工具的任务模式。团队领导者
创建任务并将它们委托给使用网络搜索收集
信息的 agent。

运行: .venvs/demo/bin/python cookbook/03_teams/task_mode/03_task_mode_with_tools.py
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team.mode import TeamMode
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools

# -- 配备工具的 agent -----------------------------------------------------

web_researcher = Agent(
    name="Web Researcher",
    role="在网络上搜索当前信息",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[DuckDuckGoTools()],
    instructions=[
        "你是一名网络研究员。",
        "使用 DuckDuckGo 搜索当前相关信息。",
        "清楚地总结发现，包括关键事实和来源。",
    ],
)

summarizer = Agent(
    name="Summarizer",
    role="将信息综合为清晰的摘要",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=[
        "你是一名专业的摘要专家。",
        "获取详细信息并将其提炼为清晰、结构化的摘要。",
        "突出最重要的要点。",
    ],
)

# -- 任务模式团队 -----------------------------------------------------------

research_team = Team(
    name="Research Team",
    mode=TeamMode.tasks,
    model=OpenAIChat(id="gpt-4o"),
    members=[web_researcher, summarizer],
    instructions=[
        "你是一个研究团队领导者。",
        "对于研究请求：",
        "1. 为网络研究员创建搜索任务以收集信息。",
        "2. 研究完成后，为摘要专家创建一个任务来汇编发现。",
        "3. 设置适当的依赖关系 -- 摘要依赖于研究完成。",
    ],
    show_members_responses=True,
    markdown=True,
    max_iterations=10,
)

# -- 运行 ---------------------------------------------------------------------

if __name__ == "__main__":
    research_team.print_response(
        "What are the latest developments in large language models in 2025? "
        "Find recent news and provide a structured summary."
    )

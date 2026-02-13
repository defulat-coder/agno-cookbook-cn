"""
并行任务执行示例

演示任务模式中的 `execute_tasks_parallel` 工具。团队领导者
创建多个独立任务并并发执行它们，然后
综合结果。

运行: .venvs/demo/bin/python cookbook/03_teams/task_mode/02_parallel_tasks.py
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team.mode import TeamMode
from agno.team.team import Team

# -- 专业分析师 agent -----------------------------------------------

market_analyst = Agent(
    name="Market Analyst",
    role="分析市场趋势和竞争格局",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=[
        "你是一名市场分析师。",
        "提供市场趋势、主要参与者和前景的简洁分析。",
    ],
)

tech_analyst = Agent(
    name="Tech Analyst",
    role="评估技术可行性和创新",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=[
        "你是一名技术分析师。",
        "评估技术方面、创新潜力和可行性。",
    ],
)

financial_analyst = Agent(
    name="Financial Analyst",
    role="评估财务可行性和投资潜力",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=[
        "你是一名财务分析师。",
        "评估财务可行性、收入潜力和投资前景。",
    ],
)

# -- 任务模式团队，强调并行性 ------------------------------------

analysis_team = Team(
    name="Industry Analysis Team",
    mode=TeamMode.tasks,
    model=OpenAIChat(id="gpt-4o"),
    members=[market_analyst, tech_analyst, financial_analyst],
    instructions=[
        "你是一个行业分析团队领导者。",
        "当给定一个要分析的主题时：",
        "1. 为市场分析、技术分析和财务分析创建单独的任务。",
        "2. 这些任务是独立的 -- 使用 `execute_tasks_parallel` 并发运行它们。",
        "3. 在所有并行任务完成后，将发现综合为统一报告。",
        "只要任务之间不相互依赖，就优先使用并行执行。",
    ],
    show_members_responses=True,
    markdown=True,
    max_iterations=10,
)

# -- 运行 ---------------------------------------------------------------------

if __name__ == "__main__":
    analysis_team.print_response(
        "Analyze the electric vehicle industry for a potential investor. "
        "Cover market dynamics, technological innovations, and financial outlook."
    )

"""
新闻搜索团队可靠性评估
===========================================

演示对团队工作流的工具调用可靠性检查。
"""

from typing import Optional

from agno.agent import Agent
from agno.eval.reliability import ReliabilityEval, ReliabilityResult
from agno.models.openai import OpenAIChat
from agno.run.team import TeamRunOutput
from agno.team.team import Team
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
team_member = Agent(
    name="News Searcher",
    model=OpenAIChat("gpt-4o"),
    role="Searches the web for the latest news.",
    tools=[WebSearchTools(enable_news=True)],
)
team = Team(
    name="News Research Team",
    model=OpenAIChat("gpt-4o"),
    members=[team_member],
    markdown=True,
    show_members_responses=True,
)
expected_tool_calls = [
    "delegate_task_to_member",
    "search_news",
]


# ---------------------------------------------------------------------------
# 创建评估函数
# ---------------------------------------------------------------------------
def evaluate_team_reliability():
    response: TeamRunOutput = team.run("What is the latest news on AI?")
    evaluation = ReliabilityEval(
        name="Team Reliability Evaluation",
        team_response=response,
        expected_tool_calls=expected_tool_calls,
    )
    result: Optional[ReliabilityResult] = evaluation.run(print_results=True)
    if result:
        result.assert_passed()


# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    evaluate_team_reliability()

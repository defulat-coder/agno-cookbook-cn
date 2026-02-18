"""
团队实例化性能评估
=========================================

演示如何测量团队实例化性能。
"""

from agno.agent import Agent
from agno.eval.performance import PerformanceEval
from agno.models.openai import OpenAIChat
from agno.team.team import Team

# ---------------------------------------------------------------------------
# 创建团队成员
# ---------------------------------------------------------------------------
team_member = Agent(model=OpenAIChat(id="gpt-4o"))


# ---------------------------------------------------------------------------
# 创建基准测试函数
# ---------------------------------------------------------------------------
def instantiate_team():
    return Team(members=[team_member])


# ---------------------------------------------------------------------------
# 创建评估
# ---------------------------------------------------------------------------
instantiation_perf = PerformanceEval(
    name="Instantiation Performance Team", func=instantiate_team, num_iterations=1000
)

# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    instantiation_perf.run(print_results=True, print_summary=True)

"""
团队 Agent 评估器评估
==============================

演示对团队输出进行响应质量评估。
"""

from typing import Optional

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.eval.agent_as_judge import AgentAsJudgeEval, AgentAsJudgeResult
from agno.models.openai import OpenAIChat
from agno.team.team import Team

# ---------------------------------------------------------------------------
# 创建数据库
# ---------------------------------------------------------------------------
db = SqliteDb(db_file="tmp/agent_as_judge_team.db")

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
researcher = Agent(
    name="Researcher",
    role="Research and gather information",
    model=OpenAIChat(id="gpt-4o"),
)
writer = Agent(
    name="Writer",
    role="Write clear and concise summaries",
    model=OpenAIChat(id="gpt-4o"),
)
research_team = Team(
    name="Research Team",
    model=OpenAIChat("gpt-4o"),
    members=[researcher, writer],
    instructions=["First research the topic thoroughly, then write a clear summary."],
    db=db,
)

# ---------------------------------------------------------------------------
# 创建评估
# ---------------------------------------------------------------------------
evaluation = AgentAsJudgeEval(
    name="Team Response Quality",
    model=OpenAIChat(id="gpt-5.2"),
    criteria="Response should be well-researched, clear, and comprehensive with good flow",
    scoring_strategy="binary",
    db=db,
)

# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    response = research_team.run("Explain quantum computing")
    result: Optional[AgentAsJudgeResult] = evaluation.run(
        input="Explain quantum computing",
        output=str(response.content),
        print_results=True,
        print_summary=True,
    )
    assert result is not None, "评估应返回结果"

    print("数据库结果:")
    eval_runs = db.get_eval_runs()
    print(f"已存储评估总数: {len(eval_runs)}")
    if eval_runs:
        latest = eval_runs[-1]
        print(f"评估 ID: {latest.run_id}")
        print(f"团队: {research_team.name}")

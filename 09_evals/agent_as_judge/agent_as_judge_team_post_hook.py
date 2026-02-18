"""
团队 Post-Hook Agent 评估器评估
========================================

演示在团队响应上运行 post-hook 评判器。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.eval.agent_as_judge import AgentAsJudgeEval
from agno.models.openai import OpenAIChat
from agno.team.team import Team

# ---------------------------------------------------------------------------
# 创建数据库
# ---------------------------------------------------------------------------
db = SqliteDb(db_file="tmp/agent_as_judge_team_post_hook.db")

# ---------------------------------------------------------------------------
# 创建团队与评估 Hook
# ---------------------------------------------------------------------------
agent_as_judge_eval = AgentAsJudgeEval(
    name="Team Response Quality",
    model=OpenAIChat(id="gpt-5.2"),
    criteria="Response should be well-researched, clear, comprehensive, and show good collaboration between team members",
    scoring_strategy="numeric",
    threshold=7,
    db=db,
)
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
    post_hooks=[agent_as_judge_eval],
    db=db,
)

# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    response = research_team.run("Explain quantum computing")
    print(response.content)

    print("评估结果:")
    eval_runs = db.get_eval_runs()
    if eval_runs:
        latest = eval_runs[-1]
        if latest.eval_data and "results" in latest.eval_data:
            result = latest.eval_data["results"][0]
            print(f"得分: {result.get('score', 'N/A')}/10")
            print(f"状态: {'通过' if result.get('passed') else '失败'}")
            print(f"原因: {result.get('reason', 'N/A')[:200]}...")

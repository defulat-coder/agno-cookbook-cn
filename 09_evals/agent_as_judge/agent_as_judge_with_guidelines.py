"""
基于指南的 Agent 评估器评估
=========================================

演示带有附加指南的 Agent 评估器评分。
"""

from typing import Optional

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.eval.agent_as_judge import AgentAsJudgeEval, AgentAsJudgeResult
from agno.models.openai import OpenAIChat

# ---------------------------------------------------------------------------
# 创建数据库
# ---------------------------------------------------------------------------
db = SqliteDb(db_file="tmp/agent_as_judge_guidelines.db")

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    instructions="You are a Tesla Model 3 product specialist. Provide detailed and helpful specifications.",
    db=db,
)

# ---------------------------------------------------------------------------
# 创建评估
# ---------------------------------------------------------------------------
evaluation = AgentAsJudgeEval(
    name="Product Info Quality",
    model=OpenAIChat(id="gpt-5.2"),
    criteria="Response should be informative, well-formatted, and accurate for product specifications",
    scoring_strategy="numeric",
    threshold=8,
    additional_guidelines=[
        "Must include specific numbers with proper units (mph, km/h, etc.)",
        "Should provide context for different model variants if applicable",
        "Information should be technically accurate and complete",
    ],
    db=db,
)

# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    response = agent.run("What is the maximum speed of the Tesla Model 3?")
    result: Optional[AgentAsJudgeResult] = evaluation.run(
        input="What is the maximum speed?",
        output=str(response.content),
        print_results=True,
    )
    assert result is not None, "评估应返回结果"

    print("数据库结果:")
    eval_runs = db.get_eval_runs()
    print(f"已存储评估总数: {len(eval_runs)}")
    if eval_runs:
        latest = eval_runs[-1]
        print(f"评估 ID: {latest.run_id}")
        print(f"使用的附加指南数: {len(evaluation.additional_guidelines)}")

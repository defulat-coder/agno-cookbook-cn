"""
二元 Agent 评估器评估
================================

演示基于通过/失败的响应质量评估。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.eval.agent_as_judge import AgentAsJudgeEval
from agno.models.openai import OpenAIChat

# ---------------------------------------------------------------------------
# 创建数据库
# ---------------------------------------------------------------------------
db = SqliteDb(db_file="tmp/agent_as_judge_binary.db")

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    instructions="You are a customer service agent. Respond professionally.",
    db=db,
)

# ---------------------------------------------------------------------------
# 创建评估
# ---------------------------------------------------------------------------
evaluation = AgentAsJudgeEval(
    name="Professional Tone Check",
    criteria="Response must maintain professional tone without informal language or slang",
    db=db,
)

# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    response = agent.run("I need help with my account")
    result = evaluation.run(
        input="I need help with my account",
        output=str(response.content),
        print_results=True,
        print_summary=True,
    )
    print(f"结果: {'通过' if result.results[0].passed else '失败'}")

"""
批量 Agent 评估器评估
===============================

演示在一次运行中评估多个案例。
"""

from agno.db.sqlite import SqliteDb
from agno.eval.agent_as_judge import AgentAsJudgeEval

# ---------------------------------------------------------------------------
# 创建数据库
# ---------------------------------------------------------------------------
db = SqliteDb(db_file="tmp/agent_as_judge_batch.db")

# ---------------------------------------------------------------------------
# 创建评估
# ---------------------------------------------------------------------------
evaluation = AgentAsJudgeEval(
    name="Customer Service Quality",
    criteria="Response should be empathetic, professional, and helpful",
    scoring_strategy="binary",
    db=db,
)

# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    result = evaluation.run(
        cases=[
            {
                "input": "My order is delayed and I'm very upset!",
                "output": "I sincerely apologize for the delay. I understand how frustrating this must be. Let me check your order status right away and see how we can make this right for you.",
            },
            {
                "input": "Can you help me with a refund?",
                "output": "Of course! I'd be happy to help with your refund. Could you please provide your order number so I can process this quickly for you?",
            },
            {
                "input": "Your product is terrible!",
                "output": "I'm sorry to hear you're disappointed. Your feedback is valuable to us. Could you share more details about what went wrong so we can improve?",
            },
        ],
        print_results=True,
        print_summary=True,
    )

    print(f"通过率: {result.pass_rate:.1f}%")
    print(f"通过数: {sum(1 for r in result.results if r.passed)}/{len(result.results)}")

    print("数据库结果:")
    eval_runs = db.get_eval_runs()
    print(f"已存储评估总数: {len(eval_runs)}")
    if eval_runs:
        latest = eval_runs[-1]
        print(f"评估 ID: {latest.run_id}")
        print(f"已评估案例数: {len(result.results)}")

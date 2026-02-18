"""
基础 Agent 评估器评估
===============================

演示同步与异步的 Agent 评估器评估。
"""

import asyncio

from agno.agent import Agent
from agno.db.postgres.postgres import PostgresDb
from agno.db.sqlite import AsyncSqliteDb
from agno.eval.agent_as_judge import AgentAsJudgeEval, AgentAsJudgeEvaluation
from agno.models.openai import OpenAIChat


def on_evaluation_failure(evaluation: AgentAsJudgeEvaluation):
    """评估分数低于阈值时触发的回调函数。"""
    print(f"评估失败 - 得分: {evaluation.score}/10")
    print(f"原因: {evaluation.reason[:100]}...")


# ---------------------------------------------------------------------------
# 创建同步资源
# ---------------------------------------------------------------------------
sync_db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
sync_db = PostgresDb(db_url=sync_db_url)

sync_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    instructions="You are a technical writer. Explain concepts clearly and concisely.",
    db=sync_db,
)

sync_evaluation = AgentAsJudgeEval(
    name="Explanation Quality",
    criteria="Explanation should be clear, beginner-friendly, and use simple language",
    scoring_strategy="numeric",
    threshold=7,
    on_fail=on_evaluation_failure,
    db=sync_db,
)

# ---------------------------------------------------------------------------
# 创建异步资源
# ---------------------------------------------------------------------------
async_db = AsyncSqliteDb(db_file="tmp/agent_as_judge_async.db")

async_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    instructions="Provide helpful and informative answers.",
    db=async_db,
)

async_evaluation = AgentAsJudgeEval(
    name="ML Explanation Quality",
    model=OpenAIChat(id="gpt-5.2"),
    criteria="Explanation should be clear, beginner-friendly, and avoid jargon",
    scoring_strategy="numeric",
    threshold=10,
    on_fail=on_evaluation_failure,
    db=async_db,
)


async def run_async_evaluation():
    async_response = await async_agent.arun("Explain machine learning in simple terms")
    async_result = await async_evaluation.arun(
        input="Explain machine learning in simple terms",
        output=str(async_response.content),
        print_results=True,
        print_summary=True,
    )
    assert async_result is not None, "评估应返回结果"

    print("异步数据库结果:")
    async_eval_runs = await async_db.get_eval_runs()
    print(f"已存储评估总数: {len(async_eval_runs)}")
    if async_eval_runs:
        latest = async_eval_runs[-1]
        print(f"评估 ID: {latest.run_id}")
        print(f"名称: {latest.name}")


# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sync_response = sync_agent.run("Explain what an API is")
    sync_evaluation.run(
        input="Explain what an API is",
        output=str(sync_response.content),
        print_results=True,
        print_summary=True,
    )

    print("数据库结果:")
    sync_eval_runs = sync_db.get_eval_runs()
    print(f"已存储评估总数: {len(sync_eval_runs)}")
    if sync_eval_runs:
        latest = sync_eval_runs[-1]
        print(f"评估 ID: {latest.run_id}")
        print(f"名称: {latest.name}")

    asyncio.run(run_async_evaluation())

"""
Post-Hook Agent 评估器评估
===================================

演示同步与异步 post-hook 评判。
"""

import asyncio

from agno.agent import Agent
from agno.db.sqlite import AsyncSqliteDb, SqliteDb
from agno.eval.agent_as_judge import AgentAsJudgeEval
from agno.models.openai import OpenAIChat

# ---------------------------------------------------------------------------
# 创建同步资源
# ---------------------------------------------------------------------------
sync_db = SqliteDb(db_file="tmp/agent_as_judge_post_hook.db")

sync_agent_as_judge_eval = AgentAsJudgeEval(
    name="Response Quality Check",
    model=OpenAIChat(id="gpt-5.2"),
    criteria="Response should be professional, well-structured, and provide balanced perspectives",
    scoring_strategy="numeric",
    threshold=7,
    db=sync_db,
)

sync_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    instructions="Provide professional and well-reasoned answers.",
    post_hooks=[sync_agent_as_judge_eval],
    db=sync_db,
)

# ---------------------------------------------------------------------------
# 创建异步资源
# ---------------------------------------------------------------------------
async_db = AsyncSqliteDb(db_file="tmp/agent_as_judge_post_hook_async.db")

async_agent_as_judge_eval = AgentAsJudgeEval(
    name="Response Quality Check",
    model=OpenAIChat(id="gpt-5.2"),
    criteria="Response should be professional, well-balanced, and provide evidence-based perspectives",
    scoring_strategy="numeric",
    threshold=7,
    db=async_db,
)

async_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    instructions="Provide professional and well-reasoned answers.",
    post_hooks=[async_agent_as_judge_eval],
    db=async_db,
)


def print_latest_result(eval_runs):
    if eval_runs:
        latest = eval_runs[-1]
        if latest.eval_data and "results" in latest.eval_data:
            result = latest.eval_data["results"][0]
            print(f"得分: {result.get('score', 'N/A')}/10")
            print(f"状态: {'通过' if result.get('passed') else '失败'}")
            print(f"原因: {result.get('reason', 'N/A')[:200]}...")


async def run_async_evaluation():
    async_response = await async_agent.arun(
        "What are the benefits of renewable energy?"
    )
    print(async_response.content)

    print("异步评估结果:")
    async_eval_runs = await async_db.get_eval_runs()
    print_latest_result(async_eval_runs)


# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sync_response = sync_agent.run("What are the benefits of renewable energy?")
    print(sync_response.content)

    print("评估结果:")
    sync_eval_runs = sync_db.get_eval_runs()
    print_latest_result(sync_eval_runs)

    asyncio.run(run_async_evaluation())

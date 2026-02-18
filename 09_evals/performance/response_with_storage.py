"""
基于存储的响应性能评估
==============================================

演示启用存储历史记录时的性能测量。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.eval.performance import PerformanceEval
from agno.models.openai import OpenAIChat

# ---------------------------------------------------------------------------
# 创建数据库
# ---------------------------------------------------------------------------
db = SqliteDb(db_file="tmp/storage.db")


# ---------------------------------------------------------------------------
# 创建基准测试函数
# ---------------------------------------------------------------------------
def run_agent():
    agent = Agent(
        model=OpenAIChat(id="gpt-5.2"),
        system_message="Be concise, reply with one sentence.",
        db=db,
        add_history_to_context=True,
    )
    response_1 = agent.run("What is the capital of France?")
    print(response_1.content)

    response_2 = agent.run("How many people live there?")
    print(response_2.content)

    return response_2.content


# ---------------------------------------------------------------------------
# 创建评估
# ---------------------------------------------------------------------------
response_with_storage_perf = PerformanceEval(
    name="Storage Performance",
    func=run_agent,
    num_iterations=1,
    warmup_runs=0,
)

# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    response_with_storage_perf.run(print_results=True, print_summary=True)

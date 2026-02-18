"""
记忆更新性能评估
====================================

演示启用记忆更新时的性能测量。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.eval.performance import PerformanceEval
from agno.models.openai import OpenAIChat

# ---------------------------------------------------------------------------
# 创建数据库
# ---------------------------------------------------------------------------
db = SqliteDb(db_file="tmp/memory.db")


# ---------------------------------------------------------------------------
# 创建基准测试函数
# ---------------------------------------------------------------------------
def run_agent():
    agent = Agent(
        model=OpenAIChat(id="gpt-5.2"),
        system_message="Be concise, reply with one sentence.",
        db=db,
        update_memory_on_run=True,
    )

    response = agent.run("My name is Tom! I'm 25 years old and I live in New York.")
    print(f"Agent 响应: {response.content}")

    return response


# ---------------------------------------------------------------------------
# 创建评估
# ---------------------------------------------------------------------------
response_with_memory_updates_perf = PerformanceEval(
    name="Memory Updates Performance",
    func=run_agent,
    num_iterations=5,
    warmup_runs=0,
)

# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    response_with_memory_updates_perf.run(print_results=True, print_summary=True)

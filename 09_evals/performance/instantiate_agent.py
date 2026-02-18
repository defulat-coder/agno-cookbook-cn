"""
Agent 实例化性能评估
==========================================

演示如何测量 Agent 实例化性能。
"""

from agno.agent import Agent
from agno.eval.performance import PerformanceEval


# ---------------------------------------------------------------------------
# 创建基准测试函数
# ---------------------------------------------------------------------------
def instantiate_agent():
    return Agent(system_message="Be concise, reply with one sentence.")


# ---------------------------------------------------------------------------
# 创建评估
# ---------------------------------------------------------------------------
instantiation_perf = PerformanceEval(
    name="Instantiation Performance", func=instantiate_agent, num_iterations=1000
)

# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    instantiation_perf.run(print_results=True, print_summary=True)

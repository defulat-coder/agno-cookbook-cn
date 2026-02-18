"""
异步函数性能评估
=====================================

演示如何对异步函数进行性能评估。
"""

import asyncio

from agno.agent import Agent
from agno.eval.performance import PerformanceEval
from agno.models.openai import OpenAIChat


# ---------------------------------------------------------------------------
# 创建基准测试函数
# ---------------------------------------------------------------------------
async def arun_agent():
    agent = Agent(
        model=OpenAIChat(id="gpt-5.2"),
        system_message="Be concise, reply with one sentence.",
    )
    response = await agent.arun("What is the capital of France?")
    return response


# ---------------------------------------------------------------------------
# 创建评估
# ---------------------------------------------------------------------------
performance_eval = PerformanceEval(func=arun_agent, num_iterations=10)

# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(performance_eval.arun(print_summary=True, print_results=True))

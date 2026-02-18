"""
异步可靠性评估
==================================

演示如何以异步方式运行可靠性检查评估。
"""

import asyncio
from typing import Optional

from agno.agent import Agent
from agno.eval.reliability import ReliabilityEval, ReliabilityResult
from agno.models.openai import OpenAIChat
from agno.run.agent import RunOutput
from agno.tools.calculator import CalculatorTools


# ---------------------------------------------------------------------------
# 创建评估函数
# ---------------------------------------------------------------------------
def factorial():
    agent = Agent(
        model=OpenAIChat(id="gpt-5.2"),
        tools=[CalculatorTools()],
    )
    response: RunOutput = agent.run("What is 10!?")
    evaluation = ReliabilityEval(
        agent_response=response,
        expected_tool_calls=["factorial"],
    )

    # 调用 arun 方法以异步方式运行评估
    result: Optional[ReliabilityResult] = asyncio.run(
        evaluation.arun(print_results=True)
    )
    if result:
        result.assert_passed()


# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    factorial()

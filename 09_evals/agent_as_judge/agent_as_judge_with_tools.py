"""
使用工具的 Agent 评估器评估
====================================

演示对使用工具的 Agent 生成的响应进行评判。
"""

from typing import Optional

from agno.agent import Agent
from agno.eval.agent_as_judge import AgentAsJudgeEval, AgentAsJudgeResult
from agno.models.openai import OpenAIChat
from agno.tools.calculator import CalculatorTools

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[CalculatorTools()],
    instructions="Use the calculator tools to solve math problems. Explain your reasoning and show calculation steps clearly.",
)

# ---------------------------------------------------------------------------
# 创建评估
# ---------------------------------------------------------------------------
evaluation = AgentAsJudgeEval(
    name="Calculator Tool Usage Quality",
    model=OpenAIChat(id="gpt-5.2"),
    criteria="Response should clearly explain the calculation process, show intermediate steps, and present the final answer in a user-friendly way",
    scoring_strategy="numeric",
    threshold=7,
)

# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    response = agent.run("What is 15 * 23 + 47?")
    result: Optional[AgentAsJudgeResult] = evaluation.run(
        input="What is 15 * 23 + 47?",
        output=str(response.content),
        print_results=True,
    )
    assert result is not None, "评估应返回结果"

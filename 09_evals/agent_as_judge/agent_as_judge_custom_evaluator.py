"""
自定义评估器 Agent 评估
==========================================

演示如何使用自定义评估器 Agent 进行评判。
"""

from agno.agent import Agent
from agno.eval.agent_as_judge import AgentAsJudgeEval
from agno.models.openai import OpenAIChat

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    instructions="Explain technical concepts simply.",
)

# ---------------------------------------------------------------------------
# 创建评估器 Agent
# ---------------------------------------------------------------------------
custom_evaluator = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description="Strict technical evaluator",
    instructions="You are a strict evaluator. Only give high scores to exceptionally clear and accurate explanations.",
)

# ---------------------------------------------------------------------------
# 创建评估
# ---------------------------------------------------------------------------
evaluation = AgentAsJudgeEval(
    name="Technical Accuracy",
    criteria="Explanation must be technically accurate and comprehensive",
    scoring_strategy="numeric",
    threshold=8,
    evaluator_agent=custom_evaluator,
)

# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    response = agent.run("What is machine learning?")
    result = evaluation.run(
        input="What is machine learning?",
        output=str(response.content),
        print_results=True,
    )
    print(f"得分: {result.results[0].score}/10")
    print(f"是否通过: {result.results[0].passed}")

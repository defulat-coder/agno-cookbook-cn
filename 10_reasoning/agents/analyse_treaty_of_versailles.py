"""
《凡尔赛条约》分析
============================

演示内置推理和 DeepSeek 推理模型在历史分析中的应用。
"""

from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.models.openai import OpenAIChat

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
task = (
    "分析导致 1919 年《凡尔赛条约》签订的关键因素。"
    "探讨该条约对德国的政治、经济和社会影响，以及它如何促成了第二次世界大战的爆发。"
    "请提供包含多元历史视角的深入评估。"
)

cot_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    reasoning=True,
    markdown=True,
)

deepseek_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    reasoning_model=DeepSeek(id="deepseek-reasoner"),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== 内置思维链（Chain Of Thought） ===")
    cot_agent.print_response(task, stream=True, show_full_reasoning=True)

    print("\n=== DeepSeek 推理模型 ===")
    deepseek_agent.print_response(task, stream=True, show_full_reasoning=True)

"""
Fibonacci 脚本规划
=========================

演示内置推理和 DeepSeek 推理模型在编程指导中的应用。
"""

from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.models.openai import OpenAIChat

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
task = "请给我编写 Fibonacci 数列 Python 脚本的步骤"

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

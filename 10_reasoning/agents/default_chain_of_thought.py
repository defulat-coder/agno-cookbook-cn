"""
OpenAI 默认思维链（Chain Of Thought）
===============================

在同一脚本中演示回退思维链和内置推理的使用。
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
manual_cot_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    reasoning_model=OpenAIChat(
        id="gpt-4o",
        max_tokens=1200,
    ),
    markdown=True,
)

default_cot_agent = Agent(
    model=OpenAIChat(id="gpt-4o", max_tokens=1200),
    reasoning=True,
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    prompt = "请给我编写 Fibonacci 数列 Python 脚本的步骤"

    print("=== 显式指定 reasoning_model 回退 ===")
    manual_cot_agent.print_response(
        prompt,
        stream=True,
        show_full_reasoning=True,
    )

    print("\n=== 内置 reasoning=True ===")
    default_cot_agent.print_response(
        prompt,
        stream=True,
        show_full_reasoning=True,
    )

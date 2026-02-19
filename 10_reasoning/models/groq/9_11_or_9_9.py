"""
9.11 还是 9.9（Groq）
===========

演示推理 Cookbook 示例。
"""

from agno.agent import Agent
from agno.models.groq import Groq


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    agent = Agent(
        model=Groq(
            id="qwen/qwen3-32b",
            temperature=0.6,
            max_tokens=1024,
            top_p=0.95,
        ),
        reasoning=True,
        markdown=True,
    )
    agent.print_response(
        "9.11 和 9.9 哪个更大？", stream=True, show_full_reasoning=True
    )


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()

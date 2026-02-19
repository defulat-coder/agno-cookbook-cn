"""
DeepSeek + Claude 组合
====================

演示推理 Cookbook 示例。
"""

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.models.groq import Groq


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    deepseek_plus_claude = Agent(
        model=Claude(id="claude-3-7-sonnet-20250219"),
        reasoning_model=Groq(
            id="qwen/qwen3-32b",
            temperature=0.6,
            max_tokens=1024,
            top_p=0.95,
        ),
    )
    deepseek_plus_claude.print_response("9.11 和 9.9 哪个更大？", stream=True)


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()

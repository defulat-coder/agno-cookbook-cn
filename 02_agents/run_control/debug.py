"""
调试
=============================

调试模式。
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat

# 你可以在 agent 上设置调试模式，让所有运行都有更详细的输出
# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    debug_mode=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response(input="Tell me a joke.")

    # 你也可以只在单次运行时设置调试模式
    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
    )
    agent.print_response(input="Tell me a joke.", debug_mode=True)

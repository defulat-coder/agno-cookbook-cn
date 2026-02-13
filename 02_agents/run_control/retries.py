"""
重试
=============================

演示如何为 Agent 设置重试机制的示例。
"""

from agno.agent import Agent
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    name="Web Search Agent",
    role="Search the web for information",
    tools=[WebSearchTools()],
    retries=3,  # 在发生错误时，Agent 运行将重试 3 次。
    delay_between_retries=1,  # 重试之间的延迟（秒）。
    exponential_backoff=True,  # 如果为 True，每次重试之间的延迟会加倍。
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response(
        "What exactly is an AI Agent?",
        stream=True,
    )

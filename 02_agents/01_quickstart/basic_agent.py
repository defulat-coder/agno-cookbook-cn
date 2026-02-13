"""
基础 Agent
=============================

基础 Agent 快速入门。
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    name="Quickstart Agent",
    model=OpenAIResponses(id="gpt-5.2"),
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response(
        "Say hello and introduce yourself in one sentence.", stream=True
    )

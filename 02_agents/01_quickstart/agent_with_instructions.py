"""
带指令的 Agent
=============================

带指令的 Agent 快速入门。
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# Agent 指令
# ---------------------------------------------------------------------------
instructions = """\
你是一个简洁的助手。
尽可能用正好 3 个要点来回答。\
"""

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    name="Instruction-Tuned Agent",
    model=OpenAIResponses(id="gpt-5.2"),
    instructions=instructions,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response("How can I improve my Python debugging workflow?", stream=True)

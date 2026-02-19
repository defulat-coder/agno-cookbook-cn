"""
WatsonX 默认思维链（COT）回退
============================

演示使用 IBM WatsonX 模型的默认思维链行为。
"""

from agno.agent import Agent
from agno.models.ibm import WatsonX

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
reasoning_agent = Agent(
    model=WatsonX(id="meta-llama/llama-3-3-70b-instruct"),
    reasoning=True,
    debug_mode=True,
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    reasoning_agent.print_response(
        "请给我编写 Fibonacci 数列 Python 脚本的步骤",
        stream=True,
        show_full_reasoning=True,
    )

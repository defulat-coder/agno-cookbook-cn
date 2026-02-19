"""
Mistral 推理思维链（COT）
=====================

演示使用 Mistral 模型进行内置思维链推理。
"""

from agno.agent import Agent
from agno.models.mistral import MistralChat

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
reasoning_agent = Agent(
    model=MistralChat(id="mistral-large-latest"),
    reasoning=True,
    markdown=True,
    use_json_mode=True,
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

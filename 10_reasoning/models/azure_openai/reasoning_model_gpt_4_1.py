"""
推理模型 GPT-4.1（Azure OpenAI）
=======================

演示推理 Cookbook 示例。
"""

from agno.agent import Agent
from agno.models.azure.openai_chat import AzureOpenAI


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    agent = Agent(
        model=AzureOpenAI(id="gpt-4o-mini"), reasoning_model=AzureOpenAI(id="gpt-4.1")
    )
    agent.print_response(
        "请解答电车难题，评估多种伦理框架，并用 ASCII 图示展示你的解答。",
        stream=True,
    )


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()

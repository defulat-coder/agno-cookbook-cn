"""
推理模型 DeepSeek（Azure AI Foundry）
========================

演示推理 Cookbook 示例。
"""

import os

from agno.agent import Agent
from agno.models.azure import AzureAIFoundry


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    agent = Agent(
        model=AzureAIFoundry(id="gpt-4o"),
        reasoning=True,
        reasoning_model=AzureAIFoundry(
            id="DeepSeek-R1",
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
            api_key=os.getenv("AZURE_API_KEY"),
        ),
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

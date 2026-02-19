"""
推理模型流式输出 DeepSeek（Azure AI Foundry）
===============================

演示推理 Cookbook 示例。
"""

import asyncio
import os

from agno.agent import Agent
from agno.models.azure import AzureAIFoundry
from agno.run.agent import RunEvent  # noqa


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    async def streaming_reasoning():
        """测试使用 Azure AI Foundry DeepSeek 模型的流式推理。"""
        # 创建启用推理的 Agent
        agent = Agent(
            reasoning_model=AzureAIFoundry(
                id="DeepSeek-R1",
                azure_endpoint=os.getenv("AZURE_ENDPOINT"),
                api_key=os.getenv("AZURE_API_KEY"),
            ),
            reasoning=True,
            instructions="请逐步思考问题。",
        )

        prompt = "25 * 37 等于多少？请展示你的推理过程。"

        await agent.aprint_response(prompt, stream=True, stream_events=True)

        # 使用手动事件循环查看所有事件
        # async for run_output_event in agent.arun(
        #     prompt,
        #     stream=True,
        #     stream_events=True,
        # ):
        #     if run_output_event.event == RunEvent.run_started:
        #         print(f"\n事件: {run_output_event.event}")

        #     elif run_output_event.event == RunEvent.reasoning_started:
        #         print(f"\n事件: {run_output_event.event}")
        #         print("推理开始...\n")

        #     elif run_output_event.event == RunEvent.reasoning_content_delta:
        #         # 这是推理内容的新流式事件
        #         print(run_output_event.reasoning_content, end="", flush=True)

        #     elif run_output_event.event == RunEvent.reasoning_step:
        #         print(f"\n事件: {run_output_event.event}")

        #     elif run_output_event.event == RunEvent.reasoning_completed:
        #         print(f"\n\n事件: {run_output_event.event}")

        #     elif run_output_event.event == RunEvent.run_content:
        #         if run_output_event.content:
        #             print(run_output_event.content, end="", flush=True)

        #     elif run_output_event.event == RunEvent.run_completed:
        #         print(f"\n\n事件: {run_output_event.event}")

    if __name__ == "__main__":
        asyncio.run(streaming_reasoning())


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()

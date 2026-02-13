"""
压缩事件
=============================

测试脚本，用于验证压缩事件是否正常工作。
"""

import asyncio

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.run.agent import RunEvent
from agno.tools.duckduckgo import DuckDuckGoTools

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[DuckDuckGoTools()],
    description="专门跟踪竞争对手活动",
    instructions="使用搜索工具，始终使用最新的信息和数据。",
    compress_tool_results=True,
)


async def main():
    print("--- 运行带压缩事件的 agent ---")

    stream = agent.arun(
        """
        研究这些 AI 公司的最近活动：
        1. OpenAI - 最新新闻
        2. Anthropic - 最新新闻
        3. Google DeepMind - 最新新闻
        """,
        stream=True,
        stream_events=True,
    )

    async for chunk in stream:
        if chunk.event == RunEvent.run_started.value:
            print(f"[运行开始] model={chunk.model}")

        elif chunk.event == RunEvent.model_request_started.value:
            print(f"[模型请求开始] model={chunk.model}")

        elif chunk.event == RunEvent.model_request_completed.value:
            print(
                f"[模型请求完成] tokens: in={chunk.input_tokens}, out={chunk.output_tokens}"
            )

        elif chunk.event == RunEvent.tool_call_started.value:
            print(f"[工具调用开始] {chunk.tool.tool_name}")

        elif chunk.event == RunEvent.tool_call_completed.value:
            print(f"[工具调用完成] {chunk.tool.tool_name}")

        elif chunk.event == RunEvent.compression_started.value:
            print("[压缩开始]")

        elif chunk.event == RunEvent.compression_completed.value:
            print(
                f"[压缩完成] compressed={chunk.tool_results_compressed} results"
            )
            print(
                f"  原始: {chunk.original_size} chars -> 压缩后: {chunk.compressed_size} chars"
            )
            if chunk.original_size and chunk.compressed_size:
                ratio = (1 - chunk.compressed_size / chunk.original_size) * 100
                print(f"  压缩率: {ratio:.1f}% 减少")

        elif chunk.event == RunEvent.run_completed.value:
            print("[运行完成]")


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())

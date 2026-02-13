"""
并发执行
=============================

使用 asyncio.gather 实现 Agent 的并发执行。
"""

import asyncio

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from rich.pretty import pprint

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
providers = ["openai", "anthropic", "ollama", "cohere", "google"]
instructions = """
你的任务是撰写一份关于 AI 提供商的深入研究报告。
报告应客观公正，基于事实。
"""

# 在循环外创建一次 agent - 这是正确的模式
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=instructions,
    tools=[DuckDuckGoTools()],
)


async def get_reports():
    """使用同一个 agent 实例并发运行多个研究任务。"""
    tasks = [
        agent.arun(f"Write a report on the following AI provider: {provider}")
        for provider in providers
    ]
    results = await asyncio.gather(*tasks)
    return results


async def main():
    results = await get_reports()
    for result in results:
        print("************")
        pprint(result.content)
        print("************")
        print("\n")


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())

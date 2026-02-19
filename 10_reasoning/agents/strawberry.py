"""
草莓字母计数
==========================

演示普通、内置推理和 DeepSeek 推理模型在字母计数任务中的应用。
"""

import asyncio

from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.models.openai import OpenAIChat
from rich.console import Console

# ---------------------------------------------------------------------------
# Create Agents
# ---------------------------------------------------------------------------
console = Console()

task = "单词 'strawberry' 中有多少个字母 'r'？"

regular_agent = Agent(model=OpenAIChat(id="gpt-4o"), markdown=True)

cot_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    reasoning=True,
    markdown=True,
)

deepseek_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    reasoning_model=DeepSeek(id="deepseek-reasoner"),
    markdown=True,
)


async def run_agents() -> None:
    console.rule("[bold blue]统计 'strawberry' 中的字母 'r'[/bold blue]")

    console.rule("[bold green]普通 Agent[/bold green]")
    await regular_agent.aprint_response(task, stream=True)

    console.rule("[bold yellow]内置推理 Agent[/bold yellow]")
    await cot_agent.aprint_response(task, stream=True, show_full_reasoning=True)

    console.rule("[bold cyan]DeepSeek 推理 Agent[/bold cyan]")
    await deepseek_agent.aprint_response(task, stream=True)


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(run_agents())

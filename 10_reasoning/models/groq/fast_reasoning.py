"""
快速推理（Groq）
==============

演示推理 Cookbook 示例。
"""

import time

from agno.agent import Agent
from agno.models.groq import Groq
from rich.console import Console


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    console = Console()

    # 需要推理的测试任务
    task = "23 × 47 等于多少？请展示逐步推理过程。"

    console.rule("[bold cyan]Groq 快速推理演示[/bold cyan]")

    # 测试 Llama 3.3（具备推理能力）
    console.print(
        "\n[bold blue]Llama 3.3 70B Versatile（具备推理能力）[/bold blue]"
    )
    try:
        start = time.time()
        agent_deepseek = Agent(
            model=Groq(id="llama-3.3-70b-versatile"),
            markdown=True,
        )
        response = agent_deepseek.run(task, stream=False)
        end = time.time()

        console.print(response.content)
        console.print(f"\n[dim]响应时间：{end - start:.2f}s[/dim]")

        if response.reasoning_content:
            reasoning_len = len(response.reasoning_content.split())
            console.print(f"[dim]推理深度：约 {reasoning_len} 个词[/dim]")
    except Exception as e:
        console.print(f"[red]错误：{e}[/red]")

    # 对比测试 Llama
    console.print("\n[bold green]Llama 3.3 70B（标准模式）[/bold green]")
    try:
        start = time.time()
        agent_llama = Agent(
            model=Groq(id="llama-3.3-70b-versatile"),
            markdown=True,
        )
        response = agent_llama.run(task, stream=False)
        end = time.time()

        console.print(response.content)
        console.print(f"\n[dim]响应时间：{end - start:.2f}s[/dim]")
    except Exception as e:
        console.print(f"[red]错误：{e}[/red]")


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()

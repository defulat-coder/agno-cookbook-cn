"""
本地推理（Ollama）
===============

演示推理 Cookbook 示例。
"""

from agno.agent import Agent
from agno.models.ollama import Ollama
from rich.console import Console


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    console = Console()

    # 测试任务
    task = "23 × 47 等于多少？请展示逐步推理过程。"

    console.rule("[bold cyan]使用 Ollama 的本地推理[/bold cyan]")

    # 测试 QwQ（阿里巴巴的推理模型）
    console.print("\n[bold blue]QwQ:32B（阿里巴巴推理模型）[/bold blue]")
    console.print("[dim]在本地完全私密地运行...[/dim]\n")

    try:
        agent_qwq = Agent(
            model=Ollama(id="qwq:32b"),
            markdown=True,
        )
        agent_qwq.print_response(task, stream=True, show_full_reasoning=True)
    except Exception as e:
        console.print(f"[red]错误：{e}[/red]")
        console.print(
            "[yellow]请确保 Ollama 正在运行且已安装 qwq:32b：[/yellow]"
        )
        console.print("  ollama pull qwq:32b")

    # 测试 DeepSeek-R1:8B（更小、更快）
    console.print("\n[bold green]DeepSeek-R1:8B（更小、更快）[/bold green]")
    console.print("[dim]在本地完全私密地运行...[/dim]\n")

    try:
        agent_deepseek = Agent(
            model=Ollama(id="deepseek-r1:8b"),
            markdown=True,
        )
        agent_deepseek.print_response(task, stream=True, show_full_reasoning=True)
    except Exception as e:
        console.print(f"[red]错误：{e}[/red]")
        console.print(
            "[yellow]请确保 Ollama 正在运行且已安装 deepseek-r1:8b：[/yellow]"
        )
        console.print("  ollama pull deepseek-r1:8b")


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()

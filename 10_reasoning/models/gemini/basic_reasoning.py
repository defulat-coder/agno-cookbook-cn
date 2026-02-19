"""
基础推理（Gemini）
===============

演示推理 Cookbook 示例。
"""

from agno.agent import Agent
from agno.models.google import Gemini
from rich.console import Console


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    console = Console()

    # 经典推理测试
    task = "9.11 和 9.9 哪个更大？请解释你的推理过程。"

    # 创建普通 Agent（无推理）
    regular_agent = Agent(
        model=Gemini(id="gemini-2.5-flash"),
        markdown=True,
    )

    # 创建带思考预算的 Agent
    reasoning_agent = Agent(
        model=Gemini(id="gemini-2.5-flash"),
        reasoning_model=Gemini(id="gemini-2.5-flash", thinking_budget=1024),
        markdown=True,
    )

    console.rule("[bold blue]普通 Gemini Agent（无推理）[/bold blue]")
    console.print("此 Agent 将直接回答，不使用扩展思考。\n")
    regular_agent.print_response(task, stream=True)

    console.rule("[bold green]Gemini（带思考预算）[/bold green]")
    console.print("此 Agent 使用思考预算来分析问题。\n")
    reasoning_agent.print_response(task, stream=True, show_full_reasoning=True)

    console.rule("[bold cyan]访问推理内容[/bold cyan]")
    response = reasoning_agent.run(task, stream=False)
    if response.reasoning_content:
        console.print(
            f"[dim]使用的推理 Token 数：约 {len(response.reasoning_content.split())} 个[/dim]"
        )
        console.print(
            f"\n[bold]推理过程：[/bold]\n{response.reasoning_content[:400]}..."
        )
    else:
        console.print("[yellow]无可用的推理内容[/yellow]")


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()

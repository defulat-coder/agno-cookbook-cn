"""
基础推理
===============

演示推理 Cookbook 示例。
"""

from agno.agent import Agent
from agno.models.anthropic import Claude
from rich.console import Console


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    console = Console()

    # 经典推理测试：比较小数大小
    task = "9.11 和 9.9 哪个更大？请逐步解释你的推理过程。"

    # 创建普通 Agent（无推理）
    regular_agent = Agent(
        model=Claude(id="claude-sonnet-4-5"),
        markdown=True,
    )

    # 创建带扩展思考功能的 Agent
    reasoning_agent = Agent(
        model=Claude(id="claude-sonnet-4-5"),
        reasoning_model=Claude(
            id="claude-sonnet-4-5",
            thinking={"type": "enabled", "budget_tokens": 1024},
        ),
        markdown=True,
    )

    console.rule("[bold blue]普通 Claude Agent（无推理）[/bold blue]")
    console.print("此 Agent 将直接回答，不使用扩展思考。\n")
    regular_agent.print_response(task, stream=True)

    console.rule("[bold green]Claude（扩展思考）[/bold green]")
    console.print("此 Agent 使用扩展思考来深入分析问题。\n")
    reasoning_agent.print_response(task, stream=True, show_full_reasoning=True)

    console.rule("[bold cyan]访问推理内容[/bold cyan]")
    response = reasoning_agent.run(task, stream=False)
    if response.reasoning_content:
        console.print(
            f"[dim]使用的推理 Token 数：{len(response.reasoning_content.split())}[/dim]"
        )
        console.print(
            f"\n[bold]推理内容前 300 个字符：[/bold]\n{response.reasoning_content[:300]}..."
        )


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()

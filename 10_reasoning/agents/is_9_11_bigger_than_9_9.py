"""
小数比较推理
============================

演示普通、内置推理和 DeepSeek 推理模型在 9.11 与 9.9 比较中的应用。
"""

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.models.deepseek import DeepSeek
from agno.models.openai import OpenAIChat
from rich.console import Console

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
console = Console()

task = "9.11 和 9.9 哪个更大？"

regular_agent_openai = Agent(model=OpenAIChat(id="gpt-4o"), markdown=True)

cot_agent_openai = Agent(
    model=OpenAIChat(id="gpt-4o"),
    reasoning=True,
    markdown=True,
)

regular_agent_claude = Agent(model=Claude("claude-3-5-sonnet-20241022"), markdown=True)

deepseek_agent_claude = Agent(
    model=Claude("claude-3-5-sonnet-20241022"),
    reasoning_model=DeepSeek(id="deepseek-reasoner"),
    markdown=True,
)

deepseek_agent_openai = Agent(
    model=OpenAIChat(id="gpt-4o"),
    reasoning_model=DeepSeek(id="deepseek-reasoner"),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    console.rule("[bold blue]普通 OpenAI Agent[/bold blue]")
    regular_agent_openai.print_response(task, stream=True)

    console.rule("[bold yellow]OpenAI 内置推理 Agent[/bold yellow]")
    cot_agent_openai.print_response(task, stream=True, show_full_reasoning=True)

    console.rule("[bold green]普通 Claude Agent[/bold green]")
    regular_agent_claude.print_response(task, stream=True)

    console.rule("[bold cyan]Claude + DeepSeek 推理 Agent[/bold cyan]")
    deepseek_agent_claude.print_response(task, stream=True)

    console.rule("[bold magenta]OpenAI + DeepSeek 推理 Agent[/bold magenta]")
    deepseek_agent_openai.print_response(task, stream=True)

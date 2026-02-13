"""人机协作：为工具调用添加用户确认

此示例展示了如何在 Agno 工具中使用 MCP Server 实现人机协作功能。
它展示了如何：
- 在工具执行期间处理用户确认
- 根据用户选择优雅地取消操作

一些实际应用：
- 在执行之前确认敏感操作
- 在进行 API 调用之前审查它们
- 验证数据转换
- 在关键系统中批准自动化操作

运行 `uv pip install openai httpx rich agno` 来安装依赖项。
"""

import asyncio

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.anthropic import Claude
from agno.tools.mcp import MCPTools
from rich.console import Console
from rich.prompt import Prompt

console = Console()

mcp_tools = MCPTools(
    transport="streamable-http",
    url="https://docs.agno.com/mcp",
    requires_confirmation_tools=["SearchAgno"],  # Note: Tool names are case-sensitive
)

agent = Agent(
    model=Claude(id="claude-sonnet-4-5"),
    tools=[mcp_tools],
    markdown=True,
    db=SqliteDb(db_file="tmp/confirmation_required_toolkit.db"),
)


async def main():
    async for run_event in agent.arun("What is Agno?", stream=True):
        if run_event.is_paused:
            # Handle confirmation requirements
            for requirement in run_event.active_requirements:
                if requirement.needs_confirmation:
                    # Ask for confirmation
                    console.print(
                        f"Tool name [bold blue]{requirement.tool_execution.tool_name}({requirement.tool_execution.tool_args})[/] requires confirmation."
                    )
                    message = (
                        Prompt.ask(
                            "Do you want to continue?", choices=["y", "n"], default="y"
                        )
                        .strip()
                        .lower()
                    )

                    if message == "n":
                        requirement.reject()
                    else:
                        requirement.confirm()

            # Continue the run after handling all confirmations
            async for resp in agent.acontinue_run(
                run_id=run_event.run_id,
                requirements=run_event.requirements,
                stream=True,
            ):
                if resp.content:
                    print(resp.content, end="")
        else:
            # Not paused - print the streaming content
            if run_event.content:
                print(run_event.content, end="")

    print()  # Final newline


if __name__ == "__main__":
    asyncio.run(main())

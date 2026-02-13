"""
外部工具执行
=============================

人机协作：在 agent 之外执行工具调用。
"""

import subprocess

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.tools import tool
from agno.utils import pprint


# 我们必须创建一个具有正确名称、参数和 docstring 的工具，以便 agent 知道要调用什么。
@tool(external_execution=True)
def execute_shell_command(command: str) -> str:
    """执行 shell 命令。

    Args:
        command (str): 要执行的 shell 命令

    Returns:
        str: shell 命令的输出
    """
    if command.startswith("ls"):
        return subprocess.check_output(command, shell=True).decode("utf-8")
    else:
        raise Exception(f"Unsupported command: {command}")


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[execute_shell_command],
    markdown=True,
    db=SqliteDb(session_table="test_session", db_file="tmp/example.db"),
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_response = agent.run("What files do I have in my current directory?")

    if run_response.is_paused:
        for requirement in run_response.active_requirements:
            if requirement.needs_external_execution:
                if requirement.tool_execution.tool_name == execute_shell_command.name:
                    print(
                        f"Executing {requirement.tool_execution.tool_name} with args {requirement.tool_execution.tool_args} externally"
                    )
                    # 我们自己执行工具。你也可以在这里执行完全外部的东西。
                    result = execute_shell_command.entrypoint(
                        **requirement.tool_execution.tool_args
                    )  # type: ignore
                    # 我们必须在工具执行对象上设置结果，以便 agent 可以继续
                    requirement.set_external_execution_result(result)

    run_response = agent.continue_run(
        run_id=run_response.run_id,
        requirements=run_response.requirements,
    )
    pprint.pprint_run_response(run_response)

    # 或者用于简单的调试流程
    # agent.print_response("What files do I have in my current directory?")

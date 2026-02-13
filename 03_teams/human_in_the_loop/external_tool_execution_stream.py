"""外部工具执行流式传输

此示例演示当成员 agent 的工具在流式模式下需要外部执行时团队如何暂停。工具结果由调用者提供，而不是由 agent 执行。

注意：与成员 agent 流式传输时，使用 isinstance() 与 TeamRunPausedEvent 以区分团队的暂停和成员 agent 的暂停。
"""

import shlex
import subprocess

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.run.team import RunPausedEvent as TeamRunPausedEvent
from agno.team.team import Team
from agno.tools import tool
from agno.utils import pprint

db = SqliteDb(db_file="tmp/team_hitl_stream.db")


@tool(external_execution=True)
def run_shell_command(command: str) -> str:
    """Execute a shell command on the server.

    Args:
        command (str): The shell command to execute
    """
    return subprocess.check_output(shlex.split(command)).decode("utf-8")


ops_agent = Agent(
    name="Ops Agent",
    role="Handles server operations",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[run_shell_command],
    db=db,
)

team = Team(
    name="SRE Team",
    members=[ops_agent],
    model=OpenAIChat(id="gpt-4o-mini"),
    db=db,
)


for run_event in team.run("List the files in the current directory", stream=True):
    # Use isinstance to check for team's pause event (not the member agent's)
    if isinstance(run_event, TeamRunPausedEvent):
        print("Team paused - requires external execution")
        for req in run_event.active_requirements:
            if req.needs_external_execution:
                print(f"  Tool: {req.tool_execution.tool_name}")
                print(f"  Args: {req.tool_execution.tool_args}")

                # Execute the tool externally
                result = run_shell_command.entrypoint(**req.tool_execution.tool_args)
                req.set_external_execution_result(result)

        response = team.continue_run(
            run_id=run_event.run_id,
            session_id=run_event.session_id,
            requirements=run_event.requirements,
            stream=True,
        )
        pprint.pprint_run_response(response)

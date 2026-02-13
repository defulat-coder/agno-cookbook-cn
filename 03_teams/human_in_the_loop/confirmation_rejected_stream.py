"""确认被拒绝流式传输

此示例演示团队在流式模式下如何处理工具调用的拒绝。拒绝后，团队继续，模型响应确认拒绝。

注意：与成员 agent 流式传输时，使用 isinstance() 与 TeamRunPausedEvent 以区分团队的暂停和成员 agent 的暂停。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.run.team import RunPausedEvent as TeamRunPausedEvent
from agno.team.team import Team
from agno.tools import tool
from agno.utils import pprint

db = SqliteDb(db_file="tmp/team_hitl_stream.db")


@tool(requires_confirmation=True)
def delete_user_account(username: str) -> str:
    """Permanently delete a user account and all associated data.

    Args:
        username (str): Username of the account to delete
    """
    return f"Account {username} has been permanently deleted"


admin_agent = Agent(
    name="Admin Agent",
    role="Handles account administration tasks",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[delete_user_account],
    db=db,
)

team = Team(
    name="Admin Team",
    members=[admin_agent],
    model=OpenAIChat(id="gpt-4o-mini"),
    db=db,
)


for run_event in team.run("Delete the account for user 'jsmith'", stream=True):
    # Use isinstance to check for team's pause event (not the member agent's)
    if isinstance(run_event, TeamRunPausedEvent):
        print("Team paused - requires confirmation")
        for req in run_event.active_requirements:
            if req.needs_confirmation:
                print(f"  Tool: {req.tool_execution.tool_name}")
                print(f"  Args: {req.tool_execution.tool_args}")

                # Reject the dangerous operation
                req.reject(note="Account deletion requires manager approval first")

        response = team.continue_run(
            run_id=run_event.run_id,
            session_id=run_event.session_id,
            requirements=run_event.requirements,
            stream=True,
        )
        pprint.pprint_run_response(response)

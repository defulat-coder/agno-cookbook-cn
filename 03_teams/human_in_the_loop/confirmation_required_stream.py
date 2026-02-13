"""流式传输需要确认

此示例演示当成员 agent 的工具在流式模式下需要人工确认时团队如何暂停。确认后，团队使用 continue_run() 恢复。

注意：与成员 agent 流式传输时，使用 isinstance() 与 TeamRunPausedEvent 以区分团队的暂停和成员 agent 的暂停。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.run.team import RunPausedEvent as TeamRunPausedEvent
from agno.team.team import Team
from agno.tools import tool
from agno.utils import pprint

# Database is required for continue_run to work - it stores the paused run
db = SqliteDb(db_file="tmp/team_hitl_stream.db")


@tool(requires_confirmation=True)
def deploy_to_production(app_name: str, version: str) -> str:
    """Deploy an application to production.

    Args:
        app_name (str): Name of the application
        version (str): Version to deploy
    """
    return f"Successfully deployed {app_name} v{version} to production"


deploy_agent = Agent(
    name="Deploy Agent",
    role="Handles deployments to production",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[deploy_to_production],
    db=db,
)

team = Team(
    name="DevOps Team",
    members=[deploy_agent],
    model=OpenAIChat(id="gpt-4o-mini"),
    db=db,
)


for run_event in team.run(
    "Deploy the payments app version 2.1 to production", stream=True
):
    # Use isinstance to check for team's pause event (not the member agent's)
    if isinstance(run_event, TeamRunPausedEvent):
        print("Team paused - requires confirmation")
        for req in run_event.active_requirements:
            if req.needs_confirmation:
                print(f"  Tool: {req.tool_execution.tool_name}")
                print(f"  Args: {req.tool_execution.tool_args}")
                req.confirm()

        response = team.continue_run(
            run_id=run_event.run_id,
            session_id=run_event.session_id,
            requirements=run_event.requirements,
            stream=True,
        )
        pprint.pprint_run_response(response)

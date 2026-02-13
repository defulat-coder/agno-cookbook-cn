"""团队工具确认流式传输

此示例演示在流式模式下直接提供给 Team（而非成员 agent）的工具的 HITL。当团队 leader 决定使用需要确认的工具时，整个团队运行会暂停，直到人工确认。

注意：对于团队级工具（而非成员 agent 工具），您可以使用 isinstance(event, TeamRunPausedEvent) 或 event.is_paused，因为没有成员 agent 暂停需要混淆。
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
def approve_deployment(environment: str, service: str) -> str:
    """Approve and execute a deployment to an environment.

    Args:
        environment (str): Target environment (staging, production)
        service (str): Service to deploy
    """
    return f"Deployment of {service} to {environment} approved and executed"


research_agent = Agent(
    name="Research Agent",
    role="Researches deployment readiness",
    model=OpenAIChat(id="gpt-4o-mini"),
    db=db,
)

team = Team(
    name="Release Team",
    members=[research_agent],
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[approve_deployment],
    db=db,
)


for run_event in team.run(
    "Check if the auth service is ready and deploy it to staging", stream=True
):
    # Use isinstance to check for team's pause event
    if isinstance(run_event, TeamRunPausedEvent):
        print("Team paused - requires confirmation for team-level tool")
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

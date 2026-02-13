"""异步流式传输需要确认

与 confirmation_required_stream.py 相同，但使用异步 run/continue_run。

注意：与成员 agent 流式传输时，使用 isinstance() 与 TeamRunPausedEvent 以区分团队的暂停和成员 agent 的暂停。
"""

import asyncio

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.run.team import RunPausedEvent as TeamRunPausedEvent
from agno.team.team import Team
from agno.tools import tool
from agno.utils import pprint

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


async def main():
    async for run_event in team.arun(
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

            # Use apprint_run_response for async streaming
            response = team.acontinue_run(
                run_id=run_event.run_id,
                session_id=run_event.session_id,
                requirements=run_event.requirements,
                stream=True,
            )
            await pprint.apprint_run_response(response)


if __name__ == "__main__":
    asyncio.run(main())

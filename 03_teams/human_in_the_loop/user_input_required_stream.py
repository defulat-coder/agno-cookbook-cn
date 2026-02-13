"""流式传输需要用户输入

此示例演示当成员 agent 的工具在流式模式下需要来自用户的附加信息才能执行时团队如何暂停。

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


@tool(requires_user_input=True, user_input_fields=["passenger_name"])
def book_flight(destination: str, date: str, passenger_name: str) -> str:
    """Book a flight to a destination.

    Args:
        destination (str): The destination city
        date (str): Travel date
        passenger_name (str): Full name of the passenger
    """
    return f"Booked flight to {destination} on {date} for {passenger_name}"


booking_agent = Agent(
    name="Booking Agent",
    role="Books travel arrangements",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[book_flight],
    db=db,
)

team = Team(
    name="Travel Team",
    members=[booking_agent],
    model=OpenAIChat(id="gpt-4o-mini"),
    db=db,
)


for run_event in team.run("Book a flight to Tokyo for next Friday", stream=True):
    # Use isinstance to check for team's pause event (not the member agent's)
    if isinstance(run_event, TeamRunPausedEvent):
        print("Team paused - requires user input")
        for req in run_event.active_requirements:
            if req.needs_user_input:
                print(f"  Tool: {req.tool_execution.tool_name}")
                for field in req.user_input_schema or []:
                    print(f"  Field needed: {field.name} - {field.description}")

                req.provide_user_input({"passenger_name": "John Smith"})

        response = team.continue_run(
            run_id=run_event.run_id,
            session_id=run_event.session_id,
            requirements=run_event.requirements,
            stream=True,
        )
        pprint.pprint_run_response(response)

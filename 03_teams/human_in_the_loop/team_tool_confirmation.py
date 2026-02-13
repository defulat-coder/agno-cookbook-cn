"""团队工具确认

此示例演示直接提供给 Team（而非成员 agent）的工具的 HITL。当团队 leader 决定使用需要确认的工具时，整个团队运行会暂停，直到人工确认。
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team.team import Team
from agno.tools import tool


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
)

team = Team(
    name="Release Team",
    members=[research_agent],
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[approve_deployment],
)

response = team.run("Check if the auth service is ready and deploy it to staging")

if response.is_paused:
    print("Team paused - requires confirmation for team-level tool")
    for req in response.requirements:
        if req.needs_confirmation:
            print(f"  Tool: {req.tool_execution.tool_name}")
            print(f"  Args: {req.tool_execution.tool_args}")
            req.confirm()

    response = team.continue_run(response)
    print(f"Result: {response.content}")
else:
    print(f"Result: {response.content}")

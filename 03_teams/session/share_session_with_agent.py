"""
与 Agent 共享 Session
========================

演示在团队和单 agent 交互之间共享一个 session。
"""

import uuid

from agno.agent import Agent
from agno.db.in_memory import InMemoryDb
from agno.models.openai import OpenAIChat
from agno.team import Team

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
db = InMemoryDb()


def get_weather(city: str) -> str:
    """获取给定城市的天气。"""
    return f"The weather in {city} is sunny."


def get_activities(city: str) -> str:
    """获取给定城市的活动。"""
    return f"The activities in {city} are swimming and hiking."


# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
agent = Agent(
    name="City Planner Agent",
    id="city-planner-agent-id",
    model=OpenAIChat(id="gpt-4o"),
    db=db,
    tools=[get_weather, get_activities],
    add_history_to_context=True,
)

weather_agent = Agent(
    name="Weather Agent",
    id="weather-agent-id",
    model=OpenAIChat(id="gpt-4o"),
    tools=[get_weather],
)

activities_agent = Agent(
    name="Activities Agent",
    id="activities-agent-id",
    model=OpenAIChat(id="gpt-4o"),
    tools=[get_activities],
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
team = Team(
    name="City Planner Team",
    id="city-planner-team-id",
    model=OpenAIChat(id="gpt-4o"),
    db=db,
    members=[weather_agent, activities_agent],
    add_history_to_context=True,
)

# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    session_id = str(uuid.uuid4())

    agent.print_response("What is the weather like in Tokyo?", session_id=session_id)
    team.print_response("What activities can I do there?", session_id=session_id)
    agent.print_response(
        "What else can you tell me about the city? Should I visit?",
        session_id=session_id,
    )

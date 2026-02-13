"""
带历史记录的直接响应
=============================

演示直接成员响应，团队历史记录持久化到 SQLite。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.team import Team


# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."


weather_agent = Agent(
    name="Weather Agent",
    role="你是一个可以回答天气相关问题的天气 agent。",
    model=OpenAIChat(id="o3-mini"),
    tools=[get_weather],
)


def get_news(topic: str) -> str:
    return f"The news about {topic} is that it is going well!"


news_agent = Agent(
    name="News Agent",
    role="你是一个可以回答新闻相关问题的新闻 agent。",
    model=OpenAIChat(id="o3-mini"),
    tools=[get_news],
)


def get_activities(city: str) -> str:
    return f"The activities in {city} are that it is going well!"


activities_agent = Agent(
    name="Activities Agent",
    role="你是一个可以回答活动相关问题的活动 agent。",
    model=OpenAIChat(id="o3-mini"),
    tools=[get_activities],
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
geo_search_team = Team(
    name="Geo Search Team",
    model=OpenAIChat("o3-mini"),
    respond_directly=True,
    members=[
        weather_agent,
        news_agent,
        activities_agent,
    ],
    instructions="你是一个地理搜索 agent，可以回答关于城市的天气、新闻和活动的问题。",
    db=SqliteDb(
        db_file="tmp/geo_search_team.db"
    ),  # 添加数据库以存储对话历史记录
    add_history_to_context=True,  # 确保团队领导者了解先前的请求
)

# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    geo_search_team.print_response(
        "I am doing research on Tokyo. What is the weather like there?", stream=True
    )

    geo_search_team.print_response(
        "Is there any current news about that city?", stream=True
    )

    geo_search_team.print_response("What are the activities in that city?", stream=True)

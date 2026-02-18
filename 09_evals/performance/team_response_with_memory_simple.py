"""
简单团队记忆性能评估
=========================================

演示启用记忆时的团队响应性能。
"""

import asyncio
import random

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.eval.performance import PerformanceEval
from agno.models.openai import OpenAIChat
from agno.team.team import Team

# ---------------------------------------------------------------------------
# 创建示例输入
# ---------------------------------------------------------------------------
cities = [
    "New York",
    "Los Angeles",
    "Chicago",
    "Houston",
    "Miami",
    "San Francisco",
    "Seattle",
    "Boston",
    "Washington D.C.",
    "Atlanta",
    "Denver",
    "Las Vegas",
]

# ---------------------------------------------------------------------------
# 创建数据库
# ---------------------------------------------------------------------------
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
db = PostgresDb(db_url=db_url)


# ---------------------------------------------------------------------------
# 创建工具
# ---------------------------------------------------------------------------
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."


# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
weather_agent = Agent(
    id="weather_agent",
    model=OpenAIChat(id="gpt-5.2"),
    role="Weather Agent",
    description="You are a helpful assistant that can answer questions about the weather.",
    instructions="Be concise, reply with one sentence.",
    tools=[get_weather],
    db=db,
    update_memory_on_run=True,
    add_history_to_context=True,
)

team = Team(
    members=[weather_agent],
    model=OpenAIChat(id="gpt-5.2"),
    instructions="Be concise, reply with one sentence.",
    db=db,
    markdown=True,
    update_memory_on_run=True,
    add_history_to_context=True,
)


# ---------------------------------------------------------------------------
# 创建基准测试函数
# ---------------------------------------------------------------------------
async def run_team():
    random_city = random.choice(cities)
    _ = team.arun(
        input=f"I love {random_city}! What weather can I expect in {random_city}?",
        stream=True,
        stream_events=True,
    )

    return "成功运行团队"


# ---------------------------------------------------------------------------
# 创建评估
# ---------------------------------------------------------------------------
team_response_with_memory_impact = PerformanceEval(
    name="Team Memory Impact",
    func=run_team,
    num_iterations=5,
    warmup_runs=0,
    measure_runtime=False,
    debug_mode=True,
    memory_growth_tracking=True,
)

# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(
        team_response_with_memory_impact.arun(print_results=True, print_summary=True)
    )

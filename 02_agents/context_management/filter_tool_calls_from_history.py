"""
从历史记录中过滤工具调用
=============================

演示 `max_tool_calls_from_history`，说明工具调用过滤仅影响模型输入历史，
而完整运行历史仍保留在存储中。
"""

import random

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat


def get_weather_for_city(city: str) -> str:
    conditions = ["Sunny", "Cloudy", "Rainy", "Snowy", "Foggy", "Windy"]
    temperature = random.randint(-10, 35)
    condition = random.choice(conditions)

    return f"{city}: {temperature}°C, {condition}"


# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
cities = [
    "Tokyo",
    "Delhi",
    "Shanghai",
    "São Paulo",
    "Mumbai",
    "Beijing",
    "Cairo",
    "London",
]


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[get_weather_for_city],
    instructions="你是一个天气助手。使用 get_weather_for_city 工具获取天气。",
    # 仅在上下文中保留历史记录中最近的 3 次工具调用（降低 token 成本）
    max_tool_calls_from_history=3,
    db=SqliteDb(db_file="tmp/weather_data.db"),
    add_history_to_context=True,
    markdown=True,
    # debug_mode=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("\n" + "=" * 90)
    print("工具调用过滤演示: max_tool_calls_from_history=3")
    print("=" * 90)
    print(
        f"{'运行':<5} | {'城市':<15} | {'历史':<8} | {'当前':<8} | {'上下文中':<11} | {'数据库中':<8}"
    )
    print("-" * 90)

    for i, city in enumerate(cities, 1):
        run_response = agent.run(f"What's the weather in {city}?")

        # 计算来自历史记录的工具调用（过滤后发送给模型）
        history_tool_calls = sum(
            len(msg.tool_calls)
            for msg in run_response.messages
            if msg.role == "assistant"
            and msg.tool_calls
            and getattr(msg, "from_history", False)
        )

        # 计算当前运行中的工具调用
        current_tool_calls = sum(
            len(msg.tool_calls)
            for msg in run_response.messages
            if msg.role == "assistant"
            and msg.tool_calls
            and not getattr(msg, "from_history", False)
        )

        total_in_context = history_tool_calls + current_tool_calls

        # 存储在数据库中的工具调用总数（未过滤）
        saved_messages = agent.get_session_messages()
        total_in_db = (
            sum(
                len(msg.tool_calls)
                for msg in saved_messages
                if msg.role == "assistant" and msg.tool_calls
            )
            if saved_messages
            else 0
        )

        print(
            f"{i:<5} | {city:<15} | {history_tool_calls:<8} | {current_tool_calls:<8} | {total_in_context:<11} | {total_in_db:<8}"
        )

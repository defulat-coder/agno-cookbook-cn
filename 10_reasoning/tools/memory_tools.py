"""
记忆工具（Memory Tools）
============

演示推理 Cookbook 示例。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.tools.memory import MemoryTools
from agno.tools.websearch import WebSearchTools


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    db = SqliteDb(db_file="tmp/memory.db")

    john_doe_id = "john_doe@example.com"

    memory_tools = MemoryTools(
        db=db,
    )

    agent = Agent(
        model=OpenAIChat(id="gpt-5-mini"),
        tools=[memory_tools, WebSearchTools()],
        instructions=[
            "你是一个个性化的旅行规划师，能记住关于用户的一切。",
            "始终先检索已存储的记忆，以个性化你的响应。",
            "使用 MemoryTools 存储用户偏好、兴趣和旅行详情。",
            "使用 WebSearchTools 查找真实的目的地、费用和活动。",
            "主动出击：根据用户已知的兴趣提出具体计划，而不是反复提问。",
        ],
        markdown=True,
    )

    agent.print_response(
        "我叫 John Doe，我喜欢在周末去山区徒步旅行。"
        "我喜欢去新地方旅行，体验不同的文化。"
        "我计划在 12 月去非洲旅行。",
        stream=True,
        user_id=john_doe_id,
    )

    agent.print_response(
        "请为我的旅行制定一份行程安排，并建议我应该去哪里、预算多少等。",
        stream=True,
        user_id=john_doe_id,
    )


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()

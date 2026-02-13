"""
搜索 Session 历史记录
======================

演示搜索先前 session，并具有用户范围的历史记录访问权限。
"""

import asyncio
import os

from agno.db.sqlite import AsyncSqliteDb
from agno.models.openai import OpenAIChat
from agno.team import Team

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
if os.path.exists("tmp/data.db"):
    os.remove("tmp/data.db")

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
team = Team(
    model=OpenAIChat(id="gpt-5.2"),
    members=[],
    db=AsyncSqliteDb(db_file="tmp/data.db"),
    search_session_history=True,
    num_history_sessions=2,
)


# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
async def main() -> None:
    print("=== 用户 1 Sessions ===")
    await team.aprint_response(
        "What is the capital of South Africa?",
        session_id="user1_session_1",
        user_id="user_1",
    )
    await team.aprint_response(
        "What is the capital of China?",
        session_id="user1_session_2",
        user_id="user_1",
    )
    await team.aprint_response(
        "What is the capital of France?",
        session_id="user1_session_3",
        user_id="user_1",
    )

    print("\n=== 用户 2 Sessions ===")
    await team.aprint_response(
        "What is the population of India?",
        session_id="user2_session_1",
        user_id="user_2",
    )
    await team.aprint_response(
        "What is the currency of Japan?",
        session_id="user2_session_2",
        user_id="user_2",
    )

    print("\n=== 测试 Session 历史记录搜索 ===")
    print(
        "用户 1 询问先前的对话（应该只看到首都相关内容，看不到人口/货币）："
    )
    await team.aprint_response(
        "What did I discuss in my previous conversations?",
        session_id="user1_session_4",
        user_id="user_1",
    )

    print(
        "\n用户 2 询问先前的对话（应该只看到人口/货币，看不到首都）："
    )
    await team.aprint_response(
        "What did I discuss in my previous conversations?",
        session_id="user2_session_3",
        user_id="user_2",
    )


if __name__ == "__main__":
    asyncio.run(main())

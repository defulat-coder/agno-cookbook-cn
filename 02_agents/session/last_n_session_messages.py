"""
最近 N 条 Session 消息
=============================

最近 N 条 Session 消息示例。
"""

import asyncio
import os

from agno.agent import Agent
from agno.db.sqlite import AsyncSqliteDb
from agno.models.openai import OpenAIChat

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
# 在运行脚本之前删除临时数据库文件
if os.path.exists("tmp/data.db"):
    os.remove("tmp/data.db")

# 为不同的用户创建 Agent 以演示用户特定的 session 历史
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    db=AsyncSqliteDb(db_file="tmp/data.db"),
    search_session_history=True,  # 允许搜索以前的 session
    num_history_sessions=2,  # 仅在搜索中包含最近 2 个 session 以避免上下文长度问题
)


async def main():
    # 用户 1 的 session
    print("=== 用户 1 的 Session ===")
    await agent.aprint_response(
        "What is the capital of South Africa?",
        session_id="user1_session_1",
        user_id="user_1",
    )
    await agent.aprint_response(
        "What is the capital of China?", session_id="user1_session_2", user_id="user_1"
    )
    await agent.aprint_response(
        "What is the capital of France?", session_id="user1_session_3", user_id="user_1"
    )

    # 用户 2 的 session
    print("\n=== 用户 2 的 Session ===")
    await agent.aprint_response(
        "What is the population of India?",
        session_id="user2_session_1",
        user_id="user_2",
    )
    await agent.aprint_response(
        "What is the currency of Japan?", session_id="user2_session_2", user_id="user_2"
    )

    # 现在测试 session 历史搜索 - 每个用户应该只看到他们自己的 session
    print("\n=== 测试 Session 历史搜索 ===")
    print(
        "用户 1 询问之前的对话（应该只看到首都，而不是人口/货币）:"
    )
    await agent.aprint_response(
        "What did I discuss in my previous conversations?",
        session_id="user1_session_4",
        user_id="user_1",
    )

    print(
        "\n用户 2 询问之前的对话（应该只看到人口/货币，而不是首都）:"
    )
    await agent.aprint_response(
        "What did I discuss in my previous conversations?",
        session_id="user2_session_3",
        user_id="user_2",
    )


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())

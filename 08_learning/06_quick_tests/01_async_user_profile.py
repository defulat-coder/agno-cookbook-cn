"""
异步用户画像测试
=======================
测试用户画像学习的异步路径。

所有其他示例使用同步（print_response）。此测试验证
异步路径（aprint_response）正常工作。

这很关键因为：
- 后台学习在异步模式下使用 asyncio 任务
- aprocess vs process 有不同的代码路径
- 异步上下文中可能存在竞态条件
"""

import asyncio

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.learn import LearningMachine, LearningMode, UserProfileConfig
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------

db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    learning=LearningMachine(
        user_profile=UserProfileConfig(
            mode=LearningMode.ALWAYS,
        ),
    ),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行异步演示
# ---------------------------------------------------------------------------


async def main():
    user_id = "async_test@example.com"

    # Session 1: 分享信息（异步）
    print("\n" + "=" * 60)
    print("SESSION 1: 异步 - 分享信息")
    print("=" * 60 + "\n")

    await agent.aprint_response(
        "Hi! I'm Diana Prince, but call me Di.",
        user_id=user_id,
        session_id="async_session_1",
        stream=True,
    )
    agent.learning_machine.user_profile_store.print(user_id=user_id)

    # Session 2: 新 Session - 验证画像已持久化（异步）
    print("\n" + "=" * 60)
    print("SESSION 2: 异步 - 画像召回")
    print("=" * 60 + "\n")

    await agent.aprint_response(
        "What's my name?",
        user_id=user_id,
        session_id="async_session_2",
        stream=True,
    )
    agent.learning_machine.user_profile_store.print(user_id=user_id)

    print("\n" + "=" * 60)
    print("异步测试完成")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

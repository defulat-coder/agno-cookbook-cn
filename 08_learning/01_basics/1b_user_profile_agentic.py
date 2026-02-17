"""
用户画像：Agentic 模式
==========================
用户画像捕获关于用户的结构化字段：
- 姓名和偏好称呼
- 自定义画像字段（使用扩展 schema 时）

AGENTIC 模式为 Agent 提供显式工具来更新画像字段。
Agent 决定何时存储信息 - 你可以看到工具调用。

对比：1a_user_profile_always.py 使用自动提取。
另见：2b_user_memory_agentic.py 了解非结构化观察。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.learn import LearningMachine, LearningMode, UserProfileConfig
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------

db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

# AGENTIC 模式：Agent 获得画像工具并决定何时使用。
# 你会在响应中看到类似 "update_user_profile" 的工具调用。
agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    learning=LearningMachine(
        user_profile=UserProfileConfig(
            mode=LearningMode.AGENTIC,
        ),
    ),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行演示
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    user_id = "bob@example.com"

    # Session 1: Agent 显式更新画像
    print("\n" + "=" * 60)
    print("SESSION 1: 分享信息（观察工具调用）")
    print("=" * 60 + "\n")

    agent.print_response(
        "Hi! I'm Robert Johnson, but everyone calls me Bob.",
        user_id=user_id,
        session_id="session_1",
        stream=True,
    )
    agent.learning_machine.user_profile_store.print(user_id=user_id)

    # Session 2: Agent 使用存储的画像
    print("\n" + "=" * 60)
    print("SESSION 2: 新 Session 中召回画像")
    print("=" * 60 + "\n")

    agent.print_response(
        "What should you call me?",
        user_id=user_id,
        session_id="session_2",
        stream=True,
    )
    agent.learning_machine.user_profile_store.print(user_id=user_id)

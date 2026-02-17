"""
用户画像：Always 模式
=========================
用户画像捕获关于用户的结构化字段：
- 姓名和偏好称呼
- 自定义画像字段（使用扩展 schema 时）

ALWAYS 模式在 Agent 响应时自动并行提取画像信息 - 无需显式工具调用。

对比：1b_user_profile_agentic.py 使用基于工具的显式更新。
另见：2a_user_memory_always.py 了解非结构化观察。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.learn import LearningMachine, LearningMode, UserProfileConfig
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------

db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

# ALWAYS 模式：每次响应后自动提取。
# Agent 不会看到或调用任何画像工具 - 这是不可见的。
# UserProfile 存储结构化字段（name、preferred_name、自定义字段）
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
# 运行演示
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    user_id = "alice@example.com"

    # Session 1: 自然分享信息
    print("\n" + "=" * 60)
    print("SESSION 1: 分享信息（自动提取）")
    print("=" * 60 + "\n")

    agent.print_response(
        "Hi! I'm Alice Chen, but please call me Ali.",
        user_id=user_id,
        session_id="session_1",
        stream=True,
    )
    agent.learning_machine.user_profile_store.print(user_id=user_id)

    # Session 2: 新 Session - 画像自动召回
    print("\n" + "=" * 60)
    print("SESSION 2: 新 Session 中召回画像")
    print("=" * 60 + "\n")

    agent.print_response(
        "What's my name again?",
        user_id=user_id,
        session_id="session_2",
        stream=True,
    )
    agent.learning_machine.user_profile_store.print(user_id=user_id)

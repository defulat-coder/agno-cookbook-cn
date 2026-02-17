"""
用户画像：Agentic 模式（深入探讨）
======================================
通过显式工具进行 Agent 控制的画像更新。

AGENTIC 模式为 Agent 提供工具来更新画像字段。
你会在响应中看到工具调用 - 比 ALWAYS 模式更透明。

对比：01_always_extraction.py 使用自动提取。
另见：01_basics/1b_user_profile_agentic.py 了解基础知识。
"""

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
    instructions=(
        "You are a helpful assistant. "
        "When users share their name or preferences, use update_user_profile to save it."
    ),
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
    user_id = "jordan@example.com"

    # Session 1: 分享姓名 - 观察工具调用
    print("\n" + "=" * 60)
    print("SESSION 1: 分享姓名（观察工具调用）")
    print("=" * 60 + "\n")

    agent.print_response(
        "Hi! I'm Jordan Chen, but everyone calls me JC.",
        user_id=user_id,
        session_id="session_1",
        stream=True,
    )
    agent.learning_machine.user_profile_store.print(user_id=user_id)

    # Session 2: 新 Session 中召回
    print("\n" + "=" * 60)
    print("SESSION 2: 新 Session 中召回画像")
    print("=" * 60 + "\n")

    agent.print_response(
        "What's my name and what should you call me?",
        user_id=user_id,
        session_id="session_2",
        stream=True,
    )
    agent.learning_machine.user_profile_store.print(user_id=user_id)

    # Session 3: 更新偏好称呼
    print("\n" + "=" * 60)
    print("SESSION 3: 更新偏好称呼")
    print("=" * 60 + "\n")

    agent.print_response(
        "Actually, I'd prefer you call me Jordan from now on.",
        user_id=user_id,
        session_id="session_3",
        stream=True,
    )
    agent.learning_machine.user_profile_store.print(user_id=user_id)

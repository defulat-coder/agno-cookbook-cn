"""
用户画像：Always 提取（深入探讨）
============================================
从自然对话中自动提取画像。

ALWAYS 模式在每次响应后在后台提取画像信息。
用户看不到工具 - 提取不可见地发生。

本示例展示跨多个对话的渐进式画像构建。

对比：02_agentic_mode.py 使用基于工具的显式更新。
另见：01_basics/1a_user_profile_always.py 了解基础知识。
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
    learning=LearningMachine(
        user_profile=UserProfileConfig(
            mode=LearningMode.ALWAYS,
        ),
    ),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行：渐进式画像构建
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    user_id = "marcus@example.com"

    # Conversation 1: 基本介绍
    print("\n" + "=" * 60)
    print("CONVERSATION 1: 基本介绍")
    print("=" * 60 + "\n")

    agent.print_response(
        "Hi! I'm Marcus, nice to meet you.",
        user_id=user_id,
        session_id="conv_1",
        stream=True,
    )
    agent.learning_machine.user_profile_store.print(user_id=user_id)

    # Conversation 2: 分享工作背景
    print("\n" + "=" * 60)
    print("CONVERSATION 2: 工作背景")
    print("=" * 60 + "\n")

    agent.print_response(
        "I'm a senior engineer at Stripe, focusing on payment systems.",
        user_id=user_id,
        session_id="conv_2",
        stream=True,
    )
    agent.learning_machine.user_profile_store.print(user_id=user_id)

    # Conversation 3: 偏好设置
    print("\n" + "=" * 60)
    print("CONVERSATION 3: 偏好设置（隐式提取）")
    print("=" * 60 + "\n")

    agent.print_response(
        "I prefer code examples over long explanations. "
        "I'm very familiar with Python and Go.",
        user_id=user_id,
        session_id="conv_3",
        stream=True,
    )
    agent.learning_machine.user_profile_store.print(user_id=user_id)

    # Conversation 4: 昵称
    print("\n" + "=" * 60)
    print("CONVERSATION 4: 更新偏好称呼")
    print("=" * 60 + "\n")

    agent.print_response(
        "By the way, most people call me Marc.",
        user_id=user_id,
        session_id="conv_4",
        stream=True,
    )
    agent.learning_machine.user_profile_store.print(user_id=user_id)

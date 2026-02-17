"""
模式：带学习的个人助手
=========================================
一个随时间了解用户的个人助手。

此模式结合：
- 用户画像：偏好、日常、沟通风格
- Session Context：当前对话状态
- 实体记忆：联系人、项目、地点、事件

助手变得越来越个性化，无需询问。

另见：01_basics/ 了解各个存储示例。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.learn import (
    EntityMemoryConfig,
    LearningMachine,
    LearningMode,
    SessionContextConfig,
    UserProfileConfig,
)
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------

db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")


def create_personal_assistant(user_id: str, session_id: str) -> Agent:
    """为特定用户创建个人助手。"""
    return Agent(
        model=OpenAIResponses(id="gpt-5.2"),
        db=db,
        instructions=(
            "You are a helpful personal assistant. "
            "Remember user preferences without being asked. "
            "Keep track of important people and events in their life."
        ),
        learning=LearningMachine(
            user_profile=UserProfileConfig(
                mode=LearningMode.ALWAYS,
            ),
            session_context=SessionContextConfig(
                enable_planning=True,
            ),
            entity_memory=EntityMemoryConfig(
                mode=LearningMode.ALWAYS,
                namespace=f"user:{user_id}:personal",
            ),
        ),
        user_id=user_id,
        session_id=session_id,
        markdown=True,
    )


# ---------------------------------------------------------------------------
# 运行演示
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from rich.pretty import pprint

    user_id = "alex@example.com"

    # Conversation 1: 介绍
    print("\n" + "=" * 60)
    print("CONVERSATION 1: 介绍")
    print("=" * 60 + "\n")

    agent = create_personal_assistant(user_id, "conv_1")
    agent.print_response(
        "Hi! I'm Alex Chen. I work as a product manager at Stripe. "
        "I prefer concise responses. My sister Sarah is visiting next month.",
        stream=True,
    )
    agent.learning_machine.user_profile_store.print(user_id=user_id)
    print("\n--- 实体 ---")
    pprint(agent.learning_machine.entity_memory_store.search(query="sarah", limit=10))

    # Conversation 2: 新 Session（演示记忆）
    print("\n" + "=" * 60)
    print("CONVERSATION 2: 新 Session（记忆测试）")
    print("=" * 60 + "\n")

    agent = create_personal_assistant(user_id, "conv_2")
    agent.print_response(
        "What do you remember about me and my sister?",
        stream=True,
    )

    # Conversation 3: 计划某事
    print("\n" + "=" * 60)
    print("CONVERSATION 3: 计划活动")
    print("=" * 60 + "\n")

    agent = create_personal_assistant(user_id, "conv_3")
    agent.print_response(
        "Help me plan activities for Sarah's visit. She likes hiking.",
        stream=True,
    )
    agent.learning_machine.session_context_store.print(session_id="conv_3")

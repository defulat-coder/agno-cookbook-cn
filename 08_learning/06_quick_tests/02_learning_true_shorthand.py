"""
Learning=True 简写测试
============================
测试启用学习的最简单方法：`learning=True`。

这是最常见的用户模式，必须完美工作。

当 learning=True 时：
- 创建默认的 LearningMachine
- 使用 ALWAYS 模式启用 UserProfile（结构化字段）
- 使用 ALWAYS 模式启用 UserMemory（非结构化观察）
- 从 Agent 注入 db 和 model

此测试验证简写与显式配置工作方式相同。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 创建 Agent - 使用最简单的配置
# ---------------------------------------------------------------------------

db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

# 这是启用学习的最简单方法 - 只需设置 learning=True
agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    learning=True,  # <-- 我们正在测试的简写
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行演示
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    user_id = "shorthand_test@example.com"

    # 注意：LearningMachine 是懒初始化的 - 仅在 Agent 运行时设置
    print("\n" + "=" * 60)
    print("SESSION 1: 分享信息（learning=True 简写）")
    print("=" * 60 + "\n")

    agent.print_response(
        "Hi! I'm Charlie Brown. Friends call me Chuck.",
        user_id=user_id,
        session_id="shorthand_session_1",
        stream=True,
    )

    # 验证 LearningMachine 已创建（首次运行后）
    print("\n" + "=" * 60)
    print("验证：从 learning=True 创建的 LearningMachine")
    print("=" * 60 + "\n")

    lm = agent.learning_machine
    print(f"LearningMachine 存在: {lm is not None}")
    print(
        f"UserProfileStore 存在: {lm.user_profile_store is not None if lm else False}"
    )
    print(
        f"UserMemoryStore 存在: {lm.user_memory_store is not None if lm else False}"
    )
    print(f"DB 已注入: {lm.db is not None if lm else False}")
    print(f"Model 已注入: {lm.model is not None if lm else False}")

    if not lm:
        print("\n失败：LearningMachine 未创建！")
        exit(1)

    if not lm.user_profile_store:
        print("\n失败：UserProfileStore 未创建！")
        exit(1)

    if not lm.user_memory_store:
        print("\n失败：UserMemoryStore 未创建！")
        exit(1)

    print("\n--- 用户画像 ---")
    lm.user_profile_store.print(user_id=user_id)

    print("\n--- 用户记忆 ---")
    lm.user_memory_store.print(user_id=user_id)

    # Session 2: 验证画像已持久化
    print("\n" + "=" * 60)
    print("SESSION 2: 画像召回")
    print("=" * 60 + "\n")

    agent.print_response(
        "What do my friends call me?",
        user_id=user_id,
        session_id="shorthand_session_2",
        stream=True,
    )

    print("\n--- 用户画像 ---")
    lm.user_profile_store.print(user_id=user_id)

    print("\n--- 用户记忆 ---")
    lm.user_memory_store.print(user_id=user_id)

    print("\n" + "=" * 60)
    print("简写测试完成")
    print("=" * 60)

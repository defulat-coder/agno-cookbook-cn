"""
无数据库优雅处理测试
============================
测试学习优雅地处理缺失的数据库。

用户可能不小心在没有提供数据库的情况下启用学习。
系统应该：
1. 不崩溃
2. 记录警告（理想情况下）
3. 仍然响应用户
4. 只是跳过学习/持久化部分

这对用户体验至关重要 - 缺失的数据库应该优雅降级，
而不是爆炸。
"""

from agno.agent import Agent
from agno.learn import LearningMachine, LearningMode, UserProfileConfig
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 创建 Agent - 故意没有数据库
# ---------------------------------------------------------------------------

# 注意：没有 db 参数 - 这是我们正在测试的边缘情况
agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
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
    user_id = "no_db_test@example.com"

    print("\n" + "=" * 60)
    print("测试：在没有数据库的情况下启用学习")
    print("=" * 60 + "\n")

    # 检查 LearningMachine 存在但没有数据库
    lm = agent.learning_machine
    print(f"LearningMachine 存在: {lm is not None}")
    if lm:
        print(f"DB 为 None: {lm.db is None}")
        print(f"UserProfileStore 存在: {lm.user_profile_store is not None}")

    # 这不应该崩溃 - 它应该正常响应
    print("\n" + "=" * 60)
    print("SESSION 1: 应该在不崩溃的情况下响应")
    print("=" * 60 + "\n")

    try:
        agent.print_response(
            "Hi! I'm Eve. Nice to meet you.",
            user_id=user_id,
            session_id="no_db_session_1",
            stream=True,
        )
        print("\n[正常] Agent 在不崩溃的情况下响应了")
    except Exception as e:
        print(f"\n[失败] Agent 崩溃了: {e}")
        exit(1)

    # 尝试打印画像 - 应该优雅地处理
    print("\n" + "=" * 60)
    print("画像检查：应该显示为空（没有数据库来持久化）")
    print("=" * 60 + "\n")

    if lm and lm.user_profile_store:
        lm.user_profile_store.print(user_id=user_id)

    # 第二条消息 - 也不应该崩溃
    print("\n" + "=" * 60)
    print("SESSION 2: 第二条消息也应该工作")
    print("=" * 60 + "\n")

    try:
        agent.print_response(
            "What's my name?",
            user_id=user_id,
            session_id="no_db_session_2",
            stream=True,
        )
        print("\n[正常] 第二条消息工作了")
    except Exception as e:
        print(f"\n[失败] 第二条消息崩溃了: {e}")
        exit(1)

    print("\n" + "=" * 60)
    print("无数据库优雅测试完成")
    print("预期：Agent 工作，但画像未持久化")
    print("=" * 60)

"""
Claude 模型测试
=================
使用 Claude 而不是 OpenAI 测试学习。

所有其他示例使用 OpenAI（gpt-5.2）。此测试验证
学习与 Claude 模型配合工作，确保实现是模型无关的。

需要验证的关键内容：
1. 画像提取与 Claude 配合工作
2. 工具调用正确工作（Claude 使用不同的工具格式）
3. 后台提取成功完成
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.learn import LearningMachine, LearningMode, UserProfileConfig
from agno.models.anthropic import Claude

# ---------------------------------------------------------------------------
# 创建 Agent - 使用 Claude 而不是 OpenAI
# ---------------------------------------------------------------------------

db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

agent = Agent(
    model=Claude(id="claude-sonnet-4-5"),  # 使用 Claude
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
    user_id = "claude_test@example.com"

    print("\n" + "=" * 60)
    print("测试：使用 Claude 模型学习")
    print("=" * 60 + "\n")

    print(f"模型类型: {type(agent.model).__name__}")

    # Session 1: 分享信息
    print("\n" + "=" * 60)
    print("SESSION 1: 分享信息（Claude 提取）")
    print("=" * 60 + "\n")

    agent.print_response(
        "Hi! I'm Bruce Wayne, but my friends call me Batman.",
        user_id=user_id,
        session_id="claude_session_1",
        stream=True,
    )

    # 检查 LearningMachine 是否已初始化
    lm = agent.learning_machine
    print(f"\nLearningMachine 存在: {lm is not None}")

    if lm and lm.user_profile_store:
        lm.user_profile_store.print(user_id=user_id)
    else:
        print("\n[警告] UserProfileStore 不可用 - 提取可能失败了")
        print(
            "注意：某些 Claude 模型可能不支持提取所需的结构化输出"
        )

    # Session 2: 验证画像已持久化
    print("\n" + "=" * 60)
    print("SESSION 2: 画像召回（Claude）")
    print("=" * 60 + "\n")

    agent.print_response(
        "What's my secret identity?",
        user_id=user_id,
        session_id="claude_session_2",
        stream=True,
    )

    if lm and lm.user_profile_store:
        lm.user_profile_store.print(user_id=user_id)

    print("\n" + "=" * 60)
    print("Claude 模型测试完成")
    print("=" * 60)

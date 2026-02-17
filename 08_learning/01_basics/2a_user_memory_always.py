"""
用户记忆：Always 模式
========================
用户记忆捕获关于用户的非结构化观察：
- 工作背景和角色
- 沟通风格偏好
- 模式和兴趣
- 任何值得记住的事实

ALWAYS 模式在 Agent 响应时自动并行提取记忆 - 无需显式工具调用。

对比：2b_user_memory_agentic.py 使用基于工具的显式更新。
另见：1a_user_profile_always.py 了解结构化画像字段。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.learn import LearningMachine, LearningMode, UserMemoryConfig
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------

db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

# ALWAYS 模式：每次响应后自动提取。
# Agent 不会看到或调用任何记忆工具 - 这是不可见的。
# Memories 存储不适合画像字段的非结构化观察。
agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    learning=LearningMachine(
        user_memory=UserMemoryConfig(
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
        "Hi! I work at Anthropic as a research scientist. "
        "I prefer concise responses without too much explanation. "
        "I'm currently working on a paper about transformer architectures.",
        user_id=user_id,
        session_id="session_1",
        stream=True,
    )
    agent.learning_machine.user_memory_store.print(user_id=user_id)

    # Session 2: 新 Session - 记忆自动召回
    print("\n" + "=" * 60)
    print("SESSION 2: 新 Session 中召回记忆")
    print("=" * 60 + "\n")

    agent.print_response(
        "What's a good Python library for async HTTP requests?",
        user_id=user_id,
        session_id="session_2",
        stream=True,
    )
    agent.learning_machine.user_memory_store.print(user_id=user_id)

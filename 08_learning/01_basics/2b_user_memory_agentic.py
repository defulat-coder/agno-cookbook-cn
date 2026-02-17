"""
用户记忆：Agentic 模式
=========================
用户记忆捕获关于用户的非结构化观察：
- 工作背景和角色
- 沟通风格偏好
- 模式和兴趣
- 任何值得记住的事实

AGENTIC 模式为 Agent 提供显式工具来保存和更新记忆。
Agent 决定何时存储信息 - 你可以看到工具调用。

对比：2a_user_memory_always.py 使用自动提取。
另见：1b_user_profile_agentic.py 了解结构化画像字段。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.learn import LearningMachine, LearningMode, UserMemoryConfig
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------

db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

# AGENTIC 模式：Agent 获得记忆工具并决定何时使用。
# 你会在响应中看到类似 "update_user_memory" 的工具调用。
agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    learning=LearningMachine(
        user_memory=UserMemoryConfig(
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

    # Session 1: Agent 显式保存记忆
    print("\n" + "=" * 60)
    print("SESSION 1: 分享信息（观察工具调用）")
    print("=" * 60 + "\n")

    agent.print_response(
        "I'm a backend engineer at Stripe. "
        "I specialize in distributed systems and prefer Rust over Go.",
        user_id=user_id,
        session_id="session_1",
        stream=True,
    )
    agent.learning_machine.user_memory_store.print(user_id=user_id)

    # Session 2: Agent 使用存储的记忆
    print("\n" + "=" * 60)
    print("SESSION 2: 新 Session 中召回记忆")
    print("=" * 60 + "\n")

    agent.print_response(
        "What programming language would you recommend for my next project?",
        user_id=user_id,
        session_id="session_2",
        stream=True,
    )
    agent.learning_machine.user_memory_store.print(user_id=user_id)

"""
学习机器：Agentic 模式
===============================
在 AGENTIC 模式下，Agent 接收工具来显式管理学习。
它根据对话上下文决定何时保存用户画像和记忆。

与 learning=True（ALWAYS 模式）对比，后者自动提取。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.learn import (
    LearningMachine,
    LearningMode,
    UserMemoryConfig,
    UserProfileConfig,
)
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
db = SqliteDb(db_file="tmp/agents.db")

agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    learning=LearningMachine(
        user_profile=UserProfileConfig(mode=LearningMode.AGENTIC),
        user_memory=UserMemoryConfig(mode=LearningMode.AGENTIC),
    ),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行演示
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    user_id = "alice2@example.com"

    # Session 1: Agent 通过工具调用决定保存什么
    print("\n--- Session 1: Agent 使用工具保存画像和记忆 ---\n")
    agent.print_response(
        "Hi! I'm Alice. I work at Anthropic as a research scientist. "
        "I prefer concise responses without too much explanation.",
        user_id=user_id,
        session_id="session_1",
        stream=True,
    )
    lm = agent.learning_machine
    lm.user_profile_store.print(user_id=user_id)
    lm.user_memory_store.print(user_id=user_id)

    # Session 2: 新 Session - Agent 记住了
    print("\n--- Session 2: Agent 跨 Session 记忆 ---\n")
    agent.print_response(
        "What do you know about me?",
        user_id=user_id,
        session_id="session_2",
        stream=True,
    )

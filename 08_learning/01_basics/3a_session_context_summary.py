"""
Session Context：摘要模式
=============================
Session Context 跟踪当前对话的状态：
- 已讨论的内容
- 做出的关键决策
- 重要上下文

摘要模式提供轻量级跟踪 - 运行摘要，无目标/计划结构。

对比：3b_session_context_planning.py 了解面向目标的跟踪。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.learn import LearningMachine
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------

db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

# 摘要模式：仅跟踪已讨论的内容，无计划开销。
# 适合需要连续性但无结构的通用对话。
agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    instructions="Be very concise. Give brief answers in 1-2 sentences.",
    learning=LearningMachine(session_context=True),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行演示
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    user_id = "session@example.com"
    session_id = "api_design"

    # Turn 1: 开始讨论
    print("\n" + "=" * 60)
    print("TURN 1: 开始讨论")
    print("=" * 60 + "\n")

    agent.print_response(
        "I'm designing a REST API for a todo app. PUT or PATCH for updates?",
        user_id=user_id,
        session_id=session_id,
        stream=True,
    )
    agent.learning_machine.session_context_store.print(session_id=session_id)

    # Turn 2: 后续问题
    print("\n" + "=" * 60)
    print("TURN 2: 后续问题")
    print("=" * 60 + "\n")

    agent.print_response(
        "What URL structure for that endpoint?",
        user_id=user_id,
        session_id=session_id,
        stream=True,
    )
    agent.learning_machine.session_context_store.print(session_id=session_id)

    # Turn 3: 测试召回
    print("\n" + "=" * 60)
    print("TURN 3: 测试上下文召回")
    print("=" * 60 + "\n")

    agent.print_response(
        "What did we decide?",
        user_id=user_id,
        session_id=session_id,
        stream=True,
    )
    agent.learning_machine.session_context_store.print(session_id=session_id)

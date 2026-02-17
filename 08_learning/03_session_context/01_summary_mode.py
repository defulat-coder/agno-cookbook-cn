"""
Session Context：摘要模式（深入探讨）
=========================================
对话状态的运行摘要。

摘要模式维护对话的运行摘要，在重新连接时持续存在。
每轮，摘要更新以包含新信息。

对比：02_planning_mode.py 了解目标/计划跟踪。
另见：01_basics/3a_session_context_summary.py 了解基础知识。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.learn import LearningMachine, SessionContextConfig
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------

db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    learning=LearningMachine(
        session_context=SessionContextConfig(
            enable_planning=False,  # 仅摘要
        ),
    ),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行：多轮摘要
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    user_id = "debug@example.com"
    session_id = "debug_session"

    # Turn 1: 初始问题
    print("\n" + "=" * 60)
    print("TURN 1: 初始问题")
    print("=" * 60 + "\n")

    agent.print_response(
        "I'm debugging a memory leak in my Python FastAPI server. "
        "It processes large JSON payloads.",
        user_id=user_id,
        session_id=session_id,
        stream=True,
    )
    agent.learning_machine.session_context_store.print(session_id=session_id)

    # Turn 2: 更多上下文
    print("\n" + "=" * 60)
    print("TURN 2: 更多上下文")
    print("=" * 60 + "\n")

    agent.print_response(
        "The memory grows even when there's no traffic. "
        "I've checked for unclosed file handles already.",
        user_id=user_id,
        session_id=session_id,
        stream=True,
    )
    agent.learning_machine.session_context_store.print(session_id=session_id)

    # Turn 3: 后续问题
    print("\n" + "=" * 60)
    print("TURN 3: 后续问题")
    print("=" * 60 + "\n")

    agent.print_response(
        "Could it be related to Pydantic model caching?",
        user_id=user_id,
        session_id=session_id,
        stream=True,
    )
    agent.learning_machine.session_context_store.print(session_id=session_id)

    # 模拟重连
    print("\n" + "=" * 60)
    print("TURN 4: '重连'后召回")
    print("=" * 60 + "\n")

    agent.print_response(
        "What were we debugging?",
        user_id=user_id,
        session_id=session_id,
        stream=True,
    )

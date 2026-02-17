"""
实体记忆：事实和事件（深入探讨）
============================================
实体的语义（事实）记忆 vs 情景（事件）记忆。

实体记忆存储关于外部实体的知识：
- 事实：无时间限制的真理（"Acme 使用 PostgreSQL"）
- 事件：有时间限制的发生（"Acme 在 1 月 15 日筹集了 3000 万美元"）

AGENTIC 模式为 Agent 提供创建/更新实体的工具。

对比：04_always_extraction.py 使用自动提取。
另见：01_basics/5a_entity_memory_always.py 了解基础知识。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.learn import EntityMemoryConfig, LearningMachine, LearningMode
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------

db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    instructions=(
        "Track information about companies and people. "
        "Distinguish between facts (timeless) and events (time-bound)."
    ),
    learning=LearningMachine(
        entity_memory=EntityMemoryConfig(
            mode=LearningMode.AGENTIC,
            namespace="global",
        ),
    ),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行演示
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from rich.pretty import pprint

    user_id = "research@example.com"
    session_id = "company_research"

    # 分享事实和事件
    print("\n" + "=" * 60)
    print("MESSAGE 1: 分享混合的事实和事件")
    print("=" * 60 + "\n")

    agent.print_response(
        "Notes from my meeting with DataPipe: "
        "They're based in San Francisco. "
        "They build real-time ETL infrastructure in Rust. "
        "Their CTO is Marcus Chen. "
        "They just hit 1000 customers last month. "
        "Series B closed at $80M two weeks ago.",
        user_id=user_id,
        session_id=session_id,
        stream=True,
    )
    print("\n--- 实体 ---")
    pprint(
        agent.learning_machine.entity_memory_store.search(query="datapipe", limit=10)
    )

    # 查询实体
    print("\n" + "=" * 60)
    print("MESSAGE 2: 查询实体")
    print("=" * 60 + "\n")

    agent.print_response(
        "What do we know about DataPipe?",
        user_id=user_id,
        session_id="session_2",
        stream=True,
    )

    # 添加更多事件
    print("\n" + "=" * 60)
    print("MESSAGE 3: 添加更多事件")
    print("=" * 60 + "\n")

    agent.print_response(
        "Update on DataPipe: They announced a partnership with BigCloud yesterday. "
        "They're also opening a London office next quarter.",
        user_id=user_id,
        session_id="session_3",
        stream=True,
    )
    print("\n--- 更新的实体 ---")
    pprint(
        agent.learning_machine.entity_memory_store.search(query="datapipe", limit=10)
    )

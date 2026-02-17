"""
实体记忆：Always 模式
==========================
实体记忆存储关于外部事物的知识：
- 公司、人员、项目
- 事实、事件、关系
- 跨用户的共享上下文

ALWAYS 模式自动从对话中提取实体信息。
无显式工具调用 - 实体在幕后发现和保存。

对比：5b_entity_memory_agentic.py 使用基于工具的显式管理。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.learn import EntityMemoryConfig, LearningMachine, LearningMode
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------

db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

# ALWAYS 模式：实体在响应后自动提取。
# Agent 不会看到记忆工具 - 提取不可见地发生。
agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    instructions="You're a sales assistant. Acknowledge notes briefly.",
    learning=LearningMachine(
        entity_memory=EntityMemoryConfig(
            mode=LearningMode.ALWAYS,
        ),
    ),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行演示
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from rich.pretty import pprint

    user_id = "sales@example.com"

    # Session 1: 自然提及实体
    print("\n" + "=" * 60)
    print("SESSION 1: 讨论实体（自动提取）")
    print("=" * 60 + "\n")

    agent.print_response(
        "Just met with Acme Corp. They're a fintech startup in SF, "
        "50 employees. CTO is Jane Smith. They use Python and Postgres.",
        user_id=user_id,
        session_id="session_1",
        stream=True,
    )

    print("\n--- 提取的实体 ---")
    entities = agent.learning_machine.entity_memory_store.search(query="acme", limit=10)
    pprint(entities)

    # Session 2: 添加关于同一实体的更多信息
    print("\n" + "=" * 60)
    print("SESSION 2: 更新同一实体")
    print("=" * 60 + "\n")

    agent.print_response(
        "Update on Acme Corp: they just raised $50M Series B from Sequoia. "
        "Jane Smith mentioned they're hiring 20 engineers.",
        user_id=user_id,
        session_id="session_2",
        stream=True,
    )

    print("\n--- 更新的实体 ---")
    entities = agent.learning_machine.entity_memory_store.search(query="acme", limit=10)
    pprint(entities)

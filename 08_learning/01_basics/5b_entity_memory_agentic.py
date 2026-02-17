"""
实体记忆：Agentic 模式
===========================
实体记忆存储关于外部事物的知识：
- 公司、人员、项目
- 事实、事件、关系
- 跨用户的共享上下文

AGENTIC 模式为 Agent 提供显式工具来管理实体：
- search_entities, create_entity
- add_fact, add_event, add_relationship

Agent 决定何时存储和检索信息。

对比：5a_entity_memory_always.py 使用自动提取。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.learn import EntityMemoryConfig, LearningMachine, LearningMode
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------

db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

# AGENTIC 模式：Agent 获得实体工具并决定何时使用。
# 你会在响应中看到类似 "create_entity"、"add_fact" 的工具调用。
agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    instructions=(
        "You're a sales assistant tracking companies and contacts. "
        "Be concise. Always search for existing entities before creating new ones."
    ),
    learning=LearningMachine(
        entity_memory=EntityMemoryConfig(
            mode=LearningMode.AGENTIC,
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

    # Session 1: 创建实体
    print("\n" + "=" * 60)
    print("SESSION 1: 创建实体（观察工具调用）")
    print("=" * 60 + "\n")

    agent.print_response(
        "Track Acme Corp - fintech startup in SF, 50 employees, "
        "uses Python and Postgres. CTO is Jane Smith.",
        user_id=user_id,
        session_id="session_1",
        stream=True,
    )

    print("\n--- 创建的实体 ---")
    entities = agent.learning_machine.entity_memory_store.search(query="acme", limit=10)
    pprint(entities)

    # Session 2: 更新同一实体
    print("\n" + "=" * 60)
    print("SESSION 2: 更新现有实体")
    print("=" * 60 + "\n")

    agent.print_response(
        "Acme Corp just raised $50M Series B from Sequoia.",
        user_id=user_id,
        session_id="session_2",
        stream=True,
    )

    print("\n--- 更新的实体 ---")
    entities = agent.learning_machine.entity_memory_store.search(query="acme", limit=10)
    pprint(entities)

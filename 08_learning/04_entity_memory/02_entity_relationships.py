"""
实体记忆：关系（深入探讨）
========================================
实体之间的图边。

关系连接实体以形成知识图谱：
- "Bob 是 Acme 的 CTO"
- "Acme 收购了 StartupX"
- "API Gateway 依赖 Auth Service"

AGENTIC 模式让 Agent 创建实体并添加关系。

对比：01_facts_and_events.py 了解事实/事件。
另见：01_basics/5b_entity_memory_agentic.py 了解基础知识。
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
        "Build a knowledge graph of entities and their relationships. "
        "Use appropriate relation types: works_at, reports_to, acquired, depends_on, etc."
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

    user_id = "org@example.com"
    session_id = "org_session"

    # 定义组织结构
    print("\n" + "=" * 60)
    print("MESSAGE 1: 定义组织结构")
    print("=" * 60 + "\n")

    agent.print_response(
        "TechCorp's leadership: "
        "Sarah Chen is the CEO and founder. "
        "Bob Martinez is the CTO, reporting to Sarah. "
        "Alice Kim leads Engineering under Bob. "
        "DevOps and Backend teams report to Alice.",
        user_id=user_id,
        session_id=session_id,
        stream=True,
    )
    print("\n--- 实体 ---")
    pprint(
        agent.learning_machine.entity_memory_store.search(query="techcorp", limit=10)
    )

    # 查询关系
    print("\n" + "=" * 60)
    print("MESSAGE 2: 查询关系")
    print("=" * 60 + "\n")

    agent.print_response(
        "Who reports to Bob Martinez?",
        user_id=user_id,
        session_id="session_2",
        stream=True,
    )

    # 添加更多关系
    print("\n" + "=" * 60)
    print("MESSAGE 3: 公司关系")
    print("=" * 60 + "\n")

    agent.print_response(
        "TechCorp just acquired StartupAI for $50M. "
        "They also partnered with CloudCo on infrastructure.",
        user_id=user_id,
        session_id="session_3",
        stream=True,
    )
    print("\n--- 更新的实体 ---")
    pprint(
        agent.learning_machine.entity_memory_store.search(query="techcorp", limit=10)
    )

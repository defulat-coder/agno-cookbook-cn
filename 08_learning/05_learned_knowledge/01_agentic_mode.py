"""
学习知识：Agentic 模式（深入探讨）
===========================================
Agent 决定何时保存和检索知识。

AGENTIC 模式为 Agent 提供工具：
- save_learning: 存储可复用的洞察
- search_learnings: 查找相关的先前知识

Agent 决定什么值得记住。

对比：02_propose_mode.py 了解人工审核的知识。
另见：01_basics/4_learned_knowledge.py 了解基础知识。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.knowledge import Knowledge
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.learn import LearnedKnowledgeConfig, LearningMachine, LearningMode
from agno.models.openai import OpenAIResponses
from agno.vectordb.pgvector import PgVector, SearchType

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
db = PostgresDb(db_url=db_url)

knowledge = Knowledge(
    vector_db=PgVector(
        db_url=db_url,
        table_name="agentic_learnings",
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    ),
)

agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    instructions=(
        "You learn from interactions. "
        "Use save_learning to store valuable, reusable insights. "
        "Use search_learnings to find and apply prior knowledge."
    ),
    learning=LearningMachine(
        knowledge=knowledge,
        learned_knowledge=LearnedKnowledgeConfig(
            mode=LearningMode.AGENTIC,
        ),
    ),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行演示
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    user_id = "learn@example.com"

    # 保存学习
    print("\n" + "=" * 60)
    print("MESSAGE 1: 保存学习")
    print("=" * 60 + "\n")

    agent.print_response(
        "Save this insight: When comparing cloud providers, always check "
        "egress costs first - they can vary by 10x between providers.",
        user_id=user_id,
        session_id="session_1",
        stream=True,
    )
    agent.learning_machine.learned_knowledge_store.print(query="cloud egress")

    # 保存另一个学习
    print("\n" + "=" * 60)
    print("MESSAGE 2: 保存另一个学习")
    print("=" * 60 + "\n")

    agent.print_response(
        "Save this: For database migrations, always test rollback "
        "procedures in staging before running in production.",
        user_id=user_id,
        session_id="session_2",
        stream=True,
    )
    agent.learning_machine.learned_knowledge_store.print(query="database migration")

    # 应用知识
    print("\n" + "=" * 60)
    print("MESSAGE 3: 将知识应用于新问题")
    print("=" * 60 + "\n")

    agent.print_response(
        "I'm setting up a new project with PostgreSQL on AWS. "
        "What best practices should I follow?",
        user_id=user_id,
        session_id="session_3",
        stream=True,
    )

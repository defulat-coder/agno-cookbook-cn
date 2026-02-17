"""
学习知识：Agentic 模式
===============================
学习知识存储可跨用户应用的可复用洞察：
- 通过使用发现的最佳实践
- 领域特定模式
- 常见问题的解决方案

AGENTIC 模式为 Agent 提供显式工具：
- search_learnings: 查找相关的过去知识
- save_learning: 存储新洞察

Agent 决定何时保存和应用知识。
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

# 学习知识需要向量数据库用于语义搜索。
knowledge = Knowledge(
    vector_db=PgVector(
        db_url=db_url,
        table_name="learned_knowledge_demo",
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    ),
)

# AGENTIC 模式：Agent 获得保存/搜索工具并决定何时使用。
agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    instructions="Be concise. Search for relevant learnings before answering questions.",
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
    user_id = "learner@example.com"

    # Session 1: 保存学习
    print("\n" + "=" * 60)
    print("SESSION 1: 保存学习（观察工具调用）")
    print("=" * 60 + "\n")

    agent.print_response(
        "Save this: Always check cloud egress costs first - they vary 10x between providers.",
        user_id=user_id,
        session_id="session_1",
        stream=True,
    )
    agent.learning_machine.learned_knowledge_store.print(query="cloud")

    # Session 2: 应用学习（新用户，新 Session）
    print("\n" + "=" * 60)
    print("SESSION 2: 新用户问相关问题")
    print("=" * 60 + "\n")

    agent.print_response(
        "I'm picking a cloud provider for a 10TB daily data pipeline. Key considerations?",
        user_id="different_user@example.com",
        session_id="session_2",
        stream=True,
    )

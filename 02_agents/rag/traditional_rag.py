"""
传统 RAG
=============================

1. 运行：`./cookbook/run_pgvector.sh` 启动带有 pgvector 的 postgres 容器。
"""

from agno.agent import Agent
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.vectordb.pgvector import PgVector, SearchType

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge = Knowledge(
    # 使用 PgVector 作为向量数据库，将嵌入存储在 `ai.recipes` 表中
    vector_db=PgVector(
        table_name="recipes",
        db_url=db_url,
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    ),
)

knowledge.insert(url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf")

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    knowledge=knowledge,
    # 通过将 `knowledge` 中的上下文添加到用户提示来启用 RAG。
    add_knowledge_to_context=True,
    # 设置为 False，因为 Agents 默认为 `search_knowledge=True`
    search_knowledge=False,
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response(
        "How do I make chicken and galangal in coconut milk soup", stream=True
    )

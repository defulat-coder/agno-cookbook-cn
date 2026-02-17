"""
Cohere Embedder
===============

演示 Cohere 嵌入和知识插入，包括批量处理变体。
"""

import asyncio

from agno.knowledge.embedder.cohere import CohereEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector


# ---------------------------------------------------------------------------
# 创建知识库
# ---------------------------------------------------------------------------
def create_knowledge() -> Knowledge:
    # 标准模式
    embedder = CohereEmbedder(dimensions=1024)

    # 批量模式（取消注释以使用）
    # embedder = CohereEmbedder(
    #     dimensions=1024,
    #     enable_batch=True,
    #     batch_size=100,
    #     exponential_backoff=True,
    # )

    return Knowledge(
        vector_db=PgVector(
            db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
            table_name="cohere_embeddings",
            embedder=embedder,
        ),
        max_results=2,
    )


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
async def main() -> None:
    embeddings = CohereEmbedder().get_embedding(
        "The quick brown fox jumps over the lazy dog."
    )
    print(f"Embeddings: {embeddings[:5]}")
    print(f"Dimensions: {len(embeddings)}")

    knowledge = create_knowledge()
    await knowledge.ainsert(path="cookbook/07_knowledge/testing_resources/cv_1.pdf")


if __name__ == "__main__":
    asyncio.run(main())

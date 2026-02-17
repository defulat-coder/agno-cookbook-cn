"""
Jina Embedder
=============

演示 Jina 嵌入、使用元数据检索以及批量处理变体。
"""

import asyncio

from agno.knowledge.embedder.jina import JinaEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector


# ---------------------------------------------------------------------------
# 创建知识库
# ---------------------------------------------------------------------------
def create_knowledge() -> Knowledge:
    # 标准模式
    embedder = JinaEmbedder(
        late_chunking=True,
        timeout=30.0,
    )

    # 批量模式（取消注释以使用）
    # embedder = JinaEmbedder(
    #     late_chunking=True,
    #     timeout=30.0,
    #     enable_batch=True,
    # )

    return Knowledge(
        vector_db=PgVector(
            db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
            table_name="jina_embeddings",
            embedder=embedder,
        ),
        max_results=2,
    )


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
async def main() -> None:
    embeddings = JinaEmbedder().get_embedding(
        "The quick brown fox jumps over the lazy dog."
    )
    print(f"Embeddings: {embeddings[:5]}")
    print(f"Dimensions: {len(embeddings)}")

    custom_embedder = JinaEmbedder(
        dimensions=1024,
        late_chunking=True,
        timeout=30.0,
    )
    embedding, usage = custom_embedder.get_embedding_and_usage(
        "Advanced text processing with Jina embeddings and late chunking."
    )
    print(f"Embedding dimensions: {len(embedding)}")
    if usage:
        print(f"Usage info: {usage}")

    knowledge = create_knowledge()
    await knowledge.ainsert(path="cookbook/07_knowledge/testing_resources/cv_1.pdf")


if __name__ == "__main__":
    asyncio.run(main())

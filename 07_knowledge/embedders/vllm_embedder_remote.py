"""
vLLM 远程 Embedder
==================

演示远程 vLLM 嵌入和知识插入，支持可选的批量处理。
"""

import asyncio

from agno.db.json import JsonDb
from agno.knowledge.embedder.vllm import VLLMEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector


# ---------------------------------------------------------------------------
# 创建知识库
# ---------------------------------------------------------------------------
def create_embedder(enable_batch: bool = False) -> VLLMEmbedder:
    return VLLMEmbedder(
        id="sentence-transformers/all-MiniLM-L6-v2",
        dimensions=384,
        base_url="http://localhost:8000/v1",
        api_key="your-api-key",
        enable_batch=enable_batch,
        batch_size=100,
    )


def create_knowledge(
    embedder: VLLMEmbedder, table_name: str, knowledge_table: str
) -> Knowledge:
    return Knowledge(
        vector_db=PgVector(
            db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
            table_name=table_name,
            embedder=embedder,
        ),
        contents_db=JsonDb(
            db_path="./knowledge_contents",
            knowledge_table=knowledge_table,
        ),
        max_results=2,
    )


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
def run_search(knowledge: Knowledge) -> None:
    query = "候选人有什么技能？"
    results = knowledge.search(query=query)
    print(f"查询: {query}")
    print(f"找到结果: {len(results)}")
    for i, result in enumerate(results, 1):
        print(f"结果 {i}: {result.content[:100]}...")


async def run_variant(enable_batch: bool = False) -> None:
    embedder = create_embedder(enable_batch=enable_batch)
    mode = "批量" if enable_batch else "标准"

    try:
        embeddings = embedder.get_embedding(
            "The quick brown fox jumps over the lazy dog."
        )
        print(f"模式: {mode}")
        print(f"嵌入维度: {len(embeddings)}")
        print(f"前5个值: {embeddings[:5]}")
    except Exception as exc:
        print(f"连接远程服务器错误: {exc}")
        return

    table_name = (
        "vllm_embeddings_minilm_batch_remote"
        if enable_batch
        else "vllm_embeddings_minilm_remote"
    )
    knowledge_table = (
        "vllm_batch_remote_knowledge" if enable_batch else "vllm_remote_knowledge"
    )
    knowledge = create_knowledge(embedder, table_name, knowledge_table)

    try:
        await knowledge.ainsert(path="cookbook/07_knowledge/testing_resources/cv_1.pdf")
        print("文档已加载")
    except Exception as exc:
        print(f"加载文档错误: {exc}")
        return

    try:
        run_search(knowledge)
    except Exception as exc:
        print(f"搜索错误: {exc}")


if __name__ == "__main__":
    asyncio.run(run_variant(enable_batch=False))
    asyncio.run(run_variant(enable_batch=True))

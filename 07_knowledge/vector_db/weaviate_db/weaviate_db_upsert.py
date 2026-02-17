"""
Weaviate Upsert
===============

演示在 Weaviate 中使用 `skip_if_exists` 进行重复插入。
"""

from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.utils.log import set_log_level_to_debug
from agno.vectordb.search import SearchType
from agno.vectordb.weaviate import Distance, VectorIndex, Weaviate

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
embedder = SentenceTransformerEmbedder()
vector_db = Weaviate(
    collection="recipes",
    search_type=SearchType.hybrid,
    vector_index=VectorIndex.HNSW,
    distance=Distance.COSINE,
    embedder=embedder,
    local=True,
)


# ---------------------------------------------------------------------------
# 创建知识库
# ---------------------------------------------------------------------------
knowledge_base = Knowledge(vector_db=vector_db)


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
def main() -> None:
    vector_db.drop()
    set_log_level_to_debug()

    knowledge_base.insert(
        url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
    )
    print(
        "知识库已加载 PDF 内容。再次加载相同数据不会重新创建。"
    )

    knowledge_base.insert(
        url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf",
        skip_if_exists=True,
    )

    vector_db.drop()


if __name__ == "__main__":
    main()

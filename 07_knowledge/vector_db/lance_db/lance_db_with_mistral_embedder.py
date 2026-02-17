"""
LanceDB 与 Mistral Embedder
============================

演示使用 Mistral embedder 的 LanceDB 混合搜索。
"""

import asyncio

from agno.knowledge.embedder.mistral import MistralEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.lancedb import LanceDb, SearchType

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
embedder_mi = MistralEmbedder()
reader = PDFReader(chunk_size=1024)

vector_db = LanceDb(
    uri="tmp/lancedb",
    table_name="documents",
    embedder=embedder_mi,
    search_type=SearchType.hybrid,
)


# ---------------------------------------------------------------------------
# 创建知识库
# ---------------------------------------------------------------------------
knowledge = Knowledge(
    name="My Document Knowledge Base",
    vector_db=vector_db,
)


# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
async def main() -> None:
    await knowledge.ainsert(
        name="CV",
        path="cookbook/07_knowledge/testing_resources/cv_1.pdf",
        metadata={"user_tag": "Engineering Candidates"},
        reader=reader,
    )


if __name__ == "__main__":
    asyncio.run(main())

"""
Agentic RAG 带重排序
=============================

1. 运行：`uv pip install openai agno cohere lancedb tantivy sqlalchemy` 安装依赖。
"""

from agno.agent import Agent
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reranker.cohere import CohereReranker
from agno.models.openai import OpenAIChat
from agno.vectordb.lancedb import LanceDb, SearchType

knowledge = Knowledge(
    # 使用 LanceDB 作为向量数据库，将嵌入存储在 `agno_docs` 表中
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="agno_docs",
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(
            id="text-embedding-3-small"
        ),  # 使用 OpenAI 进行嵌入
        reranker=CohereReranker(
            model="rerank-multilingual-v3.0"
        ),  # 使用 Cohere 进行重排序
    ),
)

knowledge.insert(name="Agno Docs", url="https://docs.agno.com/introduction.md")


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    # 当为 Agent 提供 `knowledge` 时，Agentic RAG 默认启用。
    knowledge=knowledge,
    markdown=True,
)


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 加载知识库，首次运行后可注释
    agent.print_response("What are Agno's key features?")

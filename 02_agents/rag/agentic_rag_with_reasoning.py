"""
Agentic RAG 带推理
=============================

演示带有重排序和显式推理工具的 agentic RAG。
"""

import asyncio

from agno.agent import Agent
from agno.knowledge.embedder.cohere import CohereEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reranker.cohere import CohereReranker
from agno.models.anthropic import Claude
from agno.tools.reasoning import ReasoningTools
from agno.vectordb.lancedb import LanceDb, SearchType

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
knowledge = Knowledge(
    # 使用 LanceDB 作为向量数据库，将嵌入存储在 `agno_docs` 表中
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="agno_docs",
        search_type=SearchType.hybrid,
        embedder=CohereEmbedder(id="embed-v4.0"),
        reranker=CohereReranker(model="rerank-v3.5"),
    ),
)

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=Claude(id="claude-sonnet-4-20250514"),
    # 当为 Agent 提供 `knowledge` 时，Agentic RAG 默认启用。
    knowledge=knowledge,
    # search_knowledge=True 使 Agent 能够按需搜索
    # search_knowledge 默认为 True
    search_knowledge=True,
    tools=[ReasoningTools(add_instructions=True)],
    instructions=[
        "Include sources in your response.",
        "Always search your knowledge before answering the question.",
    ],
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(
        knowledge.ainsert_many(urls=["https://docs.agno.com/basics/agents/overview.md"])
    )
    agent.print_response(
        "What are Agents?",
        stream=True,
        show_full_reasoning=True,
    )

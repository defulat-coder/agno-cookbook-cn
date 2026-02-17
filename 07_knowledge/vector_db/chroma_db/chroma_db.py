"""
Chroma 数据库
=============

演示基于 Chroma 的知识库，支持同步、异步和异步批量流程。

安装依赖：
- uv pip install chromadb
"""

import asyncio

from agno.agent import Agent
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb


# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
def create_sync_knowledge() -> tuple[Knowledge, ChromaDb]:
    vector_db = ChromaDb(
        collection="vectors", path="tmp/chromadb", persistent_client=True
    )
    knowledge = Knowledge(
        name="Basic SDK Knowledge Base",
        description="Agno 2.0 Knowledge Implementation with ChromaDB",
        vector_db=vector_db,
    )
    return knowledge, vector_db


def create_async_knowledge(enable_batch: bool = False) -> Knowledge:
    if enable_batch:
        vector_db = ChromaDb(
            collection="recipes",
            path="tmp/chromadb",
            persistent_client=True,
            embedder=OpenAIEmbedder(enable_batch=True),
        )
    else:
        vector_db = ChromaDb(
            collection="recipes",
            path="tmp/chromadb",
            persistent_client=True,
        )
    return Knowledge(vector_db=vector_db)


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
def create_agent(knowledge: Knowledge) -> Agent:
    return Agent(knowledge=knowledge)


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
def run_sync() -> None:
    knowledge, vector_db = create_sync_knowledge()
    knowledge.insert(
        name="Recipes",
        url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf",
        metadata={"doc_type": "recipe_book"},
    )

    agent = create_agent(knowledge)
    agent.print_response("列出制作 Massaman Gai 的配料", markdown=True)

    vector_db.delete_by_name("Recipes")
    vector_db.delete_by_metadata({"doc_type": "recipe_book"})


async def run_async(enable_batch: bool = False) -> None:
    knowledge = create_async_knowledge(enable_batch=enable_batch)
    agent = create_agent(knowledge)

    if enable_batch:
        await knowledge.ainsert(path="cookbook/07_knowledge/testing_resources/cv_1.pdf")
    else:
        await knowledge.ainsert(url="https://docs.agno.com/basics/agents/overview.md")

    await agent.aprint_response("Agno Agent 的目的是什么？", markdown=True)


if __name__ == "__main__":
    run_sync()
    asyncio.run(run_async(enable_batch=False))
    asyncio.run(run_async(enable_batch=True))

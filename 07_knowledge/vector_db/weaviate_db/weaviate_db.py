"""
Weaviate 向量数据库
===================

演示基于 Weaviate 的知识库，支持同步、异步和异步批量流程。

安装依赖：
- uv pip install weaviate-client
"""

import asyncio
from os import getenv

from agno.agent import Agent
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.vectordb.search import SearchType
from agno.vectordb.weaviate import Distance, VectorIndex, Weaviate


# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
def create_sync_knowledge() -> tuple[Knowledge, Weaviate]:
    vector_db = Weaviate(
        collection="vectors",
        search_type=SearchType.vector,
        vector_index=VectorIndex.HNSW,
        distance=Distance.COSINE,
        local=False,
    )
    knowledge = Knowledge(
        name="Basic SDK Knowledge Base",
        description="Agno 2.0 Knowledge Implementation with Weaviate",
        vector_db=vector_db,
    )
    return knowledge, vector_db


def create_async_knowledge(enable_batch: bool = False) -> Knowledge:
    if enable_batch:
        vector_db = Weaviate(
            wcd_url=getenv("WEAVIATE_URL", "http://localhost:8081"),
            wcd_api_key=getenv("WEAVIATE_API_KEY", ""),
            collection="documents",
            embedder=OpenAIEmbedder(enable_batch=True),
        )
    else:
        vector_db = Weaviate(
            collection="recipes_async",
            search_type=SearchType.hybrid,
            vector_index=VectorIndex.HNSW,
            distance=Distance.COSINE,
            local=True,
        )
    return Knowledge(vector_db=vector_db)


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
def create_sync_agent(knowledge: Knowledge) -> Agent:
    return Agent(knowledge=knowledge)


def create_async_agent(knowledge: Knowledge, enable_batch: bool = False) -> Agent:
    if enable_batch:
        return Agent(
            model=OpenAIChat(id="gpt-5.2"),
            knowledge=knowledge,
            search_knowledge=True,
            read_chat_history=True,
        )
    return Agent(knowledge=knowledge, search_knowledge=True)


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
def run_sync() -> None:
    knowledge, vector_db = create_sync_knowledge()
    knowledge.insert(
        name="Recipes",
        url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf",
        metadata={"doc_type": "recipe_book"},
        skip_if_exists=True,
    )

    agent = create_sync_agent(knowledge)
    agent.print_response(
        "列出制作 Massaman Gai 的配料", markdown=True
    )

    vector_db.delete_by_name("Recipes")
    vector_db.delete_by_metadata({"doc_type": "recipe_book"})


async def run_async(enable_batch: bool = False) -> None:
    knowledge = create_async_knowledge(enable_batch=enable_batch)
    agent = create_async_agent(knowledge, enable_batch=enable_batch)

    if enable_batch:
        await knowledge.ainsert(path="cookbook/07_knowledge/testing_resources/cv_1.pdf")
        await agent.aprint_response(
            "你能告诉我关于候选人的什么信息，他的技能是什么？",
            markdown=True,
        )
    else:
        await knowledge.ainsert(
            name="Recipes",
            url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf",
        )
        await agent.aprint_response("如何制作 Tom Kha Gai", markdown=True)


if __name__ == "__main__":
    run_sync()
    asyncio.run(run_async(enable_batch=False))
    asyncio.run(run_async(enable_batch=True))

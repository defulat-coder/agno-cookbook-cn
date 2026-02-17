"""
Qdrant 数据库
=============

演示基于 Qdrant 的知识库，支持同步、异步和异步批量流程。
"""

import asyncio

from agno.agent import Agent
from agno.db.postgres.postgres import PostgresDb
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.vectordb.qdrant import Qdrant

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
COLLECTION_NAME = "thai-recipes"


# ---------------------------------------------------------------------------
# 创建知识库
# ---------------------------------------------------------------------------
def create_sync_knowledge() -> tuple[Knowledge, Qdrant]:
    vector_db = Qdrant(collection=COLLECTION_NAME, url="http://localhost:6333")
    contents_db = PostgresDb(
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
        knowledge_table="knowledge_contents",
    )
    knowledge = Knowledge(
        name="My Qdrant Vector Knowledge Base",
        description="This is a knowledge base that uses a Qdrant Vector DB",
        vector_db=vector_db,
        contents_db=contents_db,
    )
    return knowledge, vector_db


def create_async_knowledge(enable_batch: bool = False) -> Knowledge:
    if enable_batch:
        vector_db = Qdrant(
            collection="recipe_documents",
            url="http://localhost:6333",
            embedder=OpenAIEmbedder(enable_batch=True),
        )
    else:
        vector_db = Qdrant(
            collection=COLLECTION_NAME,
            url="http://localhost:6333",
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
            url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
        )
        await agent.aprint_response("如何制作 Tom Kha Gai", markdown=True)


if __name__ == "__main__":
    run_sync()
    asyncio.run(run_async(enable_batch=False))
    asyncio.run(run_async(enable_batch=True))

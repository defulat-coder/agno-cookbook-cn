"""
PgVector 数据库
===============

演示基于 PgVector 的知识库，支持同步、异步和异步批量流程。
"""

import asyncio

from agno.agent import Agent
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"


# ---------------------------------------------------------------------------
# 创建知识库
# ---------------------------------------------------------------------------
def create_sync_knowledge() -> tuple[Knowledge, PgVector]:
    vector_db = PgVector(table_name="vectors", db_url=db_url)
    knowledge = Knowledge(
        name="My PG Vector Knowledge Base",
        description="This is a knowledge base that uses a PG Vector DB",
        vector_db=vector_db,
    )
    return knowledge, vector_db


def create_async_knowledge(enable_batch: bool = False) -> tuple[Knowledge, PgVector]:
    if enable_batch:
        vector_db = PgVector(
            table_name="recipes",
            db_url=db_url,
            embedder=OpenAIEmbedder(enable_batch=True),
        )
    else:
        vector_db = PgVector(table_name="recipes", db_url=db_url)
    knowledge = Knowledge(vector_db=vector_db)
    return knowledge, vector_db


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
def create_sync_agent(knowledge: Knowledge) -> Agent:
    return Agent(
        knowledge=knowledge,
        search_knowledge=True,
        read_chat_history=True,
    )


def create_async_agent(knowledge: Knowledge) -> Agent:
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
    agent.print_response("如何制作泰式炒河粉？", markdown=True)

    vector_db.delete_by_name("Recipes")
    vector_db.delete_by_metadata({"doc_type": "recipe_book"})


async def run_async(enable_batch: bool = False) -> None:
    knowledge, _ = create_async_knowledge(enable_batch=enable_batch)
    agent = create_async_agent(knowledge)

    await knowledge.ainsert(url="https://docs.agno.com/basics/agents/overview.md")
    await agent.aprint_response("Agno Agent 的目的是什么？", markdown=True)


if __name__ == "__main__":
    run_sync()
    asyncio.run(run_async(enable_batch=False))
    asyncio.run(run_async(enable_batch=True))

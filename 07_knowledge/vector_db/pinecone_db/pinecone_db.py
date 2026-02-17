"""
Pinecone 数据库
===============

演示基于 Pinecone 的知识库，支持同步和异步批量流程。
"""

import asyncio
from os import getenv

from agno.agent import Agent
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.vectordb.pineconedb import PineconeDb

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
api_key = getenv("PINECONE_API_KEY")
index_name = "thai-recipe-index"


# ---------------------------------------------------------------------------
# 创建知识库
# ---------------------------------------------------------------------------
def create_sync_knowledge() -> tuple[Knowledge, PineconeDb]:
    vector_db = PineconeDb(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec={"serverless": {"cloud": "aws", "region": "us-east-1"}},
        api_key=api_key,
    )
    knowledge = Knowledge(
        name="My Pinecone Knowledge Base",
        description="This is a knowledge base that uses a Pinecone Vector DB",
        vector_db=vector_db,
    )
    return knowledge, vector_db


def create_async_batch_knowledge() -> Knowledge:
    return Knowledge(
        vector_db=PineconeDb(
            name="recipe-documents",
            dimension=1536,
            spec={"serverless": {"cloud": "aws", "region": "us-east-1"}},
            api_key=getenv("PINECONE_API_KEY"),
            embedder=OpenAIEmbedder(enable_batch=True),
        )
    )


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
def create_sync_agent(knowledge: Knowledge) -> Agent:
    return Agent(knowledge=knowledge, search_knowledge=True, read_chat_history=True)


def create_async_batch_agent(knowledge: Knowledge) -> Agent:
    return Agent(
        model=OpenAIChat(id="gpt-5.2"),
        knowledge=knowledge,
        search_knowledge=True,
        read_chat_history=True,
    )


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


async def run_async_batch() -> None:
    knowledge = create_async_batch_knowledge()
    agent = create_async_batch_agent(knowledge)

    await knowledge.ainsert(path="cookbook/07_knowledge/testing_resources/cv_1.pdf")
    await agent.aprint_response(
        "你能告诉我关于候选人的什么信息，他的技能是什么？",
        markdown=True,
    )


if __name__ == "__main__":
    run_sync()
    asyncio.run(run_async_batch())

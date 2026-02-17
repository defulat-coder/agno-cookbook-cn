"""
SingleStore 向量数据库
======================

运行设置脚本：
`./cookbook/scripts/run_singlestore.sh`

然后在 Studio 中创建一个数据库（http://localhost:8080）。
"""

import asyncio
from os import getenv

from agno.agent import Agent
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.vectordb.singlestore import SingleStore
from sqlalchemy.engine import create_engine

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
USERNAME = getenv("SINGLESTORE_USERNAME")
PASSWORD = getenv("SINGLESTORE_PASSWORD")
HOST = getenv("SINGLESTORE_HOST")
PORT = getenv("SINGLESTORE_PORT")
DATABASE = getenv("SINGLESTORE_DATABASE")
SSL_CERT = getenv("SINGLESTORE_SSL_CERT", None)


def get_engine():
    db_url = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8mb4"
    if SSL_CERT:
        db_url += f"&ssl_ca={SSL_CERT}&ssl_verify_cert=true"
    return create_engine(db_url)


# ---------------------------------------------------------------------------
# 创建知识库
# ---------------------------------------------------------------------------
def create_sync_knowledge() -> tuple[Knowledge, SingleStore]:
    vector_db = SingleStore(
        collection="recipes",
        db_engine=get_engine(),
        schema=DATABASE,
    )
    knowledge = Knowledge(name="My SingleStore Knowledge Base", vector_db=vector_db)
    return knowledge, vector_db


def create_async_batch_knowledge() -> Knowledge:
    vector_db = SingleStore(
        collection="documents",
        db_engine=get_engine(),
        schema=DATABASE,
        embedder=OpenAIEmbedder(enable_batch=True),
    )
    return Knowledge(vector_db=vector_db)


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
def create_sync_agent(knowledge: Knowledge) -> Agent:
    return Agent(
        knowledge=knowledge,
        search_knowledge=True,
        read_chat_history=True,
    )


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

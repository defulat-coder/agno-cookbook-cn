"""
LightRAG 向量数据库
===================

演示基于 LightRAG 的知识和带引用的检索。
"""

import asyncio
import time
from os import getenv

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.wikipedia_reader import WikipediaReader
from agno.vectordb.lightrag import LightRag

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
vector_db = LightRag(
    server_url=getenv("LIGHTRAG_SERVER_URL", "http://localhost:9621"),
    api_key=getenv("LIGHTRAG_API_KEY"),
)


# ---------------------------------------------------------------------------
# 创建知识库
# ---------------------------------------------------------------------------
knowledge = Knowledge(
    name="LightRAG Knowledge Base",
    description="Knowledge base using LightRAG for graph-based retrieval",
    vector_db=vector_db,
)


# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
agent = Agent(
    knowledge=knowledge,
    search_knowledge=True,
    read_chat_history=False,
)


# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
async def main() -> None:
    await knowledge.ainsert(
        name="Recipes",
        path="cookbook/07_knowledge/testing_resources/cv_1.pdf",
        metadata={"doc_type": "recipe_book"},
    )
    await knowledge.ainsert(
        name="Recipes",
        topics=["Manchester United"],
        reader=WikipediaReader(),
    )
    await knowledge.ainsert(
        name="Recipes",
        path="cookbook/07_knowledge/testing_resources/cv_2.pdf",
    )

    time.sleep(60)

    await agent.aprint_response("What skills does Jordan Mitchell have?", markdown=True)
    await agent.aprint_response(
        "In what year did Manchester United change their name?",
        markdown=True,
    )

    results = await vector_db.async_search("What skills does Jordan Mitchell have?")
    if results:
        doc = results[0]
        print(f"References: {doc.meta_data.get('references', [])}")


if __name__ == "__main__":
    asyncio.run(main())

"""
Milvus 混合搜索
===============

演示 Milvus 混合搜索，支持同步和异步流程。
"""

import asyncio

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.milvus import Milvus, SearchType

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
vector_db = Milvus(
    collection="recipes",
    uri="/tmp/milvus_hybrid.db",
    search_type=SearchType.hybrid,
)


# ---------------------------------------------------------------------------
# 创建知识库
# ---------------------------------------------------------------------------
knowledge = Knowledge(vector_db=vector_db)


# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
agent = Agent(knowledge=knowledge)


# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
def run_sync() -> None:
    knowledge.insert(url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf")
    agent.print_response("How to make Tom Kha Gai", markdown=True)


async def run_async() -> None:
    await knowledge.ainsert(
        url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
    )
    await agent.aprint_response("How to make Tom Kha Gai", markdown=True)


if __name__ == "__main__":
    run_sync()
    asyncio.run(run_async())

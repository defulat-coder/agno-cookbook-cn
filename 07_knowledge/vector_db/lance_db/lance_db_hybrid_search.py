"""
LanceDB 混合搜索
================

演示使用 LanceDB 进行混合搜索。
"""

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.vectordb.lancedb import LanceDb, SearchType

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
vector_db = LanceDb(
    table_name="vectors",
    uri="tmp/lancedb",
    search_type=SearchType.hybrid,
)


# ---------------------------------------------------------------------------
# 创建知识库
# ---------------------------------------------------------------------------
knowledge = Knowledge(
    name="My LanceDB Knowledge Base",
    description="This is a knowledge base that uses LanceDB",
    vector_db=vector_db,
)


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    knowledge=knowledge,
    search_knowledge=True,
    markdown=True,
)


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
def main() -> None:
    knowledge.insert(
        name="Recipes",
        url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf",
        metadata={"doc_type": "recipe_book"},
    )
    agent.print_response(
        "如何制作椰奶鸡肉高良姜汤",
        stream=True,
    )


if __name__ == "__main__":
    main()

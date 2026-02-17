"""
Qdrant 混合搜索
===============

演示在交互式循环中使用 Qdrant 混合检索。
"""

import typer
from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.qdrant import Qdrant
from agno.vectordb.search import SearchType
from rich.prompt import Prompt

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
COLLECTION_NAME = "thai-recipes"
vector_db = Qdrant(
    collection=COLLECTION_NAME,
    url="http://localhost:6333",
    search_type=SearchType.hybrid,
)


# ---------------------------------------------------------------------------
# 创建知识库
# ---------------------------------------------------------------------------
knowledge = Knowledge(
    name="My Qdrant Vector Knowledge Base",
    vector_db=vector_db,
)


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
def qdrantdb_agent(user: str = "user"):
    agent = Agent(
        user_id=user,
        knowledge=knowledge,
        search_knowledge=True,
    )

    while True:
        message = Prompt.ask(f"[bold]{user}[/bold]")
        if message in ("exit", "bye"):
            break
        agent.print_response(message)


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
def main() -> None:
    knowledge.insert(
        name="Recipes",
        url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf",
        metadata={"doc_type": "recipe_book"},
    )
    typer.run(qdrantdb_agent)


if __name__ == "__main__":
    main()

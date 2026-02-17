"""
Weaviate 混合搜索
=================

演示 Weaviate 混合检索与交互式查询。
"""

import typer
from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.search import SearchType
from agno.vectordb.weaviate import Distance, VectorIndex, Weaviate
from rich.prompt import Prompt

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
vector_db = Weaviate(
    collection="recipes",
    search_type=SearchType.hybrid,
    vector_index=VectorIndex.HNSW,
    distance=Distance.COSINE,
    local=False,
    hybrid_search_alpha=0.6,
)


# ---------------------------------------------------------------------------
# 创建知识库
# ---------------------------------------------------------------------------
knowledge_base = Knowledge(
    name="Weaviate Hybrid Search",
    description="A knowledge base for Weaviate hybrid search",
    vector_db=vector_db,
)


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
def weaviate_agent(user: str = "user"):
    agent = Agent(
        user_id=user,
        knowledge=knowledge_base,
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
    knowledge_base.insert(
        url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
    )
    typer.run(weaviate_agent)


if __name__ == "__main__":
    main()

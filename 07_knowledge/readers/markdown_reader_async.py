import asyncio
from pathlib import Path

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"


knowledge = Knowledge(
    vector_db=PgVector(
        table_name="markdown_documents",
        db_url=db_url,
    ),
    max_results=5,  # 搜索时返回的结果数量
)

agent = Agent(
    knowledge=knowledge,
    search_knowledge=True,
)

if __name__ == "__main__":
    asyncio.run(
        knowledge.ainsert(
            path=Path("README.md"),
        )
    )

    asyncio.run(
        agent.aprint_response(
            "你能告诉我关于 Agno 的什么信息？",
            markdown=True,
        )
    )

import asyncio

from agno.agent import Agent
from agno.db.postgres.postgres import PostgresDb
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.web_search_reader import WebSearchReader
from agno.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

db = PostgresDb(id="web-search-db", db_url=db_url)

vector_db = PgVector(
    db_url=db_url,
    table_name="web_search_documents",
)
knowledge = Knowledge(
    name="Web Search Documents",
    contents_db=db,
    vector_db=vector_db,
)


# 使用知识初始化 Agent
agent = Agent(
    knowledge=knowledge,
    search_knowledge=True,
)


if __name__ == "__main__":
    # 首次运行后注释掉
    asyncio.run(
        knowledge.ainsert(
            topics=["web3 latest trends 2025"],
            reader=WebSearchReader(
                max_results=3,
                search_engine="duckduckgo",
                chunk=True,
            ),
        )
    )

    # 创建并使用 Agent
    asyncio.run(
        agent.aprint_response(
            "根据搜索结果，最新的 AI 趋势是什么？",
            markdown=True,
        )
    )

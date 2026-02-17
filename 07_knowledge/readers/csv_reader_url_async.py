import asyncio

from agno.agent import Agent
from agno.db.postgres.postgres import PostgresDb
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge = Knowledge(
    # Table name: ai.csv_documents
    vector_db=PgVector(
        table_name="csv_documents",
        db_url=db_url,
    ),
    contents_db=PostgresDb(db_url=db_url),
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
            url="https://agno-public.s3.amazonaws.com/demo_data/IMDB-Movie-Data.csv"
        )
    )

    # 创建并使用 Agent
    asyncio.run(
        agent.aprint_response("这里有哪些类型的电影？", markdown=True)
    )

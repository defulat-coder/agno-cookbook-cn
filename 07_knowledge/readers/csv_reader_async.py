import asyncio
from pathlib import Path

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge = Knowledge(
    vector_db=PgVector(
        table_name="csv_documents",
        db_url=db_url,
    ),
    max_results=5,  # 搜索时返回的结果数量
)

# 使用知识初始化 Agent
agent = Agent(
    knowledge=knowledge,
    search_knowledge=True,
)


if __name__ == "__main__":
    # 首次运行后注释掉
    asyncio.run(knowledge.ainsert(path=Path("data/csv")))

    # 创建并使用 Agent
    asyncio.run(agent.aprint_response("csv 文件的内容是什么", markdown=True))

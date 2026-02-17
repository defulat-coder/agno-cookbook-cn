import asyncio

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.arxiv_reader import ArxivReader
from agno.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge = Knowledge(
    # Table name: ai.arxiv_documents
    vector_db=PgVector(
        table_name="arxiv_documents",
        db_url=db_url,
    ),
)

# 创建包含知识的 Agent
agent = Agent(
    knowledge=knowledge,
    search_knowledge=True,
)


def main():
    # 加载知识
    asyncio.run(
        knowledge.ainsert(
            topics=["Generative AI", "Machine Learning"],
            reader=ArxivReader(),
        )
    )

    # 创建并使用 Agent
    asyncio.run(
        agent.aprint_response(
            "你能告诉我关于生成式 AI 的什么信息？", markdown=True
        )
    )


if __name__ == "__main__":
    main()

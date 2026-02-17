import asyncio

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# 创建包含 data/pdfs 目录中 PDF 的知识库
knowledge = Knowledge(
    vector_db=PgVector(
        table_name="pdf_documents",
        db_url=db_url,
    )
)

# 创建包含知识库的 Agent
agent = Agent(
    knowledge=knowledge,
    search_knowledge=True,
)

if __name__ == "__main__":
    asyncio.run(
        knowledge.ainsert(
            path="cookbook/07_knowledge/testing_resources/cv_1.pdf",
        )
    )
    # 创建并使用 Agent
    asyncio.run(
        agent.aprint_response(
            "申请软件工程师职位需要具备哪些技能？",
            markdown=True,
        )
    )

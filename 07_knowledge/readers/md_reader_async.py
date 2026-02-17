import asyncio

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.markdown_reader import MarkdownReader
from agno.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# 创建包含 markdown 内容的知识库
knowledge = Knowledge(
    vector_db=PgVector(
        table_name="markdown_documents",
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
            url="https://github.com/agno-agi/agno/blob/main/README.md",
            reader=MarkdownReader(),
        )
    )
    # 创建并使用 Agent
    asyncio.run(
        agent.aprint_response(
            "你能告诉我关于 Agno 的什么信息？",
            markdown=True,
        )
    )

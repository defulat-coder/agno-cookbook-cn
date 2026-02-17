import asyncio

from agno.agent import Agent
from agno.db.postgres.postgres import PostgresDb
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.tavily_reader import TavilyReader
from agno.models.openai import OpenAIChat
from agno.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# Initialize database and vector store
db = PostgresDb(id="tavily-reader-db", db_url=db_url)

vector_db = PgVector(
    db_url=db_url,
    table_name="tavily_documents",
)

knowledge = Knowledge(
    name="Tavily Extracted Documents",
    contents_db=db,
    vector_db=vector_db,
)


async def main():
    """
    演示异步 TavilyReader 与知识库集成的使用示例。

    此示例展示：
    1. 使用 TavilyReader 异步从 URL 添加内容
    2. 与知识库集成以实现 RAG
    3. 在启用 search_knowledge 的情况下查询 Agent
    """

    # 要提取内容的 URL
    urls_to_extract = [
        "https://github.com/agno-agi/agno",
        "https://docs.tavily.com/documentation/api-reference/endpoint/extract",
    ]

    print("=" * 80)
    print("使用 TavilyReader 向知识库添加内容（异步）")
    print("=" * 80)

    # 使用 TavilyReader 从 URL 添加内容
    # 注意：首次运行后注释掉，以避免重复添加相同内容
    for url in urls_to_extract:
        print(f"\n从以下位置提取内容: {url}")
        await knowledge.ainsert(
            url,
            reader=TavilyReader(
                extract_format="markdown",
                extract_depth="basic",
                chunk=True,
                chunk_size=3000,
            ),
        )

    print("\n" + "=" * 80)
    print("使用知识库创建 Agent")
    print("=" * 80)

    # 创建包含知识的 Agent
    agent = Agent(
        model=OpenAIChat(id="gpt-5.2"),
        knowledge=knowledge,
        search_knowledge=True,  # 启用知识搜索
        debug_mode=True,
    )

    print("\n" + "=" * 80)
    print("查询 Agent")
    print("=" * 80)

    # 询问有关提取内容的问题
    await agent.aprint_response(
        "根据文档，Agno 是什么以及它的主要特性是什么？",
        markdown=True,
    )

    print("\n" + "=" * 80)
    print("第二次查询")
    print("=" * 80)

    await agent.aprint_response(
        "Tavily Extract API 是什么以及它如何工作？",
        markdown=True,
    )


if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())

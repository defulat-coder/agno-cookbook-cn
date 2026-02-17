import asyncio

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pptx_reader import PPTXReader
from agno.models.openai import OpenAIChat
from agno.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge = Knowledge(
    # Table name: ai.pptx_documents
    vector_db=PgVector(
        table_name="pptx_documents",
        db_url=db_url,
    ),
)

# 创建包含知识的 Agent
agent = Agent(
    model=OpenAIChat(id="gpt-5.2"),
    knowledge=knowledge,
    search_knowledge=True,
)


def main():
    # 异步加载 PPTX 内容
    # 您可以通过多次调用 ainsert 加载多个 PPTX 文件
    asyncio.run(
        knowledge.ainsert(
            path="path/to/your/presentation.pptx",  # 替换为实际的 PPTX 文件路径
            reader=PPTXReader(),
        )
    )

    # 创建并使用 Agent
    asyncio.run(
        agent.aprint_response(
            "搜索演示文稿内容，告诉我幻灯片中涵盖了哪些关键主题、要点或信息。具体说明你在知识库中发现的内容。",
            markdown=True,
        )
    )


if __name__ == "__main__":
    main()

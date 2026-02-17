from agno.agent import Agent
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.website_reader import WebsiteReader
from agno.models.openai import OpenAIChat
from agno.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# 创建包含网站内容的知识库
knowledge = Knowledge(
    # 表名：ai.website_documents
    vector_db=PgVector(
        table_name="website_documents",
        db_url=db_url,
        embedder=OpenAIEmbedder(),
    ),
)
# 加载知识
knowledge.insert(
    url="https://en.wikipedia.org/wiki/OpenAI",
    reader=WebsiteReader(),
)

# 创建包含知识的 Agent
agent = Agent(
    model=OpenAIChat(id="gpt-5.2"),
    knowledge=knowledge,
    search_knowledge=True,
)

# 向 Agent 询问知识
agent.print_response("你能告诉我关于生成式 AI 的什么信息？", markdown=True)

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.arxiv_reader import ArxivReader
from agno.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# 创建包含 ArXiv 文档的知识库
knowledge = Knowledge(
    # 表名：ai.arxiv_documents
    vector_db=PgVector(
        table_name="arxiv_documents",
        db_url=db_url,
    ),
)
# 加载知识
knowledge.insert(
    topics=["Generative AI", "Machine Learning"],
    reader=ArxivReader(),
)

# 创建包含知识的 Agent
agent = Agent(
    knowledge=knowledge,
    search_knowledge=True,
)

# 向 Agent 询问知识
agent.print_response("你能告诉我关于生成式 AI 的什么信息？", markdown=True)

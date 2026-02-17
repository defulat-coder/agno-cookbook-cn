from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pptx_reader import PPTXReader
from agno.models.openai import OpenAIChat
from agno.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# 创建包含 PPTX 文档的知识库
knowledge = Knowledge(
    # 表名：ai.pptx_documents
    vector_db=PgVector(
        table_name="pptx_documents",
        db_url=db_url,
    ),
)

# 从文件加载 PPTX 内容
# 您可以通过多次调用 insert 加载多个 PPTX 文件
knowledge.insert(
    path="path/to/your/presentation.pptx",  # 替换为实际的 PPTX 文件路径
    reader=PPTXReader(),
)

# 创建包含知识的 Agent
agent = Agent(
    model=OpenAIChat(id="gpt-5.2"),
    knowledge=knowledge,
    search_knowledge=True,
)

# 向 Agent 询问知识
agent.print_response(
    "搜索演示文稿内容，告诉我幻灯片中涵盖了哪些关键主题、要点或信息。具体说明你在知识库中发现的内容。",
    markdown=True,
)

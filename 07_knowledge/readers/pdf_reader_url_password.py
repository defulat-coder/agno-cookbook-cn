from agno.agent import Agent
from agno.db.postgres.postgres import PostgresDb
from agno.knowledge.content import ContentAuth
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# 创建带有简化密码处理的知识库
knowledge = Knowledge(
    vector_db=PgVector(
        table_name="pdf_documents_password",
        db_url=db_url,
    ),
    contents_db=PostgresDb(db_url=db_url),
)

knowledge.insert(
    url="https://agno-public.s3.us-east-1.amazonaws.com/recipes/ThaiRecipes_protected.pdf",
    auth=ContentAuth(password="ThaiRecipes"),
)


# 创建包含知识的 Agent
agent = Agent(
    knowledge=knowledge,
    search_knowledge=True,
)

agent.print_response("给我泰式炒河粉的食谱")

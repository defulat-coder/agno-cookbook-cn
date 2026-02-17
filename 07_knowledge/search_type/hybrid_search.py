from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector, SearchType

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# 使用混合搜索加载知识库
hybrid_db = PgVector(table_name="recipes", db_url=db_url, search_type=SearchType.hybrid)
knowledge = Knowledge(
    name="Hybrid Search Knowledge Base",
    vector_db=hybrid_db,
)

knowledge.insert(
    url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf",
)

# 运行混合搜索查询
results = hybrid_db.search("chicken coconut soup", limit=5)
print("混合搜索结果:", results)

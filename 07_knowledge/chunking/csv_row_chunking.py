from agno.agent import Agent
from agno.knowledge.chunking.row import RowChunking
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.csv_reader import CSVReader
from agno.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge_base = Knowledge(
    vector_db=PgVector(table_name="imdb_movies_row_chunking", db_url=db_url),
)

knowledge_base.insert(
    url="https://agno-public.s3.amazonaws.com/demo_data/IMDB-Movie-Data.csv",
    reader=CSVReader(
        chunking_strategy=RowChunking(),
    ),
)

# 使用知识库初始化 Agent
agent = Agent(
    knowledge=knowledge_base,
    search_knowledge=True,
)

# 使用 agent
agent.print_response("告诉我关于电影《银河护卫队》的信息", markdown=True)

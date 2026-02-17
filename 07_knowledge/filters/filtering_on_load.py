from agno.agent import Agent
from agno.db.postgres.postgres import PostgresDb
from agno.knowledge.knowledge import Knowledge
from agno.utils.media import (
    SampleDataFileExtension,
    download_knowledge_filters_sample_data,
)
from agno.vectordb.pgvector import PgVector

# 下载所有样本销售文件并获取其路径
downloaded_csv_paths = download_knowledge_filters_sample_data(
    num_files=4, file_extension=SampleDataFileExtension.CSV
)

# 初始化 PgVector
vector_db = PgVector(
    table_name="recipes",
    db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
)

# 步骤 1：使用文档和元数据初始化知识库
# ------------------------------------------------------------------------------
# 加载知识库时，我们可以附加元数据，这些元数据将用于过滤

# 初始化 Knowledge
knowledge = Knowledge(
    vector_db=vector_db,
    contents_db=PostgresDb(
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
        knowledge_table="knowledge_contents",
    ),
    max_results=5,
)

knowledge.insert(
    path=downloaded_csv_paths[0],
    metadata={
        "data_type": "sales",
        "quarter": "Q1",
        "year": 2024,
        "region": "north_america",
        "currency": "USD",
    },
)

knowledge.insert(
    path=downloaded_csv_paths[1],
    metadata={
        "data_type": "sales",
        "year": 2024,
        "region": "europe",
        "currency": "EUR",
    },
)

knowledge.insert(
    path=downloaded_csv_paths[2],
    metadata={
        "data_type": "survey",
        "survey_type": "customer_satisfaction",
        "year": 2024,
        "target_demographic": "mixed",
    },
)

knowledge.insert(
    path=downloaded_csv_paths[3],
    metadata={
        "data_type": "financial",
        "sector": "technology",
        "year": 2024,
        "report_type": "quarterly_earnings",
    },
)

# 步骤 2：使用不同的过滤器组合查询知识库
# ------------------------------------------------------------------------------
agent = Agent(
    knowledge=knowledge,
    search_knowledge=True,
    knowledge_filters={"region": "north_america", "data_type": "sales"},
)
agent.print_response(
    "收入表现和最畅销产品",
    markdown=True,
)

"""
此示例演示如何在 agent 中使用知识过滤器表达式。

知识过滤器允许您将知识搜索限制为特定文档
或元数据条件，实现个性化和上下文响应。
"""

from agno.agent import Agent
from agno.filters import AND, EQ, IN, NOT
from agno.knowledge.knowledge import Knowledge
from agno.utils.media import (
    SampleDataFileExtension,
    download_knowledge_filters_sample_data,
)
from agno.vectordb.pgvector import PgVector

# 下载所有样本销售文档并获取其路径
downloaded_csv_paths = download_knowledge_filters_sample_data(
    num_files=4, file_extension=SampleDataFileExtension.CSV
)

# 初始化 PGVector
vector_db = PgVector(
    table_name="recipes",
    db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
)

# 步骤 1：使用文档和元数据初始化知识库
# -----------------------------------------------------------------------------
knowledge = Knowledge(
    name="CSV Knowledge Base",
    description="A knowledge base for CSV files",
    vector_db=vector_db,
)

# 将所有文档加载到向量数据库中
knowledge.insert_many(
    [
        {
            "path": downloaded_csv_paths[0],
            "metadata": {
                "data_type": "sales",
                "quarter": "Q1",
                "year": 2024,
                "region": "north_america",
                "currency": "USD",
            },
        },
        {
            "path": downloaded_csv_paths[1],
            "metadata": {
                "data_type": "sales",
                "year": 2024,
                "region": "europe",
                "currency": "EUR",
            },
        },
        {
            "path": downloaded_csv_paths[2],
            "metadata": {
                "data_type": "survey",
                "survey_type": "customer_satisfaction",
                "year": 2024,
                "target_demographic": "mixed",
            },
        },
        {
            "path": downloaded_csv_paths[3],
            "metadata": {
                "data_type": "financial",
                "sector": "technology",
                "year": 2024,
                "report_type": "quarterly_earnings",
            },
        },
    ],
)

# Step 2: Query the knowledge base with different filter combinations
# ------------------------------------------------------------------------------
sales_agent = Agent(
    knowledge=knowledge,
    search_knowledge=True,
)

print("--------------------------------")
print("Using IN operator")
sales_agent.print_response(
    "Describe revenue performance for the region",
    knowledge_filters=[(IN("region", ["north_america"]))],
    markdown=True,
)

print("--------------------------------")
print("Using NOT operator")
sales_agent.print_response(
    "Describe revenue performance for the region",
    knowledge_filters=[NOT(IN("region", ["north_america"]))],
    markdown=True,
)

print("--------------------------------")
print("Using AND operator")
sales_agent.print_response(
    "Describe revenue performance for the region",
    knowledge_filters=[
        AND(EQ("data_type", "sales"), NOT(EQ("region", "north_america")))
    ],
    markdown=True,
)

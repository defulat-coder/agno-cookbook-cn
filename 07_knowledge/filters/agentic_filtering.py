from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
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
# 注意：ContentsDB 对于 agentic filtering 是可选的
# - 不使用 ContentsDB：过滤器可以工作，但不会针对已知元数据键进行验证
# - 使用 ContentsDB：过滤器键会被验证，提高可靠性并提供有用的警告
#
# 不使用 ContentsDB 的示例（过滤仍然有效）：
# knowledge = Knowledge(
#     name="CSV Knowledge Base",
#     description="A knowledge base for CSV files",
#     vector_db=vector_db,
#     # contents_db 未提供 - agentic filtering 仍可在无验证的情况下工作
# )
#
# 使用 ContentsDB 的示例（添加过滤器验证）：
knowledge = Knowledge(
    name="CSV Knowledge Base",
    description="A knowledge base for CSV files",
    vector_db=vector_db,
    contents_db=PostgresDb(  # 可选 - 启用过滤器验证
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
        knowledge_table="knowledge_contents",
    ),
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
    skip_if_exists=True,
)
# 步骤 2：使用 Agent 自动从查询中提取过滤器查询知识库
# -----------------------------------------------------------------------------------

# 启用 agentic filtering
agent = Agent(
    model=OpenAIChat("gpt-5.2"),
    knowledge=knowledge,
    search_knowledge=True,
    enable_agentic_knowledge_filters=True,
)

agent.print_response(
    "告诉我关于 north_america 地区的收入表现和最畅销产品",
    markdown=True,
)

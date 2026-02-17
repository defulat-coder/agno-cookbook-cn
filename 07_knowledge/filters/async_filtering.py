import asyncio
import os

from agno.agent import Agent
from agno.db.postgres import AsyncPostgresDb
from agno.db.sqlite import AsyncSqliteDb
from agno.filters import IN
from agno.knowledge.knowledge import Knowledge
from agno.utils.media import (
    SampleDataFileExtension,
    download_knowledge_filters_sample_data,
)
from agno.vectordb.pgvector import PgVector

# 下载所有样本简历并获取其路径
downloaded_cv_paths = download_knowledge_filters_sample_data(
    num_files=5, file_extension=SampleDataFileExtension.DOCX
)

# 清理旧数据库
if os.path.exists("tmp/knowledge_contents.db"):
    os.remove("tmp/knowledge_contents.db")
db = AsyncSqliteDb(
    db_file="tmp/knowledge_contents.db",
)

db = AsyncPostgresDb(
    db_url="postgresql+psycopg_async://ai:ai@localhost:5532/ai",
    knowledge_table="knowledge_contents",
)

# 初始化向量数据库
vector_db = PgVector(
    table_name="CVs",
    db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
)

# 步骤 1：使用文档和元数据初始化知识库
# ------------------------------------------------------------------------------
# 初始化知识库时，我们可以附加将用于过滤的元数据
# 此元数据可以包括用户 ID、文档类型、日期或任何其他属性

knowledge = Knowledge(
    name="Async Filtering",
    vector_db=vector_db,
    contents_db=db,
)

asyncio.run(
    knowledge.ainsert_many(
        [
            {
                "path": downloaded_cv_paths[0],
                "metadata": {
                    "user_id": "jordan_mitchell",
                    "document_type": "cv",
                    "year": 2025,
                },
            },
            {
                "path": downloaded_cv_paths[1],
                "metadata": {
                    "user_id": "taylor_brooks",
                    "document_type": "cv",
                    "year": 2025,
                },
            },
            {
                "path": downloaded_cv_paths[2],
                "metadata": {
                    "user_id": "morgan_lee",
                    "document_type": "cv",
                    "year": 2025,
                },
            },
            {
                "path": downloaded_cv_paths[3],
                "metadata": {
                    "user_id": "casey_jordan",
                    "document_type": "cv",
                    "year": 2025,
                },
            },
            {
                "path": downloaded_cv_paths[4],
                "metadata": {
                    "user_id": "alex_rivera",
                    "document_type": "cv",
                    "year": 2025,
                },
            },
        ],
    )
)


# 步骤 2：使用不同的过滤器组合查询知识库
# ------------------------------------------------------------------------------

# 选项 1：Agent 上的过滤器
# 使用知识库和过滤器初始化 Agent
agent = Agent(
    db=db,
    knowledge=knowledge,
    search_knowledge=True,
)

if __name__ == "__main__":
    # 查询 Jordan Mitchell 的经验和技能
    asyncio.run(
        agent.aprint_response(
            "在知识库中搜索候选人的经验和技能",
            knowledge_filters={"user_id": "jordan_mitchell"},
            markdown=True,
        )
    )

    asyncio.run(
        agent.aprint_response(
            "告诉我候选人的经验和技能",
            knowledge_filters=[(IN("user_id", ["jordan_mitchell"]))],
            markdown=True,
        )
    )

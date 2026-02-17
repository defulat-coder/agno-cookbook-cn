"""
MongoDB 向量数据库
==================

1. 创建 MongoDB Atlas 账户：
   - 访问 https://www.mongodb.com/cloud/atlas/register
   - 注册免费账户

2. 创建新集群：
   - 点击"Build a Database"
   - 选择免费层级（M0）
   - 选择您首选的云提供商和区域
   - 点击"Create Cluster"

3. 设置数据库访问：
   - 按照 MongoDB Atlas UI 中的说明操作
   - 创建用户名和密码
   - 点击"Add New Database User"

5. 获取连接字符串：
   - 选择"Drivers"作为连接方法
   - 选择"Python"作为驱动程序
   - 复制连接字符串

7. 测试连接：
   - 在代码中使用连接字符串
   - 确保已安装 pymongo：uv pip install "pymongo[srv]"
   - 使用简单查询测试以验证连接

或者，要在本地测试，您可以运行 docker 容器

docker run -p 27017:27017 -d --name mongodb-container --rm -v ./tmp/mongo-data:/data/db mongodb/mongodb-atlas-local:8.0.3
"""

import asyncio

from agno.agent import Agent
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.vectordb.mongodb import MongoVectorDb

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
mdb_connection_string = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority"


# ---------------------------------------------------------------------------
# 创建知识库
# ---------------------------------------------------------------------------
def create_sync_knowledge() -> Knowledge:
    return Knowledge(
        vector_db=MongoVectorDb(
            collection_name="recipes",
            db_url=mdb_connection_string,
            search_index_name="recipes",
        )
    )


def create_async_knowledge(enable_batch: bool = False) -> Knowledge:
    if enable_batch:
        return Knowledge(
            vector_db=MongoVectorDb(
                collection_name="documents",
                db_url=mdb_connection_string,
                database="agno",
                embedder=OpenAIEmbedder(enable_batch=True),
            )
        )
    return Knowledge(
        vector_db=MongoVectorDb(
            collection_name="recipes",
            db_url=mdb_connection_string,
        )
    )


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
def create_sync_agent(knowledge: Knowledge) -> Agent:
    return Agent(knowledge=knowledge)


def create_async_agent(knowledge: Knowledge, enable_batch: bool = False) -> Agent:
    if enable_batch:
        return Agent(
            model=OpenAIChat(id="gpt-5.2"),
            knowledge=knowledge,
            search_knowledge=True,
            read_chat_history=True,
        )
    return Agent(knowledge=knowledge)


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
def run_sync() -> None:
    knowledge = create_sync_knowledge()
    knowledge.insert(
        name="Recipes",
        url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf",
        metadata={"doc_type": "recipe_book"},
    )

    agent = create_sync_agent(knowledge)
    agent.print_response("如何制作泰式咖喱？", markdown=True)


async def run_async(enable_batch: bool = False) -> None:
    knowledge = create_async_knowledge(enable_batch=enable_batch)
    agent = create_async_agent(knowledge, enable_batch=enable_batch)

    if enable_batch:
        await knowledge.ainsert(path="cookbook/07_knowledge/testing_resources/cv_1.pdf")
        await agent.aprint_response(
            "你能告诉我关于候选人的什么信息，他的技能是什么？",
            markdown=True,
        )
    else:
        await knowledge.ainsert(
            url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
        )
        await agent.aprint_response("如何制作泰式咖喱？", markdown=True)


if __name__ == "__main__":
    run_sync()
    asyncio.run(run_async(enable_batch=False))
    asyncio.run(run_async(enable_batch=True))

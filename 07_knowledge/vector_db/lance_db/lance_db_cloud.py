"""
LanceDB Cloud 连接测试。

需要环境变量：
- LANCE_DB_URI: LanceDB Cloud 数据库 URI（例如 db://your-database-id）
- LANCE_DB_API_KEY 或 LANCEDB_API_KEY: LanceDB Cloud API 密钥

从仓库根目录加载环境变量运行（例如 direnv）：
  .venvs/demo/bin/python cookbook/07_knowledge/vector_db/lance_db_cloud/lance_db_cloud.py
"""

import asyncio
import os

from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
TABLE_NAME = "agno_cloud_test"
URI = os.getenv("LANCE_DB_URI")
API_KEY = os.getenv("LANCE_DB_API_KEY") or os.getenv("LANCEDB_API_KEY")


# ---------------------------------------------------------------------------
# 创建知识库
# ---------------------------------------------------------------------------
# 云向量数据库和知识实例在验证所需环境变量后
# 在 `main()` 中创建。


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
def main():
    if not URI:
        print("设置 LANCE_DB_URI（例如 db://your-database-id）")
        return

    # ---------------------------------------------------------------------------
    # 创建知识库
    # ---------------------------------------------------------------------------
    vector_db = LanceDb(
        uri=URI,
        table_name=TABLE_NAME,
        api_key=API_KEY,
    )

    knowledge = Knowledge(
        name="LanceDB Cloud Test",
        description="Agno Knowledge with LanceDB Cloud",
        vector_db=vector_db,
    )

    async def run():
        print("插入测试内容...")
        await knowledge.ainsert(
            name="cloud_test_doc",
            text_content="LanceDB Cloud 是一个托管的向量数据库。"
            "Agno 通过带有 uri 和 api_key 的 LanceDb 向量存储支持它。"
            "使用 db:// URI 并设置 LANCEDB_API_KEY 进行云连接。",
            metadata={"source": "lance_db_cloud_cookbook"},
        )

        print("搜索'vector database'...")
        results = knowledge.search("vector database", max_results=3)
        print(f"找到 {len(results)} 个文档")
        for i, doc in enumerate(results):
            print(f"  [{i + 1}] {doc.name}: {doc.content[:80]}...")

        print("删除测试文档...")
        vector_db.delete_by_name("cloud_test_doc")
        print("完成。")

    asyncio.run(run())


if __name__ == "__main__":
    main()

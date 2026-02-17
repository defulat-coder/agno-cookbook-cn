"""
Azure Blob 存储内容源知识库
============================

从 Azure Blob 存储容器加载文件和文件夹到您的知识库。
使用 Azure AD 客户端凭证流进行身份验证。

特性：
- 递归加载单个 blob 或整个前缀（文件夹）
- 支持任何 Azure 存储账户
- 自动文件类型检测和读取器选择
- 为每个文件存储丰富的元数据（存储账户、容器、路径）

需求：
- Azure AD 应用注册，包含：
  - 应用程序（客户端）ID
  - 客户端密钥
  - 存储账户上的存储 Blob 数据读取者角色
- 存储账户名称和容器名称

设置：
    1. 在 Azure AD 中注册应用（portal.azure.com）
    2. 在存储账户上为应用分配"存储 Blob 数据读取者"角色
    3. 创建客户端密钥
    4. 设置环境变量（见下文）

环境变量：
    AZURE_TENANT_ID           - Azure AD 租户 ID
    AZURE_CLIENT_ID           - 应用注册客户端 ID
    AZURE_CLIENT_SECRET       - 应用注册客户端密钥
    AZURE_STORAGE_ACCOUNT_NAME - 存储账户名称（不带 .blob.core.windows.net）
    AZURE_CONTAINER_NAME      - 容器名称

运行此示例：
    python cookbook/07_knowledge/cloud/azure_blob.py
"""

from os import getenv

from agno.knowledge.knowledge import Knowledge
from agno.knowledge.remote_content import AzureBlobConfig
from agno.vectordb.pgvector import PgVector

# 配置 Azure Blob 存储内容源
# 所有凭证应来自环境变量
azure_config = AzureBlobConfig(
    id="company-docs",
    name="Company Documents",
    tenant_id=getenv("AZURE_TENANT_ID"),
    client_id=getenv("AZURE_CLIENT_ID"),
    client_secret=getenv("AZURE_CLIENT_SECRET"),
    storage_account=getenv("AZURE_STORAGE_ACCOUNT_NAME"),
    container=getenv("AZURE_CONTAINER_NAME"),
)

# 创建以 Azure Blob 存储作为内容源的 Knowledge
knowledge = Knowledge(
    name="Azure Blob Knowledge",
    vector_db=PgVector(
        table_name="azure_blob_knowledge",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    ),
    content_sources=[azure_config],
)

if __name__ == "__main__":
    # 从 Azure Blob 存储插入单个文件
    print("从 Azure Blob 存储插入单个文件...")
    knowledge.insert(
        name="DeepSeek Paper",
        remote_content=azure_config.file("DeepSeek_R1.pdf"),
    )

    # 插入整个文件夹（前缀）
    print("从 Azure Blob 存储插入文件夹...")
    knowledge.insert(
        name="Research Papers",
        remote_content=azure_config.folder("testfolder/"),
    )

    # 搜索知识库
    print("搜索知识库...")
    results = knowledge.search("DeepSeek 是什么？")
    for doc in results:
        print(f"- {doc.name}: {doc.content[:100]}...")

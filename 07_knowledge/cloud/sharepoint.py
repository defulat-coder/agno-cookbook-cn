"""
SharePoint 内容源知识库
=======================

从 SharePoint 文档库加载文件和文件夹到您的知识库。
使用带有 OAuth2 客户端凭证流的 Microsoft Graph API。

特性：
- 递归加载单个文件或整个文件夹
- 支持任何 SharePoint Online 站点
- 自动文件类型检测和读取器选择
- 为每个文件存储丰富的元数据（站点、路径、文件名）

需求：
- Azure AD 应用注册，包含：
  - 应用程序（客户端）ID
  - 客户端密钥
  - API 权限：Sites.Read.All（应用程序）
- SharePoint 站点 ID 或站点路径

设置：
    1. 在 Azure AD 中注册应用（portal.azure.com）
    2. 添加 API 权限：Microsoft Graph > Sites.Read.All（应用程序）
    3. 授予管理员同意
    4. 创建客户端密钥
    5. 设置环境变量（见下文）

环境变量：
    SHAREPOINT_TENANT_ID    - Azure AD 租户 ID
    SHAREPOINT_CLIENT_ID    - 应用注册客户端 ID
    SHAREPOINT_CLIENT_SECRET - 应用注册客户端密钥
    SHAREPOINT_HOSTNAME     - 例如："contoso.sharepoint.com"
    SHAREPOINT_SITE_ID      - 完整站点 ID（hostname,guid,guid 格式）

运行此示例：
    python cookbook/07_knowledge/cloud/sharepoint.py
"""

from os import getenv

from agno.knowledge.knowledge import Knowledge
from agno.knowledge.remote_content import SharePointConfig
from agno.vectordb.pgvector import PgVector

# 配置 SharePoint 内容源
# 所有凭证应来自环境变量
sharepoint_config = SharePointConfig(
    id="company-docs",
    name="Company Documents",
    tenant_id=getenv("SHAREPOINT_TENANT_ID"),
    client_id=getenv("SHAREPOINT_CLIENT_ID"),
    client_secret=getenv("SHAREPOINT_CLIENT_SECRET"),
    hostname=getenv("SHAREPOINT_HOSTNAME"),  # 例如："contoso.sharepoint.com"
    # 选项 1：直接提供 site_id（推荐，更快）
    site_id=getenv("SHAREPOINT_SITE_ID"),  # 例如："contoso.sharepoint.com,guid1,guid2"
    # 选项 2：或提供 site_path 让 API 查找站点 ID
    # site_path="/sites/documents",
)

# 创建以 SharePoint 作为内容源的 Knowledge
knowledge = Knowledge(
    name="SharePoint Knowledge",
    vector_db=PgVector(
        table_name="sharepoint_knowledge",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    ),
    content_sources=[sharepoint_config],
)

if __name__ == "__main__":
    # 从 SharePoint 插入单个文件
    print("从 SharePoint 插入单个文件...")
    knowledge.insert(
        name="Q1 Report",
        remote_content=sharepoint_config.file("Shared Documents/Reports/q1-2024.pdf"),
    )

    # 插入整个文件夹（递归）
    print("从 SharePoint 插入文件夹...")
    knowledge.insert(
        name="Policy Documents",
        remote_content=sharepoint_config.folder("Shared Documents/Policies"),
    )

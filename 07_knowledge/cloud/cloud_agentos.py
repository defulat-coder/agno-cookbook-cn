"""
知识库内容源 — DX 设计
======================

此示例演示从各种远程源（S3、GCS、SharePoint、GitHub 等）
向知识库添加内容的 API。

核心概念：
- RemoteContentConfig：配置远程内容源的基类
- 每种源类型都有自己的配置：S3Config、GcsConfig、SharePointConfig、GitHubConfig
- 配置通过 `content_sources` 参数在 Knowledge 上注册
- 配置具有工厂方法（.file()、.folder()）来创建内容引用
- 内容引用传递给 knowledge.insert()
"""

from os import getenv

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.remote_content import (
    AzureBlobConfig,
    GitHubConfig,
    SharePointConfig,
)
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.vectordb.pgvector import PgVector

# 数据库连接
contents_db = PostgresDb(
    db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    knowledge_table="knowledge_contents",
)
vector_db = PgVector(
    table_name="knowledge_vectors",
    db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
)

# 定义内容源配置（凭证可以来自环境变量）

sharepoint = SharePointConfig(
    id="sharepoint",
    name="Product Data",
    tenant_id=getenv("SHAREPOINT_TENANT_ID"),  # 或 os.getenv("SHAREPOINT_TENANT_ID")
    client_id=getenv("SHAREPOINT_CLIENT_ID"),
    client_secret=getenv("SHAREPOINT_CLIENT_SECRET"),
    hostname=getenv("SHAREPOINT_HOSTNAME"),
    site_id=getenv("SHAREPOINT_SITE_ID"),
)

github_docs = GitHubConfig(
    id="my-repo",
    name="My Repository",
    repo="private/repo",
    token=getenv("GITHUB_TOKEN"),  # 具有 Contents: read 的细粒度 PAT
    branch="main",
)

azure_blob = AzureBlobConfig(
    id="azure-blob",
    name="Azure Blob",
    tenant_id=getenv("AZURE_TENANT_ID"),
    client_id=getenv("AZURE_CLIENT_ID"),
    client_secret=getenv("AZURE_CLIENT_SECRET"),
    storage_account=getenv("AZURE_STORAGE_ACCOUNT_NAME"),
    container=getenv("AZURE_CONTAINER_NAME"),
)

# 创建包含内容源的 Knowledge
knowledge = Knowledge(
    name="Company Knowledge Base",
    description="Unified knowledge from multiple sources",
    contents_db=contents_db,
    vector_db=vector_db,
    content_sources=[sharepoint, github_docs, azure_blob],
)

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    knowledge=knowledge,
    search_knowledge=True,
)

agent_os = AgentOS(
    knowledge=[knowledge],
    agents=[agent],
)
app = agent_os.get_app()

# ============================================================================
# 运行 AgentOS
# ============================================================================
if __name__ == "__main__":
    # 提供由 AgentOS 公开的 FastAPI 应用。本地开发时使用 reload=True。
    agent_os.serve(app="cloud_agentos:app", reload=True)


# ============================================================================
# 使用 Knowledge API
# ============================================================================
"""
AgentOS 运行后，使用 Knowledge API 从远程源上传内容。

## 步骤 1：获取可用的内容源

    curl -s http://localhost:7777/v1/knowledge/company-knowledge-base/config | jq

响应：
    {
      "remote_content_sources": [
        {"id": "my-repo", "name": "My Repository", "type": "github"},
        ...
      ]
    }

## 步骤 2：上传内容

    curl -X POST http://localhost:7777/v1/knowledge/company-knowledge-base/remote-content \\
      -H "Content-Type: application/json" \\
      -d '{
        "name": "Documentation",
        "config_id": "my-repo",
        "path": "docs/README.md"
      }'
"""

"""
AgentOS 中的多个知识库实例
=========================

此示例演示如何在 AgentOS 中配置多个知识库实例，
每个实例都有隔离的内容。

核心概念：
- 多个知识库实例可以共享相同的 vector_db 和 contents_db
- 每个实例通过其 `name` 属性标识
- 内容通过 `linked_to` 字段按实例隔离
- 具有相同名称但不同数据库的实例被视为独立的
- /knowledge/config 端点返回所有已注册的实例
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.knowledge.knowledge import Knowledge
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

# 创建知识库实例
company_knowledge = Knowledge(
    name="Company Knowledge Base",
    description="Unified knowledge from multiple sources",
    contents_db=contents_db,
    vector_db=vector_db,
    # content_sources=[sharepoint, github_docs, azure_blob],
)

personal_knowledge = Knowledge(
    name="Personal Knowledge Base",
    description="Unified knowledge from multiple sources",
    contents_db=contents_db,
    vector_db=vector_db,
    # content_sources=[sharepoint, github_docs, azure_blob],
)

company_knowledge_db = PostgresDb(
    db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    knowledge_table="knowledge_contents2",
)

company_knowledge_additional = Knowledge(
    name="Company Knowledge Base",
    description="Unified knowledge from multiple sources",
    contents_db=company_knowledge_db,
    vector_db=vector_db,
    # content_sources=[sharepoint, github_docs, azure_blob],
)

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    knowledge=company_knowledge,
    search_knowledge=True,
)

agent_os = AgentOS(
    knowledge=[company_knowledge, company_knowledge_additional, personal_knowledge],
    agents=[agent],
)
app = agent_os.get_app()

# ============================================================================
# 运行 AgentOS
# ============================================================================
if __name__ == "__main__":
    # 提供由 AgentOS 公开的 FastAPI 应用。本地开发时使用 reload=True。
    agent_os.serve(app="multiple_knowledge_instances:app", reload=True)

"""
AgentOS 知识库（同步和异步）
==================================

演示 AgentOS 知识库与同步和异步数据库设置的集成。
"""

import asyncio
from textwrap import dedent

from agno.agent import Agent
from agno.db.postgres import AsyncPostgresDb, PostgresDb
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.vectordb.pgvector import PgVector, SearchType

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
USE_ASYNC = False

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

sync_documents_db = PostgresDb(
    db_url=db_url,
    id="agno_knowledge_db",
    knowledge_table="agno_knowledge_contents",
)
sync_faq_db = PostgresDb(
    db_url=db_url,
    id="agno_faq_db",
    knowledge_table="agno_faq_contents",
)

async_documents_db = AsyncPostgresDb(
    db_url=db_url,
    id="agno_knowledge_db",
    knowledge_table="agno_knowledge_contents",
)
async_faq_db = AsyncPostgresDb(
    db_url=db_url,
    id="agno_faq_db",
    knowledge_table="agno_faq_contents",
)

sync_documents_knowledge = Knowledge(
    vector_db=PgVector(
        db_url=db_url,
        table_name="agno_knowledge_vectors",
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    ),
    contents_db=sync_documents_db,
)

sync_faq_knowledge = Knowledge(
    vector_db=PgVector(
        db_url=db_url,
        table_name="agno_faq_vectors",
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    ),
    contents_db=sync_faq_db,
)

async_documents_knowledge = Knowledge(
    vector_db=PgVector(
        db_url=db_url,
        table_name="agno_knowledge_vectors",
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    ),
    contents_db=async_documents_db,
)

async_faq_knowledge = Knowledge(
    vector_db=PgVector(
        db_url=db_url,
        table_name="agno_faq_vectors",
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    ),
    contents_db=async_faq_db,
)

# ---------------------------------------------------------------------------
# Create Agents
# ---------------------------------------------------------------------------
sync_knowledge_agent = Agent(
    name="Knowledge Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    knowledge=sync_documents_knowledge,
    search_knowledge=True,
    db=sync_documents_db,
    enable_user_memories=True,
    add_history_to_context=True,
    markdown=True,
    instructions=[
        "你是一个有权访问 Agno 文档的有用助手。",
        "搜索知识库以回答有关 Agno 的问题。",
    ],
)

async_knowledge_agent = Agent(
    name="Knowledge Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    knowledge=async_documents_knowledge,
    search_knowledge=True,
    db=async_documents_db,
    enable_user_memories=True,
    add_history_to_context=True,
    markdown=True,
    instructions=[
        "你是一个有权访问 Agno 文档的有用助手。",
        "搜索知识库以回答有关 Agno 的问题。",
    ],
)

# ---------------------------------------------------------------------------
# Create AgentOS
# ---------------------------------------------------------------------------
sync_agent_os = AgentOS(
    description="带 AgentOS 知识库的示例应用",
    agents=[sync_knowledge_agent],
    knowledge=[sync_faq_knowledge],
)

async_agent_os = AgentOS(
    description="带 AgentOS 知识库的示例应用（异步）",
    agents=[async_knowledge_agent],
    knowledge=[async_faq_knowledge],
)

agent_os = async_agent_os if USE_ASYNC else sync_agent_os
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if USE_ASYNC:
        asyncio.run(
            async_documents_knowledge.ainsert(
                name="Agno Docs",
                url="https://docs.agno.com/llms-full.txt",
                skip_if_exists=True,
            )
        )
        asyncio.run(
            async_faq_knowledge.ainsert(
                name="Agno FAQ",
                text_content=dedent("""
                什么是 Agno？
                Agno 是一个用于构建 agent 的框架。
                使用它来构建具有记忆、知识、
                人机交互和 MCP 支持的多 agent 系统。
            """),
                skip_if_exists=True,
            )
        )
    else:
        sync_documents_knowledge.insert(
            name="Agno Docs",
            url="https://docs.agno.com/llms-full.txt",
            skip_if_exists=True,
        )
        sync_faq_knowledge.insert(
            name="Agno FAQ",
            text_content=dedent("""
            什么是 Agno？
            Agno 是一个用于构建 agent 的框架。
            使用它来构建具有记忆、知识、
            人机交互和 MCP 支持的多 agent 系统。
        """),
            skip_if_exists=True,
        )

    agent_os.serve(app="agentos_knowledge:app", reload=True)

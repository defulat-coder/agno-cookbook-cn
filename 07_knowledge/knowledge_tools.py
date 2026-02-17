"""
这是一个具有推理能力的工具，允许 Agent 从知识库中搜索和分析信息。

1. 运行：`uv pip install openai agno lancedb tantivy sqlalchemy` 安装依赖
2. 导出你的 OPENAI_API_KEY
3. 运行：`python cookbook/07_knowledge/knowledge_tools.py` 执行 Agent
"""

from agno.agent import Agent
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.tools.knowledge import KnowledgeTools
from agno.vectordb.lancedb import LanceDb, SearchType

# 创建一个包含来自 URL 信息的知识库
agno_docs = Knowledge(
    # 使用 LanceDB 作为向量数据库，并将嵌入存储在 `agno_docs` 表中
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="agno_docs",
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    ),
)
# 向知识库添加内容
agno_docs.insert(url="https://docs.agno.com/llms-full.txt")

knowledge_tools = KnowledgeTools(
    knowledge=agno_docs,
    enable_think=True,
    enable_search=True,
    enable_analyze=True,
    add_few_shot=True,
)

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[knowledge_tools],
    markdown=True,
)

if __name__ == "__main__":
    agent.print_response(
        "How do I build a team of agents in agno?",
        markdown=True,
        stream=True,
    )

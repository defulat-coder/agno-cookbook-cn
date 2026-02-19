"""
知识库工具（Knowledge Tools）
===============

演示推理 Cookbook 示例。
"""

from agno.agent import Agent
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.tools.knowledge import KnowledgeTools
from agno.vectordb.lancedb import LanceDb, SearchType


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    # 创建包含 URL 信息的知识库
    agno_docs = Knowledge(
        # 使用 LanceDB 作为向量数据库，将嵌入向量存储在 `agno_docs` 表中
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
            "如何在 agno 中构建一个 Agent 团队？",
            markdown=True,
            stream=True,
        )


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()

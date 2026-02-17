"""
ChromaDB 使用倒数排名融合（RRF）的混合搜索

此示例演示如何使用 ChromaDB 的混合搜索，
它结合了密集向量相似性搜索（语义）和
使用 RRF 融合的全文搜索（关键词/词汇）。

混合搜索在以下情况下很有用：
- 结合语义理解和精确关键词匹配
- 提高具有特定术语的查询的检索准确性
- 处理概念和词汇搜索需求

RRF 算法使用以下公式融合两种搜索方法的排名：
    RRF(d) = sum(1 / (k + rank_i(d))) 对于每个排名 i
"""

import asyncio
from textwrap import dedent

from agno.agent import Agent
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.vectordb.chroma import ChromaDb, SearchType

# ---------------------------------------------------------------------------
# 创建知识库
# ---------------------------------------------------------------------------
knowledge = Knowledge(
    name="Agno Documentation",
    description="Knowledge base for Agno framework documentation",
    vector_db=ChromaDb(
        name="agno_docs",
        path="tmp/chromadb_hybrid",
        persistent_client=True,
        # 启用混合搜索 - 使用 RRF 结合向量相似性和关键词匹配
        search_type=SearchType.hybrid,
        # RRF（倒数排名融合）常数 - 控制排名平滑度。
        # 较高的值（例如 60）给予排名较低的结果更多权重，
        # 较低的值使排名靠前的结果更占主导地位。默认值为 60（根据原始 RRF 论文）。
        hybrid_rrf_k=60,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    ),
    max_results=10,
)

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
description = dedent(
    """\
    你是 AgnoAssist — 一个 AI Agent，旨在帮助开发者学习和掌握 Agno 框架。
    你的目标是提供清晰的解释和完整的、可运行的代码示例，帮助用户理解并有效使用 Agno 和 AgentOS。\
    """
)

instructions = dedent(
    """\
    你的使命是为 Agno 生态系统提供全面的、以开发者为中心的支持。

    遵循此结构化流程以确保准确和可操作的响应：

    1. **分析请求**
        - 确定查询是否需要知识查找、代码生成或两者兼有。
        - 所有概念都在 Agno 的上下文中 - 你不需要澄清这一点。

    分析后，立即开始搜索过程（无需请求确认）。

    2. **搜索流程**
        - 使用 `search_knowledge` 工具检索相关概念、代码示例和实现细节。
        - 执行迭代搜索，直到你收集到足够的信息或用尽相关术语。

    一旦你的研究完成，决定是否需要创建代码。
    如果需要，询问用户是否希望你为他们生成一个 Agent。

    3. **代码创建**
        - 提供可以直接运行的完整工作代码示例。
        - 始终使用 `agent.run()`（而不是 `agent.print_response()`）。
        - 包括所有导入、设置和依赖项。
        - 添加清晰的注释、类型提示和文档字符串。
        - 使用示例查询演示用法。

        示例：
        ```python
        from agno.agent import Agent
        from agno.tools.websearch import WebSearchTools

        agent = Agent(tools=[WebSearchTools()])

        response = agent.run("法国发生了什么？")
        print(response)
        ```
    """
)

# 使用混合搜索知识库创建 agent
agent = Agent(
    name="Agno Knowledge Agent",
    model=OpenAIChat(id="gpt-5.2"),
    knowledge=knowledge,
    instructions=instructions,
    description=description,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 将 Agno 文档加载到知识库中
    asyncio.run(
        knowledge.ainsert(
            name="Agno Documentation",
            url="https://docs.agno.com/llms-full.txt",
        )
    )

    # 混合搜索将：
    # 1. 查找语义相似的文档（通过密集嵌入）
    # 2. 查找包含查询关键词的文档（通过 FTS）
    # 3. 使用 RRF 融合结果以获得最佳排名
    agent.print_response("如何创建一个带工具的 agent？", markdown=True)

"""
智能知识库搜索 - 带知识库的 Agent
============================================================
本示例展示如何为 Agent 配备可搜索的知识库。
Agent 可以在文档（PDF、文本、URL）中进行搜索以回答问题。

核心概念：
- Knowledge（知识库）：可搜索的文档集合（PDF、文本、URL）
- Agentic search（智能搜索）：Agent 自主决定何时搜索知识库
- Hybrid search（混合搜索）：结合语义相似度与关键词匹配

可尝试的示例提示：
- "Agno 是什么？"
- "AgentOS 是什么？"
"""

import os

from dotenv import load_dotenv

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAILike
from agno.vectordb.chroma import ChromaDb
from agno.vectordb.search import SearchType

load_dotenv()

# ---------------------------------------------------------------------------
# 初始化配置
# ---------------------------------------------------------------------------
agent_db = SqliteDb(db_file="tmp/agents.db")

knowledge = Knowledge(
    name="Agno Documentation",
    vector_db=ChromaDb(
        name="agno_docs",
        collection="agno_docs",
        path="tmp/chromadb",
        persistent_client=True,
        # 启用混合搜索 - 使用 RRF 算法结合向量相似度与关键词匹配
        search_type=SearchType.hybrid,
        # RRF（倒数排名融合）常数 - 控制排名的平滑程度。
        # 值越大（如 60），低排名结果获得的权重越多；
        # 值越小，排名靠前的结果更具主导性。默认值为 60（参考原始 RRF 论文）。
        hybrid_rrf_k=60,
        embedder=GeminiEmbedder(id="gemini-embedding-001"),
    ),
    # 每次查询返回 5 条结果
    max_results=5,
    # 将内容的元数据存储在 Agent 数据库中，表名为 "agno_knowledge"
    contents_db=agent_db,
)

# ---------------------------------------------------------------------------
# Agent 指令
# ---------------------------------------------------------------------------
instructions = """\
你是 Agno 框架和 AI Agent 开发方面的专家。

## 工作流程

1. 搜索
   - 对于关于 Agno 的问题，始终先搜索知识库
   - 从查询中提取关键概念以进行有效搜索

2. 综合
   - 整合多条搜索结果中的信息
   - 优先使用官方文档而非通用知识

3. 呈现
   - 以直接回答开头
   - 在有帮助时附上代码示例
   - 保持实用和可操作

## 规则

- 回答 Agno 问题前始终先搜索知识库
- 如果知识库中没有答案，请如实告知
- 对于实现相关的问题附上代码片段
- 保持简洁——开发者想要答案，不是长篇大论\
"""

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent_with_knowledge = Agent(
    name="Agent with Knowledge",
    model=OpenAILike(
        id=os.getenv("MODEL_ID", "GLM-4.7"),
        base_url=os.getenv("MODEL_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/"),
        api_key=os.getenv("MODEL_API_KEY"),
    ),
    instructions=instructions,
    knowledge=knowledge,
    search_knowledge=True,
    db=agent_db,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 将 Agno 文档的介绍页加载到知识库中
    # 为了保持示例简洁，这里只加载 1 个文件。
    knowledge.insert(
        name="Agno Introduction", url="https://docs.agno.com/introduction.md"
    )

    agent_with_knowledge.print_response(
        "Agno 是什么？",
        stream=True,
    )

# ---------------------------------------------------------------------------
# 更多示例
# ---------------------------------------------------------------------------
"""
加载你自己的知识：

1. 从 URL 加载
   knowledge.insert(url="https://example.com/docs.pdf")

2. 从本地文件加载
   knowledge.insert(path="path/to/document.pdf")

3. 直接从文本加载
   knowledge.insert(text_content="Your content here...")

混合搜索的组成：
- 语义搜索：查找概念上相似的内容
- 关键词搜索：查找精确的词项匹配
- 使用倒数排名融合（RRF）合并结果

Agent 会在需要时自动搜索知识库（智能搜索）。
"""

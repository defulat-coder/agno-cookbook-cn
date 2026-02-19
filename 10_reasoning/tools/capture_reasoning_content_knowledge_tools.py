"""
捕获推理内容 - 知识库工具
=========================================

演示推理 Cookbook 示例。
"""

import asyncio
from textwrap import dedent

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
    print("正在设置 URL 知识库...")
    agno_docs = Knowledge(
        # 使用 LanceDB 作为向量数据库
        vector_db=LanceDb(
            uri="tmp/lancedb",
            table_name="cookbook_knowledge_tools",
            search_type=SearchType.hybrid,
            embedder=OpenAIEmbedder(id="text-embedding-3-small"),
        ),
    )
    # 向知识库添加内容
    asyncio.run(agno_docs.ainsert(url="https://www.paulgraham.com/read.html"))
    print("知识库准备就绪。")

    print("\n=== 示例 1：在非流式模式下使用 KnowledgeTools ===\n")

    # 创建带有 KnowledgeTools 的 Agent
    agent = Agent(
        model=OpenAIChat(id="gpt-4o"),
        tools=[
            KnowledgeTools(
                knowledge=agno_docs,
                enable_think=True,
                enable_search=True,
                enable_analyze=True,
                add_instructions=True,
            )
        ],
        instructions=dedent("""\
            你是一位拥有强大分析能力的专业问题解决助手！请使用知识库工具整理思路、搜索信息，
            并逐步分析结果。
            \
        """),
        markdown=True,
    )

    # 使用 agent.run() 运行 Agent（非流式）以获取响应
    print("使用 KnowledgeTools 运行（非流式）...")
    response = agent.run(
        "Paul Graham 在这里关于阅读的必要性解释了什么？", stream=False
    )

    # 检查响应中的 reasoning_content
    print("\n--- 来自响应的 reasoning_content ---")
    if hasattr(response, "reasoning_content") and response.reasoning_content:
        print("[OK] 非流式响应中找到 reasoning_content")
        print(f"   长度：{len(response.reasoning_content)} 个字符")
        print("\n=== reasoning_content 预览（非流式） ===")
        preview = response.reasoning_content[:1000]
        if len(response.reasoning_content) > 1000:
            preview += "..."
        print(preview)
    else:
        print("[未找到] 非流式响应中不存在 reasoning_content")

    print("\n\n=== 示例 2：在流式模式下使用 KnowledgeTools ===\n")

    # 为流式输出创建新的 Agent
    streaming_agent = Agent(
        model=OpenAIChat(id="gpt-4o"),
        tools=[
            KnowledgeTools(
                knowledge=agno_docs,
                enable_think=True,
                enable_search=True,
                enable_analyze=True,
                add_instructions=True,
            )
        ],
        instructions=dedent("""\
            你是一位拥有强大分析能力的专业问题解决助手！请使用知识库工具整理思路、搜索信息，
            并逐步分析结果。
            \
        """),
        markdown=True,
    )

    # 处理流式响应并查找最终的 RunOutput
    print("使用 KnowledgeTools 运行（流式）...")
    final_response = None
    for event in streaming_agent.run(
        "Paul Graham 在这里关于阅读的必要性解释了什么？",
        stream=True,
        stream_events=True,
    ):
        # 实时打印内容（可选）
        if hasattr(event, "content") and event.content:
            print(event.content, end="", flush=True)

        # 流中的最终事件应该是 RunOutput 对象
        if hasattr(event, "reasoning_content"):
            final_response = event

    print("\n\n--- 来自最终流式事件的 reasoning_content ---")
    if (
        final_response
        and hasattr(final_response, "reasoning_content")
        and final_response.reasoning_content
    ):
        print("[OK] 最终流式事件中找到 reasoning_content")
        print(f"   长度：{len(final_response.reasoning_content)} 个字符")
        print("\n=== reasoning_content 预览（流式） ===")
        preview = final_response.reasoning_content[:1000]
        if len(final_response.reasoning_content) > 1000:
            preview += "..."
        print(preview)
    else:
        print("[未找到] 最终流式事件中不存在 reasoning_content")


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()

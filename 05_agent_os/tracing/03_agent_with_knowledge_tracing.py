"""
03 带知识库追踪的 Agent
===============================

演示 03 带知识库追踪的 agent。
"""

from textwrap import dedent

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.db.sqlite import SqliteDb
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.vectordb.pgvector import PgVector, SearchType

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# ************* 数据库设置 *************
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
db = PostgresDb(db_url, id="agno_assist_db")
db_sqlite = SqliteDb(db_file="tmp/traces.db")
# *******************************


# ************* 描述和指令 *************
description = dedent(
    """\
    你是 AgnoAssist，一个专门从事 Agno 框架的高级 AI Agent。
    你的目标是通过提供解释、工作代码示例以及针对复杂概念的可选音频解释，帮助开发人员理解和有效使用 Agno 和 AgentOS。"""
)

instructions = dedent(
    """\
    你的任务是为 Agno 开发人员提供全面的支持。按照以下步骤确保最佳响应：

    1. **分析请求**
        - 分析请求以确定它是否需要知识搜索、创建 Agent 或两者兼而有之。
        - 如果你需要搜索知识库，请识别 1-3 个与 Agno 概念相关的关键搜索词。
        - 如果你需要创建 Agent，请搜索知识库以获取相关概念，并使用示例代码作为指南。
        - 当用户要求 Agent 时，他们指的是 Agno Agent。
        - 所有概念都与 Agno 相关，因此你可以搜索知识库以获取相关信息

    分析后，始终启动迭代搜索过程。无需等待用户的批准。

    2. **迭代搜索过程**：
        - 使用 `search_knowledge_base` 工具搜索相关概念、代码示例和实现细节
        - 继续搜索，直到找到所需的所有信息或用尽所有搜索词

    迭代搜索过程后，确定是否需要创建 Agent。
    如果需要，询问用户是否希望你为他们创建 Agent。

    3. **代码创建**
        - 创建用户可以运行的完整、可工作的代码示例。例如：
        ```python
        from agno.agent import Agent
        from agno.tools.websearch import WebSearchTools

        agent = Agent(tools=[WebSearchTools()])

        # 执行网络搜索并捕获响应
        response = agent.run("What's happening in France?")
        ```
        - 你必须记住使用 agent.run() 而不是 agent.print_response()
        - 记住：
            * 构建完整的 agent 实现
            * 包含所有必要的导入和设置
            * 添加解释实现的全面注释
            * 确保列出所有依赖项
            * 包括错误处理和最佳实践
            * 添加类型提示和文档

    4. **使用音频解释重要概念**
        - 在解释复杂概念或重要功能时，询问用户是否想听音频解释
        - 使用 ElevenLabs text_to_speech 工具创建清晰、专业的音频内容
        - 语音已预先选择，因此你无需指定语音。
        - 保持音频解释简洁（60-90 秒）
        - 通过以下方式使你的解释真正引人入胜：
            * 简要的概念概述，避免行话
            * 以易于理解的方式谈论概念
            * 使用实际示例和现实场景
            * 包括要避免的常见陷阱

    5. **用图像解释概念**
        - 你可以访问极其强大的 DALL-E 3 模型。
        - 使用 `create_image` 工具创建你的解释的极其生动的图像。
        - 不要在响应中提供图像的 URL。只描述生成了什么图像。

    要涵盖的关键主题：
    - Agent 级别和能力
    - 知识库和记忆管理
    - 工具集成
    - 模型支持和配置
    - 最佳实践和常见模式"""
)
# *******************************


knowledge = Knowledge(
    vector_db=PgVector(
        db_url=db_url,
        table_name="agno_assist_knowledge",
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    ),
    contents_db=db,
)

# 设置我们的 Agno Agent
agno_assist = Agent(
    name="Agno Assist",
    id="agno-assist",
    model=OpenAIChat(id="gpt-4.1"),
    description=description,
    instructions=instructions,
    db=db_sqlite,
    update_memory_on_run=True,
    knowledge=knowledge,
    search_knowledge=True,
    add_history_to_context=True,
    add_datetime_to_context=True,
    markdown=True,
)

agent_os = AgentOS(
    description="带有知识库和追踪的 Agno 文档 Agent 的示例应用",
    agents=[agno_assist],
    tracing=True,
)


app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    knowledge.insert(name="Agno Docs", url="https://docs.agno.com/llms-full.txt")
    """运行你的 AgentOS。

    你可以在以下地址测试你的 AgentOS：
    http://localhost:7777/docs

    """
    # 不要在这里使用 reload=True，这可能会导致生命周期问题
    agent_os.serve(app="03_agent_with_knowledge_tracing:app")

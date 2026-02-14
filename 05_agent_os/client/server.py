"""
Cookbook Client 示例的 AgentOS 服务器
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.team.team import Team
from agno.tools.calculator import CalculatorTools
from agno.tools.websearch import WebSearchTools
from agno.vectordb.chroma import ChromaDb
from agno.workflow.step import Step
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# =============================================================================
# 数据库配置
# =============================================================================

# SQLite 数据库用于 session、记忆和内容元数据
db = SqliteDb(db_file="tmp/cookbook_client.db")

# =============================================================================
# 知识库配置
# =============================================================================

knowledge = Knowledge(
    vector_db=ChromaDb(
        path="tmp/cookbook_chromadb",
        collection="cookbook_knowledge",
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    ),
    contents_db=db,  # 内容上传/管理端点所需
)

# =============================================================================
# Agent 配置
# =============================================================================

# Agent 1：带有计算器工具和记忆的助手
assistant = Agent(
    name="Assistant",
    model=OpenAIChat(id="gpt-5.2"),
    db=db,
    instructions=[
        "你是一个有帮助的 AI 助手。",
        "对任何数学运算使用计算器工具。",
        "你可以访问知识库 - 在被问及文档时搜索它。",
    ],
    markdown=True,
    update_memory_on_run=True,  # 03_memory_operations 所需
    tools=[CalculatorTools()],
    knowledge=knowledge,
    search_knowledge=True,
)

# Agent 2：具有网络搜索功能的研究员
researcher = Agent(
    name="Researcher",
    model=OpenAIChat(id="gpt-5.2"),
    db=db,
    instructions=[
        "你是一个研究助手。",
        "需要时搜索网络信息。",
        "提供经过充分研究的、准确的响应。",
    ],
    markdown=True,
    tools=[WebSearchTools()],
)

# =============================================================================
# 团队配置
# =============================================================================

research_team = Team(
    name="Research Team",
    model=OpenAIChat(id="gpt-5.2"),
    members=[assistant, researcher],
    instructions=[
        "你是一个协调多个专家的研究团队。",
        "将数学问题委托给助手。",
        "将研究问题委托给研究员。",
        "结合团队成员的见解以获得全面的答案。",
    ],
    markdown=True,
    db=db,
)

# =============================================================================
# 工作流配置
# =============================================================================

qa_workflow = Workflow(
    name="QA Workflow",
    description="A simple Q&A workflow that uses the assistant agent",
    db=db,
    steps=[
        Step(
            name="Answer Question",
            agent=assistant,
        ),
    ],
)

# =============================================================================
# AgentOS 配置
# =============================================================================

agent_os = AgentOS(
    id="cookbook-client-server",
    description="AgentOS server for running cookbook client examples",
    agents=[assistant, researcher],
    teams=[research_team],
    workflows=[qa_workflow],
    knowledge=[knowledge],
)

# FastAPI 应用实例（用于 uvicorn）
app = agent_os.get_app()

# =============================================================================
# 主入口点
# =============================================================================

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="server:app", reload=True)

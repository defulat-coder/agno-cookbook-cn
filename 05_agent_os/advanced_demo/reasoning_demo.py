"""运行 `uv pip install openai exa_py ddgs yfinance pypdf sqlalchemy 'fastapi[standard]' youtube-transcript-api python-docx agno` 以安装依赖。"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.team import Team
from agno.tools.knowledge import KnowledgeTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.websearch import WebSearchTools
from agno.vectordb.lancedb import LanceDb, SearchType

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
db = PostgresDb(db_url)


finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    id="finance-agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[
        WebSearchTools(
            enable_news=True,
        )
    ],
    instructions=["始终使用表格显示数据"],
    db=db,
    add_history_to_context=True,
    num_history_runs=5,
    add_datetime_to_context=True,
    markdown=True,
)

cot_agent = Agent(
    name="Chain-of-Thought Agent",
    role="Answer basic questions",
    id="cot-agent",
    model=OpenAIChat(id="gpt-5.2"),
    db=db,
    add_history_to_context=True,
    num_history_runs=3,
    add_datetime_to_context=True,
    markdown=True,
    reasoning=True,
)

reasoning_model_agent = Agent(
    name="Reasoning Model Agent",
    role="Reasoning about Math",
    id="reasoning-model-agent",
    model=OpenAIChat(id="gpt-4o"),
    reasoning_model=OpenAIChat(id="o3-mini"),
    instructions=["你是一个可以对数学进行推理的推理 agent。"],
    markdown=True,
    db=db,
)

reasoning_tool_agent = Agent(
    name="Reasoning Tool Agent",
    role="Answer basic questions",
    id="reasoning-tool-agent",
    model=OpenAIChat(id="gpt-5.2"),
    db=db,
    add_history_to_context=True,
    num_history_runs=3,
    add_datetime_to_context=True,
    markdown=True,
    tools=[ReasoningTools()],
)


web_agent = Agent(
    name="Web Search Agent",
    role="Handle web search requests",
    model=OpenAIChat(id="gpt-5.2"),
    id="web_agent",
    tools=[WebSearchTools()],
    instructions="始终包含来源",
    add_datetime_to_context=True,
    db=db,
)

agno_docs = Knowledge(
    # 使用 LanceDB 作为向量数据库，并将嵌入存储在 `agno_docs` 表中
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="agno_docs",
        search_type=SearchType.hybrid,
    ),
)

knowledge_tools = KnowledgeTools(
    knowledge=agno_docs,
    enable_think=True,
    enable_search=True,
    enable_analyze=True,
    add_few_shot=True,
)
knowledge_agent = Agent(
    id="knowledge_agent",
    name="Knowledge Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[knowledge_tools],
    markdown=True,
    db=db,
)

reasoning_finance_team = Team(
    name="Reasoning Finance Team",
    model=OpenAIChat(id="gpt-4o"),
    members=[
        web_agent,
        finance_agent,
    ],
    # reasoning=True,
    tools=[ReasoningTools(add_instructions=True)],
    # 取消注释以使用知识库工具
    # tools=[knowledge_tools],
    id="reasoning_finance_team",
    instructions=[
        "仅输出最终答案，不输出其他文本。",
        "使用表格显示数据",
    ],
    markdown=True,
    show_members_responses=True,
    add_datetime_to_context=True,
    db=db,
)


# 设置我们的 AgentOS 应用
agent_os = AgentOS(
    description="Example OS setup",
    agents=[
        finance_agent,
        cot_agent,
        reasoning_model_agent,
        reasoning_tool_agent,
        knowledge_agent,
    ],
    teams=[reasoning_finance_team],
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agno_docs.insert(name="Agno Docs", url="https://www.paulgraham.com/read.html")
    agent_os.serve(app="reasoning_demo:app", reload=True)

"""
Teams 演示
==========

演示 teams demo。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.anthropic import Claude
from agno.models.google.gemini import Gemini
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.team.team import Team
from agno.tools.exa import ExaTools
from agno.tools.websearch import WebSearchTools
from agno.tools.yfinance import YFinanceTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
db = PostgresDb(db_url)

file_agent = Agent(
    name="File Upload Agent",
    id="file-upload-agent",
    role="Answer questions about the uploaded files",
    model=Claude(id="claude-3-7-sonnet-latest"),
    db=db,
    update_memory_on_run=True,
    instructions=[
        "你是一个可以分析文件的 AI agent。",
        "你被给定一个文件，你需要回答有关该文件的问题。",
    ],
    markdown=True,
)

video_agent = Agent(
    name="Video Understanding Agent",
    model=Gemini(id="gemini-3-flash-preview"),
    id="video-understanding-agent",
    role="Answer questions about video files",
    db=db,
    update_memory_on_run=True,
    add_history_to_context=True,
    add_datetime_to_context=True,
    markdown=True,
)

audio_agent = Agent(
    name="Audio Understanding Agent",
    id="audio-understanding-agent",
    role="Answer questions about audio files",
    model=OpenAIChat(id="gpt-4o-audio-preview"),
    db=db,
    update_memory_on_run=True,
    add_history_to_context=True,
    add_datetime_to_context=True,
    markdown=True,
)

web_agent = Agent(
    name="Web Agent",
    role="Search the web for information",
    model=OpenAIChat(id="gpt-4o"),
    tools=[WebSearchTools()],
    id="web_agent",
    instructions=[
        "你是一位经验丰富的网络研究员和新闻分析师。",
    ],
    update_memory_on_run=True,
    markdown=True,
    db=db,
)

finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    id="finance_agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[YFinanceTools()],
    instructions=[
        "你是一位熟练的金融分析师，擅长市场数据分析。",
        "分析金融数据时遵循以下步骤：",
        "从最新股价、交易量和每日范围开始",
        "呈现详细的分析师建议和共识目标价格",
        "包括关键指标：市盈率、市值、52周范围",
        "分析交易模式和成交量趋势",
    ],
    update_memory_on_run=True,
    markdown=True,
    db=db,
)

simple_agent = Agent(
    name="Simple Agent",
    role="Simple agent",
    id="simple_agent",
    model=OpenAIChat(id="gpt-4o"),
    instructions=["你是一个简单的 agent"],
    update_memory_on_run=True,
    db=db,
)

research_agent = Agent(
    name="Research Agent",
    role="Research agent",
    id="research_agent",
    model=OpenAIChat(id="gpt-4o"),
    instructions=["你是一个研究 agent"],
    tools=[WebSearchTools(), ExaTools()],
    update_memory_on_run=True,
    db=db,
)

research_team = Team(
    name="Research Team",
    description="A team of agents that research the web",
    members=[research_agent, simple_agent],
    model=OpenAIChat(id="gpt-4o"),
    id="research_team",
    instructions=[
        "你是一个研究团队的首席研究员。",
    ],
    update_memory_on_run=True,
    add_datetime_to_context=True,
    markdown=True,
    db=db,
)

multimodal_team = Team(
    name="Multimodal Team",
    description="A team of agents that can handle multiple modalities",
    members=[file_agent, audio_agent, video_agent],
    model=OpenAIChat(id="gpt-4o"),
    pass_user_input_to_members=True,
    respond_directly=True,
    id="multimodal_team",
    instructions=[
        "你是一家知名金融新闻台的首席编辑。",
    ],
    update_memory_on_run=True,
    db=db,
)
financial_news_team = Team(
    name="Financial News Team",
    description="A team of agents that search the web for financial news and analyze it.",
    members=[
        web_agent,
        finance_agent,
        research_agent,
        file_agent,
        audio_agent,
        video_agent,
    ],
    model=OpenAIChat(id="gpt-4o"),
    respond_directly=True,
    id="financial_news_team",
    instructions=[
        "你是一家知名金融新闻台的首席编辑。",
        "如果你收到一个文件，将其发送给文件 agent。",
        "如果你收到一个音频文件，将其发送给音频 agent。",
        "如果你收到一个视频文件，将其发送给视频 agent。",
        "使用美元作为货币。",
        "如果用户只是在进行对话，你应该直接响应，而不将任务转发给成员。",
    ],
    add_datetime_to_context=True,
    markdown=True,
    show_members_responses=True,
    db=db,
    update_memory_on_run=True,
    expected_output="A good financial news report.",
)

# 设置我们的 AgentOS 应用
agent_os = AgentOS(
    description="Example OS setup",
    agents=[
        simple_agent,
        web_agent,
        finance_agent,
        research_agent,
    ],
    teams=[research_team, multimodal_team, financial_news_team],
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="teams_demo:app", reload=True)

"""
多个实例
==================

演示多个实例。
"""

from agno.agent.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

db = SqliteDb(db_file="tmp/agentos.db")

chat_agent = Agent(
    name="Assistant",
    model=OpenAIChat(id="gpt-5.2"),
    db=db,
    instructions="你是一个有用的 AI 助手。",
    add_datetime_to_context=True,
    markdown=True,
)

web_research_agent = Agent(
    name="Web Research Agent",
    model=OpenAIChat(id="gpt-5.2"),
    db=db,
    tools=[WebSearchTools()],
    instructions="你是一个可以搜索网络的有用 AI 助手。",
    markdown=True,
)

# 设置你的 AgentOS 应用
agent_os = AgentOS(
    agents=[chat_agent, web_research_agent],
    interfaces=[
        AGUI(agent=chat_agent, prefix="/chat"),
        AGUI(agent=web_research_agent, prefix="/web-research"),
    ],
)
app = agent_os.get_app()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """运行你的 AgentOS。

    你可以在以下地址查看配置和可用应用：
    http://localhost:7777/config

    """
    agent_os.serve(app="multiple_instances:app", reload=True)

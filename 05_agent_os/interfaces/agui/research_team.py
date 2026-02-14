"""
研究团队
=============

演示研究团队。
"""

from agno.agent.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os.app import AgentOS
from agno.os.interfaces.agui.agui import AGUI
from agno.team.team import Team
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

researcher = Agent(
    name="researcher",
    role="Research Assistant",
    model=OpenAIChat(id="gpt-4o"),
    instructions="你是一个研究助手。查找信息并提供详细分析。",
    tools=[WebSearchTools()],
    markdown=True,
)

writer = Agent(
    name="writer",
    role="Content Writer",
    model=OpenAIChat(id="o4-mini"),
    instructions="你是一个内容作家。根据研究创建结构良好的内容。",
    tools=[WebSearchTools()],
    markdown=True,
)

research_team = Team(
    members=[researcher, writer],
    name="research_team",
    instructions="""
    你是一个帮助用户进行研究和内容创作的研究团队。
    首先，使用研究员收集信息，然后使用作家创建内容。
    """,
    show_members_responses=True,
    get_member_information_tool=True,
    add_member_tools_to_context=True,
    add_history_to_context=True,
)

# 设置我们的 AgentOS 应用
agent_os = AgentOS(
    teams=[research_team],
    interfaces=[AGUI(team=research_team)],
)
app = agent_os.get_app()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """运行你的 AgentOS。

    你可以在以下地址查看配置和可用应用：
    http://localhost:9001/config
    
    使用端口 9001 以兼容 Dojo。
    """
    agent_os.serve(app="research_team:app", reload=True, port=9001)

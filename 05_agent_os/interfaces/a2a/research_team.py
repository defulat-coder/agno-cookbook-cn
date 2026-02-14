"""
研究团队
=============

演示研究团队。
"""

from agno.agent.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os.app import AgentOS
from agno.team.team import Team
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

researcher = Agent(
    name="researcher",
    id="researcher",
    role="Research Assistant",
    model=OpenAIChat(id="gpt-4o"),
    instructions="你是一个研究助手。查找信息并提供详细分析。",
    tools=[WebSearchTools()],
    markdown=True,
)

writer = Agent(
    name="writer",
    id="writer",
    role="Content Writer",
    model=OpenAIChat(id="o4-mini"),
    instructions="你是一个内容作家。根据研究创建结构良好的内容。",
    tools=[WebSearchTools()],
    markdown=True,
)

research_team = Team(
    members=[researcher, writer],
    id="research_team",
    name="Research Team",
    description="一个协作研究和内容创作团队，结合深度研究能力与专业写作，提供全面、有据的内容",
    instructions="""
    你是一个帮助用户进行研究和内容创作的研究团队。
    首先，使用研究员收集信息，然后使用作家创建内容。
    """,
    show_members_responses=True,
    get_member_information_tool=True,
    add_member_tools_to_context=True,
    add_history_to_context=True,
    debug_mode=True,
)

# 设置我们的 AgentOS 应用
agent_os = AgentOS(
    teams=[research_team],
    a2a_interface=True,
)
app = agent_os.get_app()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """使用 A2A 接口运行你的 AgentOS。

    你可以通过 A2A 协议运行 Agent：
    POST http://localhost:7777/teamss/{id}/v1/message:send
    对于流式响应：
    POST http://localhost:7777/teams/{id}/v1/message:stream
    在以下地址检索 agent 卡片：
    GET  http://localhost:7777/teams/{id}/.well-known/agent-card.json

    """
    agent_os.serve(app="research_team:app", reload=True, port=7777)

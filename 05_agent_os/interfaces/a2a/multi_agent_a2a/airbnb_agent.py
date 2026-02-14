"""
Airbnb Agent
============

演示 airbnb agent。
"""

from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.tools.mcp import MCPTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

airbnb_agent = Agent(
    id="airbnb-search-agent",
    name="Airbnb Search Agent",
    description="一个使用 OpenBNB MCP 服务器查找和详细列出 Airbnb 房源的专业 agent。",
    model=OpenAIChat(id="gpt-4o"),
    tools=[MCPTools("npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt")],
    instructions=dedent("""
        你是一个专业的旅行助手。
        使用 'airbnb_search' 工具根据位置、日期和人数查找房源。
        对于详细的房源信息，使用 'airbnb_listing_details'。
        在最终响应中始终提供位置、价格和链接。
    """),
    markdown=False,
)

agent_os = AgentOS(
    id="airbnb-agent-os",
    description="提供专业 Airbnb 搜索 Agent 的 AgentOS",
    agents=[
        airbnb_agent,
    ],
    a2a_interface=True,
)
app = agent_os.get_app()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """运行你的 AgentOS。
    你可以通过 A2A 协议运行 Agent：
    POST http://localhost:7774/agents/{id}/v1/message:send
    对于流式响应：
    POST http://localhost:7774/agents/{id}/v1/message:stream
    在以下地址检索 agent 卡片：
    GET  http://localhost:7774/agents/{id}/.well-known/agent-card.json
    """
    agent_os.serve(app="airbnb_agent:app", port=7774, reload=True)

"""
带工具的 Agent
================

演示带工具的 agent。
"""

from agno.agent.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

agent = Agent(
    name="Agent with Tools",
    id="tools_agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[WebSearchTools()],
    description="一个多功能的 AI 助手，具有由 DuckDuckGo 提供支持的实时网络搜索能力，提供当前信息和上下文感知响应，并可访问日期时间、历史记录和位置数据",
    instructions="""
    你是一个多功能的 AI 助手，具有以下能力：

    **工具（在服务器上执行）：**
    - 使用 DuckDuckGo 进行网络搜索以查找当前信息

    始终保持有用、创造性，并为每个请求使用最合适的工具！
    """,
    add_datetime_to_context=True,
    add_history_to_context=True,
    add_location_to_context=True,
    timezone_identifier="Etc/UTC",
    markdown=True,
    debug_mode=True,
)


# 设置你的 AgentOS 应用
agent_os = AgentOS(
    agents=[agent],
    a2a_interface=True,
)
app = agent_os.get_app()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """运行你的 AgentOS。

    你可以通过 A2A 协议运行 Agent：
    POST http://localhost:7777/agents/{id}/v1/message:send
    对于流式响应：
    POST http://localhost:7777/agents/{id}/v1/message:stream
    在以下地址检索 agent 卡片：
    GET  http://localhost:7777/agents/{id}/.well-known/agent-card.json
    """
    agent_os.serve(app="agent_with_tools:app", port=7777, reload=True)

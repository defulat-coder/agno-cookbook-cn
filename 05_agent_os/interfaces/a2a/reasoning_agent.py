"""
推理 Agent
===============

演示推理 agent。
"""

from agno.agent.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

reasoning_agent = Agent(
    name="reasoning-agent",
    id="reasoning_agent",
    model=OpenAIChat(id="o4-mini"),
    description="具有深度推理和分析能力的高级 AI 助手，增强了实时网络搜索功能，可提供全面、深思熟虑的响应和上下文感知",
    instructions="你是一个具有推理能力的有用 AI 助手。",
    add_datetime_to_context=True,
    add_history_to_context=True,
    add_location_to_context=True,
    timezone_identifier="Etc/UTC",
    markdown=True,
    tools=[WebSearchTools()],
)

# 设置你的 AgentOS 应用
agent_os = AgentOS(
    agents=[reasoning_agent],
    a2a_interface=True,
)
app = agent_os.get_app()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """使用 A2A 接口运行你的 AgentOS。
    你可以通过 A2A 协议运行 Agent：
    POST http://localhost:7777/agents/{id}/v1/message:send
    对于流式响应：
    POST http://localhost:7777/agents/{id}/v1/message:stream
    在以下地址检索 agent 卡片：
    GET  http://localhost:7777/agents/{id}/.well-known/agent-card.json
    """
    agent_os.serve(app="reasoning_agent:app", reload=True, port=7777)

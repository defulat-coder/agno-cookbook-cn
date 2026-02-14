"""
基础
=====

演示基础功能。
"""

from agno.agent.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

chat_agent = Agent(
    name="basic-agent",
    model=OpenAIChat(id="gpt-4o"),
    id="basic_agent",
    description="一个有用且响应迅速的 AI 助手，提供深思熟虑的答案和广泛主题的协助",
    instructions="你是一个有用的 AI 助手。",
    add_datetime_to_context=True,
    markdown=True,
)

# 设置你的 AgentOS 应用
agent_os = AgentOS(
    agents=[chat_agent],
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
    agent_os.serve(app="basic:app", reload=True, port=7777)

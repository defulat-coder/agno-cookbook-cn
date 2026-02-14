"""
Cookbook 示例的 Google ADK A2A 服务器。

使用 Google 的 ADK 创建兼容 A2A 的 agent。
需要 GOOGLE_API_KEY 环境变量。

此服务器公开一个 facts-agent，提供有趣的事实，
在根 "/" 端点使用纯 JSON-RPC（Google ADK 风格）。

在运行 05_remote_adk_agent.py 之前启动此服务器
"""

import os

from a2a.types import AgentCapabilities, AgentCard
from google.adk import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.tools import google_search

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

port = int(os.getenv("PORT", "7780"))

agent = Agent(
    name="facts_agent",
    model="gemini-2.5-flash-lite",
    description="Agent that provides interesting facts.",
    instruction="你是一个提供有趣事实的有用 agent。",
    tools=[google_search],
)

# 定义 A2A agent 卡片
agent_card = AgentCard(
    name="facts_agent",
    description="Agent that provides interesting facts.",
    url=f"http://localhost:{port}",
    version="1.0.0",
    capabilities=AgentCapabilities(
        streaming=True, push_notifications=False, state_transition_history=False
    ),
    skills=[],
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
)

app = to_a2a(agent, port=port, agent_card=agent_card)

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=port)

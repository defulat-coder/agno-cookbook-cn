"""
天气 Agent
=============

演示天气 agent。
"""

from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.tools.openweather import OpenWeatherTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

weather_agent = Agent(
    id="weather-reporter-agent",
    name="Weather Reporter Agent",
    description="一个为任何城市提供最新天气信息的 agent。",
    model=OpenAIChat(id="gpt-5.2"),
    tools=[
        OpenWeatherTools(
            units="standard"  # 可以是 'standard'、'metric'、'imperial'
        )
    ],
    instructions=dedent("""
        你是一个简洁的天气播报员。
        使用 'get_current_weather' 工具获取当前状况。
        用温度和简短摘要回复。
    """),
    markdown=True,
)
agent_os = AgentOS(
    id="weather-agent-os",
    description="提供专业天气播报 Agent 的 AgentOS",
    agents=[
        weather_agent,
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
    POST http://localhost:7770/agents/{id}/v1/message:send
    对于流式响应：
    POST http://localhost:7770/agents/{id}/v1/message:stream
    在以下地址检索 agent 卡片：
    GET  http://localhost:7770/agents/{id}/.well-known/agent-card.json
    """
    agent_os.serve(app="weather_agent:app", port=7770, reload=True)

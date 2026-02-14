"""
旅行计划 A2A 客户端
========================

演示旅行计划 a2a 客户端。
"""

import uuid

import requests
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------


# --- 1. A2A 辅助函数（协议）---
def _send_a2a_message(url: str, text: str) -> str:
    """
    使用你的 A2A JSON-RPC 格式发送消息的内部辅助函数。
    """
    payload = {
        "id": "trip_planner_client",
        "jsonrpc": "2.0",
        "method": "message/send",
        "params": {
            "message": {
                "message_id": str(uuid.uuid4()),
                "role": "user",
                "parts": [{"text": text}],
            }
        },
    }

    try:
        # 发送 POST 请求
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        # 解包特定的 A2A 响应结构
        # result -> history -> last_item -> parts -> first_item -> text
        if "result" in data and "history" in data["result"]:
            history = data["result"]["history"]
            if history:
                last_msg = history[-1]
                if "parts" in last_msg and last_msg["parts"]:
                    return last_msg["parts"][0]["text"]

        return f"系统错误：位于 {url} 的 agent 响应了，但在历史中未找到文本消息。"

    except Exception as e:
        return f"连接错误：无法与位于 {url} 的 agent 通信。详细信息：{e}"


# --- 2. 两个工具函数 ---


def ask_airbnb_agent(request: str) -> str:
    """
    联系专业的 Airbnb Agent 以查找房源或获取详细信息。

    参数：
        request (str): 自然语言请求（例如，"在巴黎找一个低于 200 美元的 2 居室公寓"）。
    """
    # Airbnb Agent 服务的 URL
    AIRBNB_URL = "http://localhost:7774/a2a/agents/airbnb-search-agent/v1/message:send"
    return _send_a2a_message(AIRBNB_URL, request)


def ask_weather_agent(request: str) -> str:
    """
    联系专业的天气 Agent 以获取预报或当前状况。

    参数：
        request (str): 自然语言请求（例如，"下周东京的天气如何？"）。
    """
    # 天气 Agent 服务的 URL
    WEATHER_URL = (
        "http://localhost:7770/a2a/agents/weather-reporter-agent/v1/message:send"
    )
    return _send_a2a_message(WEATHER_URL, request)


# --- 3. 主要的旅行计划 Agent ---

trip_planner = Agent(
    name="Trip Planner",
    id="trip_planner",
    model=OpenAIChat(id="gpt-4o"),
    # 为 agent 提供我们刚刚创建的工具
    tools=[ask_airbnb_agent, ask_weather_agent],
    markdown=True,
    description="你是一个专业的旅行计划协调员。",
    instructions=[
        "你通过与专业 agent 协调来帮助用户计划完整的旅行。",
        "1. 始终首先使用 'ask_weather_agent' 检查目的地/日期的天气。",
        "2. 根据天气适宜性，使用 'ask_airbnb_agent' 搜索住宿。",
        "3. 将两个 agent 的信息综合成最终的行程提案。",
        "如果 agent 返回错误，请通知用户并尝试继续使用可用信息。",
    ],
)
agent_os = AgentOS(
    id="trip-planning-service",
    description="托管旅行计划协调器的 AgentOS。",
    agents=[
        trip_planner,
    ],
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
    agent_os.serve(app="trip_planning_a2a_client:app", port=7777, reload=True)

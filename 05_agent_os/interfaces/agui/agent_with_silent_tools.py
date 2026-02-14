"""静默外部工具 - 在前端抑制冗长消息

当使用 `external_execution=True` 时，agent 会打印"我有要执行的工具..."
消息。添加 `external_execution_silent=True` 以在生产中抑制这些消息，实现更清洁的用户体验。

此 cookbook 适用于在前端执行工具的 AgentOS/AGUI。
前端将接收工具调用并在客户端处理执行。
"""

from agno.agent.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI
from agno.tools import tool
from agno.tools.duckduckgo import DuckDuckGoTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------


# external_execution_silent=True 抑制"我有要执行的工具..."冗长消息
@tool(external_execution=True, external_execution_silent=True)
def generate_haiku(topic: str) -> str:
    """生成关于给定主题的俳句并在前端显示。

    参数：
        topic: 俳句的主题（例如，"自然"、"技术"、"爱"）

    返回：
        确认俳句已生成并显示
    """
    return f"关于 '{topic}' 的俳句已生成并在前端显示"


agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[
        DuckDuckGoTools(),
        generate_haiku,
    ],
    description="你是一个具有后端和前端能力的有用 AI 助手。你可以搜索网络、创建美丽的俳句、修改 UI、请求用户确认并创建可视化。",
    instructions="""
    你是一个多功能的 AI 助手，具有以下能力：

    **工具（在服务器上执行）：**
    - 使用 DuckDuckGo 进行网络搜索以查找当前信息

    **前端工具（在客户端执行）：**
    - generate_haiku: 创建关于给定主题的俳句

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
    interfaces=[AGUI(agent=agent)],
)
app = agent_os.get_app()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """运行你的 AgentOS。

    你可以在以下地址查看配置和可用应用：
    http://localhost:9001/config

    使用端口 9001 配置 Dojo 端点。
    """
    agent_os.serve(app="agent_with_silent_tools:app", port=9001, reload=True)

"""
带工具的 Agent
================

演示带工具的 agent。
"""

from typing import List

from agno.agent.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI
from agno.tools import tool
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------


# 前端工具
@tool(external_execution=True)
def generate_haiku(
    english: List[str], japanese: List[str], image_names: List[str]
) -> str:
    """生成日语和英语的俳句并在前端显示。"""
    return "俳句已生成并在前端显示"


agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[
        WebSearchTools(),
        generate_haiku,
    ],
    description="你是一个具有后端和前端能力的有用 AI 助手。你可以搜索网络、创建美丽的俳句、修改 UI、请求用户确认并创建可视化。",
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
    agent_os.serve(app="agent_with_tools:app", port=9001, reload=True)

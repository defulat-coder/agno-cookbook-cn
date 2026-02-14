"""
带媒体的 Agent
================

演示带媒体的 agent。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.google import Gemini
from agno.os.app import AgentOS
from agno.os.interfaces.whatsapp import Whatsapp

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

agent_db = SqliteDb(db_file="tmp/persistent_memory.db")
media_agent = Agent(
    name="Media Agent",
    model=Gemini(id="gemini-3-flash-preview"),
    db=agent_db,
    add_history_to_context=True,
    num_history_runs=3,
    add_datetime_to_context=True,
    markdown=True,
)

# 设置我们的 AgentOS 应用
agent_os = AgentOS(
    agents=[media_agent],
    interfaces=[Whatsapp(agent=media_agent)],
)
app = agent_os.get_app()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """运行你的 AgentOS。

    你可以在以下地址查看配置和可用应用：
    http://localhost:7777/config

    """
    agent_os.serve(app="agent_with_media:app", reload=True)

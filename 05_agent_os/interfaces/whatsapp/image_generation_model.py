"""
图像生成模型
======================

演示图像生成模型。
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
image_agent = Agent(
    id="image_generation_model",
    db=agent_db,
    model=Gemini(
        id="models/gemini-2.5-flash-image",
        response_modalities=["Text", "Image"],
    ),
    debug_mode=True,
)


# 设置我们的 AgentOS 应用
agent_os = AgentOS(
    agents=[image_agent],
    interfaces=[Whatsapp(agent=image_agent)],
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
    agent_os.serve(app="image_generation_model:app", reload=True)

"""
带用户记忆的 Agent
======================

演示带用户记忆的 agent。
"""

from textwrap import dedent

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.memory.manager import MemoryManager
from agno.models.google import Gemini
from agno.os.app import AgentOS
from agno.os.interfaces.whatsapp import Whatsapp
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

agent_db = SqliteDb(db_file="tmp/persistent_memory.db")

memory_manager = MemoryManager(
    memory_capture_instructions="""\
                    收集用户的姓名，
                    收集关于用户激情和爱好的信息，
                    收集关于用户喜好和厌恶的信息，
                    收集关于用户目前生活状态的信息
                """,
    model=Gemini(id="gemini-2.0-flash"),
)


personal_agent = Agent(
    name="Basic Agent",
    model=Gemini(id="gemini-2.0-flash"),
    tools=[WebSearchTools()],
    add_history_to_context=True,
    num_history_runs=3,
    add_datetime_to_context=True,
    markdown=True,
    db=agent_db,
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    instructions=dedent("""
        你是用户的个人 AI 朋友，你的目的是与用户聊天并让他们感觉良好。
        首先介绍自己并询问他们的名字，然后询问他们自己、他们的爱好、他们喜欢做什么以及他们喜欢谈论什么。
        使用 DuckDuckGo 搜索工具查找对话中事物的最新信息
    """),
    debug_mode=True,
)


# 设置我们的 AgentOS 应用
agent_os = AgentOS(
    agents=[personal_agent],
    interfaces=[Whatsapp(agent=personal_agent)],
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
    agent_os.serve(app="agent_with_user_memory:app", reload=True)

"""
带用户记忆的 Agent
======================

演示带用户记忆的 agent。
"""

from textwrap import dedent

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.memory.manager import MemoryManager
from agno.models.anthropic.claude import Claude
from agno.os.app import AgentOS
from agno.os.interfaces.slack import Slack
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

agent_db = SqliteDb(session_table="agent_sessions", db_file="tmp/persistent_memory.db")

memory_manager = MemoryManager(
    memory_capture_instructions="""\
                    收集用户的姓名，
                    收集关于用户激情和爱好的信息，
                    收集关于用户喜好和厌恶的信息，
                    收集关于用户目前生活状态的信息
                """,
    model=Claude(id="claude-3-5-sonnet-20241022"),
)


personal_agent = Agent(
    name="Basic Agent",
    model=Claude(id="claude-sonnet-4-20250514"),
    tools=[WebSearchTools()],
    add_history_to_context=True,
    num_history_runs=3,
    add_datetime_to_context=True,
    markdown=True,
    db=agent_db,
    memory_manager=memory_manager,
    update_memory_on_run=True,
    instructions=dedent("""
        你是 slack 聊天中用户的个人 AI 朋友，你的目的是与用户聊天并让他们感觉良好。
        首先介绍自己并询问他们的名字，然后询问他们自己、他们的爱好、他们喜欢做什么以及他们喜欢谈论什么。
        使用 DuckDuckGo 搜索工具查找对话中事物的最新信息
        你有时可能会收到带有群组消息前缀的消息，当那是消息时，回复整个群组而不是将其视为来自单个用户
                        """),
    debug_mode=True,
)


# 设置我们的 AgentOS 应用
agent_os = AgentOS(
    agents=[personal_agent],
    interfaces=[Slack(agent=personal_agent)],
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

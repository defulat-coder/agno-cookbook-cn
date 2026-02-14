"""
研究助手
==================

演示研究助手。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.os.app import AgentOS
from agno.os.interfaces.slack import Slack
from agno.tools.slack import SlackTools
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

agent_db = SqliteDb(session_table="agent_sessions", db_file="tmp/research_assistant.db")

research_assistant = Agent(
    name="Research Assistant",
    model=OpenAIChat(id="gpt-4o"),
    db=agent_db,
    tools=[
        SlackTools(
            enable_search_messages=True,
            enable_get_thread=True,
            enable_list_users=True,
            enable_get_user_info=True,
        ),
        WebSearchTools(),
    ],
    instructions=[
        "你是一个帮助查找信息的研究助手。",
        "你可以使用以下方式搜索 Slack 消息：from:@user, in:#channel, has:link, before:/after:date",
        "你还可以搜索网络以获取最新信息。",
        "当被要求研究某事时：",
        "1. 在 Slack 中搜索内部讨论",
        "2. 在网络上搜索外部背景",
        "3. 将发现综合成清晰的摘要",
        "通过查看谁参与了讨论来识别相关专家。",
    ],
    add_history_to_context=True,
    num_history_runs=3,
    add_datetime_to_context=True,
    markdown=True,
)

agent_os = AgentOS(
    agents=[research_assistant],
    interfaces=[
        Slack(
            agent=research_assistant,
            reply_to_mentions_only=True,
        )
    ],
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="research_assistant:app", reload=True)

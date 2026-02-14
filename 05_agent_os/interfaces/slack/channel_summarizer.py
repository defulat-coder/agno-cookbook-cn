"""
频道摘要生成器
==================

演示频道摘要生成器。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.os.app import AgentOS
from agno.os.interfaces.slack import Slack
from agno.tools.slack import SlackTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

agent_db = SqliteDb(session_table="agent_sessions", db_file="tmp/summarizer.db")

summarizer = Agent(
    name="Channel Summarizer",
    model=OpenAIChat(id="gpt-4o"),
    db=agent_db,
    tools=[
        SlackTools(
            enable_get_thread=True,
            enable_search_messages=True,
            enable_list_users=True,
        )
    ],
    instructions=[
        "你总结 Slack 频道活动。",
        "当被问及某个频道时：",
        "1. 获取最近的消息历史",
        "2. 识别活跃的讨论串并展开它们",
        "3. 按主题/主题对消息进行分组",
        "4. 突出显示决策、行动项和障碍",
        "用清晰的部分格式化摘要：",
        "- 关键讨论",
        "- 做出的决策",
        "- 行动项",
        "- 问题/障碍",
        "使用项目符号，保持摘要简洁。",
    ],
    add_history_to_context=True,
    num_history_runs=3,
    add_datetime_to_context=True,
    markdown=True,
)

agent_os = AgentOS(
    agents=[summarizer],
    interfaces=[
        Slack(
            agent=summarizer,
            reply_to_mentions_only=True,
        )
    ],
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="channel_summarizer:app", reload=True)

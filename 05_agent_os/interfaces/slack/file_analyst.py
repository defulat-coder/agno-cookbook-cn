"""
文件分析师
============

演示文件分析师。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.anthropic import Claude
from agno.os.app import AgentOS
from agno.os.interfaces.slack import Slack
from agno.tools.slack import SlackTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

agent_db = SqliteDb(session_table="agent_sessions", db_file="tmp/file_analyst.db")

file_analyst = Agent(
    name="File Analyst",
    model=Claude(id="claude-sonnet-4-20250514"),
    db=agent_db,
    tools=[
        SlackTools(
            enable_download_file=True,
            enable_get_channel_history=True,
            enable_upload_file=True,
            output_directory="/tmp/slack_analysis",
        )
    ],
    instructions=[
        "你是一个文件分析助手。",
        "当用户分享文件或提及文件 ID（F12345...）时，下载并分析它们。",
        "对于 CSV/数据文件：识别模式、异常值和关键统计数据。",
        "对于代码文件：解释代码的功能，提出改进建议。",
        "对于文本/文档：总结关键点。",
        "你可以将分析结果作为新文件上传回 Slack。",
        "始终用简单的语言解释你的分析。",
    ],
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

agent_os = AgentOS(
    agents=[file_analyst],
    interfaces=[
        Slack(
            agent=file_analyst,
            reply_to_mentions_only=True,
        )
    ],
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="file_analyst:app", reload=True)

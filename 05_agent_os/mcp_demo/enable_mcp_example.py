"""
启用 MCP 的示例 AgentOS 应用。

启动此 AgentOS 应用后，你可以使用 test_client.py 文件测试 MCP 服务器。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.anthropic import Claude
from agno.os import AgentOS
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# 设置数据库
db = SqliteDb(db_file="tmp/agentos.db")

# 设置基础研究 agent
web_research_agent = Agent(
    id="web-research-agent",
    name="Web Research Agent",
    model=Claude(id="claude-sonnet-4-0"),
    db=db,
    tools=[WebSearchTools()],
    add_history_to_context=True,
    num_history_runs=3,
    add_datetime_to_context=True,
    enable_session_summaries=True,
    markdown=True,
)


# 设置启用 MCP 的 AgentOS
agent_os = AgentOS(
    description="启用 MCP 的示例应用",
    agents=[web_research_agent],
    enable_mcp_server=True,  # 这会在 /mcp 启用一个 LLM 友好的 MCP 服务器
)

app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """运行你的 AgentOS。

    你可以在以下地址查看你的 LLM 友好 MCP 服务器：
    http://localhost:7777/mcp

    """
    agent_os.serve(app="enable_mcp_example:app")

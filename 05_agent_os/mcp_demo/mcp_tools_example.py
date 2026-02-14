"""
agent 具有 MCPTools 的示例 AgentOS 应用。

AgentOS 内部处理 MCPTools 的生命周期。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.anthropic import Claude
from agno.os import AgentOS
from agno.tools.mcp import MCPTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# 设置数据库
db = SqliteDb(db_file="tmp/agentos.db")

mcp_tools = MCPTools(transport="streamable-http", url="https://docs.agno.com/mcp")

# 设置基础 agent
agno_support_agent = Agent(
    id="agno-support-agent",
    name="Agno Support Agent",
    model=Claude(id="claude-sonnet-4-0"),
    db=db,
    tools=[mcp_tools],
    add_history_to_context=True,
    num_history_runs=3,
    markdown=True,
)


agent_os = AgentOS(
    description="带有 MCP 工具的示例应用",
    agents=[agno_support_agent],
)


app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """运行你的 AgentOS。

    你可以在以下地址测试你的 AgentOS：
    http://localhost:7777/docs

    """
    # 不要在这里使用 reload=True，这可能会导致生命周期问题
    agent_os.serve(app="mcp_tools_example:app")

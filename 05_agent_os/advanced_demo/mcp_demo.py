"""此示例展示如何在 Agno OS 中使用我们的 MCP 集成运行 Agent。

为使此示例运行，你需要：
- 按照以下步骤创建 GitHub 个人访问令牌：
    - https://github.com/modelcontextprotocol/servers/tree/main/src/github#setup
- 设置 GITHUB_TOKEN 环境变量：`export GITHUB_TOKEN=<你的 GitHub 访问令牌>`
- 运行：`uv pip install agno mcp openai` 以安装依赖
"""

from contextlib import asynccontextmanager
from os import getenv
from textwrap import dedent

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.tools.mcp import MCPTools
from fastapi import FastAPI
from mcp import StdioServerParameters

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

agent_storage_file: str = "tmp/agents.db"


# MCP 服务器参数设置
github_token = getenv("GITHUB_TOKEN") or getenv("GITHUB_ACCESS_TOKEN")
if not github_token:
    raise ValueError("GITHUB_TOKEN environment variable is required")

server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-github"],
)


# 这是在 FastAPI 生命周期中正确启动 MCP 连接所必需的
@asynccontextmanager
async def lifespan(app: FastAPI):
    """在 FastAPI 应用中管理 MCP 连接生命周期"""
    global mcp_tools

    # 启动逻辑：连接到我们的 MCP 服务器
    mcp_tools = MCPTools(server_params=server_params)
    await mcp_tools.connect()

    # 将 MCP 工具添加到我们的 Agent
    agent.tools = [mcp_tools]

    yield

    # 关闭：关闭 MCP 连接
    await mcp_tools.close()


agent = Agent(
    name="MCP GitHub Agent",
    instructions=dedent("""\
        你是一个 GitHub 助手。帮助用户探索仓库及其活动。

        - 使用标题组织你的响应
        - 简洁并专注于相关信息\
    """),
    model=OpenAIChat(id="gpt-4o"),
    db=SqliteDb(db_file=agent_storage_file),
    update_memory_on_run=True,
    enable_session_summaries=True,
    add_history_to_context=True,
    num_history_runs=3,
    add_datetime_to_context=True,
    markdown=True,
)

# 设置我们的 AgentOS 应用
agent_os = AgentOS(
    description="Example OS setup",
    agents=[agent],
)
app = agent_os.get_app()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="mcp_demo:app", reload=True)

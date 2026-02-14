"""用于测试 A2AClient 的 Agno AgentOS A2A 服务器。

此服务器使用 Agno 的 AgentOS 创建一个兼容 A2A 的
agent，可以使用 A2AClient 进行测试。

前置条件：
    export OPENAI_API_KEY=your_key

用法：
    python cookbook/06_agent_os/client_a2a/servers/agno_server.py

服务器将在 http://localhost:7003 启动
"""

from agno.agent.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

db = SqliteDb(db_file="tmp/agent.db")
chat_agent = Agent(
    name="basic-agent",
    model=OpenAIChat(id="gpt-5.2"),
    id="basic-agent",
    db=db,
    description="一个提供深思熟虑答案的有用 AI 助手。",
    instructions="你是一个有用的 AI 助手。",
    add_datetime_to_context=True,
    add_history_to_context=True,
    markdown=True,
)

agent_os = AgentOS(
    agents=[chat_agent],
    a2a_interface=True,
)
app = agent_os.get_app()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="agno_server:app", reload=True, port=7003)

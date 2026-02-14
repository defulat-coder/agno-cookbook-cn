"""用于 AgentOS 的示例，展示如何将依赖项传递给 agent。"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.os import AgentOS

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# 设置数据库
db = PostgresDb(id="basic-db", db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

# 设置基本的 agent、团队和工作流
story_writer = Agent(
    id="story-writer-agent",
    name="Story Writer Agent",
    db=db,
    markdown=True,
    instructions="你是一个故事作家。你被要求写一个关于机器人的故事。始终将机器人命名为 {robot_name}",
)

# 设置我们的 AgentOS 应用
agent_os = AgentOS(
    description="展示如何将依赖项传递给 agent 的示例 AgentOS",
    agents=[story_writer],
)
app = agent_os.get_app()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """运行你的 AgentOS。

    测试将依赖项传递给 agent：
    curl --location 'http://localhost:7777/agents/story-writer-agent/runs' \
        --header 'Content-Type: application/x-www-form-urlencoded' \
        --data-urlencode 'message=Write me a 5 line story.' \
        --data-urlencode 'dependencies={"robot_name": "Anna"}'
    """
    agent_os.serve(app="pass_dependencies_to_agent:app", reload=True)

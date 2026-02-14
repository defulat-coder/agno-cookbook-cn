"""
带有自定义健康端点的 AgentOS 示例应用。

此示例演示如何向你的 AgentOS 应用添加自定义健康端点。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.anthropic import Claude
from agno.os import AgentOS
from agno.os.routers.health import get_health_router
from agno.tools.websearch import WebSearchTools
from fastapi import FastAPI

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# 设置数据库
db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

web_research_agent = Agent(
    id="web-research-agent",
    name="Web Research Agent",
    model=Claude(id="claude-sonnet-4-0"),
    db=db,
    tools=[WebSearchTools()],
    add_history_to_context=True,
    num_history_runs=3,
    add_datetime_to_context=True,
    markdown=True,
)

# 自定义 FastAPI 应用
app: FastAPI = FastAPI(
    title="Custom FastAPI App",
    version="1.0.0",
)


# 自定义健康端点
health_router = get_health_router(health_endpoint="/health-check")
app.include_router(health_router)


# 通过在 app_config 参数中传递你的 FastAPI 应用来设置 AgentOS 应用
agent_os = AgentOS(
    description="Example app with custom health endpoint",
    agents=[web_research_agent],
    base_app=app,
)

app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """运行你的 AgentOS。

    你可以在此处测试自定义健康端点：http://localhost:7777/health-check
    而 AgentOS 健康端点仍然可用于：http://localhost:7777/health
    """
    agent_os.serve(app="custom_health_endpoint:app", reload=True)

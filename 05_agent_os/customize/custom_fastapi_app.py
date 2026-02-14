"""
自定义 FastAPI 应用的 AgentOS 示例应用，带有基本路由。

你也可以使用 FastAPI cli 运行此应用（uv pip install fastapi["standard"]）：
```
fastapi run custom_fastapi_app.py
```
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.anthropic import Claude
from agno.os import AgentOS
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


# 添加你自己的路由
@app.get("/customers")
async def get_customers():
    return [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john.doe@example.com",
        },
        {
            "id": 2,
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
        },
    ]


# 通过在 app_config 参数中传递你的 FastAPI 应用来设置 AgentOS 应用
agent_os = AgentOS(
    description="Example app with custom routers",
    agents=[web_research_agent],
    base_app=app,
)

app = agent_os.get_app()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """运行你的 AgentOS。

    使用此设置：
    - API 文档：http://localhost:7777/docs

    """
    agent_os.serve(app="custom_fastapi_app:app", reload=True)

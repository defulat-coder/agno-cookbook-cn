"""基础计划 agent 运行。

启动启用调度器的 AgentOS。服务器运行后，
使用 REST API 创建一个每 5 分钟触发 agent 的计划。

前置条件：
    pip install agno[scheduler]
    # 启动 postgres: ./cookbook/scripts/run_pgvector.sh

用法：
    python cookbook/05_agent_os/scheduler/basic_schedule.py

然后，在另一个终端中，创建一个计划：
    curl -X POST http://localhost:7777/schedules \
        -H "Content-Type: application/json" \
        -d '{
            "name": "greeting-every-5m",
            "cron_expr": "*/5 * * * *",
            "endpoint": "/agents/greeter/runs",
            "payload": {"message": "Say hello!"}
        }'
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

db = PostgresDb(
    id="scheduler-demo-db",
    db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
)

greeter = Agent(
    id="greeter",
    name="Greeter Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=[
        "你是一个友好的迎宾员。打个招呼并包含当前时间。"
    ],
    db=db,
    markdown=True,
)

app = AgentOS(
    agents=[greeter],
    db=db,
    scheduler=True,
    scheduler_poll_interval=15,
).get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=7777)

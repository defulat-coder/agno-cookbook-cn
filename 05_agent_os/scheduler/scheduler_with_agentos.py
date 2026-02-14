"""在 AgentOS 内运行调度器并自动轮询。

此示例演示调度器的主要 DX：
- 在 AgentOS 上设置 scheduler=True 以启用 cron 轮询
- 轮询器在应用启动时自动启动并在关闭时停止
- 通过 REST API 创建计划（POST /schedules）
- 内部服务令牌处理调度器和 agent 端点之间的认证

运行方式：
    .venvs/demo/bin/python cookbook/05_agent_os/scheduler/scheduler_with_agentos.py
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS

# --- 设置 ---

db = SqliteDb(id="scheduler-os-demo", db_file="tmp/scheduler_os_demo.db")

greeter = Agent(
    name="Greeter",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=["你是一个友好的迎宾员。"],
    db=db,
)

reporter = Agent(
    name="Reporter",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=["你用 2-3 句话总结新闻头条。"],
    db=db,
)

# 创建启用调度器的 AgentOS。
# 这执行三件事：
#   1. 注册 /schedules REST 端点
#   2. 在应用启动时启动 SchedulePoller（默认每 15 秒轮询一次）
#   3. 自动生成用于调度器 -> agent 认证的内部服务令牌
agent_os = AgentOS(
    name="Scheduled OS",
    agents=[greeter, reporter],
    db=db,
    scheduler=True,
    scheduler_poll_interval=15,  # 轮询周期之间的秒数（默认：15）
    # scheduler_base_url="http://127.0.0.1:7777",  # 默认
    # internal_service_token="my-secret",  # 如果省略则自动生成
)
app = agent_os.get_app()

# --- 运行服务器 ---
# 运行后，通过以下方式创建计划：
#
#   curl -X POST http://127.0.0.1:7777/schedules \
#     -H "Content-Type: application/json" \
#     -d '{
#       "name": "greet-every-5-min",
#       "cron_expr": "*/5 * * * *",
#       "endpoint": "/agents/greeter/runs",
#       "payload": {"message": "Say hello!"}
#     }'
#
# 轮询器将在下一个轮询周期中获取它并运行 agent。

if __name__ == "__main__":
    agent_os.serve(app="scheduler_with_agentos:app", reload=True)

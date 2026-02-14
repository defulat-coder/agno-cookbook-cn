"""在 AgentOS 内通过编程方式创建计划运行调度器。

此示例演示：
- 在 AgentOS 上设置 scheduler=True 以启用 cron 轮询
- 使用 ScheduleManager 直接创建计划（无需 curl）
- 轮询器在应用启动时自动启动并执行到期的计划

运行方式：
    .venvs/demo/bin/python cookbook/05_agent_os/scheduler/demo.py
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.scheduler import ScheduleManager

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

# --- 以编程方式创建计划 ---

mgr = ScheduleManager(db)

# 为 greeter agent 创建计划（每 5 分钟）
greet_schedule = mgr.create(
    name="greet-every-5-min",
    cron="* * * * *",
    endpoint="/agents/greeter/runs",
    payload={"message": "Say hello!"},
    description="每 5 分钟问候一次",
    if_exists="update",
)
print(f"Schedule ready: {greet_schedule.name} (next run: {greet_schedule.next_run_at})")

# 为 reporter agent 创建计划（每天上午 9 点）
report_schedule = mgr.create(
    name="daily-news-report",
    cron="* * * * *",
    endpoint="/agents/reporter/runs",
    payload={"message": "Summarize today's top headlines."},
    description="UTC 上午 9 点的每日新闻摘要",
    if_exists="update",
)
print(
    f"Schedule ready: {report_schedule.name} (next run: {report_schedule.next_run_at})"
)

# --- 创建启用调度器的 AgentOS ---

agent_os = AgentOS(
    name="Scheduled OS",
    agents=[greeter, reporter],
    db=db,
    scheduler=True,
    scheduler_poll_interval=15,
)

# --- 运行服务器 ---
# 轮询器将自动获取上面创建的计划。

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(agent_os.get_app(), host="0.0.0.0", port=7777)

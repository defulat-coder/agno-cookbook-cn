"""调度团队和工作流（不仅仅是 agent）。

此示例演示：
- 创建针对团队端点（/teams/*/runs）的计划
- 创建针对工作流端点（/workflows/*/runs）的计划
- 团队与工作流的不同负载配置
- 直接使用 ScheduleManager 进行设置
"""

from agno.db.sqlite import SqliteDb
from agno.scheduler import ScheduleManager
from agno.scheduler.cli import SchedulerConsole

# --- 设置 ---

db = SqliteDb(id="team-wf-demo", db_file="tmp/team_wf_demo.db")
mgr = ScheduleManager(db)
console = SchedulerConsole(mgr)

# =============================================================================
# 1. 调度团队运行
# =============================================================================

print("=== 团队计划 ===\n")

team_schedule = mgr.create(
    name="daily-research-team",
    cron="0 9 * * 1-5",
    endpoint="/teams/research-team/runs",
    description="每个工作日上午 9 点运行研究团队",
    payload={
        "message": "Research the latest developments in AI safety",
        "stream": False,
    },
    timeout_seconds=1800,
    max_retries=2,
    retry_delay_seconds=60,
)
print(f"已创建团队计划: {team_schedule.name}")
console.show_schedule(team_schedule.id)

# =============================================================================
# 2. 调度工作流运行
# =============================================================================

print("\n=== 工作流计划 ===\n")

wf_schedule = mgr.create(
    name="nightly-data-pipeline",
    cron="0 2 * * *",
    endpoint="/workflows/data-pipeline/runs",
    description="每晚凌晨 2 点运行数据管道工作流",
    payload={
        "message": "Process and aggregate daily data",
    },
    timeout_seconds=3600,
)
print(f"已创建工作流计划: {wf_schedule.name}")
console.show_schedule(wf_schedule.id)

# =============================================================================
# 3. Agent、团队和工作流计划的混合
# =============================================================================

print("\n=== 混合计划 ===\n")

agent_sched = mgr.create(
    name="hourly-monitor",
    cron="0 * * * *",
    endpoint="/agents/monitor-agent/runs",
    description="每小时运行监控 agent",
    payload={"message": "Check system health"},
)

# 一起显示所有计划
console.show_schedules()

# =============================================================================
# 4. 非运行端点的不同 HTTP 方法
# =============================================================================

print("\n=== 非运行端点计划 ===\n")

# 调度 GET 请求（例如，健康检查）
health_sched = mgr.create(
    name="health-ping",
    cron="*/10 * * * *",
    endpoint="/health",
    method="GET",
    description="每 10 分钟 ping 健康端点",
)
print(
    f"已创建 GET 计划: {health_sched.name} -> {health_sched.method} {health_sched.endpoint}"
)

# =============================================================================
# 清理
# =============================================================================

print("\n=== 清理 ===\n")
for s in mgr.list():
    mgr.delete(s.id)
print("所有计划已清理。")

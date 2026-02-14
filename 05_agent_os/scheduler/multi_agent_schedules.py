"""具有不同 cron 模式和负载的多 agent 调度。

此示例演示：
- 具有不同角色的多个 agent
- 每个 agent 获得具有不同 cron、时区、负载的计划
- 用于可靠性的重试配置
- 显示所有计划的 Rich 表格
- 过滤视图（仅启用、仅禁用）
"""

from agno.db.sqlite import SqliteDb
from agno.scheduler import ScheduleManager
from agno.scheduler.cli import SchedulerConsole

# --- 设置 ---

db = SqliteDb(id="multi-agent-demo", db_file="tmp/multi_agent_demo.db")
mgr = ScheduleManager(db)
console = SchedulerConsole(mgr)

# =============================================================================
# 创建具有不同配置的计划
# =============================================================================

print("为 3 个 agent 创建计划...\n")

# 研究 agent：每天东部时间上午 7 点，带自定义负载
s_research = mgr.create(
    name="daily-research",
    cron="0 7 * * *",
    endpoint="/agents/research-agent/runs",
    description="收集每日研究见解",
    timezone="America/New_York",
    payload={
        "message": "Research the latest AI developments",
        "stream": False,
    },
)

# 作家 agent：工作日 UTC 上午 10 点
s_writer = mgr.create(
    name="weekday-report",
    cron="0 10 * * 1-5",
    endpoint="/agents/writer-agent/runs",
    description="生成工作日摘要报告",
    payload={
        "message": "Write a summary of yesterday's research",
    },
)

# 监控 agent：每 15 分钟一次，带重试配置
s_monitor = mgr.create(
    name="health-monitor",
    cron="*/15 * * * *",
    endpoint="/agents/monitor-agent/runs",
    description="每 15 分钟进行系统健康检查",
    payload={
        "message": "Check system health and report anomalies",
    },
    max_retries=3,
    retry_delay_seconds=30,
    timeout_seconds=120,
)

print("所有计划已创建。")

# =============================================================================
# 显示所有计划
# =============================================================================

print("\n--- 所有计划 ---")
console.show_schedules()

# =============================================================================
# 显示单个计划详细信息
# =============================================================================

print("\n--- 监控计划详细信息 ---")
console.show_schedule(s_monitor.id)

# =============================================================================
# 禁用一个计划并显示过滤视图
# =============================================================================

mgr.disable(s_writer.id)
print("\n已禁用 'weekday-report' 计划。")

print("\n--- 仅启用的计划 ---")
enabled = console.show_schedules(enabled=True)
print(f"({len(enabled)} 已启用)")

print("\n--- 仅禁用的计划 ---")
disabled = console.show_schedules(enabled=False)
print(f"({len(disabled)} 已禁用)")

# =============================================================================
# 重新启用并验证
# =============================================================================

mgr.enable(s_writer.id)
print("\n重新启用 'weekday-report' 计划。")

all_schedules = mgr.list()
print(f"总计划数: {len(all_schedules)}")

# =============================================================================
# 清理
# =============================================================================

# 取消注释以从数据库清理计划：
# for s in [s_research, s_writer, s_monitor]:
#     mgr.delete(s.id)
# print("\n所有计划已清理。")

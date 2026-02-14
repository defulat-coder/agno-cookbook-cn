"""查看和分析计划运行历史。

此示例演示：
- 创建计划并模拟运行记录
- 使用 SchedulerConsole.show_runs() 进行 Rich 格式化的运行历史
- 使用分页查询运行历史
- 理解运行状态（成功、失败、运行中、暂停）
"""

import time
from uuid import uuid4

from agno.db.sqlite import SqliteDb
from agno.scheduler import ScheduleManager
from agno.scheduler.cli import SchedulerConsole

# --- 设置 ---

db = SqliteDb(id="run-history-demo", db_file="tmp/run_history_demo.db")
mgr = ScheduleManager(db)
console = SchedulerConsole(mgr)

# --- 创建计划 ---

schedule = mgr.create(
    name="monitored-task",
    cron="*/5 * * * *",
    endpoint="/agents/monitor/runs",
    description="要检查的运行历史的计划",
    payload={"message": "Run health check"},
    max_retries=2,
    retry_delay_seconds=30,
)
print(f"已创建计划: {schedule.name} (id={schedule.id})")

# --- 通过直接插入模拟一些运行记录 ---
# 在生产中，ScheduleExecutor 会自动创建这些。
# 这里我们手动插入它们以演示历史显示。

now = int(time.time())

# 模拟具有不同状态的 3 次运行
run_records = [
    {
        "id": str(uuid4()),
        "schedule_id": schedule.id,
        "attempt": 1,
        "triggered_at": now - 600,
        "completed_at": now - 590,
        "status": "success",
        "status_code": 200,
        "run_id": str(uuid4()),
        "session_id": str(uuid4()),
        "error": None,
        "created_at": now - 600,
    },
    {
        "id": str(uuid4()),
        "schedule_id": schedule.id,
        "attempt": 1,
        "triggered_at": now - 300,
        "completed_at": now - 280,
        "status": "failed",
        "status_code": 500,
        "run_id": str(uuid4()),
        "session_id": None,
        "error": "Internal server error",
        "created_at": now - 300,
    },
    {
        "id": str(uuid4()),
        "schedule_id": schedule.id,
        "attempt": 2,
        "triggered_at": now - 240,
        "completed_at": now - 230,
        "status": "success",
        "status_code": 200,
        "run_id": str(uuid4()),
        "session_id": str(uuid4()),
        "error": None,
        "created_at": now - 240,
    },
]

for record in run_records:
    db.create_schedule_run(record)

# --- 使用 Rich 显示运行历史 ---

print("\n=== 运行历史（Rich 表格）===\n")
console.show_runs(schedule.id)

# --- 以编程方式查询运行 ---

print("\n=== 运行历史（编程方式）===\n")
runs = mgr.get_runs(schedule.id, limit=10)
print(f"总运行数: {len(runs)}")
for run in runs:
    status = run.status
    attempt = run.attempt
    error = run.error or "-"
    print(f"  尝试 {attempt}: {status} (error={error})")

# --- 分页 ---

print("\n=== 分页（limit=2, offset=0）===\n")
page1 = mgr.get_runs(schedule.id, limit=2, offset=0)
print(f"第 1 页: {len(page1)} 次运行")

page2 = mgr.get_runs(schedule.id, limit=2, offset=2)
print(f"第 2 页: {len(page2)} 次运行")

# --- 清理 ---

mgr.delete(schedule.id)
print("\n计划和运行已删除。")

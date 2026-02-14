"""计划验证和错误处理。

此示例演示：
- 无效的 cron 表达式处理
- 无效的时区处理
- 重复的计划名称处理
- 复杂的 cron 模式（范围、步骤、列表）
- 方法自动大写
"""

from agno.db.sqlite import SqliteDb
from agno.scheduler import ScheduleManager
from agno.scheduler.cli import SchedulerConsole

# --- 设置 ---

db = SqliteDb(id="validation-demo", db_file="tmp/validation_demo.db")
mgr = ScheduleManager(db)

# =============================================================================
# 1. 无效的 cron 表达式
# =============================================================================

print("1. 无效的 cron 表达式:")
try:
    mgr.create(name="bad-cron", cron="not valid", endpoint="/test")
except ValueError as e:
    print(f"   Caught ValueError: {e}")

# =============================================================================
# 2. 无效的时区
# =============================================================================

print("\n2. 无效的时区:")
try:
    mgr.create(name="bad-tz", cron="0 9 * * *", endpoint="/test", timezone="Fake/Zone")
except ValueError as e:
    print(f"   Caught ValueError: {e}")

# =============================================================================
# 3. 重复的计划名称
# =============================================================================

print("\n3. 重复的计划名称:")
s = mgr.create(name="unique-schedule", cron="0 9 * * *", endpoint="/test")
try:
    mgr.create(name="unique-schedule", cron="0 10 * * *", endpoint="/test")
except ValueError as e:
    print(f"   Caught ValueError: {e}")
mgr.delete(s.id)

# =============================================================================
# 4. 复杂的 cron 模式
# =============================================================================

print("\n4. 复杂的 cron 模式:")

# 每 5 分钟
s1 = mgr.create(name="every-5-min", cron="*/5 * * * *", endpoint="/test")
print(f"   */5 * * * * -> Created: {s1.name}")

# 工作日 9-17 点
s2 = mgr.create(name="business-hours", cron="0 9-17 * * 1-5", endpoint="/test")
print(f"   0 9-17 * * 1-5 -> Created: {s2.name}")

# 每月第一天午夜
s3 = mgr.create(name="monthly-report", cron="0 0 1 * *", endpoint="/test")
print(f"   0 0 1 * * -> Created: {s3.name}")

# =============================================================================
# 5. 方法自动大写
# =============================================================================

print("\n5. 方法自动大写:")
s4 = mgr.create(
    name="lowercase-method", cron="0 9 * * *", endpoint="/test", method="get"
)
print(f"   Input: 'get' -> Stored: '{s4.method}'")

# =============================================================================
# 6. 显示所有有效计划
# =============================================================================

print()
console = SchedulerConsole(mgr)
console.show_schedules()

# =============================================================================
# 清理
# =============================================================================

for s in [s1, s2, s3, s4]:
    mgr.delete(s.id)
print("所有计划已清理。")

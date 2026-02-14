"""使用异步 ScheduleManager API 进行异步计划管理。

此示例演示：
- 使用 acreate(), alist(), aget(), aupdate(), adelete() 进行异步 CRUD
- 使用 aenable() 和 adisable() 切换计划
- 使用 aget_runs() 列出运行历史
- 使用 SchedulerConsole 进行 Rich 格式化显示
"""

import asyncio

from agno.db.sqlite import SqliteDb
from agno.scheduler import ScheduleManager
from agno.scheduler.cli import SchedulerConsole


async def main():
    # --- 设置 ---
    db = SqliteDb(id="async-scheduler-demo", db_file="tmp/async_scheduler_demo.db")
    mgr = ScheduleManager(db)
    console = SchedulerConsole(mgr)

    # --- 异步创建计划 ---
    s1 = await mgr.acreate(
        name="async-morning-report",
        cron="0 8 * * *",
        endpoint="/agents/async-agent/runs",
        description="通过异步 API 的早晨报告",
        payload={"message": "Generate the morning report"},
    )
    print(f"Created: {s1.name} (id={s1.id})")

    s2 = await mgr.acreate(
        name="async-evening-summary",
        cron="0 18 * * *",
        endpoint="/agents/async-agent/runs",
        description="通过异步 API 的晚间摘要",
        payload={"message": "Summarize the day"},
    )
    print(f"Created: {s2.name} (id={s2.id})")

    # --- 列出所有计划 ---
    all_schedules = await mgr.alist()
    print(f"\nTotal schedules: {len(all_schedules)}")

    # --- 通过 ID 获取 ---
    fetched = await mgr.aget(s1.id)
    print(f"Fetched: {fetched.name}")

    # --- 更新 ---
    updated = await mgr.aupdate(s1.id, description="更新的早晨报告描述")
    print(f"Updated description: {updated.description}")

    # --- 禁用并重新启用 ---
    await mgr.adisable(s2.id)
    disabled = await mgr.aget(s2.id)
    print(f"\n{disabled.name} enabled={disabled.enabled}")

    await mgr.aenable(s2.id)
    enabled = await mgr.aget(s2.id)
    print(f"{enabled.name} enabled={enabled.enabled}")

    # --- 检查运行（尚无，因为我们还没有执行） ---
    runs = await mgr.aget_runs(s1.id)
    print(f"\nRuns for {s1.name}: {len(runs)}")

    # --- 使用 Rich 显示 ---
    print()
    console.show_schedules()

    # --- 清理 ---
    await mgr.adelete(s1.id)
    await mgr.adelete(s2.id)
    print("\nAll schedules deleted.")


if __name__ == "__main__":
    asyncio.run(main())

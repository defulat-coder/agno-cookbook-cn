"""通过 REST API 进行计划管理。

演示创建、列出、更新、启用/禁用、
手动触发和删除计划。

前置条件：
    pip install agno[scheduler] httpx

使用方法：
    # 首先，启动服务器：
    python cookbook/05_agent_os/scheduler/basic_schedule.py

    # 然后运行此脚本：
    python cookbook/05_agent_os/scheduler/schedule_management.py
"""

import httpx

# ---------------------------------------------------------------------------
# Create Example
# ---------------------------------------------------------------------------

BASE_URL = "http://localhost:7777"


def main():
    client = httpx.Client(base_url=BASE_URL, timeout=30)

    # 1. 创建计划
    print("--- 创建计划 ---")
    resp = client.post(
        "/schedules",
        json={
            "name": "hourly-greeting",
            "cron_expr": "0 * * * *",
            "endpoint": "/agents/greeter/runs",
            "payload": {"message": "Hourly check-in"},
            "timezone": "UTC",
            "max_retries": 2,
            "retry_delay_seconds": 30,
        },
    )
    print(f"  Status: {resp.status_code}")
    schedule = resp.json()
    schedule_id = schedule["id"]
    print(f"  ID: {schedule_id}")
    print(f"  Next run at: {schedule['next_run_at']}")
    print()

    # 2. 列出所有计划
    print("--- 列出计划 ---")
    resp = client.get("/schedules")
    schedules = resp.json()
    for s in schedules:
        print(f"  {s['name']} (enabled={s['enabled']}, next_run={s['next_run_at']})")
    print()

    # 3. 更新计划
    print("--- 更新计划 ---")
    resp = client.patch(
        f"/schedules/{schedule_id}",
        json={"description": "每小时整点运行", "max_retries": 3},
    )
    print(f"  Updated description: {resp.json()['description']}")
    print()

    # 4. 禁用计划
    print("--- 禁用计划 ---")
    resp = client.post(f"/schedules/{schedule_id}/disable")
    print(f"  Enabled: {resp.json()['enabled']}")
    print()

    # 5. 重新启用计划
    print("--- 启用计划 ---")
    resp = client.post(f"/schedules/{schedule_id}/enable")
    print(f"  Enabled: {resp.json()['enabled']}")
    print(f"  Next run at: {resp.json()['next_run_at']}")
    print()

    # 6. 手动触发
    print("--- 触发计划 ---")
    resp = client.post(f"/schedules/{schedule_id}/trigger")
    print(f"  Trigger status: {resp.status_code}")
    print(f"  Run: {resp.json()}")
    print()

    # 7. 查看运行历史
    print("--- 运行历史 ---")
    resp = client.get(f"/schedules/{schedule_id}/runs")
    runs = resp.json()
    print(f"  Total runs: {len(runs)}")
    for run in runs:
        print(
            f"    attempt={run['attempt']} status={run['status']} triggered_at={run['triggered_at']}"
        )
    print()

    # 8. 删除计划
    print("--- 删除计划 ---")
    resp = client.delete(f"/schedules/{schedule_id}")
    print(f"  Delete status: {resp.status_code}")

    # 验证删除
    resp = client.get(f"/schedules/{schedule_id}")
    print(f"  Get after delete: {resp.status_code} (expected 404)")


# ---------------------------------------------------------------------------
# Run Example
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()

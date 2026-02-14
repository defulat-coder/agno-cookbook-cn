"""直接使用调度器 REST API 端点。

此示例演示：
- 通过 POST /schedules 创建计划
- 通过 GET /schedules 列出计划
- 通过 PATCH /schedules/{id} 更新
- 通过 POST /schedules/{id}/enable 和 /disable 启用/禁用
- 通过 POST /schedules/{id}/trigger 手动触发
- 通过 GET /schedules/{id}/runs 查看运行历史
- 通过 DELETE /schedules/{id} 删除

要求：运行中的 AgentOS 服务器，scheduler=True

    .venvs/demo/bin/python cookbook/05_agent_os/scheduler/scheduler_with_agentos.py

然后在另一个终端中：

    .venvs/demo/bin/python cookbook/05_agent_os/scheduler/rest_api_schedules.py
"""

import httpx

BASE_URL = "http://127.0.0.1:7777"

client = httpx.Client(base_url=BASE_URL, timeout=30)


def main():
    # =========================================================================
    # 1. 创建计划
    # =========================================================================
    print("=== 创建计划 ===\n")
    resp = client.post(
        "/schedules",
        json={
            "name": "api-demo-schedule",
            "cron_expr": "*/5 * * * *",
            "endpoint": "/agents/greeter/runs",
            "description": "通过 REST API 创建",
            "payload": {"message": "Hello from the REST API!"},
            "timezone": "UTC",
            "max_retries": 1,
            "retry_delay_seconds": 30,
        },
    )
    resp.raise_for_status()
    schedule = resp.json()
    schedule_id = schedule["id"]
    print(f"已创建: {schedule['name']} (id={schedule_id})")
    print(f"  Cron: {schedule['cron_expr']}")
    print(f"  下次运行: {schedule['next_run_at']}")

    # =========================================================================
    # 2. 列出所有计划
    # =========================================================================
    print("\n=== 列出计划 ===\n")
    resp = client.get("/schedules")
    resp.raise_for_status()
    result = resp.json()
    schedules = result["data"]
    meta = result["meta"]
    print(
        f"第 {meta['page']} 页，共 {meta['total_pages']} 页（总计: {meta['total_count']}）\n"
    )
    for s in schedules:
        status = "已启用" if s["enabled"] else "已禁用"
        print(f"  {s['name']} [{status}] -> {s['endpoint']}")

    # =========================================================================
    # 3. 获取单个计划
    # =========================================================================
    print("\n=== 获取计划 ===\n")
    resp = client.get(f"/schedules/{schedule_id}")
    resp.raise_for_status()
    detail = resp.json()
    print(f"  名称: {detail['name']}")
    print(f"  Cron: {detail['cron_expr']}")
    print(f"  时区: {detail['timezone']}")
    print(f"  最大重试次数: {detail['max_retries']}")

    # =========================================================================
    # 4. 更新计划
    # =========================================================================
    print("\n=== 更新计划 ===\n")
    resp = client.patch(
        f"/schedules/{schedule_id}",
        json={
            "description": "通过 REST API 更新的描述",
            "cron_expr": "0 * * * *",
        },
    )
    resp.raise_for_status()
    updated = resp.json()
    print(f"  描述: {updated['description']}")
    print(f"  Cron: {updated['cron_expr']}")

    # =========================================================================
    # 5. 禁用和重新启用
    # =========================================================================
    print("\n=== 禁用/启用 ===\n")
    resp = client.post(f"/schedules/{schedule_id}/disable")
    resp.raise_for_status()
    print(f"  已禁用: enabled={resp.json()['enabled']}")

    resp = client.post(f"/schedules/{schedule_id}/enable")
    resp.raise_for_status()
    print(f"  重新启用: enabled={resp.json()['enabled']}")

    # =========================================================================
    # 6. 手动触发
    # =========================================================================
    print("\n=== 手动触发 ===\n")
    try:
        resp = client.post(f"/schedules/{schedule_id}/trigger")
        if resp.status_code == 200:
            trigger_result = resp.json()
            print(f"  触发结果: status={trigger_result.get('status')}")
            print(f"  运行 ID: {trigger_result.get('run_id')}")
        elif resp.status_code == 503:
            print("  触发返回 503（调度器执行器尚未运行）")
        else:
            print(f"  触发响应: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"  触发超时或失败: {type(e).__name__}")

    # =========================================================================
    # 7. 查看运行历史
    # =========================================================================
    print("\n=== 运行历史 ===\n")
    resp = client.get(f"/schedules/{schedule_id}/runs", params={"limit": 5, "page": 1})
    resp.raise_for_status()
    result = resp.json()
    runs = result["data"]
    meta = result["meta"]
    if runs:
        print(f"显示 {len(runs)} / {meta['total_count']} 总运行数\n")
        for run in runs:
            print(
                f"  运行 {run['id'][:8]}... status={run['status']} attempt={run['attempt']}"
            )
    else:
        print("  尚无运行（计划尚未轮询）")

    # =========================================================================
    # 8. 删除计划
    # =========================================================================
    print("\n=== 删除 ===\n")
    resp = client.delete(f"/schedules/{schedule_id}")
    resp.raise_for_status()
    try:
        result = resp.json()
        print(f"  已删除: {result}")
    except Exception:
        print(f"  删除成功（状态 {resp.status_code}）")

    print("\n完成。")


if __name__ == "__main__":
    main()

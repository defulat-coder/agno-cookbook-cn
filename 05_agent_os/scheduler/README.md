# Scheduler Cookbook

AgentOS 中 `scheduler` 的示例。

## 文件
- `basic_schedule.py` — 基本的定时 Agent 运行。
- `schedule_management.py` — 通过 REST API 进行调度管理。

## 前置条件
- 使用 `direnv allow` 加载环境变量（需要 `.envrc` 文件）。
- 使用 `.venvs/demo/bin/python <path-to-file>.py` 运行示例。
- 某些示例需要本地服务（例如 Postgres、Redis、Slack 或 MCP 服务器）。

安装调度器依赖项：

```bash
pip install agno[scheduler]
```

这将安装 `croniter` 和 `pytz`。

## 示例

### basic_schedule.py

最小示例：创建一个包含单个 Agent 的 AgentOS 并启用调度器。通过 API 创建一个调度任务，每 5 分钟触发一次 Agent。

### schedule_management.py

演示完整的 CRUD 生命周期：通过 REST API 创建、列出、更新、启用/禁用、触发和删除调度任务。

## 关键概念

- **Cron 表达式**：标准的 5 字段 cron 语法（分钟、小时、日期、月份、星期）
- **时区**：所有调度任务通过 pytz 支持时区感知调度
- **重试**：可配置的重试次数和失败执行的延迟
- **内部认证**：调度器使用自动生成的内部服务令牌向 AgentOS 进行身份验证
- **运行历史**：每次执行都会跟踪状态、时间和错误详细信息

## 配置

```python
AgentOS(
    agents=[my_agent],
    db=db,
    scheduler=True,                  # 启用调度器
    scheduler_poll_interval=15,      # 每 15 秒轮询一次（默认值）
    scheduler_base_url="http://127.0.0.1:7777",  # AgentOS 基础 URL
)
```

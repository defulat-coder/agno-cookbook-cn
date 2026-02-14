# CLAUDE.md - Scheduler Cookbook

Claude Code 测试 Scheduler Cookbook 时的说明。

---

## 快速参考

**测试环境：**
```bash
# 包含所有依赖项的虚拟环境
.venvs/demo/bin/python

# 需要 croniter 和 pytz（包含在 agno[scheduler] 和 agno[demo] 中）
```

**运行 Cookbook：**
```bash
.venvs/demo/bin/python cookbook/05_agent_os/scheduler/basic_schedule.py
```

**测试结果文件：**
```
cookbook/05_agent_os/scheduler/TEST_LOG.md
```

---

## 测试工作流

### 1. 测试前

确保虚拟环境存在：
```bash
./scripts/demo_setup.sh
```

Scheduler Cookbook 需要运行具有数据库的 AgentOS 实例。
如果需要，启动 PostgreSQL：
```bash
./cookbook/scripts/run_pgvector.sh
```

### 2. 运行测试

使用 demo 环境运行单独的 Cookbook：
```bash
.venvs/demo/bin/python cookbook/05_agent_os/scheduler/basic_schedule.py
.venvs/demo/bin/python cookbook/05_agent_os/scheduler/schedule_management.py
```

### 3. 更新 TEST_LOG.md

每次测试后，使用以下内容更新 `cookbook/05_agent_os/scheduler/TEST_LOG.md`：
- 测试名称和路径
- 状态：PASS 或 FAIL
- 测试内容的简要描述
- 任何值得注意的观察或问题

---

## 代码位置

| 组件 | 位置 |
|-----------|----------|
| Scheduler 核心 | `libs/agno/agno/scheduler/` |
| Cron 工具 | `libs/agno/agno/scheduler/cron.py` |
| 调度执行器 | `libs/agno/agno/scheduler/executor.py` |
| 调度轮询器 | `libs/agno/agno/scheduler/poller.py` |
| 数据库 Schema | `libs/agno/agno/db/schemas/scheduler.py` |
| API 路由 | `libs/agno/agno/os/routers/schedules/` |
| API Schema | `libs/agno/agno/os/routers/schedules/schema.py` |
| AgentOS 集成 | `libs/agno/agno/os/app.py` |

---

## 关键概念

- **croniter** 和 **pytz** 是 `agno[scheduler]` 下的可选依赖项
- 调度器以可配置的间隔（默认：15 秒）轮询数据库
- 调度任务以原子方式声明以防止重复执行
- 执行器使用内部服务令牌调用 AgentOS 服务器上的端点
- 运行端点（`/agents/*/runs`、`/teams/*/runs`）使用 `background=true` 调用，执行器轮询完成情况

---

## 已知问题

1. SQLite 声明是尽力而为的，不支持多进程安全（生产环境使用 PostgreSQL）
2. 调度器需要在 `AgentOS` 构造函数上设置 `scheduler=True`

如果这些规则影响你的更改，请考虑它们。

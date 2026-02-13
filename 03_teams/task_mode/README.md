# Task Mode for Teams（团队任务模式）

任务模式（`mode=TeamMode.tasks`）启用基于任务的自主执行，团队领导将：

1. **分解**用户目标为离散任务
2. **分配**任务给最有能力的成员 agent
3. **执行**具有适当依赖顺序的任务
4. **并行运行任务**（当它们彼此独立时）
5. **综合**结果为最终响应

## 快速开始

```bash
.venvs/demo/bin/python cookbook/03_teams/task_mode/01_basic_task_mode.py
```

## 示例

| 文件 | 描述 |
|------|-------------|
| `01_basic_task_mode.py` | 基本任务分解，包括研究、写作和审查 |
| `02_parallel_tasks.py` | 独立分析任务的并行执行 |
| `03_task_mode_with_tools.py` | 带工具的任务模式（网络搜索）|
| `04_async_task_mode.py` | 使用 `arun()` 的异步任务模式 |
| `05_dependency_chain.py` | 产品发布流程中的复杂依赖链 |
| `06_custom_tools.py` | 带自定义 Python 函数工具的 agent（财务计算器）|
| `07_multi_run_session.py` | 跨顺序请求的多运行会话持久化 |

## 关键概念

### 创建任务模式团队

```python
from agno.team.team import Team
from agno.team.mode import TeamMode

team = Team(
    name="My Team",
    mode=TeamMode.tasks,
    model=OpenAIChat(id="gpt-4o"),
    members=[agent1, agent2],
    max_iterations=10,  # 最大任务循环迭代次数
)
```

### 可用工具（自动提供给团队领导）

- `create_task` - 创建新任务，包括标题、描述、负责人和依赖项
- `execute_task` - 通过委派给成员 agent 执行单个任务
- `execute_tasks_parallel` - 并发执行多个独立任务
- `update_task_status` - 手动更新任务状态
- `list_tasks` - 查看所有任务及其当前状态
- `add_task_note` - 向任务添加备注
- `mark_all_complete` - 标记总体目标已完成

### 任务依赖

任务可以使用 `depends_on`（任务 ID 列表）声明依赖项。带有未解决依赖项的任务会自动标记为 `blocked`，并且在所有依赖项完成之前无法执行。

### 并行执行

当任务彼此独立（没有相互依赖）时，团队领导可以使用 `execute_tasks_parallel` 并发运行它们，从而显著减少总执行时间。
